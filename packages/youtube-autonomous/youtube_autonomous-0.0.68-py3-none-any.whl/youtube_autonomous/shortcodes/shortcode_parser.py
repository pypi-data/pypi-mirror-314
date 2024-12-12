from youtube_autonomous.shortcodes.enums import ShortcodeTagType
from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTag
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode
from yta_general_utils.text.transformer import fix_unseparated_periods, fix_excesive_blank_spaces, fix_separated_parenthesis, add_missing_spaces_before_and_after_parenthesis, fix_separated_square_brackets, add_missing_spaces_before_and_after_square_brackets, fix_ellipsis
from shortcodes import Parser

import re


class ShortcodeParser:
    """
    This class parses the shortcodes from a text, classifies
    them and is capable of handling the information inside.

    We only accept simple shortcodes '[tag]' and block-scoped
    shortcodes '[block_tag] something inside [/block_tag]. 
    The parsing process will detect any invalid shortcode and
    raise an exception.

    _Developer needs to manually register the shortcode parser
    method for each shortcode that this parser will accept._
    """
    __parser: Parser = None
    """
    The shortcodes library parser object.
    """
    text: str = ''
    """
    The last text that this parser object has parsed, as it
    was originally.
    """
    text_sanitized: str = ''
    """
    The last text that this parser object has parsed, but
    sanitized. Any double blank space, any missing blank
    space after a parenthesis, a period or a square bracket
    has been added. Sanitization process is needed to have
    no problems when finding the shortcodes and detecting
    them through the entire text.

    This is the text that is actually used in the parsing
    process to look for the different shortcodes.
    """
    text_sanitized_with_simplified_shortcodes: str = ''
    """
    The last text that this parser object has parsed, with
    the shortcodes simplified after the parsing process
    has detected them. The text used has been sanitized
    previously.
    """
    text_sanitized_without_shortcodes: str = ''
    """
    The last text that this parser object has parsed, with
    no shortcodes on it. The text used has been sanitized
    previously.
    """
    shortcodes: list[Shortcode] = []
    """
    The shortcodes found by the parser in the last text
    parsed.
    """

    def __init__(self, shortcode_tags: list[ShortcodeTag]):
        # TODO: Check that 'shortcode_tags' elements are ShortcodeTags
        self.__parser = Parser(start = '[', end = ']', inherit_globals = False)

        # We register each shortcode in provided 'shortcode_tags'
        self.handlers = []
        for shortcode_tag in shortcode_tags:
            if shortcode_tag.is_block_scoped():
                self.__parser.register(lambda pargs, kwargs, context, content: shortcode_tag.handler(self.shortcodes, pargs, kwargs, context, content), shortcode_tag.tag.value, f'/{shortcode_tag.tag.value}')
            else:
                self.__parser.register(lambda pargs, kwargs, context: shortcode_tag.handler(self.shortcodes, pargs, kwargs, context, None), shortcode_tag.tag.value)

        # Wildcards seems to be not working here so we cannot handle
        # any unknown shortcode by ourselves. It is better to raise
        # the exception when an unknown shortcode is found because it
        # means that something is wrong with the next (could be user
        # mitstake or our own mistake)

    def parse(self, text: str):
        """
        This method parses the provided 'text' according to the shortcode
        tags passed in the initializing process. This method will return
        the original text, the text without shortcodes and the list of
        shortcodes found with their indexes and attributes.
        """
        if not text:
            text = ''
            #raise Exception('No "text" provided.')
        
        self.text = text
        self.text_sanitized = fix_excesive_blank_spaces(fix_ellipsis(fix_unseparated_periods(fix_separated_parenthesis(fix_separated_square_brackets(add_missing_spaces_before_and_after_parenthesis(add_missing_spaces_before_and_after_square_brackets(text)))))))
        self.text_sanitized_with_simplified_shortcodes = ''
        self.text_sanitized_without_shortcodes = ''
        self.shortcodes = []

        # At the begining we have full shortcodes containing attributes
        # but when parsing ([tag attribute=value]), we extract that 
        # information to Shortcode objects and we just preserve the 
        # simple tag ([tag]) to know that there is a shortcode in that
        # position.
        #
        # Once we've done that, we can iterate over the text again,
        # obtaining each shortcode position and extracting the 
        # previous word position in the text.
        
        # We parse shortcodes and extract the information
        self.text_sanitized_with_simplified_shortcodes = self.__parser.parse(self.text_sanitized, context = None)
        
        # After this parse we have 'self.shortcodes' fulfilled

        words = self.text_sanitized_with_simplified_shortcodes.split(' ')

        # Regex to detect any shortcode (start and end tags)
        shortcode_regex_pattern = r'\[(/?[a-zA-Z0-9-_]+)\]'

        # We will iterate over all 
        index = 0
        while index < len(words):
            word = words[index]
            if re.fullmatch(shortcode_regex_pattern, word):
                # TODO: Improve this to avoid the ones completed
                for shortcode in self.shortcodes:
                    if '/' in word:
                        # End shortcode
                        if shortcode.tag == word.replace('[', '').replace(']', '').replace('/', '') and not shortcode.previous_end_word_index:
                            # Is that shortcode
                            shortcode.previous_end_word_index = index - 1
                            break
                    else:
                        # Start shortcode
                        if shortcode.tag == word.replace('[', '').replace(']', '') and not shortcode.previous_start_word_index:
                            # Is that shortcode
                            shortcode.previous_start_word_index = index - 1
                            break

                # TODO: Remove that word
                del(words[index])
            else:
                index += 1

        self.text_sanitized_without_shortcodes = ' '.join(words)

        return self.text_sanitized_without_shortcodes
    
    """
    Specific shortcode handlers below
    TODO: Please, make them work dynamically so I don't need to create 
    a new method in code to any new shortcode, that is stupid.
    """

    # TODO: We need to manually register all shortcode handlers because
    # of some shared code that doesn't allow to do this dynamically (at
    # least by now, there is a task to improve this)
    # TODO: Remove this one, it is a test
    def __meme_shortcode_handler(self, pargs, kwargs, context):
        return self.__simple_shortcode_base_handler(pargs, kwargs, context, 'meme')
    
    def __simple_shortcode_base_handler(self, pargs, kwargs, context, tag: str):
        """
        Handles a simple [tag] shortcode.
        """
        attributes = []

        for parg in pargs:
            attributes.append({
                parg: None
            })

        for kwarg in kwargs:
            attribute_name = kwarg
            attribute_value = kwargs[attribute_name]

            attributes.append({
                attribute_name: attribute_value
            })

        # TODO: We need to handle the position within the text
        self.shortcodes.append(Shortcode(tag, ShortcodeTagType.SIMPLE, attributes, context, None))
            
        # This will replace the shortcode in the text
        return f'[{tag}]'

    # TODO: Remove this one, it is a test
    def __blocke_shortcode_handler(self, pargs, kwargs, context, content):
        return self.__block_shortcode_base_handler(pargs, kwargs, context, content, 'blocke')

    def __block_shortcode_base_handler(self, pargs, kwargs, context, content, tag: str):
        """
        Handles a block [tag] ... [/tag] shortcode.
        """
        attributes = []

        for parg in pargs:
            attributes.append({
                parg: None
            })

        for kwarg in kwargs:
            attribute_name = kwarg
            attribute_value = kwargs[attribute_name]

            attributes.append({
                attribute_name: attribute_value
            })

        # TODO: We need to handle the position within the text
        self.shortcodes.append(Shortcode(tag, ShortcodeTagType.BLOCK, attributes, context, content))
            
        # This will replace the shortcode and its content in the text
        return f'[{tag}]{content}[/{tag}]'