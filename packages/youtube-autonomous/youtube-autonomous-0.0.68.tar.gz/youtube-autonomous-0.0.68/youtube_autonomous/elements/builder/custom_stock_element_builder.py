from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField, EnhancementField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from yta_general_utils.logger import print_in_progress
from yta_general_utils.temp import create_temp_filename
from moviepy import VideoFileClip, concatenate_videoclips
from typing import Union


class CustomStockElementBuilder(ElementBuilder):
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

        youtube_downloader = YoutubeDownloader()

        videos = []
        do_use_youtube = True # to stop searching in Youtube if no videos available
        accumulated_duration = 0
        while accumulated_duration < duration:
            downloaded_filename = None
            if do_use_youtube:
                # We try to download if from Youtube
                print_in_progress('Downloading youtube stock video')
                youtube_stock_video = youtube_downloader.get_stock_video(keywords)
                if youtube_stock_video:
                    downloaded_filename = youtube_stock_video.download_with_audio(output_filename = create_temp_filename('youtube.mp4'))
                    if downloaded_filename:
                        youtube_downloader.add_ignored_id(youtube_stock_video.id)

            if not downloaded_filename:
                # Not found or not searching on Youtube, so build 'stock'
                print_in_progress('Downloading stock video (youtube not found)')
                do_use_youtube = False
                video = StockElementBuilder.build(keywords, duration)
            else:
                video = VideoFileClip(downloaded_filename)

            accumulated_duration += video.duration

            if accumulated_duration > duration:
                end = video.duration - (accumulated_duration - duration)
                start = 0
                if youtube_stock_video:
                    if youtube_stock_video.key_moment != 0:
                        # Ok, lets use that key moment as the center of our video
                        start = youtube_stock_video.key_moment - (end / 2)
                        end = youtube_stock_video.key_moment + (end / 2)
                        if start < 0:
                            end += abs(0 - start)
                            start = 0
                        if end > video.duration:
                            start -= abs(end - video.duration)
                            end = video.duration
                    video = video.with_subclip(start, end)
                else:
                    video = video.with_subclip(start, end)

            videos.append(video)

        return concatenate_videoclips(videos)