# TODO: Remove this in a near future

from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement, EnhancementMode
from yta_multimedia.video.utils import parse_parameter_as_moviepy_clip
from yta_multimedia.video.generation import generate_video_from_image
from yta_multimedia.image.edition.filter.sticker import image_file_to_sticker
from yta_general_utils.downloader.image import download_image
from yta_general_utils.temp import create_temp_filename
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class StickerEnhancementElement(EnhancementElement):
    @classmethod
    def get_valid_modes(cls):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.

        See this link: https://www.notion.so/Segment-types-configuration-107f5a32d46280beb793d84a2af7f75e?pvs=4
        """
        return [EnhancementMode.INLINE, EnhancementMode.OVERLAY]
    
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
        return StickerEnhancementElement.get_valid_modes()

    def _build(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        filename = ''
        if self.filename:
            filename = self.filename
        elif self.url:
            filename = download_image(self.url)
        elif self.keywords:
            # TODO: Search image and download it from somewhere
            filename = download_image('https://png.pngtree.com/thumb_back/fh260/background/20230611/pngtree-wolf-animals-images-wallpaper-for-pc-384x480-image_2916211.jpg')

        tmp_filename = create_temp_filename('image.png')
        image_file_to_sticker(filename, tmp_filename)
        enhancement_clip = generate_video_from_image(tmp_filename, self.duration)

        super().recalculate_duration(enhancement_clip, video)

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