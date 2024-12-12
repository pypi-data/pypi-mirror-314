
from youtube_autonomous.segments.enums import SegmentType, EnhancementType, SegmentStatus, ProjectStatus
from youtube_autonomous.segments.enhancement.edition_manual.enums import EditionManualTermContext, EditionManualTermMode
from youtube_autonomous.elements.validator import RULES_SUBCLASSES, BUILDER_SUBCLASSES
from yta_general_utils.programming.parameter_validator import PythonValidator, NumberValidator
from yta_general_utils.file.filename import FileType
from typing import Union


# TODO: This is a new class here because the old one
# was generating a lot of cyclic import issues so we
# are starting from cero again
# TODO: Apply ErrorMessage when possible, please
class ParameterValidator:
    @staticmethod
    def validate_mandatory_parameter(parameter_name: str, parameter_value: any):
        """
        Validate if the provided 'parameter_value' has any
        value or raises an Exception if it is None.
        """
        if not PythonValidator.is_string(parameter_name):
            raise Exception('The provided "parameter_name" is not a string.')
        
        if parameter_value is None:
            raise Exception(f'The provided parameter "{parameter_name}" is None and it is a mandatory parameter.')
        
        return True
    
    @staticmethod
    def validate_string_mandatory_parameter(parameter_name: str, parameter_value: str):
        """
        Validate if the provided 'parameter_value' has a
        string value or raises an Exception if not.
        """
        ParameterValidator.validate_mandatory_parameter(parameter_name, parameter_value)

        if not PythonValidator.is_string(parameter_value):
            raise Exception(f'The provided parameter "{parameter_name}" is not a string.')
        
        return True
    
    @staticmethod
    def validate_positive_number_mandatory_parameter(parameter_name: str, parameter_value: Union[int, float]):
        ParameterValidator.validate_mandatory_parameter(parameter_name, parameter_value)

        if not NumberValidator.is_positive_number(parameter_value):
            raise Exception(f'The provided parameter "{parameter_name}" is not a numeric value.')
        
        return True
    
    @staticmethod
    def validate_is_class(parameter_name: str, parameter_value: any, classes: list):
        if not PythonValidator.is_class(parameter_value, classes):
            # TODO: Show 'classes' as string for the error message
            raise Exception(f'The provided parameter "{parameter_name}" is not a parameter of the provided classes.')
        
        return True

    @staticmethod
    def validate_is_bool(parameter_name: str, parameter_value: bool):
        if not PythonValidator.is_boolean(parameter_value):
            raise Exception(f'The provided parameter "{parameter_name}" is not a bool parameter.')

        return True
    
    # TODO: Build this method, please
    # @staticmethod
    # def validate_type_mandatory_parameter(parameter_name: str, parameter_value: any, parameter_type: str):
    #     # TODO: How to validate dynamically (?)
    #     ParameterValidator.validate_mandatory_parameter()


