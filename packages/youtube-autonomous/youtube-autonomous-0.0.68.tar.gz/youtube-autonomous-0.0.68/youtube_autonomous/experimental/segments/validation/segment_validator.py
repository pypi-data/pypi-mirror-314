from youtube_autonomous.exceptions.invalid_segment_exception import InvalidSegmentException
from youtube_autonomous.segments.enums import SegmentType, SegmentField
from youtube_autonomous.experimental.segments.validation.consts import VALID_SEGMENT_TYPES, NEED_KEYWORDS_SEGMENT_TYPES, URL_SEGMENT_TYPES, NARRATION_SEGMENT_TYPES, NEED_TEXT_SEGMENT_TYPES
from yta_general_utils.file.checker import file_exists, file_is_audio_file
from yta_general_utils.checker.url import url_is_ok, verify_image_url


class SegmentValidator:
    """
    Class that validates the segment structure and parameters to
    ensure that it is possible to build the content we expect from
    that segment.
    """
    def __init__(self):
        pass

    # TODO: We need to build a 'validate_pre' and a 'validate_post'
    # because we first need to know if we have the basic structure
    # to build a Segment, but then we need to validate that the
    # provided data is also valid (images are downloadable, etc.)

    # TODO: Apply 'segment' type
    def validate(self, segment):
        """
        Validates the provided 'segment' to check if it is a processable one
        so we can store it to be processed later when requested. Checks if 
        the provided 'segment' is valid or not. It returns True if yes or 
        raises a detailed InvalidSegmentException if not.

        The 'segment' parameter must be a dict representing the json that is
        used to define the segment structure and expected content.
        """
        # No type provided
        if not SegmentField.TYPE.value in segment:
            raise InvalidSegmentException(f'Field "{SegmentField.TYPE.value}" not provided.')
        
        # Is a non-accepted type
        if self.__is_invalid_type(segment):
            raise InvalidSegmentException(f'Type "{segment[SegmentField.TYPE.value]}" is not valid. Valid values are: {SegmentType.get_all_values_as_str()}.')
        
        # Need keywords but doesn't have
        if self.__has_no_keywords(segment):
            raise InvalidSegmentException(f'No "{SegmentField.KEYWORDS.value}" field provided and it is mandatory for the "{segment[SegmentField.TYPE.value]}" segment type.')

        # Need url but doesn't have
        if self.__has_no_url(segment):
            raise InvalidSegmentException(f'No "{SegmentField.URL.value}" field provided and it is mandatory for the "{segment[SegmentField.TYPE.value]}" segment type.')
        
        # Need text but doesn't have
        if self.__has_no_text(segment):
            raise InvalidSegmentException(f'No "{SegmentField.TEXT.value}" field provided and it is mandatory for the "{segment[SegmentField.TYPE.value]}" segment type.')
        
        # Need voice and text at the same time, but only one
        if self.__has_no_voice_and_text(segment):
            raise InvalidSegmentException('Fields "' + SegmentField.VOICE.value + '" and "' + SegmentField.TEXT.value + '" must exist at the same time to be able to narrate.')
        
        # Need to calculate duration but cannot
        if self.__has_no_duration(segment):
            raise InvalidSegmentException('We need "' + SegmentField.TEXT.value + '", "' + SegmentField.DURATION.value + '" or "' + SegmentField.AUDIO_NARRATION_FILENAME.value + '". We need something to know how much time in some way.')
        
        # Need url but is not available
        if self.__has_invalid_url(segment):
            raise InvalidSegmentException('Provided "' + SegmentField.URL.value + '" is not available.')
        
        # Need image url but is not valid
        if self.__has_no_image_url(segment):
            raise InvalidSegmentException('Provided "' + SegmentField.URL.value + '" is not a valid image.')
        
        # Has narration file but is not valid
        if self.__has_no_valid_audio_narration_file(segment):
            raise InvalidSegmentException('Provided ' + SegmentField.AUDIO_NARRATION_FILENAME.value + ' "' + segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) + '" is not a valid file.')
        
        # Has narration file but is not audio file
        if self.__has_no_audio_file(segment):
            raise InvalidSegmentException('Provided ' + SegmentField.AUDIO_NARRATION_FILENAME.value + ' "' + segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) + '" is not an audio file.')
        
        # TODO: Implement content available validation. Check that 'url' 
        # parameter is available and we can obtain the yt video, check
        # that there is a result (a meme, for example) with the given
        # keywords. Check that the youtube video duration is longer than
        # the expected as 'duration' parameter... All those things that
        # are not included above yet

        return True
        
    def __is_invalid_type(self, segment):
        """
        Returns True if the provided 'segment' has an invalid type.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')

        return not SegmentType.is_valid(type)

    def __has_no_keywords(self, segment):
        """
        Returns True if the provided 'segment' needs the keywords field but
        doesn't have it.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            keywords = segment[SegmentField.KEYWORDS.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            keywords = segment.get(SegmentField.KEYWORDS.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')

        return type in SegmentType.get_keywords_type_values() and not keywords

    def __has_no_url(self, segment):
        """
        Returns True if the provided 'segment' needs the url field but doesn't
        have it.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            url = segment[SegmentField.URL.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            url = segment.get(SegmentField.URL.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')

        return type in SegmentType.get_url_type_values() and not url

    def __has_no_text(self, segment):
        """
        Returns True if the provided 'segment' needs the text field but doesn't
        have it.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            text = segment[SegmentField.TEXT.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            text = segment.get(SegmentField.TEXT.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')

        return type in SegmentType.get_text_type_values() and not text

    def __has_no_voice_and_text(self, segment):
        """
        Returns True if the provided 'segment' is a narration type segment
        but has only one narration field (voice or text) but not both at
        the same time.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            narration_text = segment[SegmentField.NARRATION_TEXT.value]
            voice = segment[SegmentField.VOICE.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            narration_text = segment.get(SegmentField.NARRATION_TEXT.value, None)
            voice = segment.get(SegmentField.VOICE.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')
        
        return type in SegmentType.get_narration_type_values() and ((narration_text and not voice) or (voice and not narration_text))

    def __has_no_duration(self, segment):
        """
        Returns True if the provided 'segment' has no field to calculate
        the duration.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            narration_text = segment[SegmentField.NARRATION_TEXT.value]
            voice = segment[SegmentField.VOICE.value]
            audio_narration_filename = segment[SegmentField.AUDIO_NARRATION_FILENAME.value]
            duration = segment[SegmentField.DURATION.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            narration_text = segment.get(SegmentField.NARRATION_TEXT.value, None)
            voice = segment.get(SegmentField.VOICE.value, None)
            audio_narration_filename = segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value, None)
            duration = segment.get(SegmentField.DURATION.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')

        return not (voice and narration_text) and not audio_narration_filename and type in SegmentType.get_narration_type_values() and not duration

    def __has_invalid_url(self, segment):
        """
        Returns True if the provided 'segment' has an invalid url.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            url = segment[SegmentField.URL.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            url = segment.get(SegmentField.URL.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')
        
        # TODO: I can check, depending on the type, if url is valid for the
        # expected purpose depending on type
        # If YOUTUBE_VIDEO => detect youtube is of a valid and available 
        # youtube video
        # If IMAGE => detect that is available to download

        return type in SegmentType.get_url_type_values() and not url_is_ok(url)
    
    def __has_no_valid_filename(self, segment):
        """
        Returns True if the provided 'segment' has a 'filename' field
        but that filename is not an existing and valid file.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            filename = segment[SegmentField.FILENAME.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            filename = segment.get(SegmentField.FILENAME.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')
        
        # TODO: I should check the type (audio, image, video)
        
        return type in SegmentType.get_filename_type_values() and filename and not file_exists(filename)

    def __has_no_image_url(self, segment):
        """
        Returns True if the provided 'segment' is an image segment but has
        no valid image url.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            url = segment[SegmentField.URL.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            url = segment.get(SegmentField.URL.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')
        
        return type == SegmentType.IMAGE.value and not verify_image_url(url)

    def __has_no_valid_audio_narration_file(self, segment):
        """
        Returns True if the provided 'segment' has a narration file but is 
        not a valid file.
        """
        from youtube_autonomous.experimental.segments.segment import Segment

        if isinstance(segment, Segment):
            type = segment[SegmentField.TYPE.value]
            if isinstance(type, SegmentType):
                type = type.value
            audio_narration_filename = segment[SegmentField.AUDIO_NARRATION_FILENAME.value]
        elif isinstance(segment, dict):
            type = segment.get(SegmentField.TYPE.value, None)
            audio_narration_filename = segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value, None)

        if not type:
            raise Exception('No "type" in the provided segment.')
        
        return type in SegmentType.get_narration_type_values() and audio_narration_filename and not file_is_audio_file(audio_narration_filename)

    def __has_no_audio_file(self, segment):
        """
        Returns True if the provided 'segment' has a narration file but is
        not an audio file.
        """
        return segment.get(SegmentField.TYPE.value) in NARRATION_SEGMENT_TYPES and segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) and not file_is_audio_file(segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value))
    
    # TODO: Keep working with these below:
    # TODO: Check if 'youtube_video' language exist and is valid
    # TODO: Check if 'youtube_video' duration is valid (not str, not negative nor excesive)
    # TODO: Check if effects provided are valid