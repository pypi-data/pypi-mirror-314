from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import TextPremade
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from moviepy import VideoFileClip


class TextElementBuilder(ElementBuilder):
    @classmethod
    def text_premade_name_to_class(cls, text_premade_name: str):
        """
        Returns the corresponding text premade class according to
        the provided 'text_premade_name'. If no text premade class
        found, the return will be None.
        """
        valid_name = TextPremade.get_valid_name(text_premade_name)

        if not valid_name:
            raise Exception(f'The provided text premade name "{text_premade_name}" is not valid. The valid ones are: {TextPremade.get_all_names_as_str()}')
        
        return TextPremade[valid_name].value

    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        text_premade_name = enhancement.keywords

        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration', 'text']
        parameters_not_from_extra = ['duration', 'text']
        parameters = cls.get_building_parameters(enhancement, parameters_to_ignore, parameters_not_from_extra)

        return cls.build_custom_from_text_premade_name(text_premade_name, **parameters)

    @classmethod
    def build_from_segment(cls, segment: dict):
        text_premade_name = segment.keywords

        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration', 'text']
        parameters_not_from_extra = ['duration', 'text']
        parameters = cls.get_building_parameters(segment, parameters_to_ignore, parameters_not_from_extra)

        return cls.build_custom_from_text_premade_name(text_premade_name, **parameters)
    
    @classmethod
    def build_custom_from_text_premade_name(cls, text_premade_name, **parameters):
        """
        This method instantiates the 'text_animation_class' Manim
        text animation class and uses the provided 'parameters' to
        build the text animation. The provided 'parameters' must 
        fit the ones requested by the provided class 'generate'
        method.
        """
        ElementParameterValidator.validate_premade_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)

        # We generate the animation to return it
        filename = text_premade_class().generate(**parameters)

        # TODO: Maybe 'mask' to set background as transparent if available (?)
        return VideoFileClip(filename)
    
    @classmethod
    def get_building_parameters(cls, element: dict, parameters_to_ignore: list[str], parameters_not_from_extra: list[str]):
        """
        This method extracts the parameters needed for building the text
        premade that exist in the 'extra_params' field of the provided
        'element' dict, replaces the ones in 'not_extra_parameters' with
        the ones in the main 'element' dict and, finally, keeps the only
        parameters needed to build the effect and returns them. This means
        that only the 'mandatory' or 'optional' parameters to build the
        effect, if existing, will be returned extracted from where it was
        specified.
        """
        text_premade_name = element.keywords
        
        ElementParameterValidator.validate_text_class_name(text_premade_name)

        text_premade_class = cls.text_premade_name_to_class(text_premade_name)
        parameters = ElementBuilder.extract_extra_params(element, text_premade_class.generate, parameters_to_ignore)

        # TODO: What if not extra parameter does not exist in main (?)
        for parameter_not_from_extra in parameters_not_from_extra:
            parameters[parameter_not_from_extra] = getattr(element, parameter_not_from_extra)
        
        actual_parameters = ParameterObtainer.get_parameters_from_method(text_premade_class.generate)

        # We keep only 'mandatory' or 'optional' parameters removing useless
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return parameters