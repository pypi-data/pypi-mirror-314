from yta_general_utils.programming.enum import YTAEnum as Enum


class ShortcodeTagType(Enum):
    """
    This Enum represents the different type of shortcodes that
    we can handle according to their scopes. It could be simple
    [tag] shortcode or a block-scoped one [tag] ... [/tag].
    """
    BLOCK = 'block'
    """
    Shortcode type that is built with a start tag [tag], an
    end tag [/tag] and a content between both of those tags.
    """
    SIMPLE = 'simple'
    """
    Shortcode type that is built with a simple tag [tag].
    """