from youtube_autonomous.segments.enums import Type, SegmentType, EnhancementType, ShortcodeType, SegmentMode, EnhancementMode, ShortcodeMode, SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration
from youtube_autonomous.elements.validator.element_parameter_validator import ParameterValidator
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.decorators import classproperty
from abc import ABCMeta
from typing import Union


def get_configuration(type: Union[str, Type]):
    type = Type.to_enum(type)

    if type == Type.STOCK:
        return StockConfiguration
    
class SegmentConfiguration:
    """
    The configuration of an element as a Segment.
    """
    type: SegmentType
    modes: list[SegmentMode]
    default_mode: SegmentMode
    string_durations: list[SegmentStringDuration]
    """
    A list containing the StringDuration values that we accept
    in this segment configuration.
    """

    def __init__(self, type: SegmentType, string_durations = None):
        self.type = type,
        self.modes = None, # By now we don't accept modes
        self.default_mode = None # By now we don't accept modes
        self.string_durations = None 

        if string_durations is not None:
            self.string_durations = string_durations

    # TODO: Should we keep this below (?)
    @staticmethod
    def is_valid_type(segment_type: Union[str, SegmentType]):
        """
        Validates if the provided 'segment_type' is a valid name or 
        value of the registered and valid SegmentType enums. This
        method will return the Enum item if valid, or False if not.
        """
        return SegmentType.is_valid(segment_type)

    @staticmethod
    def is_valid_duration(duration: Union[float, int, str, SegmentStringDuration]):
        if PythonValidator.is_string(duration):
            return SegmentStringDuration.is_valid(duration)
        
        ParameterValidator.validate_positive_number_mandatory_parameter('duration', duration)
    # TODO: Should we keep this above (?)

class EnhancementConfiguration:
    """
    The configuration of an element as an Enhancement.
    """
    type: EnhancementType
    modes: list[EnhancementMode]
    default_mode: EnhancementMode
    string_durations: list[EnhancementStringDuration]

    def __init__(self, type: EnhancementType, modes: list[EnhancementMode], default_mode: EnhancementMode, string_durations: list[EnhancementStringDuration]):
        self.type = type
        self.modes = modes
        self.default_mode = default_mode
        self.string_durations = string_durations

class ShortcodeConfiguration:
    """
    The configuration of an element as a Shortcode.
    """
    type: ShortcodeType
    modes: list[ShortcodeMode]
    default_mode: ShortcodeMode
    string_durations: list[ShortcodeStringDuration]

    def __init__(self, type: EnhancementType, modes: list[ShortcodeMode], default_mode: ShortcodeMode, string_durations: list[ShortcodeStringDuration]):
        self.type = type
        self.modes = modes
        self.default_mode = default_mode
        self.string_durations = string_durations

class Configuration(metaclass = ABCMeta):
    _type: Type

    _can_have_narration: bool
    _need_narration: bool
    _can_have_specific_duration: bool
    _need_specific_duration: bool
    _can_have_text: bool
    _need_text: bool
    _can_have_filename: bool
    _can_have_url: bool
    _need_filename_or_url: bool
    _can_have_keywords: bool
    _need_keywords: bool
    _can_have_more_parameters: bool

    _config_as_segment: SegmentConfiguration
    _config_as_enhancement: EnhancementConfiguration
    _config_as_shortcode: ShortcodeConfiguration

    @classproperty
    def type(cls):
        return cls._type

    @classproperty
    def can_have_narration(cls):
        return cls._can_have_narration
    
    @classproperty
    def need_narration(cls):
        return cls._need_narration
    
    @classproperty
    def can_have_specific_duration(cls):
        return cls._can_have_specific_duration
    
    @classproperty
    def need_specific_duration(cls):
        return cls._need_specific_duration
    
    @classproperty
    def can_have_text(cls):
        return cls._can_have_text
    
    @classproperty
    def need_text(cls):
        return cls._need_text
    
    @classproperty
    def can_have_filename(cls):
        return cls._can_have_filename
    
    @classproperty
    def can_have_url(cls):
        return cls._can_have_url
    
    @classproperty
    def need_filename_or_url(cls):
        return cls._need_filename_or_url

    @classproperty
    def can_have_keywords(cls):
        return cls._can_have_keywords
    
    @classproperty
    def need_keywords(cls):
        return cls._need_keywords
    
    @classproperty
    def can_have_more_parameters(cls):
        return cls._can_have_more_parameters
    
    @classproperty
    def config_as_segment(cls):
        return cls._config_as_segment
    
    @classproperty
    def config_as_enhancement(cls):
        return cls._config_as_enhancement
    
    @classproperty
    def config_as_shortcode(cls):
        return cls._config_as_shortcode
    
    @staticmethod
    def get_configuration_by_type(type: Union[str, Type]):
        """
        Returns the configuration object that corresponds to
        the provided 'type' that need to be a valid type string
        or object.
        """
        if isinstance(type, (SegmentType, EnhancementType, ShortcodeType)):
            type = Type.to_enum(type.value)
        else:
            type = Type.to_enum(type)

        if type == Type.STOCK:
            return StockConfiguration
        elif type == Type.CUSTOM_STOCK:
            return CustomStockConfiguration
        elif type == Type.AI_IMAGE:
            return AIImageConfiguration
        elif type == Type.IMAGE:
            return ImageConfiguration
        elif type == Type.AI_VIDEO:
            return AIVideoConfiguration
        elif type == Type.VIDEO:
            return VideoConfiguration
        elif type == Type.SOUND:
            return SoundConfiguration
        elif type == Type.YOUTUBE_VIDEO:
            return YoutubeVideoConfiguration
        elif type == Type.TEXT:
            return TextConfiguration
        elif type == Type.MEME:
            return MemeConfiguration
        elif type == Type.EFFECT:
            return EffectConfiguration
        elif type == Type.PREMADE:
            return PremadeConfiguration
        elif type == Type.GREENSCREEN:
            return GreenscreenConfiguration

