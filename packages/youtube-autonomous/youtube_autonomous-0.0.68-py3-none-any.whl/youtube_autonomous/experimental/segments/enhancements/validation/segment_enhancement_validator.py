# TODO: Remove this in a near future

from youtube_autonomous.segments.enums import EnhancementField, EnhancementType, EnhancementDuration, EnhancementStart, EnhancementMode
from yta_general_utils.checker.type import variable_is_positive_number
from typing import Union


class SegmentEnhancementValidator:
    """
    This class is to validate the Segment enhancement elements that
    are terms that the user register to enhance (to improve) the
    project video experience.

    These terms need to have a valid structure and that's what we
    check here.
    """
    def is_valid(enhancement_terms):
        """
        We will receive the content of a enhancement term and will raise an
        Exception if some structure element or value is not valid according
        to our rules.

        TODO: Write a little bit more about what we are receiving here.
        """
        # TODO: Maybe refactor the terms to simplify them
        for enhancement_term_key in enhancement_terms:
            enhancement_term = enhancement_terms[enhancement_term_key]
            for type in enhancement_term:
                content = enhancement_term[type]
                if not EnhancementType.is_valid(type):
                    raise Exception('Enhancement element type "' + type + '" not accepted.')

                # Lets check values
                keywords = content.get(EnhancementField.KEYWORDS.value)
                filename = content.get(EnhancementField.FILENAME.value)
                url = content.get(EnhancementField.URL.value)
                start = content.get(EnhancementField.START.value)
                mode = content.get(EnhancementField.MODE.value)
                duration = content.get(EnhancementField.DURATION.value)

                if not keywords and not filename and not url:
                    raise Exception('No "keywords" nor "filename" nor "url" provided.')
                
                # TODO: Search for the element with 'keywords' to check that it
                # doesn't exist (or it does)
                # TODO: Check that provided 'filename' is a valid file and the
                # type is appropriate for the type
                # TODO: Check that the provided 'url' is valid, available and
                # suitable for the type we want
                
                if type == EnhancementType.MEME.value and not keywords:
                    raise Exception(f'No "keywords" provided when necessary for the "{EnhancementType.MEME.value}" type.')

                start_values = EnhancementStart.get_all_values()
                if start and start not in start_values and not variable_is_positive_number(start):
                    
                    raise Exception(f'No valid "start" value provided. Must be one of these "{EnhancementStart.get_all_values_as_str()}" or a valid positive number (including 0).')

                duration_values = EnhancementDuration.get_all_values()
                if duration and duration not in duration_values and not variable_is_positive_number(duration):
                    raise Exception(f'No valid "duration" value provided. Must be one of these "{EnhancementDuration.get_all_values_as_str()}" or a valid positive number (including 0).')

                mode_values = EnhancementMode.get_all_values()
                if mode and mode not in mode_values:
                    raise Exception(f'No valid "mode" value provided. Must be one of these "{EnhancementMode.get_all_values_as_str()}".')
                
    @classmethod
    def validate_type(cls, type: Union[EnhancementType, str]):
        """
        This method validates if the provided 'type' parameter is an
        EnhancementType enum or if it is a valid string value 
        of a EnhancementType enum.

        This method will raise an Exception if any of the rules are 
        not fit.
        """
        if not type:
            raise Exception('No "type" provided.')
        
        if not isinstance(type, (EnhancementType, str)):
            raise Exception(f'The "type" parameter provided {type} is not an EnhancementType nor a string.')
        
        if isinstance(type, str):
            if not EnhancementType.is_valid(type):
                raise Exception(f'The "type" parameter provided {type} is not a valid EnhancementType value.')
            
            type = EnhancementType(type)

    @classmethod
    def validate_duration(cls, duration: Union[EnhancementDuration, int, float, str]):
        """
        This method validates if the provided 'duration' parameter is a valid
        and positive numeric value, if it is a EnhancementDuration
        enum or if it is a valid string value of a EnhancementDuration
        enum.

        This method will raise an Exception if any of the rules are not fit.
        """
        # 'duration' can be a EnhancementDuration enum, a positive
        # numeric value or a string that represents the string value of an
        # EnhancementDuration
        if not duration and duration != 0 and duration != 0.0:
            raise Exception('No "duration" provided.')
        
        if not isinstance(duration, EnhancementDuration):
            if isinstance(str, duration):
                if not EnhancementDuration.is_valid(duration):
                    raise Exception(f'The "duration" parameter provided {str(duration)} is not a valid EnhancementDuration value.')
            elif not variable_is_positive_number(duration):
                raise Exception(f'The "duration" parameter provided {str(duration)} is not a positive number.')
            
    @classmethod
    def validate_start(cls, start: Union[EnhancementStart, int, float, str]):
        """
        This method validates if the provided 'start' parameter is a valid
        and positive numeric value, if it is a EnhancementStart enum
        or if it is a valid string value of a EnhancementStart enum.

        This method will raise an Exception if any of the rules are not fit.
        """
        # 'start' can be a EnhancementStart enum, a positive
        # numeric value or a string that represents the string value
        # of an EnhancementStart
        if not start and start != 0 and start != 0.0:
            raise Exception('No "start" provided.')
        
        if not isinstance(start, EnhancementStart):
            if isinstance(start, str):
                if not EnhancementStart.is_valid(start):
                    raise Exception(f'The "start" parameter provided {str(start)} is not a valid EnhancementStart value.')
                elif not variable_is_positive_number(start):
                    raise Exception(f'The "start" parameter provided {str(start)} is not a positive number.')
                
                start = EnhancementStart(start)

        return start
                
    @classmethod
    def validate_mode(cls, mode: Union[EnhancementMode, str], valid_modes: Union[EnhancementMode, str] = []):
        """
        This method will check if the provided 'mode' is an
        EnhancementMode enum or if it is a valid string 
        value of a EnhancementMode enum. It will also
        check, if the 'valid_modes' parameter is provided, if
        the provided 'mode' is one of the provided 'valid_modes'.
        If you don't provide the 'valid_modes' this condition 
        will not be checked.

        This method will raise an Exception if any of the rules 
        are not fit.
        """
        if not mode:
            raise Exception('No "mode" provided.')
        
        if not isinstance(mode, (EnhancementMode, str)):
            raise Exception(f'The "mode" parameter provided {mode} is not a EnhancementMode nor a string.')
        
        if isinstance(mode, str):
            if not EnhancementMode.is_valid(mode):
                raise Exception(f'The "mode" provided string {mode} is not a valid EnhancementMode enum value.')
            
            mode = EnhancementMode(mode)

        if valid_modes and len(valid_modes) > 0:
            if isinstance(valid_modes[0], EnhancementMode):
                if not mode in valid_modes:
                    raise Exception(f'The "mode" parameter provided {str(mode)} is not a valid EnhancementMode enum.')
            elif isinstance(valid_modes[0], str):
                if not mode.value in valid_modes:
                    raise Exception(f'The "mode" parameter provided {str(mode)} is not a valid value of an EnhancementElement enum.')
            else:
                raise Exception('The provided "valid_modes" are not EnhancementMode nor string items.')