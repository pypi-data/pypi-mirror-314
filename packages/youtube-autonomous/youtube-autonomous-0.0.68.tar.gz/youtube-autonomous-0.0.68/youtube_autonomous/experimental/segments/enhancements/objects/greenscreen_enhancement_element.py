# TODO: Remove this in a near future

from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement, EnhancementMode
from yta_multimedia.video.utils import parse_parameter_as_moviepy_clip
from yta_multimedia.greenscreen.custom.image_greenscreen import ImageGreenscreen
from yta_multimedia.greenscreen.custom.video_greenscreen import VideoGreenscreen
from yta_general_utils.downloader.google_drive import download_file_from_google_drive
from yta_general_utils.file.checker import file_is_video_file
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class GreenscreenEnhancementElement(EnhancementElement):
    @classmethod
    def get_valid_modes(cls):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.

        See this link: https://www.notion.so/Segment-types-configuration-107f5a32d46280beb793d84a2af7f75e?pvs=4
        """
        return [EnhancementMode.REPLACE]

    @classmethod
    def get_default_mode(cls):
        """
        The EnhancementMode enum defined as value by default.
        """
        return EnhancementMode.REPLACE

    @property
    def valid_modes(self):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.

        See this link: https://www.notion.so/Segment-types-configuration-107f5a32d46280beb793d84a2af7f75e?pvs=4
        """
        return GreenscreenEnhancementElement.get_valid_modes()

    def _build(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        filename = ''
        if self.filename:
            filename = self.filename
        elif self.url:
            # TODO: This won't work, I need to modify this method to
            # accept different type of urls and analyze them
            # TODO: By now, accept only Google Drive urls
            filename = download_file_from_google_drive(self.url)
        elif self.keywords:
            # TODO: Look for green screens in a new channel that I must
            # create about greenscreen backgrounds only
            # TODO: By now I'm forcing this ImageScreen
            filename = download_file_from_google_drive('https://drive.google.com/file/d/1WQVnXY1mrw-quVXOqTBJm8x9scEO_JNz/view?usp=drive_link')

        if file_is_video_file(filename):
            greenscreen = VideoGreenscreen(filename)
            # TODO: If 'filename' duration is less than 'video' we
            # should, at least, let the user know that we will make
            # our own modification strategy
        else:
            greenscreen = ImageGreenscreen(filename)

        super().recalculate_duration(None, video)

        end = self.start + self.duration
        enhancement_clip = greenscreen.from_video_to_video(video.with_subclip(self.start, end))

        return enhancement_clip
    
    def apply(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        """
        This method will apply this Enhancement Element in the provided
        'video' and will return it modified including the generated
        enhancement clip.
        """
        video = parse_parameter_as_moviepy_clip(video)

        enhancement_clip = self._build(video)
        
        video = super().apply(enhancement_clip, video)

        return video


