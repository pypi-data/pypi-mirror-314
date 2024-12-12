from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementMode


class EffectElementRules(ElementRules):
    def __init__(self):
        self.can_have_narration = False
        self.need_narration = False
        self.can_have_specific_duration = False
        self.need_specific_duration = False
        self.can_have_text = False
        self.need_text = False
        self.can_have_filename = False
        self.can_have_url = False
        self.need_filename_or_url = False
        self.can_have_keywords = True
        self.need_keywords = True
        self.can_have_more_parameters = True
        # TODO: The effect should have some way to detect the
        # mandatory parameters so we can dynamically raise an
        # Exception if any of those mandatory parameters are
        # not provided

        self.can_be_segment = False
        self.can_be_enhancement_element = True
        self.valid_enhancement_modes = [EnhancementMode.REPLACE]
        self.default_enhancement_mode = EnhancementMode.REPLACE