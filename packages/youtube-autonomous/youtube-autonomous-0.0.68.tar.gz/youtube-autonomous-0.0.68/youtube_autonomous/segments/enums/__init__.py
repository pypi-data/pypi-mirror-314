# TODO: Refactor this, too many unneeded Enums
from yta_general_utils.programming.enum import YTAEnum as Enum, get_values


# TODO: Make 'EnhancementType' and 'SegmentType' dynamic
# because that is actually set in each Rule so if I 
# manually change one rule I have to change it also here.


class Type(Enum):
    """
    A Type that represents any kind of type that can be used in the
    app, that includes the Segment, the Enhancement and the 
    Shortcode types.
    """
    CUSTOM_STOCK = 'custom_stock'
    STOCK = 'stock'
    AI_IMAGE = 'ai_image'
    IMAGE = 'image'
    AI_VIDEO = 'ai_video'
    STICKER = 'sticker'
    VIDEO = 'video'
    SOUND = 'sound'
    YOUTUBE_VIDEO = 'youtube_video'
    TEXT = 'text'
    MEME = 'meme'
    EFFECT = 'effect'
    PREMADE = 'premade'
    GREENSCREEN = 'greenscreen'

class SegmentType(Enum):
    """
    These Enums represent the types that a Segment could
    be, allowing us to check and detect if it is valid.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    CUSTOM_STOCK = Type.CUSTOM_STOCK.value
    """
    Stock videos but extracted from our own custom sources.
    """
    STOCK = Type.STOCK.value
    """
    Stock videos extracted from external stock platforms.
    """
    AI_IMAGE = Type.AI_IMAGE.value
    IMAGE = Type.IMAGE.value
    STICKER = Type.STICKER.value
    AI_VIDEO = Type.AI_VIDEO.value
    VIDEO = Type.VIDEO.value
    SOUND = Type.SOUND.value
    YOUTUBE_VIDEO = Type.YOUTUBE_VIDEO.value
    TEXT = Type.TEXT.value
    MEME = Type.MEME.value
    PREMADE = Type.PREMADE.value

    # TODO: This below is now available through the rules...
    # This should be removed in a near future
    @classmethod
    def get_premade_types(cls):
        """
        Returns a list containing all the Segment Types that are 
        premades.
        """
        return [
            # SegmentType.YOUTUBE_SEARCH,
            # SegmentType.GOOGLE_SEARCH
        ]

    @classmethod
    def get_narration_types(cls):
        """
        Returns the SegmentType enums that are compatible with 
        audio narration.
        """
        return cls.get_all()
    
    @classmethod
    def get_narration_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with audio narration.
        """
        return get_values(cls.get_narration_types())
    
    @classmethod
    def get_url_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'url' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.YOUTUBE_VIDEO,
            SegmentType.VIDEO,
            SegmentType.SOUND
        ]
    
    @classmethod
    def get_url_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with the 'url' parameter.
        """
        return get_values(cls.get_url_types())
    
    @classmethod
    def get_keywords_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'keywords' parameter.
        """
        return [
            SegmentType.MEME,
            SegmentType.AI_IMAGE,
            SegmentType.CUSTOM_STOCK,
            SegmentType.STOCK,
            # TODO: Add IMAGE in the future with Bing or Google Search
            # TODO: Add YOUTUBE_VIDEO in the future for Youtube Search
        ]
    
    @classmethod
    def get_keywords_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'keywords' parameter.
        """
        return get_values(cls.get_keywords_types())
    
    @classmethod
    def get_filename_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'filename' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.SOUND,
            SegmentType.VIDEO
        ]
    
    @classmethod
    def get_filename_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'filename' parameter.
        """
        return get_values(cls.get_filename_types())
    
    @classmethod
    def get_text_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'text' parameter.
        """
        # TODO: This is defined in element rules
        return [
            SegmentType.TEXT,
        ]
    
    @classmethod
    def get_text_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'text' parameter.
        """
        return get_values(cls.get_text_types())

class ShortcodeType(Enum):
    """
    These Enums represent the types that a Shortcode could 
    be, allowing us to check and detect if it is valid.
    """
    CUSTOM_STOCK = Type.CUSTOM_STOCK.value
    STOCK = Type.STOCK.value
    AI_IMAGE = Type.AI_IMAGE.value
    IMAGE = Type.IMAGE.value
    STICKER = Type.STICKER.value
    AI_VIDEO = Type.AI_VIDEO.value
    VIDEO = Type.VIDEO.value
    SOUND = Type.SOUND.value
    YOUTUBE_VIDEO = Type.YOUTUBE_VIDEO.value
    TEXT = Type.TEXT.value
    MEME = Type.MEME.value
    PREMADE = Type.PREMADE.value
    EFFECT = Type.EFFECT.value
    GREENSCREEN = Type.GREENSCREEN.value

