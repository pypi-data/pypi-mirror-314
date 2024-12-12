from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField, EnhancementField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
from youtube_autonomous.segments.builder.stock.stock_downloader import StockDownloader
from yta_multimedia.video.edition.resize import resize_video, ResizeMode
from yta_general_utils.logger import print_in_progress
from moviepy import concatenate_videoclips
from typing import Union


class StockElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        keywords = enhancement.get(EnhancementField.KEYWORDS.value, None)
        duration = enhancement.get('duration', None)

        return cls.build(keywords, duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        keywords = segment.get(SegmentField.KEYWORDS.value, None)
        duration = segment.get('duration', None)

        return cls.build(keywords, duration)

    @classmethod
    def build(cls, keywords: str, duration: Union[float, int]):
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)

        stock_downloader = StockDownloader()

        videos = []
        accumulated_duration = 0
        while accumulated_duration < duration:
            print_in_progress('Downloading stock video')
            # TODO: Make this force 1920x1080 resolution
            downloaded_filename = stock_downloader.download_video(keywords, True)

            if not downloaded_filename:
                # No stock videos available, lets build with AI
                # TODO: Maybe video with stock images (?)
                video = AIImageElementBuilder.build(keywords, duration)
            else:
                # TODO: Read these values from size constants
                video = resize_video(downloaded_filename, (1920, 1080), resize_mode = ResizeMode.RESIZE_KEEPING_ASPECT_RATIO)

            accumulated_duration += video.duration
            # Last clip must be cropped to fit the expected duration
            if accumulated_duration > duration:
                video = video.with_subclip(0, video.duration - (accumulated_duration - duration))
            # TODO: I'm forcing 1920, 1080 here but it must come from Pexels
            videos.append(video)

        return concatenate_videoclips(videos)