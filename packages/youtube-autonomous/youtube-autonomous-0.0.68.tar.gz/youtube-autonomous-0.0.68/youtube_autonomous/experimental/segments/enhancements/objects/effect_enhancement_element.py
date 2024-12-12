# TODO: Remove this in a near future

from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement, EnhancementMode
from yta_multimedia.video.utils import parse_parameter_as_moviepy_clip
from yta_multimedia.video.edition.effect.moviepy.black_and_white_moviepy_effect import BlackAndWhiteMoviepyEffect
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class EffectEnhancementElement(EnhancementElement):
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
        return EffectEnhancementElement.get_valid_modes()

    def _build(self, video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, str]):
        super().recalculate_duration(None, video)
        
        enhancement_clip = None
        end = self.start + self.duration
        if self.keywords == 'black_and_white':
            parameters = {}
            # TODO: Read parameters from attributes
            enhancement_clip = BlackAndWhiteMoviepyEffect(video.with_subclip(self.start, end)).apply(parameters)
        
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