class EnhancementType(Enum):
    """
    These Enums represent the types that a Enhancement could 
    be, allowing us to check and detect if it is valid.
    """
    CUSTOM_STOCK = Type.CUSTOM_STOCK.value
    STOCK = Type.STOCK.value
    AI_IMAGE = Type.AI_IMAGE.value
    IMAGE = Type.IMAGE.value
    STICKER = Type.STICKER.value
    AI_VIDEO = Type.AI_VIDEO.value
    VIDEO = Type.VIDEO.value
    SOUND = Type.SOUND.value
    YOUTUBE_VIDEO = Type.YOUTUBE_VIDEO.value
    TEXT = Type.TEXT.value
    MEME = Type.MEME.value
    PREMADE = Type.PREMADE.value
    EFFECT = Type.EFFECT.value
    GREENSCREEN = Type.GREENSCREEN.value

class Field(Enum):
    """
    The representation of a common Field element, which
    will be used when creating each specific field type.
    """
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    FILENAME = 'filename'
    NARRATION_TEXT = 'narration_text'
    VOICE = 'voice'
    TEXT = 'text'
    DURATION = 'duration'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    MUSIC = 'music'
    SEGMENTS = 'segments'
    ENHANCEMENTS = 'enhancements'
    START = 'start'
    MODE = 'mode'
    EXTRA_PARAMS = 'extra_params'

class ProjectField(Enum):
    SEGMENTS = Field.SEGMENTS.value
    