class ElementParameterValidator:
    """
    A class to validate the parameters we often use in our
    code so we can check faster if they are provided and
    valid or not.
    """
    @staticmethod
    def validate_keywords(keywords: str):
        ParameterValidator.validate_string_mandatory_parameter('keywords', keywords)

        return keywords
    
    @staticmethod
    def validate_text(text: str):
        ParameterValidator.validate_string_mandatory_parameter('text', text)

        return text

    @staticmethod
    def validate_premade_name(premade_name: str):
        ParameterValidator.validate_string_mandatory_parameter('premade_name', premade_name)
        # TODO: Maybe validate if it is a valid premade key (?)

        return premade_name

    @staticmethod
    def validate_text_class_name(text_class_name: str):
        ParameterValidator.validate_string_mandatory_parameter('text_class_name', text_class_name)

        return text_class_name
    
    @staticmethod
    def validate_effect_name(effect_name: str):
        ParameterValidator.validate_string_mandatory_parameter('effect_name', effect_name)

        return effect_name
    
    @staticmethod
    def validate_duration(duration: Union[int, float]):
        ParameterValidator.validate_positive_number_mandatory_parameter('duration', duration)

        return duration

    # TODO: Check methods below

    @staticmethod
    def validate_url(url: str, is_mandatory: bool = True):
        if is_mandatory:
            ParameterValidator.validate_string_mandatory_parameter('url', url)

        # TODO: Validate if url is ok means sending a request
        # which could be an unexpected situation, but I keep
        # this comment here to let you know
        # url_is_ok(url)

        return url
    
    @staticmethod
    def validate_filename(filename: str, file_type: FileType = None, is_mandatory = True):
        if is_mandatory:
            ParameterValidator.validate_string_mandatory_parameter('filename', filename)

        # TODO: Validate file exists (?)
        # cls.validate_file_exists('filename', filename)
        # TODO: Validate file type (?)
        # if file_type:
        #     cls.validate_filename_is_type('filename', filename, file_type)

        return filename
    
    @staticmethod
    def validate_rules(rules: 'ElementRules'):
        """
        Validate the provided ElementRules 'rules'.
        """
        if type(rules).__name__ not in RULES_SUBCLASSES:
            raise Exception('The provided "rules" are not ElementRules.')
            # raise Exception(ErrorMessage.parameter_is_not_rules('rules'))
        
        return rules
    
    @staticmethod
    def validate_builder(builder: 'ElementBuilder'):
        """
        Validate the provided ElementBuilder 'builder'.
        """
        if type(builder).__name__ not in BUILDER_SUBCLASSES:
            raise Exception('The provided "builder" is not an ElementBuilder.')
            # raise Exception(ErrorMessage.parameter_is_not_builder('builder'))

        return builder
    
    @staticmethod
    def validate_segment_type(type: Union[SegmentType, str]):
        SegmentType.to_enum(type)

    @staticmethod
    def validate_enhancement_type(type: Union[EnhancementType, str]):
        EnhancementType.to_enum(type)

    @staticmethod
    def validate_segment_or_enhancement_type(type: Union[SegmentType, EnhancementType, str]):
        enum_type = None
        try:
            enum_type = SegmentType.to_enum(type)
        except:
            pass

        if not enum_type:
            try:
                enum_type = EnhancementType.to_enum(type)
            except:
                pass

        if not enum_type:
            raise Exception('The provided "type" parameter is not a valid SegmentType or EnhancementType.')
        
        return enum_type
    
    # TODO: Continue here

    @staticmethod
    def validate_segment_status(status: Union[SegmentStatus, str]):
        SegmentStatus.to_enum(status)

    @staticmethod
    def validate_project_status(status: Union[ProjectStatus, str]):
        ProjectStatus.to_enum(status)

    @staticmethod
    def validate_edition_manual_term_mode(mode: Union[EditionManualTermMode, str]):
        EditionManualTermMode.to_enum(mode)

    @staticmethod
    def validate_edition_manual_term_context(context: Union[EditionManualTermContext, str]):
        EditionManualTermContext.to_enum(context)

    @staticmethod
    def validate_edition_manual_term(edition_manual_term: dict):
        _, term_content = next(iter(edition_manual_term.items()))

        # TODO: Apply Enums (?)
        ElementParameterValidator.validate_edition_manual_term_mode(term_content.get('mode', None))
        ElementParameterValidator.validate_edition_manual_term_context(term_content.get('context', None))

        enhancements = term_content.get('enhancements', None)
        if enhancements is None:
            raise Exception('No "enhancements" field found in the provided "edition_manual_term".')
        
        if len(enhancements) == 0:
            raise Exception('The "enhancements" field is empty.')
    
        # TODO: Cyclic import error
        # for enhancement in enhancements:
        #     ElementParameterValidator.validate_segment_or_enhancement(enhancement)

    @staticmethod
    def validate_transcription_parameter(transcription: list[dict]):
         if any(key not in transcription_word for key in ['text', 'start', 'end'] for transcription_word in transcription):
            raise Exception('At least one term of the provided "transcription" parameter has no "text", "start" or "end" field.')
