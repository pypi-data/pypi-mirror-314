import hashlib
import json
from importlib.metadata import version

from media_muncher.framerate import FrameRate
from media_muncher.gop_size import GopSizeCalculator
from media_muncher.h264_levels import H264LevelValidator
from media_muncher.messages import WarningMessage
from media_muncher.profile.schemas.base import BaseSchemaGenerator
from media_muncher.resolution import Resolution
from media_muncher.segment_size import SegmentSizer

PRESET_MAPPING = {
    "VERYFAST": 3,
    "FAST": 5,
    "MEDIUM": 7,
    "SLOW": 9,
    "SLOWER": 11,
    "VERYSLOW": 13,
    "PLACEBO": 15,
}

# TODO - Improve to take into account the different codecs and channel layouts
STANDARD_BITRATES = {
    "mp4a.40.2": {
        48000: {
            "stereo": [96000, 128000, 160000, 192000, 224000, 256000, 320000],
        }
    },
    "mp4a.40.5": {48000: {"stereo": [16000, 32000, 64000, 80000, 96000, 128000]}},
    "ac-3": {
        48000: {
            "stereo": [
                32000,
                48000,
                64000,
                96000,
                112000,
                128000,
                160000,
                192000,
                224000,
                256000,
                320000,
                384000,
                448000,
                512000,
                576000,
                640000,
            ]
        }
    },
}

DEFAULT_FRAMERATE = 25
DEFAULT_CHANNEL_LAYOUT = "stereo"


