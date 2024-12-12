from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.config import MAX_DURATION_PER_IMAGE, MIN_DURATION_PER_IMAGE
from youtube_autonomous.segments.builder.ai import create_ai_image
from moviepy import concatenate_videoclips
from typing import Union


class AIImageElementBuilder(ElementBuilder):
    """
    Builder to obtain videos generated with AI image (or images) 
    turned into video.
    """
    @classmethod
    def get_images_array(cls, keywords: str, duration: Union[float, int]):
        """
        Builds an array containing as much image descriptions as
        needed to build a video of 'duration' seconds according
        to our MAX_DURATION_PER_IMAGE configuration settings.

        Each image of the array will have 'keywords' and 'duration'
        fields to be able to build the video.

        TODO: The 'keywords' field is not necessary in each array
        element, but...
        """
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)

        images = []
        if duration > MAX_DURATION_PER_IMAGE:
            number_of_images = int(duration / MAX_DURATION_PER_IMAGE)
            for _ in range(number_of_images):
                images.append({
                    'keywords': keywords,
                    'duration': MAX_DURATION_PER_IMAGE
                })

            remaining_duration = duration % MAX_DURATION_PER_IMAGE
            if remaining_duration <= MIN_DURATION_PER_IMAGE:
                # We won't create an image animation that is too short, we
                # will make the previous one longer
                images[len(images) - 1]['duration'] += remaining_duration
            else:
                images.append({
                    'keywords': keywords,
                    'duration': remaining_duration
                })
        else:
            images.append({
                'keywords': keywords,
                'duration': duration
            })

        return images

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
        images = cls.get_images_array(keywords, duration)

        videos = []
        for image in images:
            videos.append(cls.ai_image_to_video(image.get('keywords'), image.get('duration'), None))

        video = concatenate_videoclips(videos)

        return video
    
    @classmethod
    def ai_image_to_video(cls, keywords: str, duration: Union[float, int], effect = None):
        """
        Creates an AI image with the provided 'keywords' and builds a video
        that lasts 'duration' seconds with the given 'effect'.

        TODO: Apply 'effect' that is not working by now
        """
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)
        
        return ImageElementBuilder.image_to_video(create_ai_image(keywords), duration, effect)