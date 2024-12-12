from youtube_autonomous.segments.enums import EnhancementMode
from youtube_autonomous.segments.enums import SegmentType, EnhancementType
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator, ParameterValidator
from typing import Union


class ElementRules:
    """
    Class to specify the rules that a Project Element must follow.
    The Project Element is equivalent to a Segment.
    """
    can_have_narration: bool = False
    """
    Can be narrated by setting a 'audio_narration_filename' or
    'narration_text' and 'voice'.
    """
    need_narration: bool = False
    """
    Narration is mandatory so 'audio_narration_filename' or 'voice'
    and 'narration_text' are needed.
    """
    can_have_specific_duration: bool = False
    """
    Duration of this element can be set specifically so the element
    will long as much as 'duration' field says.
    """
    need_specific_duration: bool = False
    """
    Specific 'duration' field is mandatory if it can't have narration
    or if it can but the fields needed for the narration do not exist.
    """
    can_have_text: bool = False
    """
    A 'text' field can be used to build the element in an specific
    way (determined by its type).
    """
    need_text: bool = False
    """
    The 'text' is mandatory for this element type so it must exist.
    """
    can_have_filename: bool = False
    """
    The 'filename' field can be present to load the file from that
    local stored filename.
    """
    can_have_url: bool = False
    """
    The 'url' field can be set to obtain the element from that 
    source.
    """
    need_filename_or_url: bool = False
    """
    The 'url' field or the 'filename' field are needed to be able
    to obtain the object. Priority is first 'url' then 'filename'
    if both are provided.
    """
    can_have_keywords: bool = False
    """
    The field 'keywords' can be set to look for the source in an 
    specific way or to build correctly the element (the way those
    'keywords' are used depends on the element type).
    """
    need_keywords: bool = False
    """
    The field 'keywords' is mandatory and must be set to be able
    to build this element.
    """
    can_have_more_parameters: bool = False
    """
    This field acts as a flag to let us know if the element can
    have more dynamic parameters according to the element 
    requirements. Texts or premades could have more parameters
    to be able to build them properly, and those parameters will
    be added dynamically and obtained also dynamically (they will
    be different of the static ones we have defined as the main
    fields).
    """
    can_be_segment: bool = False
    """
    This field indicates if the element with this rule can be used
    as a segment or not.
    """
    can_be_enhancement_element: bool = False
    """
    This field indicates if the element with this rule can be used
    as an enhancement element (that is added on a segment element).
    """
    valid_enhancement_modes: list[EnhancementMode] = []
    """
    This field indicates the valid modes for this element when
    being used as an enhancement element.
    """
    default_enhancement_mode: EnhancementMode = None
    """
    This field indicates the mode by default for this element when
    used as an enhancement element (if possible).
    """

    def __init__(self, can_have_narration: bool, need_narration: bool, can_have_specific_duration: bool, need_specific_duration: bool, can_have_text: bool, need_text: bool, can_have_filename: bool, can_have_url: bool, need_filename_or_url: bool, can_have_keywords: bool, need_keywords: bool, can_have_more_parameters: bool, can_be_segment: bool, can_be_enhancement_element: bool, valid_enhancement_modes: list[EnhancementMode], default_enhancement_mode: EnhancementMode):
        ParameterValidator.validate_is_bool('can_have_narration', can_have_narration)
        ParameterValidator.validate_is_bool('can_have_narration', can_have_narration)
        ParameterValidator.validate_is_bool('need_narration', need_narration)
        ParameterValidator.validate_is_bool('can_have_specific_duration', can_have_specific_duration)
        ParameterValidator.validate_is_bool('need_specific_duration', need_specific_duration)
        ParameterValidator.validate_is_bool('can_have_text', can_have_text)
        ParameterValidator.validate_is_bool('need_text', need_text)
        ParameterValidator.validate_is_bool('can_have_filename', can_have_filename)
        ParameterValidator.validate_is_bool('can_have_url', can_have_url)
        ParameterValidator.validate_is_bool('need_filename_or_url', need_filename_or_url)
        ParameterValidator.validate_is_bool('can_have_keywords', can_have_keywords)
        ParameterValidator.validate_is_bool('need_keywords', need_keywords)
        ParameterValidator.validate_is_bool('can_have_more_parameters', can_have_more_parameters)
        ParameterValidator.validate_is_bool('can_be_segment', can_be_segment)
        ParameterValidator.validate_is_bool('can_be_enhancement_element', can_be_enhancement_element)
        # TODO: Validate 'valid_enhancement_modes'
        ParameterValidator.validate_is_class('default_enhancement_mode', default_enhancement_mode, ['EnhancementMode'])
        
        self.can_have_narrration = can_have_narration
        self.need_narration = need_narration
        self.can_have_specific_duration = can_have_specific_duration
        self.need_specific_duration = need_specific_duration
        self.can_have_text = can_have_text
        self.need_text = need_text
        self.can_have_filename = can_have_filename
        self.can_have_url = can_have_url
        self.need_filename_or_url = need_filename_or_url
        self.can_have_keywords = can_have_keywords
        self.need_keywords = need_keywords
        self.can_have_more_parameters = can_have_more_parameters

        self.can_be_segment = can_be_segment
        self.can_be_enhancement_element = can_be_enhancement_element
        self.valid_enhancement_modes = valid_enhancement_modes
        self.default_enhancement_mode = default_enhancement_mode

    @staticmethod
    def get_subclasses():
        from youtube_autonomous.elements.rules.ai_image_element_rules import AIImageElementRules
        from youtube_autonomous.elements.rules.ai_video_element_rules import AIVideoElementRules
        from youtube_autonomous.elements.rules.image_element_rules import ImageElementRules
        from youtube_autonomous.elements.rules.video_element_rules import VideoElementRules
        from youtube_autonomous.elements.rules.stock_element_rules import StockElementRules
        from youtube_autonomous.elements.rules.custom_stock_element_rules import CustomStockElementRules
        from youtube_autonomous.elements.rules.meme_element_rules import MemeElementRules
        from youtube_autonomous.elements.rules.sound_element_rules import SoundElementRules
        from youtube_autonomous.elements.rules.youtube_video_element_rules import YoutubeVideoElementRules
        from youtube_autonomous.elements.rules.text_element_rules import TextElementRules
        from youtube_autonomous.elements.rules.premade_element_rules import PremadeElementRules
        from youtube_autonomous.elements.rules.effect_element_rules import EffectElementRules
        from youtube_autonomous.elements.rules.greenscreen_element_rules import GreenscreenElementRules

        return [
            AIVideoElementRules,
            VideoElementRules,
            AIImageElementRules,
            ImageElementRules,
            CustomStockElementRules,
            StockElementRules,
            MemeElementRules,
            SoundElementRules,
            YoutubeVideoElementRules,
            TextElementRules,
            PremadeElementRules,
            EffectElementRules,
            GreenscreenElementRules
        ]

    @staticmethod
    def get_subclasses_as_str():
        return ', '.join(ElementRules.get_subclasses())
    
    @staticmethod
    def get_subclass_by_type(type: Union[SegmentType, EnhancementType, str]):
        type = ElementParameterValidator.validate_segment_or_enhancement_type(type)

        from youtube_autonomous.elements.rules.ai_image_element_rules import AIImageElementRules
        from youtube_autonomous.elements.rules.ai_video_element_rules import AIVideoElementRules
        from youtube_autonomous.elements.rules.image_element_rules import ImageElementRules
        from youtube_autonomous.elements.rules.video_element_rules import VideoElementRules
        from youtube_autonomous.elements.rules.stock_element_rules import StockElementRules
        from youtube_autonomous.elements.rules.custom_stock_element_rules import CustomStockElementRules
        from youtube_autonomous.elements.rules.meme_element_rules import MemeElementRules
        from youtube_autonomous.elements.rules.sound_element_rules import SoundElementRules
        from youtube_autonomous.elements.rules.youtube_video_element_rules import YoutubeVideoElementRules
        from youtube_autonomous.elements.rules.text_element_rules import TextElementRules
        from youtube_autonomous.elements.rules.premade_element_rules import PremadeElementRules
        from youtube_autonomous.elements.rules.effect_element_rules import EffectElementRules
        from youtube_autonomous.elements.rules.greenscreen_element_rules import GreenscreenElementRules

        if type in [SegmentType.MEME, EnhancementType.MEME]:
            return MemeElementRules
        elif type in [SegmentType.AI_IMAGE, EnhancementType]:
            return AIImageElementRules
        elif type in [SegmentType.AI_VIDEO, EnhancementType.AI_VIDEO]:
            return AIVideoElementRules
        elif type in [SegmentType.IMAGE, EnhancementType.IMAGE]:
            return ImageElementRules
        elif type in [SegmentType.VIDEO, EnhancementType.VIDEO]:
            return VideoElementRules
        elif type in [SegmentType.STOCK, EnhancementType.STOCK]:
            return StockElementRules
        elif type in [SegmentType.CUSTOM_STOCK, EnhancementType.CUSTOM_STOCK]:
            return CustomStockElementRules
        elif type in [SegmentType.SOUND, EnhancementType.SOUND]:
            return SoundElementRules
        elif type in [SegmentType.YOUTUBE_VIDEO, EnhancementType.YOUTUBE_VIDEO]:
            return YoutubeVideoElementRules
        elif type in [SegmentType.TEXT, EnhancementType.TEXT]:
            return TextElementRules
        elif type in [SegmentType.PREMADE, EnhancementType.PREMADE]:
            return PremadeElementRules
        elif type in [EnhancementType.EFFECT]:
            return EffectElementRules
        elif type in [EnhancementType.GREENSCREEN]:
            return GreenscreenElementRules