from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy import VideoFileClip
from typing import Union


class MemeElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
       # TODO: Is always an object (?)
       return cls.build(enhancement.keywords, enhancement.duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        # TODO: Is always an object (?)
        return cls.build(segment.keywords, segment.duration)

    @classmethod
    def build(cls, keywords: str, duration: Union[float, int]):
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)

        youtube_downloader = YoutubeDownloader()

        youtube_downloader.deactivate_ignore_repeated()
        temp_filename = youtube_downloader.download_meme_video(keywords, True, True)
        youtube_downloader.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception('No meme found with the given "keywords": ' + str(keywords) + '.')
        
        video = VideoFileClip(temp_filename)

        if NumberValidator.is_positive_number(duration) and duration < video.duration:
            video = video.with_subclip(0, duration)

        return video