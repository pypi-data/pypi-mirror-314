from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementMode


class ImageElementRules(ElementRules):
    def __init__(self):
        # super().__init__(True, False, True, True, False, False, True, True, True, False, False, False, True, True, [EnhancementMode.INLINE, EnhancementMode.OVERLAY], EnhancementMode.OVERLAY)
        # super().__init__(
        #     can_have_narration = True,
        #     need_narration = False,
        #     can_have_specific_duration = True,
        #     need_specific_duration = True,
        #     can_have_text = False,
        #     need_text = False,
        #     can_have_filename = True,
        #     can_have_url = True,
        #     need_filename_or_url = True,
        #     can_have_keywords = False,
        #     need_keywords = False,
        #     can_have_more_parameters = False,

        #     can_be_segment = True,
        #     can_be_enhancement_element = True,
        #     valid_enhancement_modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        #     default_enhancement_mode = EnhancementMode.OVERLAY
        # )
        self.can_have_narration = True
        self.need_narration = False
        self.can_have_specific_duration = True
        self.need_specific_duration = True
        self.can_have_text = False
        self.need_text = False
        self.can_have_filename = True
        self.can_have_url = True
        self.need_filename_or_url = True
        self.can_have_keywords = False
        self.need_keywords = False
        self.can_have_more_parameters = False

        self.can_be_segment = True
        self.can_be_enhancement_element = True
        self.valid_enhancement_modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY]
        self.default_enhancement_mode = EnhancementMode.OVERLAY