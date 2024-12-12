from youtube_autonomous.segments.enums import SegmentField


class ElementData:
    """
    A class to handle any project Element information.
    """
    # Others
    type: str
    """
    The segment or enhancement type, that must be a SegmentType value or 
    an EnhancementType value, and will determine the type of video that 
    will be created. This type is also used to read the necessary 
    parameters to be able to build it, that vary for each segment type 
    value (see SegmentType enums to know valid values).
    """
    status: str
    # Narration
    audio_narration_filename: str
    """
    The filename (if existing) of the audio narration that the user has 
    manually provided to the project. This is a voice narration that will
    should be included as the audio of the segment, transcripted and used
    in the video generation. This parameter can be provided, in which case
    it will be used as the main audio and will be transcripted, or could 
    be not provided. This parameter, if provided, will generate the
    segment 'transcription' parameter.
    """
    narration_text: str
    narration_text_sanitized_without_shortcodes: str
    narration_text_with_simplified_shortcodes: str
    narration_text_sanitized: str
    voice: str
    """
    The voice that would be used to narrate the segment 'text' parameter
    when provided. This will be used to handle the narration system voice
    that will generate the audio narration to be used as the main segment
    audio, that will be also transcripted to the segment 'transcription'
    parameter. This parameter must be a valid value and the 'text' 
    parameter must be also set to be able to build the narration.
    """
    # Text
    text: str
    """
    The text that will be shown in the screen or that will be narrated 
    according to the type of segment. This text could be treated to
    improve it or add missing blank spaces, or could be modified to be
    able to build the content in a better way.
    """
    # Specific duration
    duration: float
    """
    The duration the user wants this segment content to last. This can be
    included when there is no audio narration to determine the actual
    segment content duration, so it is manually set by the user.
    """
    # Source (filename or url)
    filename: str
    url: str
    """
    The url from which the content for the segment has to be obtained. 
    This can be included in the segment types that use this parameter and
    the resource will be downloaded (if available) in those cases to let
    the segment content be built.
    """
    # Source or identifier (keywords)
    keywords: str
    """
    The keywords to look for a custom video, to create a custom image, etc.
    They have different uses according to the segment type, but they are
    used to look for the resource necessary to build the video.
    """
    # Enhancements
    enhancements: list['Enhancement']

    # During building
    calculated_duration: float
    """
    A parameter that is set when the audio part has been created
    to know which duration we need to use when creating the video
    part. This parameters acts as the 'duration' parameter when 
    it has to be calculated dynamically based on the content that
    is created.

    _This parameter is not manually set by the user._
    """
    start: float
    mode: str
    audio_filename: str
    """
    The audio clip filename that is generated during this project
    segment building process. The file is written when the audio
    processing has ended, so it works as a backup to avoid the
    need of generating it again if something goes wrong in other
    part of this (or another) segment building process.

    This file is stored locally in a segments content specific
    folder, so if the project needs to be built again, it can be
    recovered from this local file.

    _This parameter is not manually set by the user._
    """
    video_filename: str
    """
    The video clip filename that is generated during this project
    segment building process. The file is written when the video
    processing has ended, so it works as a backup to avoid the
    need of generating it again if something goes wrong in other
    part of this (or another) segment building process.

    This file is stored locally in a segments content specific
    folder, so if the project needs to be built again, it can be
    recovered from this local file.

    _This parameter is not manually set by the user._
    """
    full_filename: str
    """
    The full clip filename that is generated during this project
    segment building process. The file is written when the whole
    processing has ended, so it works as a backup to avoid the
    need of generating it again if something goes wrong in any
    other segment building process.

    This file is stored locally in a segments content specific
    folder, so if the project needs to be built again, it can be
    recovered from this local file.

    Having this filename set in the project means that this 
    segment has been completely and succesfully generated, so it
    won't be generated again.

    _This parameter is not manually set by the user._
    """
    transcription = None
    """
    The audio transcription (if available) that is a list of dict words that
    contains 'text' (the word string), 'start' (the time in which the word
    starts being said), 'end' (the moment in which the word stops being said)
    and 'confidence' (how sure the system is that the word has been correctly
    listened and fits the audio).

    _This parameter is not manually set by the user._
    """
    shortcodes = []

    def __init__(self, json: dict):
        # TODO: Apply 'SegmentField' instead of this strings, please
        self.type = json.get('type', '')
        self.status = json.get('status', '')

        self.audio_narration_filename = json.get(SegmentField.AUDIO_NARRATION_FILENAME.value, '')

        self.narration_text = json.get(SegmentField.NARRATION_TEXT.value, '')
        self.narration_text_sanitized_without_shortcodes = json.get('narration_text_sanitized_without_shortcodes', '')
        self.narration_text_with_simplified_shortcodes = json.get('narration_text_with_simplified_shortcodes', '')
        self.narration_text_sanitized = json.get('narration_text_sanitized', '')
        self.voice = json.get(SegmentField.VOICE.value, '')

        self.text = json.get(SegmentField.TEXT.value, '')

        self.duration = json.get(SegmentField.DURATION.value, None)
        
        self.filename = json.get(SegmentField.FILENAME.value, '')
        self.url = json.get(SegmentField.URL.value, '')

        self.keywords = json.get(SegmentField.KEYWORDS.value, '')

        self.shortcodes = json.get('shortcodes', [])
        self.transcription = json.get('transcription', None)

        self.enhancements = json.get(SegmentField.ENHANCEMENTS.value, [])

        self.calculated_duration = json.get('calculated_duration', None)
        self.start = json.get('start', None)
        self.mode = json.get('mode', '')
        self.audio_filename = json.get('audio_filename', '')
        self.video_filename = json.get('video_filename', '')
        self.full_filename = json.get('full_filename', '')

    def as_enum(self):
        """
        Returns the information
        """
        # TODO: (?)