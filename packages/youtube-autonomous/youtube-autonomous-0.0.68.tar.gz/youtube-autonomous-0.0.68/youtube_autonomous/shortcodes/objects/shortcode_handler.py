from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTagType
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode


class ShortcodeHandler:
    @staticmethod
    def simple_shortcode_base_handler(shortcodes, pargs, kwargs, context, tag: str):
        """
        Handles a simple scoped [tag] shortcode.
        """
        attributes = {}

        for parg in pargs:
            attributes[parg] = None

        if kwargs:
            for kwarg in kwargs:
               attributes[kwarg] = kwargs[kwarg]

        # TODO: We need to handle the position within the text
        shortcodes.append(Shortcode(tag, ShortcodeTagType.SIMPLE, attributes, context, None))
            
        # This will replace the shortcode in the text
        return f'[{tag}]'
    
    @staticmethod
    def block_shortcode_base_handler(shortcodes, pargs, kwargs, context, content, tag: str):
        """
        Handles a block scoped [tag] ... [/tag] shortcode.
        """
        attributes = []

        for parg in pargs:
            attributes[parg] = None

        if kwargs:
            for kwarg in kwargs:
               attributes[kwarg] = kwargs[kwarg]

        # TODO: We need to handle the position within the text
        shortcodes.append(Shortcode(tag, ShortcodeTagType.BLOCK, attributes, context, content))
            
        # This will replace the shortcode and its content in the text
        return f'[{tag}]{content}[/{tag}]'