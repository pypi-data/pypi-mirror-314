from youtube_autonomous.segments.enums import SegmentField, EnhancementField, ShortcodeType, EnhancementMode, ShortcodeStringDuration, EnhancementStringDuration, SegmentStringDuration, EnhancementStringDuration, SegmentMode, ShortcodeMode, ShortcodeField, SegmentStart, EnhancementStart, ShortcodeStart
from youtube_autonomous.config import Configuration
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


# TODO: Move this enum to enums file
class Component(Enum):
    SEGMENT = 'segment'
    ENHANCEMENT = 'enhancement'
    SHORTCODE = 'shortcode'

class ElementValidator:
    """
    Class to validate the segment o enhancement element fields and
    their values.
    """
    @staticmethod
    def validate_segment_fields(segment: dict):
        """
        Validates that the 'segment' dictionary provided has all the
        required segment fields and only those ones and raises an
        Exception if more parameters or less parameters exist.

        This method returns the 'segment' provided if everything is
        ok.
        """
        return ElementValidator.validate_fields(Component.SEGMENT, segment)

    @staticmethod
    def validate_enhancement_fields(enhancement: dict):
        """
        Validates that the 'enhancement' dictionary provided has 
        all the required enhancement fields and only those ones and 
        raises an Exception if more parameters or less parameters
        exist.

        This method returns the 'enhancement' provided if everything is
        ok.
        """
        return ElementValidator.validate_fields(Component.ENHANCEMENT, enhancement)

    @staticmethod
    def validate_shortcode_fields(shortcode: dict):
        """
        Validates that the 'shortcode' dictionary provided has 
        all the required shortcode fields and only those ones and 
        raises an Exception if more parameters or less parameters
        exist.

        This method returns the 'shortcode' provided if everything is
        ok.
        """
        return ElementValidator.validate_fields(Component.SEGMENT, shortcode)

    @staticmethod
    def validate_fields(component: Component, element: dict):
        if component == Component.SEGMENT:
            accepted_fields = SegmentField.get_all_values()
        elif component == Component.ENHANCEMENT:
            accepted_fields = EnhancementField.get_all_values()
        elif component == Component.SHORTCODE:
            accepted_fields = ShortcodeField.get_all_values()

        accepted_fields_str = ', '.join(accepted_fields)
        unaccepted_fields = [key for key in element.keys() if key not in accepted_fields]
        unaccepted_fields_str = ', '.join(unaccepted_fields)
        missing_fields = [field for field in accepted_fields if field not in element]
        missing_fields_str = ', '.join(missing_fields)

        if missing_fields:
            raise Exception(f'The next fields are mandatory and were not found in the element: "{missing_fields_str}". The mandatory fields are: "{accepted_fields_str}".')

        if unaccepted_fields:
            raise Exception(f'The next fields are not accepted in the provided element by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}".')
        
        return element
    
    @staticmethod
    def validate_segment_mode_field(mode: Union[SegmentMode, str, None]):
        """
        Validates if the provided 'mode' parameter is a valid parameter
        for a segment object. It should be a SegmentMode enum or one of
        its string values to be accepted.
        
        This method will raise an Exception if not valid or will return
        it as it is, or as a SegmentMode if one of its valid string
        values provided.
        """
        return ElementValidator.validate_mode_field(Component.SEGMENT, mode)

    @staticmethod
    def validate_enhancement_mode_field(mode: Union[EnhancementMode, str, None]):
        """
        Validates if the provided 'mode' parameter is a valid parameter
        for an enhancement object. It should be a EnhancementMode enum
        or one of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return
        it as it is, or as a EnhancementMode if one of its valid string
        values provided.
        """
        return ElementValidator.validate_mode_field(Component.ENHANCEMENT, mode)
    
    @staticmethod
    def validate_shortcode_mode_field(mode: Union[ShortcodeMode, str, None]):
        """
        Validates if the provided 'mode' parameter is a valid parameter
        for a shortcode object. It should be a ShortcodeMode enum
        or one of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return
        it as it is, or as a ShortcodeMode if one of its valid string
        values provided.
        """
        return ElementValidator.validate_mode_field(Component.SHORTCODE, mode)
    
    @staticmethod
    def validate_mode_field(component: Component, mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None]):
        if mode is not None:
            if component == Component.SEGMENT:
                mode = SegmentMode.to_enum(mode)
            elif component == Component.ENHANCEMENT:
                mode = EnhancementMode.to_enum(mode)
            elif component == Component.SHORTCODE:
                mode = ShortcodeMode.to_enum(mode)

        return mode

    @staticmethod
    def validate_segment_mode_field_for_type(mode: Union[SegmentMode, str, None], type: str):
        """
        Validates if the provided 'mode' parameter is a valid parameter
        for a segment object of the provided 'type'. The 'mode' parameter
        should be a SegmentMode enum or one of its string values to be
        accepted.
        
        This method will raise an Exception if not valid or will return
        it as it is, or as a SegmentMode if one of its valid string
        values provided.
        """
        return ElementValidator.validate_mode_for_type(Component.SEGMENT, mode, type)

    @staticmethod
    def validate_enhancement_mode_field_for_type(mode: Union[EnhancementMode, str, None], type: str):
        """
        Validates if the provided 'mode' parameter is a valid parameter for
        an enhancement object of the provided 'type'. The 'mode' parameter
        should be an EnhancementMode enum or one of its string values to be
        accepted.
        
        This method will raise an Exception if not valid or will return it
        as it is, or as a EnhancementMode if one of its valid string values
        provided.
        """
        return ElementValidator.validate_mode_for_type(Component.ENHANCEMENT, mode, type)

    @staticmethod
    def validate_shortcode_mode_field_for_type(mode: Union[ShortcodeMode, str, None], type: str):
        """
        Validates if the provided 'mode' parameter is a valid parameter for
        a shortcode object of the provided 'type'. The 'mode' parameter
        should be a ShortcodeMode enum or one of its string values to be
        accepted.
        
        This method will raise an Exception if not valid or will return it
        as it is, or as a ShortcodeMode if one of its valid string values
        provided.
        """
        return ElementValidator.validate_mode_for_type(Component.SHORTCODE, mode, type)
    
    @staticmethod
    def validate_mode_for_type(component: Component, mode: Union[str, None], type: str):
        type = ShortcodeType.to_enum(type)

        if component == Component.SEGMENT:
            config = ElementValidator.get_config_as_segment(type)
            mode = ElementValidator.validate_segment_mode_field(mode)
        elif component == Component.ENHANCEMENT:
            config = ElementValidator.get_config_as_enhancement(type)
            mode = ElementValidator.validate_enhancement_mode_field(mode)
        elif component == Component.SHORTCODE:
            config = ElementValidator.get_config_as_shortcode(type)
            mode = ElementValidator.validate_shortcode_mode_field(mode)

        if not mode in config.modes:
            raise Exception(f'The "{type}" type does not accept the provided "{mode}" mode.')
        
        return mode
    
    @staticmethod
    def validate_segment_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for a segment.

        This method will raise an Exception if not None value 
        provided but a invalid one.
        """
        return ElementValidator.validate_duration_field(Component.SEGMENT, duration)

    @staticmethod
    def validate_enhancement_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for an enhancement.

        This method will raise an Exception if not None value 
        provided but a invalid one.
        """
        return ElementValidator.validate_duration_field(Component.ENHANCEMENT, duration)
    
    @staticmethod
    def validate_shortcode_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for a shortcode.

        This method will raise an Exception if not None value 
        provided but a invalid one.
        """
        return ElementValidator.validate_duration_field(Component.SHORTCODE, duration)
    
    @staticmethod
    def validate_duration_field(component: Component, duration: Union[int, float, str, None]):
        if duration is not None:
            if not NumberValidator.is_positive_number(duration):
                if component == Component.SEGMENT:
                    duration = SegmentStringDuration.to_enum(duration)
                elif component == Component.ENHANCEMENT:
                    duration = EnhancementStringDuration.to_enum(duration)
                elif component == Component.SHORTCODE:
                    duration = ShortcodeStringDuration.to_enum(duration)

        return duration
    
    @staticmethod
    def validate_segment_duration_field_for_type(duration: Union[SegmentStringDuration, int, float, str, None], type: str):
        """
        Validates if the provided 'duration' parameter is a valid
        parameter for a segment object of the provided 'type'. The
        'duration' parameter should be a SegmentStringDuration enum or one
        of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return it
        as it is, or as a SegmentStringDuration if one of its valid string
        values provided.
        """
        return ElementValidator.validate_duration_for_type(Component.SEGMENT, duration, type)
        
    @staticmethod
    def validate_enhancement_duration_field_for_type(duration: Union[EnhancementStringDuration, int, float, str, None], type: str):
        """
        Validates if the provided 'duration' parameter is a valid
        parameter for an enhancement object of the provided 'type'. The
        'duration' parameter should be a EnhancementStringDuration enum or
        one of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return it
        as it is, or as a EnhancementStringDuration if one of its valid
        string values provided.
        """
        return ElementValidator.validate_duration_for_type(Component.ENHANCEMENT, duration, type)
    
    @staticmethod
    def validate_shortcode_duration_field_for_type(duration: Union[ShortcodeStringDuration, int, float, str, None], type: str):
        """
        Validates if the provided 'duration' parameter is a valid
        parameter for a shortcode object of the provided 'type'. The
        'duration' parameter should be a ShortcodeStringDuration enum or
        one of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return it
        as it is, or as a ShortcodeStringDuration if one of its valid
        string values provided.
        """
        return ElementValidator.validate_duration_for_type(Component.SHORTCODE, duration, type)
    
    @staticmethod
    def validate_duration_for_type(component: Component, duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str, None], type: str):
        type = ShortcodeType.to_enum(type)

        if component == Component.SEGMENT:
            config = ElementValidator.get_config_as_segment(type)
            duration = ElementValidator.validate_segment_duration_field(duration)
        elif component == Component.ENHANCEMENT:
            config = ElementValidator.get_config_as_enhancement(type)
            duration = ElementValidator.validate_enhancement_duration_field(duration)
        elif component == Component.SHORTCODE:
            config = ElementValidator.get_config_as_shortcode(type)
            duration = ElementValidator.validate_shortcode_duration_field(duration)

        if not NumberValidator.is_positive_number(duration) and not duration in config.strin_durations:
            raise Exception(f'The "{type.value}" type does not accept the provided "{duration}" duration.')
        
        return duration
    
    @staticmethod
    def validate_segment_start_field(start: Union[int, float, str, None]):
        return ElementValidator.validate_start_field(Component.SEGMENT, start)
    
    @staticmethod
    def validate_enhancemen_start_field(start: Union[int, float, str, None]):
        return ElementValidator.validate_start_field(Component.ENHANCEMENT, start)
    
    @staticmethod
    def validate_shortcode_start_field(start: Union[int, float, str, None]):
        return ElementValidator.validate_start_field(Component.SHORTCODE, start)

    @staticmethod
    def validate_start_field(component: Component, start: Union[int, float, str, None]):
        if start is not None:
            if not NumberValidator.is_positive_number(start):
                if component == Component.SEGMENT:
                    start = SegmentStart.to_enum(start)
                elif component == Component.ENHANCEMENT:
                    start = EnhancementStart.to_enum(start)
                elif component == Component.SHORTCODE:
                    start = ShortcodeStart.to_enum(start)

        return start




    @staticmethod
    def get_config_as_segment(type: str):
        """
        Returns the .config_as_segment if existing or raises an Exception if not.
        """
        config_as_segment = Configuration.get_configuration_by_type(type).config_as_segment
        if not config_as_segment:
            raise Exception(f'The "{type}" type cannot be used as a segment.')
        
        return config_as_segment
    
    @staticmethod
    def get_config_as_enhancement(type: str):
        """
        Returns the .config_as_enhancement if existing or raises an Exception if not.
        """
        config_as_enhancement = Configuration.get_configuration_by_type(type).config_as_enhancement
        if not config_as_enhancement:
            raise Exception(f'The "{type}" type cannot be used as an enhancement.')
        
        return config_as_enhancement
    
    @staticmethod
    def get_config_as_shortcode(type: str):
        """
        Returns the .config_as_shortcode if existing or raises an Exception if not.
        """
        config_as_shortcode = Configuration.get_configuration_by_type(type).config_as_shortcode
        if not config_as_shortcode:
            raise Exception(f'The "{type}" type cannot be used as a shortcode.')
        
        return config_as_shortcode

