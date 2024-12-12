from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.enums import Premade
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from moviepy import VideoFileClip


class PremadeElementBuilder(ElementBuilder):
    @classmethod
    def premade_name_to_class(cls, premade_name: str):
        """
        Returns the corresponding premade class according to the
        provided 'premade_name'. If no premade class found, the
        return will be None.
        """
        valid_name = Premade.get_valid_name(premade_name)

        if not valid_name:
            raise Exception(f'The provided premade name "{premade_name}" is not valid. The valid ones are: {Premade.get_all_names_as_str()}')
        
        return Premade[valid_name].value

    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        premade_name = enhancement.keywords

        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'duration']
        parameters_not_from_extra = ['duration']
        parameters = cls.get_building_parameters(enhancement, parameters_to_ignore, parameters_not_from_extra)

        premade_class = cls.premade_name_to_class(premade_name)

        generated = premade_class().generate(**parameters)

        if isinstance(generated, str):
            # If the premade is generated with manim we will only
            # get the filename as return, so we need it as a clip
            generated = VideoFileClip(generated)

        return generated

    @classmethod
    def build_from_segment(cls, segment: dict):
        premade_name = segment.keywords

        parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'duration']
        parameters_not_from_extra = ['duration']
        parameters = cls.get_building_parameters(segment, parameters_to_ignore, parameters_not_from_extra)

        premade_class = cls.premade_name_to_class(premade_name)

        generated = premade_class().generate(**parameters)

        if isinstance(generated, str):
            # If the premade is generated with manim we will only
            # get the filename as return, so we need it as a clip
            generated = VideoFileClip(generated)

        return generated

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
        premade_name = element.keywords
        
        ElementParameterValidator.validate_premade_name(premade_name)

        premade_class = cls.premade_name_to_class(premade_name)
        parameters = ElementBuilder.extract_extra_params(element, premade_class.generate, parameters_to_ignore)

        # TODO: What if not extra parameter does not exist in main (?)
        for parameter_not_from_extra in parameters_not_from_extra:
            parameters[parameter_not_from_extra] = getattr(element, parameter_not_from_extra)
        
        actual_parameters = ParameterObtainer.get_parameters_from_method(premade_class.generate)

        # We keep only 'mandatory' or 'optional' parameters removing useless
        parameters = {key: value for key, value in parameters.items() if key in actual_parameters['mandatory'] or key in actual_parameters['optional']}

        return parameters