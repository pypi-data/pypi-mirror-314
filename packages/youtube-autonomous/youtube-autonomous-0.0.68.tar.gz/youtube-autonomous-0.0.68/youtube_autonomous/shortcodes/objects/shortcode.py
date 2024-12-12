from youtube_autonomous.shortcodes.enums import ShortcodeTagType
from youtube_autonomous.segments.enums import ShortcodeStart, ShortcodeDuration, ShortcodeField, ShortcodeType, ShortcodeMode
from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement
from youtube_autonomous.elements.validator.element_validator import ElementValidator
from youtube_autonomous.config import Configuration
from youtube_autonomous.experimental.shortcodes.consts import FILE_DURATION
from typing import Union


LOWER_INDEX = -1
UPPER_INDEX = 99999

class Shortcode:
    """
    Class that represent a shortcode detected in a text, containing 
    its attributes and values and also the content if block-scoped.
    """
    _tag: ShortcodeType
    """
    The shortcode tag that represents and identifies it. It
    determines the way it will be built and applied.
    """
    _type: ShortcodeTagType
    _start: float
    _duration: float
    _keywords: str
    _filename: str
    _url: str
    _mode: ShortcodeMode
    _context: any # TODO: Do I really need this (?)
    _content: str
    _previous_start_word_index: int
    _previous_end_word_index: int

    def __init__(self, tag: ShortcodeType, type: ShortcodeTagType, attributes: dict, context, content: str):
        """
        The shortcode has a 'type' and could include some 'attributes' that
        are the parameters inside the brackets, that could also be simple or
        include an associated value. If it is a block-scoped shortcode, it
        will have some 'content' inside of it.
        """
        self.tag = tag
        self.type = type

        self.config = Configuration.get_configuration_by_type(self.tag).config_as_shortcode
        
        self.start = attributes.get(ShortcodeField.START.value, None)
        self.duration = attributes.get(ShortcodeField.DURATION.value, None)
        self.keywords = attributes.get(ShortcodeField.KEYWORDS.value, '')
        self.filename = attributes.get(ShortcodeField.FILENAME.value, '')
        self.url = attributes.get(ShortcodeField.URL.value, '')
        self.mode = attributes.get(ShortcodeField.MODE.value, None)

        # TODO: Should I treat these shortcodes as Enhancement so I need
        # to make the same checks (more specific that these ones below) (?)

        if not self.keywords and not self.filename and not self.url:
            raise Exception('No "keywords" nor "filename" nor "url" sources available.')

        # TODO: Do we actually need the context (?)
        self.context = context
        # TODO: Do we actually need the content (?)
        self.content = content

        # TODO: We are not acepting None
        self.previous_start_word_index = None
        self.previous_end_word_index = None

        # TODO: Maybe we need to create an abstract Shortcode class to inherit
        # in specific shortcode classes

    @property
    def tag(self):
        """
        The shortcode tag that represents and identifies it. It
        determines the way it will be built and applied.
        """
        return self._tag
    
    @tag.setter
    def tag(self, tag: Union[ShortcodeType, str]):
        self._tag = ShortcodeType.to_enum(tag)

    @property
    def type(self):
        """
        The type of the shortcode, that identifies its structure and
        parameters it must have.
        """
        return self._type
    
    @type.setter
    def type(self, type: Union[ShortcodeTagType, str]):
        self._type = ShortcodeTagType.to_enum(type)
        
    @property
    def start(self):
        """
        The time moment of the current segment in which this element is
        expected to be applied.
        """
        return self.start
    
    @start.setter
    def start(self, start: Union[ShortcodeStart, int, float, None]):
        if start is None:
            if self.type == ShortcodeTagType.BLOCK:
                start = ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD
            else:
                start = ShortcodeStart.BETWEEN_WORDS

        self._start = ElementValidator.validate_shortcode_start_field(start)

    @property
    def duration(self):
        """
        The duration of the shortcode, that it is calculated according to the
        field or to its content.
        """
        return self._duration
    
    @duration.setter
    def duration(self, duration: Union[ShortcodeDuration, int, float, None]):
        if duration is None:
            if self.type == ShortcodeTagType.BLOCK:
                duration = ShortcodeDuration.SHORTCODE_CONTENT
            else:
                duration = ShortcodeDuration.FILE_DURATION

        # TODO: I'm setting "file_duration" but checking if it is 99998 value
        # so it is failing. Should I put the numeric value here (?)
        self._duration = ElementValidator.validate_shortcode_duration_field(duration.name)

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, mode: Union[ShortcodeMode, str]):
        mode = ShortcodeMode.to_enum(mode)

        if mode not in self.config.modes:
            raise Exception(f'The provided "{mode.value}" is not a valid mode for this shortcode type "{self.type.value}" and tag "{self.tag.value}".')

        self._mode = mode
    
    @property
    def context(self):
        """
        The context of the shortcode.

        TODO: Do I really need this (?)
        """
        return self._context
    
    @context.setter
    def context(self, context: any):
        # TODO: Do I need to check something (?)

        self._context = context

    @property
    def content(self):
        """
        The text that is between the shortcode open and end tag
        and can include shortcodes. This parameter makes sense if
        the shortcode is a block-scoped shortcode.
        """
        return self._content
    
    @content.setter
    def content(self, content: str):
        # TODO: Do I need to check something (?)
        if content is not None and not isinstance(content, str):
            raise Exception('The "content" parameter provided is not a string.')
        
        if content is None:
            content = ''

        self._content = content

    @property
    def previous_start_word_index(self):
        """
        The index, obtained from the whole text of the segment, of the
        word that is inmediately before the shortcode start tag.
        """
        return self._previous_start_word_index
    
    @previous_start_word_index.setter
    def previous_start_word_index(self, previous_start_word_index: int):
        if previous_start_word_index is None:
            self._previous_start_word_index = previous_start_word_index
            # TODO: Sorry, fix this
            return

        if not previous_start_word_index and previous_start_word_index != 0:
            raise Exception('No "previous_start_word_index" provided.')
        
        if not isinstance(previous_start_word_index, int):
            raise Exception('The "previous_start_word_index" parameter provided is not an int number.')

        if previous_start_word_index < LOWER_INDEX or previous_start_word_index > UPPER_INDEX:
            raise Exception(f'No valid "previous_start_word_index" parameter provided. Must be between {LOWER_INDEX} and {UPPER_INDEX}.')
        
        self._previous_start_word_index = previous_start_word_index

    @property
    def previous_end_word_index(self):
        """
        The index, obtained from the whole text of the segment, of the
        word that is inmediately before the shortcode end tag.
        """
        return self._previous_end_word_index
    
    @previous_end_word_index.setter
    def previous_end_word_index(self, previous_end_word_index: int):
        if previous_end_word_index is None:
            self._previous_end_word_index = None
            # TODO: Sorry, fix this
            return

        if not previous_end_word_index and previous_end_word_index != 0:
            raise Exception('No "previous_end_word_index" provided.')
        
        if not isinstance(previous_end_word_index, int):
            raise Exception('The "previous_end_word_index" parameter provided is not an int number.')
        
        if previous_end_word_index < LOWER_INDEX or previous_end_word_index > UPPER_INDEX:
            raise Exception(f'No valid "previous_end_word_index" parameter provided. Must be between {LOWER_INDEX} and {UPPER_INDEX}.')
        
        self._previous_end_word_index = previous_end_word_index

    def __calculate_start_and_duration(self, transcription):
        """
        Processes this shortcode 'start' and 'duration' fields by using
        the 'transcription' if needed (if 'start' and 'duration' fields
        are not numbers manually set by the user in the shortcode when
        written).

        This will consider the current 'start' and 'duration' strategy
        and apply them to the words related to the shortcode to obtain
        the real 'start' and 'duration' number values.
        """
        if isinstance(self.start, ShortcodeStart):
            # TODO: What if single shortcode with no next word (?)
            if self.type == ShortcodeTagType.SIMPLE:
                if self.start == ShortcodeStart.BETWEEN_WORDS:
                    self.start = (transcription[self._previous_start_word_index]['end'] + transcription[self._previous_start_word_index + 1]['start']) / 2
                # TODO: What about block-scoped value when simple type (?)
            else:
                if self.start == ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD:
                    self.start = transcription[self._previous_start_word_index + 1]['start']
                elif self.start == ShortcodeStart.MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD:
                    self.start = (transcription[self._previous_start_word_index + 1]['start'] + transcription[self._previous_start_word_index + 1]['end']) / 2
                elif self.start == ShortcodeStart.END_OF_FIRST_SHORTCODE_CONTENT_WORD:
                    self.start = transcription[self._previous_start_word_index + 1]['end']
                # TODO: What about simple value when block-scoped type (?)

        if isinstance(self.duration, ShortcodeDuration):
            if self.type == ShortcodeTagType.SIMPLE:
                if self.duration == ShortcodeDuration.FILE_DURATION:
                    # This duration must be set when the file is ready, so 
                    # we use a number value out of limits to flag it
                    self.duration = FILE_DURATION
            else:
                if self.duration == ShortcodeDuration.SHORTCODE_CONTENT:
                    self.duration = transcription[self.previous_end_word_index]['end'] - transcription[self.previous_start_word_index + 1]['start']

    def to_enhancement_element(self, transcription):
        """
        Turns the current shortcode to an EnhancementElement by using
        the provided 'transcription' and using its words to set the
        actual 'start' and 'duration' fields according the narration.

        The provided 'transcription' could be not needed if the segment
        is not narrated and 'start' and 'duration' fields are manually
        set by the user in the shortcode.
        """
        if self.type == ShortcodeTagType.SIMPLE and self.previous_start_word_index is None:
            raise Exception(f'Found {ShortcodeTagType.SIMPLE.value} shortcode without "previous_start_word_index".')
        
        if self.type == ShortcodeTagType.BLOCK and (self.previous_start_word_index is None or self.previous_end_word_index is None):
            raise Exception(f'Found {ShortcodeTagType.BLOCK.value} shortcode without "previous_start_word_index" or "previous_end_word_index".')
        
        self.__calculate_start_and_duration(transcription)

        # TODO: Build it
        enhancement_element = EnhancementElement.get_class_from_type(self.tag)(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)

        # TODO: Remove this below if the code above is working
        # if self.tag == ShortcodeType.MEME:
        #     enhancement_element = MemeEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # elif self.tag == ShortcodeType.SOUND:
        #     enhancement_element = SoundEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # elif self.tag == ShortcodeType.IMAGE:
        #     enhancement_element = ImageEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # elif self.tag == ShortcodeType.STICKER:
        #     enhancement_element = StickerEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # elif self.tag == ShortcodeType.GREEN_SCREEN:
        #     enhancement_element = GreenscreenEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # elif self.tag == ShortcodeType.EFFECT:
        #     enhancement_element = EffectEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
        # else:
        #     raise Exception(f'No valid shortcode "{self.tag}" type provided.')
        #     # TODO: Implement the other EnhancementElements
        #     enhancement_element = EnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)

        return enhancement_element