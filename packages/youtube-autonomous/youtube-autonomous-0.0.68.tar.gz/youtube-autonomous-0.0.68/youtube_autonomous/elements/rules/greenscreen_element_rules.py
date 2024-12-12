from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementMode


class GreenscreenElementRules(ElementRules):
    def __init__(self):
        self.can_have_narration = False
        self.need_narration = False
        self.can_have_specific_duration = True
        self.need_specific_duration = False
        self.can_have_text = False
        self.need_text = False
        self.can_have_filename = True
        self.can_have_url = True
        self.need_filename_or_url = True
        self.can_have_keywords = False
        self.need_keywords = False
        self.can_have_more_parameters = False

        self.can_be_segment = False
        self.can_be_enhancement_element = True
        self.valid_enhancement_modes = [EnhancementMode.REPLACE]
        self.default_enhancement_mode = EnhancementMode.REPLACE