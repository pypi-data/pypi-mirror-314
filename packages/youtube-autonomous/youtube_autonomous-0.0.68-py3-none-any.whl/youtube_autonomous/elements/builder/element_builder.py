from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator, ParameterValidator
from youtube_autonomous.segments.enums import SegmentType, EnhancementType
from youtube_autonomous.segments.builder.ai import create_ai_narration
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from typing import Union


class ElementBuilder:
    # TODO: Maybe __init__ that returns the corresponding subclass
    # according to the provided 'type' (?)
    # https://stackoverflow.com/questions/9187388/possible-to-prevent-init-from-being-called

    @staticmethod
    def get_subclasses():
        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        return [
            AIImageElementBuilder,
            AIVideoElementBuilder,
            ImageElementBuilder,
            VideoElementBuilder,
            CustomStockElementBuilder,
            StockElementBuilder,
            MemeElementBuilder,
            SoundElementBuilder,
            YoutubeVideoElementBuilder,
            TextElementBuilder,
            PremadeElementBuilder,
            EffectElementBuilder,
            GreenscreenElementBuilder
        ]

    @staticmethod
    def get_subclasses_as_str():
        return ', '.join(ElementBuilder.get_subclasses())
    
    @staticmethod
    def get_subclass_by_type(type: Union[SegmentType, EnhancementType, str]):
        type = ElementParameterValidator.validate_segment_or_enhancement_type(type)

        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        if type in [SegmentType.MEME, EnhancementType.MEME]:
            return MemeElementBuilder
        elif type in [SegmentType.AI_IMAGE, EnhancementType]:
            return AIImageElementBuilder
        elif type in [SegmentType.AI_VIDEO, EnhancementType.AI_VIDEO]:
            return AIVideoElementBuilder
        elif type in [SegmentType.IMAGE, EnhancementType.IMAGE]:
            return ImageElementBuilder
        elif type in [SegmentType.VIDEO, EnhancementType.VIDEO]:
            return VideoElementBuilder
        elif type in [SegmentType.STOCK, EnhancementType.STOCK]:
            return StockElementBuilder
        elif type in [SegmentType.CUSTOM_STOCK, EnhancementType.CUSTOM_STOCK]:
            return CustomStockElementBuilder
        elif type in [SegmentType.SOUND, EnhancementType.SOUND]:
            return SoundElementBuilder
        elif type in [SegmentType.YOUTUBE_VIDEO, EnhancementType.YOUTUBE_VIDEO]:
            return YoutubeVideoElementBuilder
        elif type in [SegmentType.TEXT, EnhancementType.TEXT]:
            return TextElementBuilder
        elif type in [SegmentType.PREMADE, EnhancementType.PREMADE]:
            return PremadeElementBuilder
        elif type in [EnhancementType.EFFECT]:
            return EffectElementBuilder
        elif type in [EnhancementType.GREENSCREEN]:
            return GreenscreenElementBuilder
    
    @classmethod
    def build_narration(cls, text: str, output_filename: str):
        """
        Generates a narration file that narrates the 'text' provided and
        is stored locally as 'output_filename'. If 'text' or 
        'output_filename' fields are not provided it will raise an 
        Exception.
        """
        ParameterValidator.validate_string_mandatory_parameter('text', text)
        ParameterValidator.validate_string_mandatory_parameter('output_filename', output_filename)

        return create_ai_narration(text, output_filename = output_filename)
    
    @classmethod
    def extract_extra_params(cls, element, method, params_to_ignore: list[str] = ['self', 'cls', 'args', 'kwargs']):
        """
        Returns an object containing 'mandatory' and 'optional' fields that
        are the parameters extracted from the provided 'element' 'extra_data'
        field and according to the also provided 'method' (the parameters in
        the signature of that 'method' are the ones that are extracted).

        This method raises an exception if some of the 'mandatory' fields are
        not given in the 'extra_data' field.
        """
        parameters_needed = ParameterObtainer.get_parameters_from_method(method, params_to_ignore)  
        parameters = {}

        if isinstance(element, dict):
            extra_params = element.get('extra_params')
        else:
            extra_params = element.extra_params

        if not extra_params and not isinstance(extra_params, dict):
            raise Exception('No "extra_params" found.')

        missing_mandatory_parameters = []
        for mandatory_parameter in parameters_needed['mandatory']:
            if not mandatory_parameter in extra_params:
                missing_mandatory_parameters.append(mandatory_parameter)
            else:
                parameters[mandatory_parameter] = extra_params[mandatory_parameter]

        if len(missing_mandatory_parameters) > 0:
            missing_params_str = ', '.join(missing_mandatory_parameters)
            raise Exception(f'The extra parameters "{missing_params_str}" are missing on the provided element and they are needed to build it.')

        for optional_parameter in parameters_needed['optional']:
            if optional_parameter in extra_params:
                parameters[optional_parameter] = extra_params[optional_parameter]

        return parameters
    
    @classmethod
    def handle_narration_from_segment(cls, segment: dict):
        pass