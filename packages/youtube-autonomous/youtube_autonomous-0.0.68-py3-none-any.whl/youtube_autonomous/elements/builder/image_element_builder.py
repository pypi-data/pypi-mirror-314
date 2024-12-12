from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.enums import SegmentField
from yta_multimedia.image.edition.resize import resize_image_scaling
from yta_multimedia.video.generation import generate_video_from_image
from yta_general_utils.downloader.image import download_image
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import create_temp_filename
from typing import Union


class ImageElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'IMAGE' content for the
    segments.
    """
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        # TOOD: Here, what about duration or 'calculated_duration' (?)
        if enhancement.filename:
            return cls.build_from_filename(enhancement.filename, enhancement.duration)
        return cls.build_from_url(enhancement.url, enhancement.duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        # TOOD: Here, what about duration or 'calculated_duration' (?)
        if segment.filename:
            return cls.build_from_filename(segment.filename, segment.duration)
        return cls.build_from_url(segment.url, segment.duration)

    @classmethod
    def build_from_filename(cls, filename: str, duration: Union[float, int]):
        ElementParameterValidator.validate_filename(filename)
        ElementParameterValidator.validate_duration(duration)

        return cls.image_to_video(filename, duration, None)

    @classmethod
    def build_from_url(cls, url: str, duration: Union[float, int]):
        ElementParameterValidator.validate_url(url)
        ElementParameterValidator.validate_duration(duration)

        # TODO: Try to do all this process in memory, writting not the image
        image_filename = download_image(url)

        return cls.image_to_video(image_filename, duration, None)
    
    @classmethod
    def build_from_filename_from_segment(cls, segment: dict):
        filename = segment.get(SegmentField.FILENAME.value, None)
        duration = segment.get('duration', None)

        return cls.build_from_filename(filename, duration)

    @classmethod
    def build_from_url_from_segment(cls, segment: dict):
        url = segment.get(SegmentField.URL.value, None)
        duration = segment.get('duration', None)

        return cls.build_from_url(url, duration)
    
    # TODO: Move this to a helper (?)
    @classmethod
    def image_to_video(cls, filename: str, duration: Union[float, int], effect = None):
        ElementParameterValidator.validate_filename(filename)
        ElementParameterValidator.validate_duration(duration)
        
        # Resize image to fit the screen
        tmp_image_filename = create_temp_filename(f'image{get_file_extension(filename)}')
        resize_image_scaling(filename, 1920, 1080, tmp_image_filename)

        # TODO: Apply and Effect (this need work)
        video = generate_video_from_image(tmp_image_filename, duration, effect)

        return video