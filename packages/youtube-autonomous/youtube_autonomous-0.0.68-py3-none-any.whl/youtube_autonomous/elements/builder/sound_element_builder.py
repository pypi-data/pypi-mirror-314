from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField, EnhancementField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy import AudioFileClip
from typing import Union


class SoundElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        keywords = enhancement.get(EnhancementField.KEYWORDS.value, None)
        duration = enhancement.get('duration', None)

        return cls.build(keywords, duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        keywords = segment.get(SegmentField.KEYWORDS.value, None)
        duration = segment.get(SegmentField.DURATION.value, None)

        return cls.build(keywords, duration)

    @classmethod
    def build(cls, keywords: str, duration: Union[float, int]) -> AudioFileClip:
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)

        youtube_downloader = YoutubeDownloader()

        youtube_downloader.deactivate_ignore_repeated()
        temp_filename = youtube_downloader.download_sound_audio(keywords)
        youtube_downloader.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception('No sound found with the given "keywords": ' + str(keywords) + '.')
        
        audio = AudioFileClip(temp_filename)

        if NumberValidator.is_positive_number(duration) and duration < audio.duration:
            audio = audio.with_subclip(0, duration)

        return audio