class StockConfiguration(Configuration):
    """
    The 'Stock' element configuration, that defines if it can be used
    as a segment or as a enhancement (or both) and all the things it
    needs to work as expected.
    """
    _type = Type.STOCK
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = False
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.STOCK,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.STOCK,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.STOCK,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class CustomStockConfiguration(Configuration):
    """
    The 'CustomStock' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.CUSTOM_STOCK
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = False
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.CUSTOM_STOCK,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.CUSTOM_STOCK,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.CUSTOM_STOCK,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class AIImageConfiguration(Configuration):
    """
    The 'AIImage' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.AI_IMAGE
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.AI_IMAGE,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.AI_IMAGE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.AI_IMAGE,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class ImageConfiguration(Configuration):
    """
    The 'Image' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.IMAGE
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _need_keywords: bool = False
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.IMAGE,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.IMAGE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.IMAGE,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')

class AIVideoConfiguration(Configuration):
    """
    The 'AIVideo' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.AI_VIDEO
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.AI_VIDEO,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.AI_VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.AI_VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class VideoConfiguration(Configuration):
    """
    The 'Video' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.VIDEO
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _need_keywords: bool = False
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.VIDEO,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class SoundConfiguration(Configuration):
    """
    The 'Sound' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.SOUND
    
    _can_have_narration = False
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = False
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _need_filename_or_url: bool = True
    _can_have_keywords: bool = True
    _need_keywords: bool = False
    _can_have_more_parameters: bool = False

    _config_as_segment: None
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.SOUND,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION, EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.SOUND,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT, ShortcodeStringDuration.FILE_DURATION]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')

class YoutubeVideoConfiguration(Configuration):
    """
    The 'YoutubeVideo' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.YOUTUBE_VIDEO
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = True
    _need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _need_keywords: bool = False
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.YOUTUBE_VIDEO,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.YOUTUBE_VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.YOUTUBE_VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')

class TextConfiguration(Configuration):
    """
    The 'Text' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.TEXT
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = True
    _need_text: bool = True
    _can_have_filename: bool = False
    _can_have_url: bool = True
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = True

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.TEXT,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.TEXT,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.TEXT,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class MemeConfiguration(Configuration):
    """
    The 'Meme' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.MEME
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = False
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = False

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.MEME,
        string_durations = [EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.MEME,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION, EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.MEME,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.INLINE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT, ShortcodeStringDuration.FILE_DURATION]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class EffectConfiguration(Configuration):
    """
    The 'Effect' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.EFFECT
    
    _can_have_narration = False
    _need_narration: bool = False
    _can_have_specific_duration: bool = False
    _need_specific_duration: bool = False
    _can_have_text: bool = False
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = True

    _config_as_segment: None
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.EFFECT,
        modes = [EnhancementMode.REPLACE, EnhancementMode.INLINE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.EFFECT,
        modes = [ShortcodeMode.REPLACE, ShortcodeMode.INLINE],
        default_mode = ShortcodeMode.REPLACE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class PremadeConfiguration(Configuration):
    """
    The 'Premade' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.PREMADE
    
    _can_have_narration = True
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = True
    _can_have_text: bool = False  # dynamic parameters will be applied
    _need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _need_keywords: bool = True
    _can_have_more_parameters: bool = True

    _config_as_segment: SegmentConfiguration = SegmentConfiguration(
        type = SegmentType.PREMADE,
    )
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.PREMADE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.PREMADE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
    
class GreenscreenConfiguration(Configuration):
    """
    The 'Greenscreen' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = Type.GREENSCREEN
    
    _can_have_narration = False
    _need_narration: bool = False
    _can_have_specific_duration: bool = True
    _need_specific_duration: bool = False
    _can_have_text: bool = False  # dynamic parameters will be applied
    _need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _need_keywords: bool = False
    _can_have_more_parameters: bool = False

    _config_as_segment: None
    _config_as_enhancement: EnhancementConfiguration = EnhancementConfiguration(
        type = EnhancementType.GREENSCREEN,
        modes = [EnhancementMode.REPLACE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ShortcodeConfiguration = ShortcodeConfiguration(
        type = ShortcodeType.GREENSCREEN,
        modes = [EnhancementMode.REPLACE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(self):
        raise Exception('Sorry, this class is not instantiable.')