class BktV2dot1ProfileSchemaGenerator(BaseSchemaGenerator):
    schema_name = "bkt-v2.1"

    def generate(self, renditions, packaging, name: str = ""):
        self.video_renditions = [r for r in renditions if r["type"] == "video"]
        self.audio_renditions = [r for r in renditions if r["type"] == "audio"]

        # Default framerate (in case of audio-only or if cannot be determined)
        self.common_framerate = FrameRate(DEFAULT_FRAMERATE)

        video_ladder = self._process_video_renditions()

        default_audio_sample_rate = 48000

        self.messages.append(
            WarningMessage(
                "This tool currently only assumes an audio sample rate of 48kHz.",
                topic="audio",
            )
        )

        audio_ladder = self._process_audio_renditions(default_audio_sample_rate)

        packaging_options = self._process_packaging(
            packaging, default_audio_sample_rate
        )

        profile = {
            "version": "02.00.05",
            "type": "OFFLINE_TRANSCODING",
            "audios": audio_ladder,
            "videos": video_ladder,
            "packaging": packaging_options,
            "_generator": "bpkio-python-sdk/" + version("bpkio-python-sdk"),
        }

        # Create a hash of the profile
        hash = hashlib.sha256(json.dumps(profile).encode()).hexdigest()
        profile["name"] = f"bic_{name}_{hash}"

        return profile

    def _process_video_renditions(self):
        perf_level = PRESET_MAPPING.get(self.config["preset"].upper(), 7)

        # Video renditions (if any)
        if len(self.video_renditions) == 0:
            return {}
        else:
            # First pass to set the resolution and framerate
            for r in self.video_renditions:
                # TODO - must be done on the basis of the codec
                # Ensure that the resolutions are even
                r["resolution"] = Resolution(*r["resolution"]).make_even()

                # Ensure that we have a framerate for all video renditions
                if "framerate" not in r:
                    r["framerate"] = FrameRate(self.config.get("framerate"))
                    self.messages.append(
                        WarningMessage(
                            f"Default video framerate of {self.config.get('framerate')} was selected, "
                            f"since it could not be detected in the source",
                            topic="framerate",
                        )
                    )
                else:
                    if r["framerate"] is not None:
                        r["framerate"] = FrameRate(r["framerate"])
                    else:
                        r["framerate"] = FrameRate(DEFAULT_FRAMERATE)

            # Get a common framerate
            all_framerates = [r.get("framerate") for r in self.video_renditions]

            # if they're not all the same, find the common one
            if len(set(all_framerates)) == 1:
                multi_rates = False
                self.common_framerate = all_framerates[0]
            else:
                multi_rates = True
                try:
                    self.common_framerate = FrameRate.get_common_framerate(
                        all_framerates
                    )
                except ValueError:
                    self.common_framerate = all_framerates[0]
                    multi_rates = False
                    self.messages.append(
                        WarningMessage(
                            f"The video frame rates are different and incompatible between the renditions. "
                            f"Forcing the first framerate if {self.common_framerate} on all other renditions",
                            topic="framerate",
                        )
                    )
                    for r in self.video_renditions:
                        r["framerate"] = self.common_framerate

            video_ladder = {
                "common": {
                    "perf_level": perf_level,
                }
            }

            if not multi_rates:
                video_ladder["common"]["framerate"] = {
                    "num": self.common_framerate.numerator,
                    "den": self.common_framerate.denominator,
                }
                video_ladder["common"]["gop_size"] = GopSizeCalculator(
                    video_frame_rate=self.common_framerate
                ).for_target_duration(max_duration=1.1, max_frames=300)[0]

            # Second pass to define the ladder
            for i, r in enumerate(self.video_renditions):
                # Adjust the H264 level
                resol, _, bitrate = H264LevelValidator(r["level"]).adjust(
                    resolution=r.get("resolution"),
                    framerate=r.get("framerate"),
                    bitrate=r.get("bitrate"),
                )
                if resol != r.get("resolution"):
                    self.messages.append(
                        WarningMessage(
                            f"Resolution was adjusted to {resol} (from {r.get('resolution')}) to comply with the H264 level {r['level']}",
                            topic="H264 level",
                        )
                    )
                if bitrate != r.get("bitrate"):
                    self.messages.append(
                        WarningMessage(
                            f"Bitrate was adjusted to {bitrate} bps (from {r.get('bitrate')} bps) to comply with the H264 level {r['level']}",
                            topic="H264 level",
                        )
                    )

                rung = {
                    "_codec_info": f"{r['codec']} {r['profile']} {r['level']}",
                    "codec_string": r["codecstring"],
                    "scale": {"width": -2, "height": resol.height},
                    "bitrate": bitrate,
                }
                if multi_rates:
                    rung["framerate"] = {
                        "num": r["framerate"].numerator,
                        "den": r["framerate"].denominator,
                    }
                    rung["gop_size"] = GopSizeCalculator(
                        video_frame_rate=r["framerate"]
                    ).for_target_duration(max_duration=1.1, max_frames=300)[0]

                video_ladder[f"video_{i}"] = rung

            return video_ladder

    def _process_audio_renditions(self, audio_sample_rate):
        channel_layout = DEFAULT_CHANNEL_LAYOUT

        audio_ladder = {
            "common": {
                "sampling_rate": audio_sample_rate,
                "loudnorm": {"i": -23, "tp": -1},
            }
        }

        # Find distinct codecs and languages
        distinct_languages = list(
            set([r.get("language") for r in self.audio_renditions])
        )
        distinct_codecs = list(
            set([r.get("codecstring") for r in self.audio_renditions])
        )

        if any(c not in STANDARD_BITRATES for c in distinct_codecs):
            self.messages.append(
                WarningMessage(
                    "This tool currently only supports the following audio codecs: "
                    + ", ".join(STANDARD_BITRATES.keys()),
                    topic="audio codec",
                )
            )

        # Find distinct bitrates for each codec
        distinct_codec_bitrates = {}
        for ic in distinct_codecs:
            distinct_codec_bitrates[ic] = list(
                set(
                    [
                        r.get("bitrate")
                        for r in self.audio_renditions
                        if r["codecstring"] == ic
                    ]
                )
            )

        rendition_count = 0
        for ic in distinct_codecs:
            first_rendition = next(
                r for r in self.audio_renditions if r["codecstring"] == ic
            )
            this_codec_info = (
                f"{first_rendition['codec']} {first_rendition.get('mode', '')}"
            )

            for ib in distinct_codec_bitrates[ic]:
                rend_name = f"audio_{rendition_count}"
                rend = {
                    "_codec_info": this_codec_info,
                    "codec_string": ic,
                    "channel_layout": channel_layout,
                }
                # Find nearest standard bitrate
                try:
                    nearest_bitrate = max(
                        filter(
                            lambda x: x <= ib,
                            STANDARD_BITRATES[ic][audio_sample_rate][channel_layout],
                        )
                    )
                except Exception as e:
                    nearest_bitrate = STANDARD_BITRATES[ic][audio_sample_rate][
                        channel_layout
                    ][0]
                    self.messages.append(
                        WarningMessage(
                            f"Invalid bitrate. Bitrate was set to {nearest_bitrate} bps (from {ib} bps) to comply with the AAC codec",
                            topic="AAC codec",
                        )
                    )

                if nearest_bitrate != ib:
                    self.messages.append(
                        WarningMessage(
                            f"Bitrate was adjusted to {nearest_bitrate} bps (from {ib} bps) to comply with the AAC codec",
                            topic="AAC codec",
                        )
                    )

                rend["bitrate"] = nearest_bitrate

                if len(distinct_languages) > 1:
                    rend["advanced"] = {}
                    for il in distinct_languages:
                        if il is not None:
                            rend["advanced"][f"--track_language={il}"] = ""

                audio_ladder[rend_name] = rend
                rendition_count += 1

        return audio_ladder

    def _process_packaging(self, packaging, default_audio_sample_rate):
        # Packaging options
        packaging_options = {}

        # Calculate the segment duration
        target_segment_duration = packaging.get("segment_duration", 4)
        segment_sizer = SegmentSizer(
            framerate=self.common_framerate, samplerate=default_audio_sample_rate
        )
        if packaging.get("muxed_audio") is True:
            segment_sizer.set_target_duration(
                target_segment_duration, ignore_audio=True
            )
        else:
            segment_sizer.set_target_duration(target_segment_duration)

        if segment_sizer.actual_duration != target_segment_duration:
            self.messages.append(
                WarningMessage(
                    f"Target segment duration of {target_segment_duration} seconds was adjusted to "
                    f"{round(segment_sizer.actual_duration, 3)} seconds for compatibility "
                    f"with the framerate and audio sample rate.",
                    topic="Segment duration",
                )
            )

        # TODO - check if the gop size is compatible with the segment duration: a segment duration must be a multiple of the gop size

        # HLS packaging config
        hls_config = {}
        packaging_options["hls"] = hls_config
        hls_config["fragment_length"] = {
            "num": segment_sizer.numerator,
            "den": segment_sizer.denominator,
        }

        # Specific HLS configuration
        if packaging.get("packaging") == "HLS":
            # TODO - not a great default if done alongside DASH...
            hls_config["version"] = packaging.get("version", 3)
            advanced_config = {}

            if packaging.get("container") == "ISOBMFF":
                hls_config["fragmented_mp4"] = True

            if packaging.get("container") == "MPEG-TS":
                if packaging.get("muxed_audio") is False:
                    hls_config["audio_not_multiplex"] = True

                if packaging.get("audio_only") is False:
                    # Only if there is a single audio rendition. It helps with BkYou to ensure there is an audio-only rendition
                    if len(self.audio_renditions) == 1:
                        advanced_config["--hls.no_audio_only"] = ""

            if advanced_config:
                hls_config["advanced"] = advanced_config

        dash_config = {}
        packaging_options["dash"] = dash_config

        dash_config["fragment_length"] = {
            "num": segment_sizer.numerator,
            "den": segment_sizer.denominator,
        }

        # TODO - segment template time or number (for compatibility)

        return packaging_options