class SegmentField(Enum):
    """
    These Enums represent the fields that a Segment has, allowing us
    to check that any required field is provided and/or to detect 
    which one is missing.

    Examples: TYPE, KEYWORDS, URL, etc.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    TYPE = Field.TYPE.value
    KEYWORDS = Field.KEYWORDS.value
    URL = Field.URL.value
    FILENAME = Field.FILENAME.value
    NARRATION_TEXT = Field.NARRATION_TEXT.value
    VOICE = Field.VOICE.value
    TEXT = Field.TEXT.value
    DURATION = Field.DURATION.value
    AUDIO_NARRATION_FILENAME = Field.AUDIO_NARRATION_FILENAME.value
    MUSIC = Field.MUSIC.value
    ENHANCEMENTS = Field.ENHANCEMENTS.value
    EXTRA_PARAMS = Field.EXTRA_PARAMS.value

class EnhancementField(Enum):
    """
    Fields accepted for enhancement elements.
    """
    TYPE = Field.TYPE.value
    KEYWORDS = Field.KEYWORDS.value
    URL = Field.URL.value
    FILENAME = Field.FILENAME.value
    NARRATION_TEXT = Field.NARRATION_TEXT.value
    VOICE = Field.VOICE.value
    TEXT = Field.TEXT.value
    DURATION = Field.DURATION.value
    AUDIO_NARRATION_FILENAME = Field.AUDIO_NARRATION_FILENAME.value
    MUSIC = Field.MUSIC.value
    ENHANCEMENTS = Field.ENHANCEMENTS.value
    START = Field.START.value
    MODE = Field.MODE.value
    EXTRA_PARAMS = Field.EXTRA_PARAMS.value

class ShortcodeField(Enum):
    """
    Fields accepted for shortcodes.
    """
    TYPE = Field.TYPE.value
    KEYWORDS = Field.KEYWORDS.value
    URL = Field.URL.value
    FILENAME = Field.FILENAME.value
    NARRATION_TEXT = Field.NARRATION_TEXT.value
    VOICE = Field.VOICE.value
    TEXT = Field.TEXT.value
    DURATION = Field.DURATION.value
    AUDIO_NARRATION_FILENAME = Field.AUDIO_NARRATION_FILENAME.value
    MUSIC = Field.MUSIC.value
    ENHANCEMENTS = Field.ENHANCEMENTS.value
    START = Field.START.value
    MODE = Field.MODE.value
    EXTRA_PARAMS = Field.EXTRA_PARAMS.value

class BuildingField(Enum):
    STATUS = 'status'
    TRANSCRIPTION = 'transcription'
    AUDIO_FILENAME = 'audio_filename'
    AUDIO_CLIP = 'audio_clip'
    VIDEO_FILENAME = 'video_filename'
    VIDEO_CLIP = 'video_clip'
    FULL_FILENAME = 'full_filename'
    FULL_CLIP = 'full_clip'

class ProjectBuildingField(Enum):
    STATUS = BuildingField.STATUS.value

class SegmentBuildingField(Enum):
    """
    The fields that are used when building the segment and are
    not provided by the user in the initial segment json data.
    """
    STATUS = BuildingField.STATUS.value
    TRANSCRIPTION = BuildingField.TRANSCRIPTION.value
    AUDIO_FILENAME = BuildingField.AUDIO_FILENAME.value
    AUDIO_CLIP = BuildingField.AUDIO_CLIP.value
    VIDEO_FILENAME = BuildingField.VIDEO_FILENAME.value
    VIDEO_CLIP = BuildingField.VIDEO_CLIP.value
    FULL_FILENAME = BuildingField.FULL_FILENAME.value
    FULL_CLIP = BuildingField.FULL_CLIP.value

class EnhancementBuildingField(Enum):
    STATUS = BuildingField.STATUS.value
    TRANSCRIPTION = BuildingField.TRANSCRIPTION.value
    AUDIO_FILENAME = BuildingField.AUDIO_FILENAME.value
    AUDIO_CLIP = BuildingField.AUDIO_CLIP.value
    VIDEO_FILENAME = BuildingField.VIDEO_FILENAME.value
    VIDEO_CLIP = BuildingField.VIDEO_CLIP.value
    FULL_FILENAME = BuildingField.FULL_FILENAME.value
    FULL_CLIP = BuildingField.FULL_CLIP.value

class Origin(Enum):
    USER = 'user'
    """
    Manually written or entered by the user when creating
    the project.
    """
    NARRATION_TEXT_SHORTCODE = 'narration_text_shortcode'
    """
    Automatically extracted from the narration text that
    included some manually written shortcodes.
    """
    EDITION_MANUAL = 'edition_manual'
    """
    Automatically extracted from the narration transcription
    by applying the edition manual.
    """
    AI_GENERATED = 'ai_generated'
    """
    Automatically generated by the AI that has interpreted 
    the intention of the text, the topic being talked about
    or other things and has deemed it appropriate to apply
    the element.
    """
    
class SegmentOrigin(Enum):
    USER = Origin.USER.value
    AI_GENERATED = Origin.AI_GENERATED.value

class EnhancementOrigin(Enum):
    USER = Origin.USER.value
    NARRATION_TEXT_SHORTCODE = Origin.NARRATION_TEXT_SHORTCODE.value
    EDITION_MANUAL = Origin.EDITION_MANUAL.value
    AI_GENERATED = Origin.AI_GENERATED.value

class Start(Enum):
    BETWEEN_WORDS = 'between_words'
    """
    This will make the enhancement element start just in the middle of 
    two words that are dictated in narration. This means, after the end
    of the first and and before the start of the next one (that should
    fit a silence part).
    """
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = 'start_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content starts being dictated.
    """
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = 'middle_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content is in the middle of the dictation.
    """
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = 'end_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content ends being dictated.
    """

class SegmentStart(Enum):
    pass

# TODO: Review this (maybe rename as it is for shortcodes, 
# not enhancement elements yet).
class EnhancementStart(Enum):
    pass
    
class ShortcodeStart(Enum):
    BETWEEN_WORDS = Start.BETWEEN_WORDS.value
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = Start.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = Start.MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD.value
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = Start.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value

    @classmethod
    def get_default(cls):
        return cls.START_OF_FIRST_SHORTCODE_CONTENT_WORD
    
class Duration(Enum):
    SEGMENT_DURATION = 'segment_duration'
    SHORTCODE_CONTENT = 'shortcode_content'
    """
    This will make the enhancement element last until the shortcode
    block-scoped content is narrated.
    """
    FILE_DURATION = 'file_duration'
    """
    This will make the segment last the clip duration. It will be
    considered when the file is downloaded, and that duration will
    be flagged as 9999. This is for videos or audios that have a
    duration based on file.
    """

class SegmentDuration(Enum):
    pass

class EnhancementDuration(Enum):
    SEGMENT_DURATION = Duration.SEGMENT_DURATION.value
    FILE_DURATION = Duration.FILE_DURATION.value

class ShortcodeDuration(Enum):
    SEGMENT_DURATION = Duration.SEGMENT_DURATION.value
    FILE_DURATION = Duration.FILE_DURATION.value
    SHORTCODE_CONTENT = Duration.SHORTCODE_CONTENT.value
    
    @classmethod
    def get_default(cls):
        return cls.SHORTCODE_CONTENT
    
