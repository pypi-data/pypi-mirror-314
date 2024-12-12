from youtube_autonomous.shortcodes.enums import ShortcodeTagType
from youtube_autonomous.segments.enums import ShortcodeType
from youtube_autonomous.shortcodes.objects.shortcode_handler import ShortcodeHandler
from typing import Union


class ShortcodeTag:
    """
    Class that represent a shortcode tag to implement with
    the ShortcodeParser. This is just to let the parser know
    if it is a block-scoped shortcode tag, a simple shortcode
    tag and some more information needed.
    """
    tag: ShortcodeType
    """
    The ShortcodeType that corresponds to that tag.
    """
    type: ShortcodeTagType
    """
    The ShortcodeTagType that corresponds to that type.
    """

    def __init__(self, tag: str, type: Union[ShortcodeTagType, str]):
        """
        Initializes a shortcode tag object. The 'tag' parameter represents
        the shortcode name [tag], and the 'type' parameter is to point if
        the shortcode includes some text inside it [tag] ... [/tag] or if
        it is a simple one [tag].
        """
        tag = ShortcodeType.to_enum(tag)
        type = ShortcodeTagType.to_enum(type)
        
        self.tag = tag
        self.type = type

    def is_block_scoped(self):
        """
        Returns True if the shortcode is a block scoped one, that
        should look like this: [tag] ... [/tag], or False if not.
        """
        return self.type == ShortcodeTagType.BLOCK
    
    def handler(self, shortcodes, pargs, kwargs, context, content):
        """
        The function that handles the shortcode, fills the provided
        'shortcodes' list with a new shortcode object and all the
        required attributes and values.
        """
        if self.is_block_scoped():
            return ShortcodeHandler.block_shortcode_base_handler(shortcodes, pargs, kwargs, context, content, self.tag)
        
        return ShortcodeHandler.simple_shortcode_base_handler(shortcodes, pargs, kwargs, context, self.tag)

