# TODO: Remove this in a near future

from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement, EnhancementMode
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from yta_multimedia.video.utils import parse_parameter_as_moviepy_clip
from yta_general_utils.downloader.audio import download_audio
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, AudioFileClip
from typing import Union


class SoundEnhancementElement(EnhancementElement):
    @classmethod
    def get_valid_modes(cls):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.

        See this link: https://www.notion.so/Segment-types-configuration-107f5a32d46280beb793d84a2af7f75e?pvs=4
        """
        return [EnhancementMode.OVERLAY]
    
    @classmethod
    def get_default_mode(cls):
        """
        The EnhancementMode enum defined as value by default.
        """
        return EnhancementMode.OVERLAY

    @property
    def valid_modes(self):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.

        See this link: https://www.notion.so/Segment-types-configuration-107f5a32d46280beb793d84a2af7f75e?pvs=4
        """
        return SoundEnhancementElement.get_valid_modes()

    def _build(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        youtube_downloader = YoutubeDownloader()

        filename = ''
        if self.filename:
            filename = self.filename
        elif self.url:
            filename = download_audio(self.url)
        elif self.keywords:
            youtube_downloader.activate_ignore_repeated()
            filename = youtube_downloader.download_sound_audio(self.keywords)
            youtube_downloader.deactivate_ignore_repeated()

        enhancement_clip = AudioFileClip(filename)

        super().recalculate_duration(enhancement_clip, video)

        return enhancement_clip

    def apply(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        video = parse_parameter_as_moviepy_clip(video)

        enhancement_clip = self._build(video)

        video = super().apply(enhancement_clip, video)

        return video