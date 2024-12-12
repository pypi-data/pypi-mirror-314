from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import EnhancementField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_general_utils.file.filename import FileType
from yta_general_utils.downloader.video import download_video
from yta_general_utils.temp import create_temp_filename
from moviepy import VideoFileClip
from typing import Union


class VideoElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        filename = enhancement.get(EnhancementField.FILENAME.value, None)
        url = enhancement.get(EnhancementField.URL.value, None)
         # TODO: I should always have 'calculated_duration' when duration
        # has been processed
        duration = enhancement.get('duration', None)

        # TODO: What about this strategy. Do we apply the strategy here or
        # should get the call when its been applied (?)
        # By now I'm applying it here, feel free to change this in when
        # you know
        if filename and url:
            return cls.build_from_filename(filename)
        elif url:
            return cls.build_from_url(url)
        
        raise Exception('No "url" nor "filename" provided.')

    @classmethod
    def build_from_segment(cls, segment: dict):
        filename = segment.filename
        url = segment.url
         # TODO: I should always have 'calculated_duration' when duration
        # has been processed
        duration = segment.duration

        # TODO: What about this strategy. Do we apply the strategy here or
        # should get the call when its been applied (?)
        # By now I'm applying it here, feel free to change this in when
        # you know
        if filename and url:
            return cls.build_from_filename(filename, duration)
        elif url:
            return cls.build_from_url(url, duration)
        
        raise Exception('No "url" nor "filename" provided.')

    @classmethod
    def build_from_filename(cls, filename: str, duration: Union[float, int]):
        ElementParameterValidator.validate_filename(filename, FileType.VIDEO)
        ElementParameterValidator.validate_duration(duration)

        video = VideoFileClip(filename)

        if duration < video.duration:
            video = video.with_subclip(0, duration)

        return video

    @classmethod
    def build_from_url(cls, url: str, duration: Union[float, int]):
        ElementParameterValidator.validate_url(url)
        ElementParameterValidator.validate_duration(duration)

        # TODO: Try to do all this process in memory, writting not the video
        tmp_filename = create_temp_filename('video.mp4')
        download_video(url, tmp_filename)

        video = VideoFileClip(tmp_filename)

        if duration < video.duration:
            video = video.with_subclip(0, duration)

        return video