class Mode(Enum):
    INLINE = 'inline'
    """
    Those segment elements that will be displayed in 'inline' mode, that
    means they will interrupt the main video, be played, and then go back
    to the main video. This will modify the clip length, so we need to 
    refresh the other objects start times.
    """
    OVERLAY = 'overlay'
    """
    Those segment elements that will be displayed in 'overlay' mode, that
    means they will be shown in the foreground of the main clip, changing
    not the main video duration, so they don't force to do any refresh.
    """
    REPLACE = 'replace'
    """
    Those enhancement elements that will replace the video in this mode.
    This means that the original video is modified by this enhancement
    element and that modified part will be placed instead of the original
    video. This modified part could be the whole video or only a part of
    it. This is how most of the greenscreens or effects are applied.
    """

class SegmentMode(Enum):
    pass

class EnhancementMode(Enum):
    """
    These Enums represent the different ways in which the project
    segment elements can be built according to the way they are
    included in the segment.
    """
    INLINE = Mode.INLINE.value
    OVERLAY = Mode.OVERLAY.value
    REPLACE = Mode.REPLACE.value

    @classmethod
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE
    
class ShortcodeMode(Enum):
    INLINE = Mode.INLINE.value
    OVERLAY = Mode.OVERLAY.value
    REPLACE = Mode.REPLACE.value

    @classmethod
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE
    
class Status(Enum):
    TO_START = 'to_start'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'

class SegmentStatus(Enum):
    """
    The current segment status defined by this string.
    """
    TO_START = Status.TO_START.value
    IN_PROGRESS = Status.IN_PROGRESS.value
    FINISHED = Status.FINISHED.value

class EnhancementStatus(Enum):
    """
    The current enhancement status defined by this string.
    """
    TO_START = Status.TO_START.value
    IN_PROGRESS = Status.IN_PROGRESS.value
    FINISHED = Status.FINISHED.valueTO_START = Status.TO_START.value

class ProjectStatus(Enum):
    """
    The current project status defined by this string.
    """
    TO_START = Status.TO_START.value
    IN_PROGRESS = Status.IN_PROGRESS.value
    FINISHED = Status.FINISHED.value

class StringDuration(Enum):
    """
    This string value is only accepted in the segment dict that
    the user provides to the system. The key will be accepted
    and transformed into the value to be processed dynamically
    when building the content.
    """
    SHORTCODE_CONTENT = 99997
    """
    This string value determines that the duration is expected
    to be from the begining of the shortcode content (first 
    word) to the end of it (last word).

    This duration is accepted only in shortcodes.
    """
    FILE_DURATION = 99998
    """
    This string value determines that the duration is expected
    to be the source file (downloaded or obtained from the 
    local system) duration.

    This duration is accepted in shortcodes, in segments and in
    enhancements.
    """
    SEGMENT_DURATION = 99999
    """
    This string value determines that the duration is expected
    to be the whole segment duration (known when built).

    This duration is accepted only in segments and shortcodes.
    """
    
    @staticmethod
    def convert_duration(duration: str):
        """
        Converts the provided 'duration' string to its actual value
        according to the existing StringDuration enums or raises an
        Exception if not valid.

        This method returns the int value of the given 'duration'.
        """
        if duration == StringDuration.SHORTCODE_CONTENT.name:
            duration = StringDuration.SHORTCODE_CONTENT.value
        elif duration == StringDuration.FILE_DURATION.name:
            duration = StringDuration.FILE_DURATION.value
        elif duration == StringDuration.SEGMENT_DURATION.name:
            duration = StringDuration.SEGMENT_DURATION.value
        else:
            raise Exception(f'The provided "duration" parameter {duration} is not a valid StringDuration name.')

        return duration
    
class SegmentStringDuration(Enum):
    FILE_DURATION = StringDuration.FILE_DURATION.value

    @staticmethod
    def convert_duration(duration: str):
        StringDuration.convert_duration(duration)

class EnhancementStringDuration(Enum):
    FILE_DURATION = StringDuration.FILE_DURATION.value
    SEGMENT_DURATION = StringDuration.SEGMENT_DURATION.value

    @staticmethod
    def convert_duration(duration: str):
        StringDuration.convert_duration(duration)

class ShortcodeStringDuration(Enum):
    FILE_DURATION = StringDuration.FILE_DURATION.value
    SEGMENT_DURATION = StringDuration.SEGMENT_DURATION.value
    SHORTCODE_CONTENT = StringDuration.SHORTCODE_CONTENT.value

    @staticmethod
    def convert_duration(duration: str):
        StringDuration.convert_duration(duration)