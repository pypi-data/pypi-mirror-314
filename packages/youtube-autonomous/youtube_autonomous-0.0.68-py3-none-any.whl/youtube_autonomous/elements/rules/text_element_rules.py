from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementMode


class TextElementRules(ElementRules):
    def __init__(self):
        self.can_have_narration = True
        self.need_narration = False
        self.can_have_specific_duration = True
        self.need_specific_duration = True
        self.can_have_text = True
        self.need_text = True
        self.can_have_filename = False
        self.can_have_url = False
        self.need_filename_or_url = False
        self.can_have_keywords = True
        self.need_keywords = True
        self.can_have_more_parameters = True

        self.can_be_segment = True
        self.can_be_enhancement_element = True
        self.valid_enhancement_modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY]
        self.default_enhancement_mode = EnhancementMode.OVERLAY