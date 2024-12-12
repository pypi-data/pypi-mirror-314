"""
This class represents a Segment that will handle all the information
that it contains to build the project segment video part.
"""
# from exceptions.invalid_segment_exception import InvalidSegmentException
# from objects.segment_content_builder import SegmentContentBuilder
# from moviepy import AudioFileClip
# from yta_multimedia.audio.sound.generation import create_silence_audio_file
# from yta_general_utils.logger import print_completed, print_error, print_in_progress
# from yta_multimedia.audio.voice.generation.tts.google import narrate as generate_google_narration
# from utils.shortcodes import handle_shortcodes
# from utils.general import create_segment_filename
# from yta_general_utils.url_checker import url_is_ok, url_is_image
# from yta_general_utils.file_processor import file_exists, file_is_audio_file
# from utils.video_utils import apply_effects, apply_sounds, apply_green_screens, apply_images, apply_stickers, apply_memes
# from yta_ai_utils.transcription import get_transcription_with_timestamps
# from utils.validation.segment.validator import VALID_SEGMENT_TYPES
# from segments.building.objects.enums import *
# from os import getenv as os_getenv
# from dotenv import load_dotenv
# from utils.mongo_utils import get_project_by_id, set_project_segment_audio_filename, set_project_segment_transcription, set_project_segment_full_filename, set_project_segment_as_finished
# from segments.building.objects.enums import EnhancementField

# import re
# import segments.building.objects.green_screen
# import segments.building.objects.image
# import segments.building.objects.meme
# import segments.building.objects.sticker
# import segments.building.objects.sound
# import segments.building.objects.effect

# load_dotenv()

# BAN_WORDS_PROBABILITY = os_getenv('BAN_WORDS_PROBABILITY')
# ENHANCE_WORDS_PROBABILITY = os_getenv('ENHANCE_WORDS_PROBABILITY')


from youtube_autonomous.experimental.segments.validation.segment_validator import SegmentValidator
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode
from youtube_autonomous.segments.enums import SegmentType, SegmentField, SegmentStatus
from youtube_autonomous.segments.builder.ai import create_ai_narration
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement
from youtube_autonomous.segments.enhancement.edition_manual.edition_manual_term import EditionManualTerm
from yta_multimedia.audio.voice.transcription.stt.whisper import get_transcription_with_timestamps
from yta_multimedia.audio.sound.generation.sound_generator import SoundGenerator
from yta_general_utils.logger import print_in_progress, print_completed
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.file.checker import file_exists, file_is_audio_file, file_is_video_file
from yta_general_utils.file.reader import read_json_from_file
from typing import Union
from bson.objectid import ObjectId
from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip


class Segment:
    """
    This is a Segment to build itself. This is a post-processed segment. It
    will receive a json file that has been previously processed to fill any
    missing field that can be guessed by an AI.
    """
    __segment_validator: SegmentValidator = None
    """
    Segment validator to validate that the structure is valid and that the
    content is able to be built with the parameters provided.

    _This parameter is not manually set by the user._
    """
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.

    _This parameter is not manually set by the user._
    """
    __builder: SegmentContentBuilder = None
    """
    Segment content builder that generates the content for the segment based
    on the parameters provided.

    _This parameter is not manually set by the user._
    """
    __shortcode_parser: ShortcodeParser = None
    """
    Shortcode parser that parses the shortcodes in the text to be able to
    enhance the final clip by applying those shortcode effects properly.

    _This parameter is not manually set by the user._
    """
    _project_id: str = None
    """
    The unique id that identifies the project to which this segment belongs.
    This, in our project, is a mongo ObjectId that is set when stored in 
    the database as a valid project.

    _This parameter is not manually set by the user._
    """
    _segment_index: int = None
    """
    The index (order) in which this segment has been set in the project to
    which it belongs. This is necessary to build the whole project video in
    the expected order.

    _This parameter is not manually set by the user._
    """
    _status: SegmentStatus = None
    """
    The current status of the segment, that must be a SegmentStatus enum.

    _This parameter is not manually set by the user._
    """
    _type: SegmentType = None
    """
    The segment type, that must be a SegmentType value and will determine
    the type of video that will be created. This type is also used to read
    the necessary parameters to be able to build it, that vary for each
    segment type value (see SegmentType enums to know valid values).
    """
    _keywords: Union[str, None] = None
    """
    The keywords to look for a custom video, to create a custom image, etc.
    They have different uses according to the segment type, but they are
    used to look for the resource necessary to build the video.
    """
    _text: Union[str, None] = None
    """
    The text that will be shown in the screen or that will be narrated 
    according to the type of segment. This text could be treated to
    improve it or add missing blank spaces, or could be modified to be
    able to build the content in a better way.
    """
    # TODO: Add the other 'texts' if I definitely keep them here
    _audio_narration_filename: Union[str, None] = None
    """
    The filename (if existing) of the audio narration that the user has 
    manually provided to the project. This is a voice narration that will
    should be included as the audio of the segment, transcripted and used
    in the video generation. This parameter can be provided, in which case
    it will be used as the main audio and will be transcripted, or could 
    be not provided. This parameter, if provided, will generate the
    segment 'transcription' parameter.
    """
    _voice: Union[str, None] = None
    """
    The voice that would be used to narrate the segment 'text' parameter
    when provided. This will be used to handle the narration system voice
    that will generate the audio narration to be used as the main segment
    audio, that will be also transcripted to the segment 'transcription'
    parameter. This parameter must be a valid value and the 'text' 
    parameter must be also set to be able to build the narration.
    """
    _frame: Union[str, None] = None # TODO: Not well defined, could change
    """
    The wrapper of the generated content. This means that the segment
    content will be generated and, when done, will be wrapped in this 
    frame if set. This frame could be a greenscreen, a custom frame.
    """
    _duration: Union[float, None] = None
    """
    The duration the user wants this segment content to last. This can be
    included when there is no audio narration to determine the actual
    segment content duration, so it is manually set by the user.
    """
    _url: Union[str, None] = None
    """
    The url from which the content for the segment has to be obtained. 
    This can be included in the segment types that use this parameter and
    the resource will be downloaded (if available) in those cases to let
    the segment content be built.
    """
    _transcription = None
    """
    The audio transcription (if available) that is a list of dict words that
    contains 'text' (the word string), 'start' (the time in which the word
    starts being said), 'end' (the moment in which the word stops being said)
    and 'confidence' (how sure the system is that the word has been correctly
    listened and fits the audio).

    _This parameter is not manually set by the user._
    """
    _shortcodes = []
    """
    The list of shortcodes that has been found in the text.

    _This parameter is not manually set by the user._

    TODO: Explain this better when done and working properly.
    """
    _calculated_duration = None
    """
    A parameter that is set when the audio part has been created
    to know which duration we need to use when creating the video
    part. This parameters acts as the 'duration' parameter when 
    it has to be calculated dynamically based on the content that
    is created.

    _This parameter is not manually set by the user._
    """
    _audio_clip: Union[AudioFileClip, CompositeAudioClip, None] = None
    """
    The audio clip that is generated during this project segment
    building process. This is a moviepy audio clip that will be
    appended to the final clip.

    _This parameter is not manually set by the user._
    """
    _audio_filename: Union[str, None] = None
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
    _video_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, None] = None
    """
    The video clip that is generated during this project segment
    building process. This is a moviepy video clip that will be
    used as the main video clip and it is the core video part of
    this segment.

    _This parameter is not manually set by the user._
    """
    _video_filename: Union[str, None] = None
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
    _full_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, None] = None
    """
    The full video clip (including audio) that is generated during
    this project segment building process. This is a moviepy video
    clip (including audio) that will be used as the final clip and
    it is the definitive segment content clip.

    This parameter is set when the building process has finished,
    so having it means that the project segment has been built
    completely and succesfully.

    _This parameter is not manually set by the user._
    """
    _full_filename: Union[str, None] = None
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
    __do_use_setter: bool = True
    """
    Internal variable to know if we should use the custom property setters
    or just assign the value directly.

    _This parameter is not manually set by the user._
    """
    __do_update_database: bool = True
    """
    Internal variable to know if we should persist the change in the database
    or just assign the value.

    _This parameter is not manually set by the user._
    """

    def __init__(self, json, project_id: Union[ObjectId, str], segment_index):
        self._segment_validator = SegmentValidator()
        self._database_handler = DatabaseHandler()
        self._builder = SegmentContentBuilder()
        self._shortcode_parser = ShortcodeParser([])

        # Invalid json will raise an Exception here
        self._segment_validator.validate(json)
        
        self.project_id = project_id
        self.segment_index = segment_index

        # Load available segment fields from json
        for field in SegmentField.get_all():
            setattr(self, field.value, json.get(field.value, None))
        # TODO: Add 'frame', that means a frame that wraps the content created
        # (could be a greenscreen or something similar) to be able to make it
        # more dynamic
        self._do_use_setter = False
        self.status = json.get('status', SegmentStatus.TO_START)
        self._do_use_setter = True

        # Segment enhancement elements we could need to append/implement
        #self.effects = self.__check_and_format_effects(json)
        self.enhancements = []
        self.json_effects = json.get('effects', [])
        self.sounds = []
        self.greenscreens = []
        self.images = []
        self.stickers = []
        self.memes = []

        # Post-processing fields
        # TODO: These are initialized by definition (I think)
        self.shortcodes = []
        # TODO: These below could be an interesting implementation
        self.tmp_filenames = [] # For creation time, to preserve for failures
        self._do_update_database = False
        self.transcription = json.get('transcription', None) # Audio transcription
        self.audio_filename = json.get('audio_filename', None) # Filename of the used audio
        self.video_filename = json.get('video_filename', None) # Filename of the used video
        self.full_filename = json.get('full_filename', None) # Filename of the final video
        self._do_update_database = True

    @property
    def _segment_validator(self):
        """
        Segment validator to validate that the structure is valid and that the
        content is able to be built with the parameters provided.

        _This parameter is not manually set by the user._
        """
        return self.__segment_validator

    @_segment_validator.setter
    def _segment_validator(self, segment_validator: SegmentValidator):
        if not segment_validator:
            raise Exception('No "segment_validator" provided.')
        
        if not isinstance(segment_validator, SegmentValidator):
            raise Exception('The "segment_validator" parameter provided is not a SegmentValidator.')

        self.__segment_validator = segment_validator
        
    @property
    def _database_handler(self):
        """
        Object to interact with the database and get and create projects.

        _This parameter is not manually set by the user._
        """
        return self.__database_handler

    @_database_handler.setter
    def _database_handler(self, database_handler: DatabaseHandler):
        if not database_handler:
            raise Exception('No "database_handler" provided.')
        
        if not isinstance(database_handler, DatabaseHandler):
            raise Exception('The "database_handler" parameter provided is not a DatabaseHandler.')

        self.__database_handler = database_handler

    @property
    def _builder(self):
        """
        Segment content builder that generates the content for the segment based
        on the parameters provided.

        _This parameter is not manually set by the user._
        """
        return self.__builder
    
    @_builder.setter
    def _builder(self, builder: SegmentContentBuilder):
        if not builder:
            raise Exception('No "builder" provided.')

        if not isinstance(builder, SegmentContentBuilder):
            raise Exception('The "builder" parameter provided is not a SegmentContentBuilder.')
        
        self.__builder = builder

    @property
    def _shortcode_parser(self):
        """
        Shortcode parser that parses the shortcodes in the text to be able to
        enhance the final clip by applying those shortcode effects properly.

        _This parameter is not manually set by the user._
        """
        return self.__shortcode_parser
    
    @_shortcode_parser.setter
    def _shortcode_parser(self, shortcode_parser: ShortcodeParser):
        if not shortcode_parser:
            raise Exception('No "shortcode_parser" provided.')

        if not isinstance(shortcode_parser, ShortcodeParser):
            raise Exception('The "shortcode_parser" parameter is not a ShortcodeParser.')
        
        self.__shortcode_parser = shortcode_parser

    @property
    def project_id(self):
        """
        The unique id that identifies the project to which this segment belongs.
        This, in our project, is a mongo ObjectId that is set when stored in 
        the database as a valid project.

        _This parameter is not manually set by the user._
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: Union[ObjectId, str]):
        if not project_id:
            raise Exception('No "project_id" provided.')

        if not isinstance(project_id, (str, ObjectId)):
            raise Exception('The "project_id" parameter is not a string or an ObjectId.')
        
        if isinstance(id, ObjectId):
            project_id = str(project_id)

        self._project_id = project_id

    @property
    def segment_index(self):
        """
        The index (order) in which this segment has been set in the project to
        which it belongs. This is necessary to build the whole project video in
        the expected order.

        _This parameter is not manually set by the user._
        """
        return self._segment_index
    
    @segment_index.setter
    def segment_index(self, segment_index):
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        # TODO: Check that 'segment_index' is a number
        
        self._segment_index = segment_index

    @property
    def status(self):
        """
        The current status of the segment, that must be a SegmentStatus enum.

        _This parameter is not manually set by the user._
        """
        return self._status

    @status.setter
    def status(self, status: Union[SegmentStatus, str] = SegmentStatus.TO_START):
        if not status:
            raise Exception('No "status" provided.')

        if not isinstance(status, (SegmentStatus, str)):
            raise Exception('The "status" parameter provided is not a SegmentStatus nor a string.')
        
        if isinstance(status, str): 
            if not SegmentStatus.is_valid(status):
                raise Exception('The "status" provided string is not a valid SegmentStatus enum value.')
            
            status = SegmentStatus(status)

        self._status = status.value
        if self._do_use_setter:
            self._database_handler.update_project_segment_status(self.project_id, self.segment_index, status)

    @property
    def type(self):
        """
        The segment type, that must be a SegmentType value and will determine
        the type of video that will be created. This type is also used to read
        the necessary parameters to be able to build it, that vary for each
        segment type value (see SegmentType enums to know valid values).
        """
        return self._type
    
    @type.setter
    def type(self, type: Union[SegmentType, str]):
        if not type:
            raise Exception('No "type" provided.')
        
        if not isinstance(type, (SegmentType, str)):
            raise Exception('The "type" parameter provided is not a SegmentType nor a string.')
        
        if isinstance(type, str) and not SegmentType.is_valid(type):
            raise Exception('The "type" provided string is not a valid SegmentType enum value.')

        self._type = type

    @property
    def keywords(self):
        """
        The keywords to look for a custom video, to create a custom image, etc.
        They have different uses according to the segment type, but they are
        used to look for the resource necessary to build the video.
        """
        return self._keywords
    
    @keywords.setter
    def keywords(self, keywords: Union[str, None]):
        if keywords is not None and not isinstance(keywords, str):
            raise Exception('The "keywords" parameter provided is not a string.')
        
        if keywords is None:
            keywords = ''

        self._keywords = keywords

    @property
    def text(self):
        """
        The text that will be shown in the screen or that will be narrated 
        according to the type of segment. This text could be treated to
        improve it or add missing blank spaces, or could be modified to be
        able to build the content in a better way.
        """
        return self._text

    @text.setter
    def text(self, text: Union[str, None]):
        if not self._do_use_setter:
            self._text = text
        else:
            if text is not None and not isinstance(text, str):
                raise Exception('The "text" parameter provided is not a string.')

            if text is None:
                text = ''

            # I need text, yes, but I need to remove shortcodes to narrate
            self._text = text
            self._shortcode_parser.parse(self.text)
            self.shortcodes = self._shortcode_parser.shortcodes
            self.text_sanitized = self._shortcode_parser.text_sanitized
            self.text_sanitized_without_shortcodes = self._shortcode_parser.text_sanitized_without_shortcodes
            self.text_sanitized_with_simplified_shortcodes = self._shortcode_parser.text_sanitized_with_simplified_shortcodes

    @property
    def text_sanitized(self):
        return self._text_sanitized

    @text_sanitized.setter
    def text_sanitized(self, text: str):
        if not self._do_use_setter:
            self._text_sanitized = text
        else:
            if text is not None and not isinstance(text, str):
                raise Exception('The "text" parameter provided is not a string.')

            if text is None:
                text = ''
            
            self._text_sanitized = text
            if self._do_update_database:
                self._database_handler.update_project_segment_field(self.project_id, self.segment_index, 'text_sanitized', text)

    @property
    def text_sanitized_without_shortcodes(self):
        return self._text_sanitized_without_shortcodes

    @text_sanitized_without_shortcodes.setter
    def text_sanitized_without_shortcodes(self, text: str):
        if not self._do_use_setter:
            self._text_sanitized_without_shortcodes = text
        else:
            if text is not None and not isinstance(text, str):
                raise Exception('The "text" parameter provided is not a string.')

            if text is None:
                text = ''
            
            self._text_sanitized_without_shortcodes = text
            if self._do_update_database:
                self._database_handler.update_project_segment_field(self.project_id, self.segment_index, 'text_sanitized_without_shortcodes', text)

    @property
    def text_sanitized_with_simplified_shortcodes(self):
        return self._text_sanitized_with_simplified_shortcodes

    @text_sanitized_with_simplified_shortcodes.setter
    def text_sanitized_with_simplified_shortcodes(self, text: str):
        if not self._do_use_setter:
            self._text_sanitized_with_simplified_shortcodes = text
        else:
            if text is not None and not isinstance(text, str):
                raise Exception('The "text" parameter provided is not a string.')

            if text is None:
                text = ''
            
            self._text_sanitized_with_simplified_shortcodes = text
            if self._do_update_database:
                self._database_handler.update_project_segment_field(self.project_id, self.segment_index, 'text_sanitized_with_simplified_shortcodes', text)
    
    @property
    def audio_narration_filename(self):
        """
        The filename (if existing) of the audio narration that the user has 
        manually provided to the project. This is a voice narration that will
        should be included as the audio of the segment, transcripted and used
        in the video generation. This parameter can be provided, in which case
        it will be used as the main audio and will be transcripted, or could 
        be not provided. This parameter, if provided, will generate the
        segment 'transcription' parameter.
        """
        return self._audio_narration_filename

    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        if not self._do_use_setter:
            self._audio_narration_filename = audio_narration_filename
        else:
            if audio_narration_filename is not None:
                if not audio_narration_filename:
                    raise Exception('No "audio_narration_filename" provided.')
                
                if not isinstance(audio_narration_filename, str):
                    raise Exception('The "audio_narration_filename" parameter provided is not a string.')
                
                if not file_exists(audio_narration_filename):
                    raise Exception('The "audio_narration_filename" parameter provided is not a file, it does not exist.')

                if not file_is_audio_file(audio_narration_filename):
                    raise Exception('The "audio_narration_filename" parameter provided is not a valid video file.')
            else:
                audio_narration_filename = ''

            self._audio_narration_filename = audio_narration_filename
            if self._do_update_database:
                # TODO: Update this in database
                pass
            
    @property
    def voice(self):
        """
        The voice that would be used to narrate the segment 'text' parameter
        when provided. This will be used to handle the narration system voice
        that will generate the audio narration to be used as the main segment
        audio, that will be also transcripted to the segment 'transcription'
        parameter. This parameter must be a valid value and the 'text' 
        parameter must be also set to be able to build the narration.
        """
        return self._voice
    
    @voice.setter
    def voice(self, voice: Union[str, None]):
        if voice is not None and not isinstance(voice, str):
            raise Exception('The "voice" parameter provided is not a string.')

        if voice is None:
            voice = ''
        
        self._voice = voice

    @property
    def frame(self):
        """
        The wrapper of the generated content. This means that the segment
        content will be generated and, when done, will be wrapped in this 
        frame if set. This frame could be a greenscreen, a custom frame.
        """
        return self._frame
    
    @frame.setter
    def frame(self, frame: Union[str, None]):
        if frame is not None and not isinstance(frame, str):
            raise Exception('The "frame" parameter provided is not a string.')

        if frame is None:
            frame = ''
        
        self._frame = frame

    @property
    def duration(self):
        """
        The duration the user wants this segment content to last. This can be
        included when there is no audio narration to determine the actual
        segment content duration, so it is manually set by the user.
        """
        return self._duration
    
    @duration.setter
    def duration(self, duration: Union[int, float, None]):
        # TODO: Add all number types (no negative)
        if not duration and duration is not None:
            raise Exception('No "duration" provided.')
        
        # TODO: Check it is a valid number type
        
        self._duration = duration

    @property
    def url(self):
        """
        The url from which the content for the segment has to be obtained. 
        This can be included in the segment types that use this parameter and
        the resource will be downloaded (if available) in those cases to let
        the segment content be built.
        """
        return self._url
    
    @url.setter
    def url(self, url: Union[str, None]):
        if url is not None and not isinstance(url, str):
            raise Exception('The "url" parameter provided is not a string.')

        if url is None:
            url = ''
        
        # TODO: We should check if url is valid according to parameters
        self._url = url

    @property
    def transcription(self):
        """
        The audio transcription (if available) that is a list of dict words that
        contains 'text' (the word string), 'start' (the time in which the word
        starts being said), 'end' (the moment in which the word stops being said)
        and 'confidence' (how sure the system is that the word has been correctly
        listened and fits the audio).

        _This parameter is not manually set by the user._
        """
        return self._transcription

    @transcription.setter
    def transcription(self, transcription):
        if not self._do_use_setter:
            self._transcription = transcription
        else:
            # TODO: Maybe something else (?)
            self._transcription = transcription
            if self._do_update_database:
                self._database_handler.set_project_segment_transcription(self.project_id, self.segment_index, self.transcription)
                print_completed('Transcription stored in database.')

    @property
    def shortcodes(self):
        """
        The list of shortcodes that has been found in the text.

        _This parameter is not manually set by the user._

        TODO: Explain this better when done and working properly.
        """
        return self._shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: list[Shortcode]):
        if not shortcodes and shortcodes != []:
            raise Exception('No "shortcodes" provided.')
        
        # TODO: Check each element type

        self._shortcodes = shortcodes
        # TODO: Update in database (?)

    @property
    def calculated_duration(self):
        """
        A parameter that is set when the audio part has been created
        to know which duration we need to use when creating the video
        part. This parameters acts as the 'duration' parameter when 
        it has to be calculated dynamically based on the content that
        is created.

        _This parameter is not manually set by the user._
        """
        return self._calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[int, float, None]):
        # TODO: Accept any type of number (no negatives)
        if not calculated_duration and calculated_duration is not None:
            raise Exception('No "calculated_duration" provided.')
        
        # TODO: Check type and valid number

        self._calculated_duration = calculated_duration

    @property
    def audio_clip(self):
        """
        The audio clip that is generated during this project segment
        building process. This is a moviepy audio clip that will be
        appended to the final clip.

        _This parameter is not manually set by the user._
        """
        return self._audio_clip
    
    @audio_clip.setter
    def audio_clip(self, audio_clip: Union[AudioFileClip, CompositeAudioClip, None]):
        if audio_clip is not None and not isinstance(audio_clip, (AudioFileClip, CompositeAudioClip)):
            raise Exception('The "audio_clip" parameter is not a AudioFileClip nor a CompositeAudioClip.')
        
        self._audio_clip = audio_clip

    @property
    def audio_filename(self):
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
        return self._audio_filename

    @audio_filename.setter
    def audio_filename(self, audio_filename: str):
        if not self._do_use_setter:
            self._audio_filename = audio_filename
        else:
            if audio_filename is not None and audio_filename != '':
                if not audio_filename:
                    raise Exception('No "audio_filename" provided.')
                
                if not isinstance(audio_filename, str):
                    raise Exception('The "audio_filename" parameter provided is not a string.')
                
                if not file_exists(audio_filename):
                    raise Exception('The "audio_filename" parameter provided is not a file, it does not exist.')

                if not file_is_audio_file(audio_filename):
                    raise Exception('The "audio_filename" parameter provided is not a valid video file.')
            else:
                audio_filename = ''
            
            self._audio_filename = audio_filename
            if self._do_update_database:
                self._database_handler.set_project_segment_audio_filename(self.project_id, self.segment_index, self.audio_filename)
                print_completed('Audio filename stored in database.')
            
            if self._audio_filename == '':
                self.audio_clip = None
                self.calculated_duration = None
            else:
                self.audio_clip = AudioFileClip(self.audio_filename)
                self.calculated_duration = self.audio_clip.duration
                print_completed('Audio clip loaded in memory.')

    @property
    def video_clip(self):
        """
        The video clip that is generated during this project segment
        building process. This is a moviepy video clip that will be
        used as the main video clip and it is the core video part of
        this segment.

        _This parameter is not manually set by the user._
        """
        return self._video_clip
    
    @video_clip.setter
    def video_clip(self, video_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, None]):
        if video_clip is not None and not isinstance(video_clip, (VideoFileClip, CompositeVideoClip, ImageClip, ColorClip)):
            raise Exception('The "video_clip" parameter is not a VideoFileClip nor a CompositeVideoClip nor a ImageClip nor a ColorClip.')
        
        self._video_clip = video_clip

    @property
    def video_filename(self):
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
        return self._video_filename

    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        if not self._do_use_setter:
            self._video_filename = video_filename
        else:
            if video_filename is not None and video_filename != '':
                if not video_filename:
                    raise Exception('No "video_filename" provided.')
                
                if not isinstance(video_filename, str):
                    raise Exception('The "video_filename" parameter provided is not a string.')
                
                if not file_exists(video_filename):
                    raise Exception('The "video_filename" parameter provided is not a file, it does not exist.')

                if not file_is_video_file(video_filename):
                    raise Exception('The "video_filename" parameter provided is not a valid video file.')
            else:
                video_filename = ''
                
            self._video_filename = video_filename
            if self._do_update_database:
                self._database_handler.set_project_segment_video_filename(self.project_id, self.segment_index, self.video_filename)
                print_completed('Video filename stored in database.')

            if self.video_filename == '':
                self.video_clip = None
            else:
                self.video_clip = VideoFileClip(self.video_filename)
                print_completed('Video clip loaded in memory.')

    @property
    def full_clip(self):
        """
        The full video clip (including audio) that is generated during
        this project segment building process. This is a moviepy video
        clip (including audio) that will be used as the final clip and
        it is the definitive segment content clip.

        This parameter is set when the building process has finished,
        so having it means that the project segment has been built
        completely and succesfully.

        _This parameter is not manually set by the user._
        """
        return self._full_clip
    
    @full_clip.setter
    def full_clip(self, full_clip: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, None]):
        if full_clip is not None and not isinstance(full_clip, (VideoFileClip, CompositeVideoClip, ImageClip, ColorClip)):
            raise Exception('The "full_clip" parameter is not a VideoFileClip nor a CompositeVideoClip nor a ImageClip nor a ColorClip.')
        
        self._full_clip = full_clip

    @property
    def full_filename(self):
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
        return self._full_filename

    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        if not self._do_use_setter:
            self._full_filename = full_filename
        else:
            if full_filename is not None and full_filename != '':
                if not full_filename:
                    raise Exception('No "full_filename" provided.')
                
                if not isinstance(full_filename, str):
                    raise Exception('The "full_filename" parameter provided is not a string.')
                
                if not file_exists(full_filename):
                    raise Exception('The "full_filename" parameter provided is not a file, it does not exist.')

                if not file_is_video_file(full_filename):
                    raise Exception('The "full_filename" parameter provided is not a valid video file.')
            else:
                full_filename = ''
            
            self._full_filename = full_filename
            if self._do_update_database:
                self._database_handler.set_project_segment_full_filename(self.project_id, self.segment_index, self.full_filename)
                print_completed('Full filename stored in database.')
            
            if self.full_filename == '':
                self.full_clip = None
            else:
                self.full_clip = VideoFileClip(self.full_filename)
                print_completed('Full clip loaded in memory.')

    @property
    def _do_use_setter(self):
        """
        Internal variable to know if we should use the custom property setters
        or just assign the value directly.

        _This parameter is not manually set by the user._
        """
        return self.__do_use_setter
    
    @_do_use_setter.setter
    def _do_use_setter(self, do_use_setter: bool):
        if not isinstance(do_use_setter, bool):
            raise Exception('The "do_use_setter" parameter is not a bool.')
        
        self.__do_use_setter = do_use_setter

    @property
    def _do_update_database(self):
        """
        Internal variable to know if we should persist the change in the database
        or just assign the value.

        _This parameter is not manually set by the user._
        """
        return self.__do_update_database
    
    @_do_update_database.setter
    def _do_update_database(self, do_update_database: bool):
        if not isinstance(do_update_database, bool):
            raise Exception('The "do_update_database" parameter is not a bool.')
        
        self.__do_update_database = do_update_database
    

    """
            [  F U N C T I O N A L I T Y  ]
    """
    def __create_segment_file(self, filename: str):
        """
        Creates a filename within the definitive segments folder
        to keep the generated file locally to recover it in the
        next project execution if something goes wrong. The 
        definitive filename will be built using the provided
        'filename' and adding some more information in the name.

        This method will generate a temporary filename that uses
        the current segment index in its name and is placed in 
        segment parts folder.

        This method returns the final filename created.
        """
        if not filename:
            raise Exception('No "filename" provided.')

        temp_filename = get_temp_filename(filename)

        return f'{DEFAULT_SEGMENT_PARTS_FOLDER}/segment_{self.segment_index}_{temp_filename}'
    
    def __handle_narration(self):
        """
        This method processes the narration if needed. This means that
        the audio will be generated based on the custom narration
        filename provided, or by a auto-generated ai voice narration
        with the 'text' and 'voice' provided.

        This method will return None if no narration is needed due to
        the segment parameters, or the moviepy 'audio_clip' once it
        has been generated.
        """
        if not self.__needs_narration_and_transcription():
            return None
        
        if not self.audio_clip:
            if self.audio_narration_filename:
                segment_part_filename = self.__create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
                copy_file(self.audio_narration_filename, segment_part_filename)
                print_completed('Original voice narration file copied to segment parts folder')
                # TODO: I think we should update this field in database
                self.audio_narration_filename = segment_part_filename
                self.audio_filename = segment_part_filename
            # TODO: This 'voice' has to change to a more complex engine 
            # parameter that allows choosing the engine and the voice
            elif self.text_sanitized_without_shortcodes and self.voice:
                # TODO: Use segment file
                segment_part_filename = self.__create_segment_file('narration.wav')
                self.audio_filename = create_ai_narration(self.text_sanitized_without_shortcodes, output_filename = segment_part_filename)
                print_completed('Voice narration created successfully')
                
            print_completed('Voice narration updated in database')
                
        return self.audio_clip

    def __handle_transcription(self):
        """
        This method will check if the segment needs a transcription and
        if that transcription has been done previously or not. If it is
        needed and has not been done yet, it will be generated. It will
        make a '__handle_narration()' method call inside.

        This method will return the transcription (that is generated here
        if needed), or None if not (if needed and not done yet, it will 
        be done right now). It will also raise an exception if something
        goes wrong when generating the transcription.
        """
        if not self.__handle_narration():
            return None

        if not self.transcription: 
            print_in_progress('Generating audio transcription')
            initial_prompt = None
            if self.text_sanitized_without_shortcodes and len(self.text_sanitized_without_shortcodes) > 0:
                initial_prompt = self.text_sanitized_without_shortcodes

            transcription = get_transcription_with_timestamps(self.audio_filename, initial_prompt = initial_prompt)

            # We join all words together as we don't need segments, just words with time
            words = []
            for transcription_segment in transcription['segments']:
                words += transcription_segment['words']
            self.transcription = words
            print_completed('Transcription obtained')

        return self.transcription
    
    def __process_audio(self):
        """
        Processes the basic audio part by generating the audio narration
        and transcription if needed, 
        """
        self.__handle_transcription()

        if self.audio_clip and not self.calculated_duration:
            # TODO: This cannot happen, remove in a near future
            self.calculated_duration = self.audio_clip.duration
        elif not self.audio_clip and self.duration:
            # No audio but fixed 'duration' so build a silence of that duration
            self.calculated_duration = self.duration
            segment_part_filename = self.__create_segment_file('silence.wav')
            # This 'self.audio_clip' could be not assigned so it is set by the
            # 'self.audio_filename' setter
            self.audio_clip = SoundGenerator().create_silence_audio(self.calculated_duration, segment_part_filename)
            self.audio_filename = segment_part_filename
            print_completed('Created audio silence of expected duration and updated in database')
        else:
            # TODO: Maybe remove this 'else' because it is just explaining (?)
            # Specific segments like youtube_video, meme, premade, that doesn't
            # have a basic audio, they have their own audio when built/downloaded
            pass

    def __process_video(self):
        """
        Processes the basic video part by generating the video clip needed
        for the segment type and its parameters.
        """
        if not self.video_clip:
            self.video_clip = self._builder.build_segment(self)
            # We write this video part to be able to recover it in the future
            segment_part_filename = self.__create_segment_file('video.mp4')
            self.video_clip.write_videofile(segment_part_filename)
            self.video_filename = segment_part_filename
            print_completed('Created basic video part and stored locally and in database.')

        return self.video_clip
    
    def __process_full_part(self):
        """
        Processes the basic video and audio parts together by adding 
        the basic generated audio to the also basic generated video.
        """
        if not self.full_clip:
            if not self.audio_clip:
                self.full_clip = self.video_clip
            else:
                self.full_clip = self.video_clip.with_audio(self.audio_clip)

            segment_part_filename = self.__create_segment_file('full.mp4')
            self.full_clip.write_videofile(segment_part_filename)
            self.full_filename = segment_part_filename
            print_completed('Joined basic video and audio parts and stored locally and in database.')

        return self.full_clip
    
    def __process_base_video(self):
        """
        This method processes the basic audio and video part and puts it
        together to build the base video that we will enhance later with
        shortcodes, effects, compositions, etc.
        """
        self.__process_audio()
        self.__process_video()
        self.__process_full_part()

    def build(self, do_force: bool = False):
        if do_force:
            # TODO: Reset parameters and build it again
            pass

        print_in_progress(f'Starting to build the segment [{str(self.segment_index)}]')
        self.status = SegmentStatus.IN_PROGRESS

        # We handle basic parts and put them together
        self.__process_base_video()

        # Ok, now we have the basic. Lets enhance it by processing the
        # enhancement elements in the correct order
        self.__process_enhancements()

        # TODO: Continue enhancing it
        self.status = SegmentStatus.FINISHED
        print_completed(f'Segment [{str(self.segment_index)}] built successfully!')
            
    def __process_enhancements(self):
        # TODO: We need to handle our guidelines to make the enhancements
        # we need to do in the current video. Maybe stickers on camera
        # when some term appears, maybe some effect, I don't know
        # TODO: Process the enhancement dictionaries of the segment
        
        #       P R O C E S S
        # [1] Detect shortcodes in text
        # This is done when the Segment is instantiated
        # [2] Add our own shortcodes from our edition manual terms book
        # TODO: Read guideline 
        test_edition_manual = 'C:/Users/dania/Desktop/PROYECTOS/youtube-autonomous/youtube_autonomous/segments/enhancement/edition_manual/example.json'
        edition_manual = read_json_from_file(test_edition_manual)
        terms = edition_manual['terms']
        for term in terms:
            term_obj = EditionManualTerm()
            #term_obj = EnhancementElement.get_class_from_type()

        # TODO: Do it
        pass

        # Here we could have 'shortcodes' detected previously in
        # the 'text' parameter

        if self.json_effects:
            # There are effects provided by the user
            pass

    # def buildx(self):
    #     """
    #     Builds the segment files and returns the 'full_clip'.
    #     """
    #     print_in_progress('Lets build it...')
    #     if self.type == 'meme':
    #         self.video_clip = self.__get_videoclip()
    #         self.full_clip = self.video_clip
    #     else:
    #         # TODO: I should handle manually written shortcodes and preserve them to add into
    #         # the transcription_text, but by now I'm just ignoring and removing them
    #         manual_shortcodes = handle_shortcodes(self.text)
    #         self.shortcodes = manual_shortcodes

    #         self.text = manual_shortcodes['text_without_shortcodes']
    #         db_project = get_project_by_id(self.project_id)

    #         # Look for audio narration filename if previously created
    #         if 'audio_filename' in db_project['segments'][self.segment_index] and self.__has_narration():
    #             print_in_progress('Audio previously created and found in database. Reading it')
    #             self.audio_filename = db_project['segments'][self.segment_index]['audio_filename']
    #             self.audio_clip = AudioFileClip(self.audio_filename)
    #             self.calculated_duration = self.audio_clip.duration
    #         else:
    #             print_in_progress('Generating audioclip as it has been not found in database')
    #             self.audio_clip = self.__get_audioclip()
    #             set_project_segment_audio_filename(self.project_id, self.segment_index, self.audio_filename)
            
    #         # Look for narration if previously handled
    #         if 'transcription' in db_project['segments'][self.segment_index] and self.__has_narration():
    #             print_in_progress('Transcription previously created and found in database. Reading it')
    #             self.transcription = db_project['segments'][self.segment_index]['transcription']
    #         else:
    #             print_in_progress('Generating transcription as it has been not found in database')
    #             self.transcription = self.__get_transcription()
    #             set_project_segment_transcription(self.project_id, self.segment_index, self.transcription)

    #         self.transcription_text = ''
    #         if self.transcription:
    #             for word in self.transcription:
    #                 self.transcription_text += word['text'] + ' '
    #             self.transcription_text = self.transcription_text.strip()
    #             # TODO: Maybe I should store this as 'self.transcription_text_with_shortcodes'
    #             # and handle the shortcodes from there, and also store it in database
    #             self.transcription_text = self.__insert_automated_shortcodes()

    #         shortcodes = handle_shortcodes(self.transcription_text)
    #         self.shortcodes = shortcodes['shortcodes_found']

    #         print(self.transcription_text)

    #         self.video_clip = self.__get_videoclip()
    #         # TODO: Do I really need the video clip? I have full_clip
    #         #from utils.mongo_utils import set_project_segment_video_filename
    #         #set_project_segment_video_filename(self.project_id, self.segment_index, self.transcription)
    #         self.full_clip = self.__get_fullclip()

    #         print('full clip duration pre everything')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration pre everything')
    #         print(self.full_clip.audio.duration)

    #         # Then, with full_clip built, is time to process later elements

    #         # We could have some shortcodes that need to be processed and added
    #         self.effects += self.__extract_from_shortcodes(EnhancementType.EFFECT)
    #         self.full_clip = self.__apply_effects()

    #         print('full clip duration post effects')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post effects')
    #         print(self.full_clip.audio.duration)

    #         self.green_screens = self.__extract_from_shortcodes(EnhancementType.GREEN_SCREEN)
    #         self.full_clip = self.__apply_green_screens()

    #         print('full clip duration post green screens')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post green screens')
    #         print(self.full_clip.audio.duration)

    #         self.images = self.__extract_from_shortcodes(EnhancementType.IMAGE)
    #         self.full_clip = self.__apply_images()

    #         print('full clip duration post images')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post images')
    #         print(self.full_clip.audio.duration)

    #         self.stickers = self.__extract_from_shortcodes(EnhancementType.STICKER)
    #         self.full_clip = self.__apply_stickers()

    #         print('full clip duration post stickers')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post stickers')
    #         print(self.full_clip.audio.duration)

    #         self.sounds = self.__extract_from_shortcodes(EnhancementType.SOUND)
    #         self.full_clip = self.__apply_sounds()

    #         print('full clip duration post sounds')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post sounds')
    #         print(self.full_clip.audio.duration)

    #         self.memes = self.__extract_from_shortcodes(EnhancementType.MEME)
    #         self.full_clip = self.__apply_memes()
            
    #         # I apply memes at the end because they enlarge the video duration

    #         print('full clip duration post memes')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post memes')
    #         print(self.full_clip.audio.duration)

    #         #self.premades = self.__extract_premades_from_shortcodes()
    #         #self.full_clip = self.__apply_premades()
            
    #         # I apply premades at the end because they enlarge the video duration

    #         print('full clip duration post premades')
    #         print(self.full_clip.duration)
    #         print('full clip audio duration post premades')
    #         print(self.full_clip.audio.duration)

    #         self.full_clip = self.__fix_audio_glitch()

    #     # By now I only write the full clip and update it in database
    #     tmp_segment_full_filename = create_segment_filename('segment' + str(self.segment_index) + '.mp4')
    #     print('Audio file clip duration:')
    #     print(self.audio_clip.duration)
    #     print('Video file clip duration:')
    #     print(self.video_clip.duration)
    #     print('Full clip duration:')
    #     print(self.full_clip.duration)
    #     print('Full clip audio duration:')
    #     print(self.full_clip.audio.duration)
    #     self.full_clip.write_videofile(tmp_segment_full_filename)
    #     set_project_segment_full_filename(self.project_id, self.segment_index, tmp_segment_full_filename)
    #     set_project_segment_as_finished(self.project_id, self.segment_index)

    #     return self.full_clip

    # def __get_shortcodes(self):
    #     """
    #     This method processes the received text looking for shortcodes, stores them
    #     and also cleans the text removing those shortcodes.

    #     This method returns the shortcodes.
    #     """
    #     if not self.shortcodes and self.__has_narration():
    #         if self.transcription:
    #             print_in_progress('Processing shortcodes (on transcription)')

    #             shortcodes = handle_shortcodes(self.transcription_text)
    #             #self.text = shortcodes['text_without_shortcodes']
    #             self.transcription_text = shortcodes['text_without_shortcodes']
    #             self.shortcodes = shortcodes['shortcodes_found']
    #             print_completed('Shortcodes processed = ' + str(len(self.shortcodes)) + '. Text cleaned')

    #     return self.shortcodes

    
    # def __get_videoclip(self):
    #     if not self.video_clip:
    #         # TODO: Create video according to type
    #         print_in_progress('Creating "' + self.type + '" video clip')
    #         if self.type == 'ia_image':
    #             self.video_clip = self.builder.build_ai_image_content_clip_from_segment(self)
    #         elif self.type == 'image':
    #             self.video_clip = self.builder.build_image_content_clip_from_segment(self)
    #         elif self.type == 'youtube_video':
    #             self.video_clip = self.builder.build_youtube_video_content_clip_from_segment(self)
    #         elif self.type == 'text':
    #             self.video_clip = self.builder.build_text_video_content_clip_from_segment(self)
    #         elif self.type == 'my_stock':
    #             self.video_clip = self.builder.build_my_stock_video_content_clip_from_segment(self)
    #         elif self.type == 'stock':
    #             self.video_clip = self.builder.build_stock_video_content_clip_from_segment(self)

    #         # Other types to create
    #         elif self.type == 'meme':
    #             # This can be None
    #             self.video_clip = self.builder.build_meme_content_clip_from_segment(self)

    #         # Custom easy premades below
    #         elif self.type == 'google_search':
    #             self.video_clip = self.builder.build_premade_google_search_from_segment(self)
    #         elif self.type == 'youtube_search':
    #             self.video_clip = self.builder.build_premade_youtube_search_from_segment(self)
    #         print_completed('Video content built successfully')

    #     # I force fps to 60fps because of some problems I found. We are working with those
    #     # 60fps everywhere, to also improve 'manim' animations, so force it
    #     self.video_clip = self.video_clip.with_fps(60)

    #     return self.video_clip

    # def __apply_effects(self):
    #     """
    #     Applies the effects that we have to the full_clip that has been previously
    #     generated according to what the script said.

    #     We have main effects (written in 'effects' section in the script) and also
    #     shortcode effects that have been processed. The ones from the 'effects' 
    #     section are processed first, as are the "main" effects, and the ones from
    #     shortcodes are processed later.

    #     This method should be called after whole full_clip has been generated. As
    #     a reminder, the effects that we handle to this day, they should not modify
    #     the final clip duration as they are only aesthetic.
    #     """
    #     if self.effects:
    #         print_in_progress('Applying ' + str(len(self.effects)) + ' effects')
    #         self.full_clip = apply_effects(self.full_clip, self.effects)
    #         print_completed('All effects applied correctly')

    #     return self.full_clip
    
    # def __apply_memes(self):
    #     if len(self.memes) > 0:
    #         index = 0
    #         while index < len(self.memes):
    #             meme = self.memes[index]
    #             video_filename = meme.download()
    #             if not video_filename:
    #                 # Remove any meme that was not found, we will ignore it
    #                 print_error('Meme "' + meme.keywords + '" not found, ignoring it')
    #                 del self.memes[index]
    #             else:
    #                 index += 1

    #     # Add all found green screens to our 'self.full_clip'
    #     if len(self.memes) > 0:
    #         print_in_progress('Applying ' + str(len(self.memes)) + ' memes')
    #         # Meme start is updated in 'apply_meme' method if 'inline' memes added
    #         self.full_clip = apply_memes(self.full_clip, self.memes)
    #         print_completed('All memes applied correctly')

    #     return self.full_clip

    # def __apply_sounds(self):
    #     """
    #     This method will try to get the requested sounds (as shortcodes) from
    #     our sounds Youtube account and, if existing, download them and add the
    #     sound to the audioclip.
    #     """
    #     # 1. Process, download and ignore unavailable sounds
    #     if len(self.sounds) > 0:
    #         index = 0
    #         while index < len(self.sounds):
    #             sound: segments.building.objects.sound.Sound = self.sounds[index]
    #             audio_filename = sound.download()
    #             if not audio_filename:
    #                 # Remove any sound that was not found, we will ignore it
    #                 print_error('Sound "' + sound.keywords + '" not found, ignoring it')
    #                 del self.sounds[index]
    #             else:
    #                 index += 1

    #     # Add all found sounds to our 'self.audio_clip'
    #     if len(self.sounds) > 0:
    #         self.full_clip = self.full_clip.with_audio(apply_sounds(self.full_clip.audio, self.sounds))

    #     return self.full_clip
    
    # def __apply_stickers(self):
    #     if len(self.stickers) > 0:
    #         index = 0
    #         while index < len(self.stickers):
    #             sticker: segments.building.objects.sticker.Sticker = self.stickers[index]
    #             print('( ( ( ) ) )  Downloading sticker "' + sticker.keywords + '"')
    #             video_filename = sticker.download()
    #             if not video_filename:
    #                 # Remove any sticker that was not found, we will ignore it
    #                 print_error('Sticker "' + sticker.keywords + '" not found, ignoring it')
    #                 del self.stickers[index]
    #             else:
    #                 index += 1

    #     # Add all found stickers to our 'self.full_clip'
    #     if len(self.stickers) > 0:
    #         print_in_progress('Applying ' + str(len(self.stickers)) + ' stickers')
    #         self.full_clip = apply_stickers(self.full_clip, self.stickers)
    #         print_completed('All stickers applied correctly')

    #     return self.full_clip

    # def __apply_images(self):
    #     if len(self.images) > 0:
    #         index = 0
    #         while index < len(self.images):
    #             image: segments.building.objects.image.Image = self.images[index]
    #             video_filename = image.download()
    #             if not video_filename:
    #                 # Remove any image that was not found, we will ignore it
    #                 print_error('Image "' + image.keywords + '" not found, ignoring it')
    #                 del self.images[index]
    #             else:
    #                 index += 1

    #     # Add all found images to our 'self.full_clip'
    #     if len(self.images) > 0:
    #         print_in_progress('Applying ' + str(len(self.images)) + ' images')
    #         self.full_clip = apply_images(self.full_clip, self.images)
    #         print_completed('All images applied correctly')

    #     return self.full_clip
    
    # def __apply_green_screens(self):
    #     if len(self.green_screens) > 0:
    #         index = 0
    #         while index < len(self.green_screens):
    #             green_screen: segments.building.objects.green_screen.GreenScreen = self.green_screens[index]
    #             video_filename = green_screen.download()
    #             if not video_filename:
    #                 # Remove any sound that was not found, we will ignore it
    #                 print_error('Green screen "' + green_screen.keywords + '" not found, ignoring it')
    #                 del self.green_screens[index]
    #             else:
    #                 index += 1

    #     # Add all found green screens to our 'self.full_clip'
    #     if len(self.green_screens) > 0:
    #         print_in_progress('Applying ' + str(len(self.green_screens)) + ' green screens')
    #         self.full_clip = apply_green_screens(self.full_clip, self.green_screens)
    #         print_completed('All green screens applied correctly')

    #     return self.full_clip
    
    # def __fix_audio_glitch(self):
    #     """
    #     This method was built to try to fix the audio glitch that always come back when
    #     using moviepy. I'm trying to remove the last audio "frames" to avoid that 
    #     glitch. This is not nice, but I need to do something with that...

    #     I'm detecting the silences in the audio to ensure that the end has a silence, so
    #     I can remove a part of the end without removing important audio part.
    #     """
    #     audio = self.full_clip.audio
    #     # from yta_multimedia.sound.silences import detect_silences_in_audio_file
    #     # silences = detect_silences(self.audio_filename)
    #     # if len(silences) > 0 and (silences[len(silences) - 1][1] + 0.2) > self.audio_clip.duration:
    #     #     # If silence at the end of the audio, remove a little to avoid glitches
    #     #     FRAMES = 5    # 5 frames is for my testing narrate, don't calibrated for external
    #     #     audio = audio.with_subclip(0, self.audio_clip.duration - ((1 / 60) * FRAMES))
    #     audio = audio.with_subclip(0, -0.12)

    #     self.full_clip = self.full_clip.with_audio(audio)

    #     return self.full_clip
    
    # def __get_fullclip(self):
    #     if not self.full_clip and self.audio_clip and self.video_clip:
    #         self.full_clip = self.video_clip.with_audio(self.audio_clip)

    #     return self.full_clip
    
    # def write_fullclip(self, output_filename):
    #     """
    #     Writes the segment fullclip to t he 'output_filename'.
    #     """
    #     if self.full_clip:
    #         print_in_progress('Writing full clip as "' + output_filename + '"')
    #         self.full_clip.write_videofile(output_filename)
    #         self.full_filename = output_filename
    #         print_completed('Output file wrote successfully')

    #     return output_filename


    """
            [   M I D - T I M E     P R O C E S S I N G ]
    """
    # def __extract_effects_from_shortcodes(self):
    #     """
    #     Detects our shortcodes, that should have been loaded previously, and extracts
    #     the 'effect' shortcodes (if existing), checking if valid and adding to our
    #     effects list to be (later) processed as well as script-written effects.
    #     """
    #     # We could have shortcodes that are effects. We will process those shortcodes
    #     # and add them to our effects list.

    #     # We only accept effect shortcodes if there is a transcription that we
    #     # need to adjust shortcodes timing
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 try:
    #                     keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                     meme = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
    #                     print_in_progress('Adding "' + meme.keywords + '" meme')
    #                     self.memes.append(meme)
    #                 except Exception as e:
    #                     print(e)
    #                     print_error('Failed instantiating meme ' + keywords)
    #                     continue

    #     return self.effects
    
    # def __parse_enhancement_type_fields(self, shortcode):
    #     """
    #     This method is only for internal use and has been created to allow
    #     reusing this method of segment enhancement object fields extraction.
    #     """
    #     word_index = int(shortcode['previous_word_index'])
    #     word = self.transcription[word_index]

    #     print(shortcode)

    #     keywords = shortcode[EnhancementField.KEYWORDS.value]
    #     start = shortcode[EnhancementField.START.value]
    #     duration = shortcode[EnhancementField.DURATION.value]
    #     origin = shortcode[EnhancementField.ORIGIN.value]
    #     mode = shortcode[EnhancementField.MODE.value]

    #     # start
    #     if start == Start.START_OF_CURRENT_WORD.value:
    #         start = word['start']
    #     elif start == Start.END_OF_CURRENT_WORD.value:
    #         # The end of the segment but also start at 'end'? Not good
    #         # TODO: Special case
    #         start = word['end']
    #     elif start == Start.BEFORE_NEXT_WORD.value:
    #         if (word_index + 1) < len(self.transcription):
    #             # Between the word and the next one, in the silence gap in between
    #             start = (self.transcription[word_index + 1]['end'] + self.transcription[word_index + 1]['start']) / 2
    #         else:
    #             # The end of the segment but also start at 'end'? Not good
    #             # TODO: Special case
    #             if mode == Mode.INLINE.value:
    #                 start = self.full_clip.duration
    #             else:
    #                 start = word['end']

    #     # duration
    #     if duration == Duration.END_OF_CURRENT_WORD.value:
    #         duration = word['end'] - start
    #     elif duration == Duration.FILE_DURATION.value:
    #         if mode == Mode.INLINE.value:
    #             duration = Constants.FILE_DURATION.value
    #         else:
    #             # This is the maximum as it will be overlayed
    #             duration = self.full_clip.duration - start
    #     elif duration.startswith(Duration.END_OF_SUBSEQUENT_WORD.value):
    #         aux = duration.split('_')
    #         subsequent_word_index = int(aux[len(aux) - 1])

    #         if (word_index + subsequent_word_index) < (len(self.transcription) - 1):
    #             duration = self.transcription[word_index + subsequent_word_index]['end'] - start
    #         else:
    #             # TODO: Special case
    #             # Asking for the end of the segment, so lets use the segment end
    #             duration = self.full_clip.duration - start
    #     else:
    #         # By now, only float value
    #         duration = float(duration)

    #     # Special cases:
    #     # - End of segment
    #     # if word_index == len(self.transcription) - 1
    #     #   if inline => 

    #     return keywords, start, duration, mode, origin

    # def __extract_memes_from_shortcodes(self):
    #     # We only accept these shortcodes if there is the text is narrated
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # green screen shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == 'meme':
    #                     # Options:
    #                     #   Inline meme with no duration
    #                     #   Inline meme with duration as end_of_word:X (non-sense, I think)
    #                     #   Inline meme with duration as 3
    #                     #   Inline meme with duration as video_duration
    #                     #
    #                     #   Overlay meme with no duration
    #                     #   Overlay meme with duration as end_of_word:X
    #                     #   Overlay meme with duration as 3
    #                     #   Overlay meme with duration as video_duration (non-sense, I think)
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         meme = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
    #                         print_in_progress('Adding "' + meme.keywords + '" meme')
    #                         self.memes.append(meme)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating meme ' + keywords)
    #                         continue
                    
    #     return self.memes
    
    # def __extract_stickers_from_shortcodes(self):
    #     # We only accept these shortcodes if there is the text is narrated
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # green screen shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == 'sticker':
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         sticker = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
    #                         print_in_progress('Adding "' + sticker.keywords + '" sticker')
    #                         self.stickers.append(sticker)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating sticker ' + keywords)
    #                         continue
                    
    #     return self.stickers
    
    # def __extract_images_from_shortcodes(self):
    #     # We only accept these shortcodes if there is the text is narrated
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # green screen shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == 'image':
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         sticker = segments.building.objects.image.Image(keywords, start, duration, origin, mode)
    #                         print_in_progress('Adding "' + sticker.keywords + '" sticker')
    #                         self.stickers.append(sticker)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating image ' + keywords)
    #                         continue
                    
    #     return self.images

    # def __extract_green_screens_from_shortcodes(self):
    #     # We only accept these shortcodes if there is the text is narrated
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # green screen shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == 'green_meme':
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         sticker = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
    #                         print_in_progress('Adding "' + sticker.keywords + '" sticker')
    #                         self.stickers.append(sticker)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating sticker ' + keywords)
    #                         continue
                    
    #     return self.green_screens
    
    # def __extract_from_shortcodes(self, type: EnhancementType):
    #     objects = []
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # sound shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == type.value:
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         # TODO: Do this dynamically calling object
    #                         if type == EnhancementType.GREEN_SCREEN:
    #                             object = segments.building.objects.green_screen.GreenScreen(keywords, start, duration, origin, mode)
    #                         elif type == EnhancementType.MEME:
    #                             object = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
    #                         elif type == EnhancementType.SOUND:
    #                             object = segments.building.objects.sound.Sound(keywords, start, duration, origin, mode)
    #                         elif type == EnhancementType.IMAGE:
    #                             object = segments.building.objects.image.Image(keywords, start, duration, origin, mode)
    #                         elif type == EnhancementType.STICKER:
    #                             object = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
    #                         elif type == EnhancementType.EFFECT:
    #                             object = segments.building.objects.effect.Effect(keywords, start, duration, origin, mode, {})

    #                         print_in_progress('Adding "' + object.keywords + '" ' + type.value + '"')
    #                         objects.append(object)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating ' + type.value + ' ' + keywords)
    #                         continue

    #     return objects
    
    # def __extract_sounds_from_shortcodes(self):
    #     # We only accept these shortcodes if there is the text is narrated
    #     if self.transcription:
    #         if self.shortcodes and (len(self.shortcodes) > 0):
    #             for shortcode in self.shortcodes:
    #                 # Any shortcode has 'shortcode' and 'previous_word_index'
    #                 # sound shortcode also should have 'keywords' and 'duration'
    #                 if shortcode['shortcode'] == 'sound':
    #                     try:
    #                         keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
    #                         sound = segments.building.objects.sound.Sound(keywords, start, duration, origin, mode)
    #                         print_in_progress('Adding "' + sound.keywords + '" sound')
    #                         self.sounds.append(sound)
    #                     except Exception as e:
    #                         print(e)
    #                         print_error('Failed instantiating sound ' + keywords)
    #                         continue

    #     return self.sounds

    """
            [   M I N O R     C H E C K S  ]
    """
    def __needs_narration_and_transcription(self):
        """
        This method returns True if this segment needs to implement
        an audio narration (and transcription) according to its 
        parameters. This will be done when a custom narration file 
        has been provided or when an audio narration is generated by
        the 'text' and 'voice' parameters provided.
        """
        return self.audio_narration_filename or (self.text_sanitized_without_shortcodes and self.voice)

    """
            [   O T H E R S   ]
    """

    # def __insert_automated_shortcodes(self):
    #     """
    #     Appends the automated shortcodes (banning, enhancement, etc.) to the transcripted
    #     text to enhanced the video.
    #     """
    #     from utils.narration_script.enhancer import get_shortcodes_by_word_index

    #     # 1. Apply enhancement words (including censorship)
    #     shortcodes_by_word_index = get_shortcodes_by_word_index(self.transcription)
    #     print(self.transcription_text)
    #     text_as_words = self.transcription_text.split(' ')
    #     for key in shortcodes_by_word_index:
    #         text_as_words[int(key)] += ' ' + shortcodes_by_word_index[key]
    #     self.transcription_text = ' '.join(text_as_words)
    #     print(self.transcription_text)

    #     # 2. Check double or triple (or more) consecutive blank spaces and remove again
    #     print_in_progress('Fixing excesive blank spaces')
    #     self.transcription_text = self.__fix_excesive_blank_spaces(self.transcription_text)
    #     print_completed('Excesive blank spaces fixed')

    #     print(self.transcription_text)

    #     return self.transcription_text

    # def __check_script_text(self):
    #     """
    #     Checks if the existing text is well written (shortcodes can be processed well),
    #     applies a censorship sound to banned words and enhaces words to enhance  with 
    #     some specific strategies (if active).
    #     """
    #     if self.__has_narration():
    #         # 1. Check double or triple (or more) consecutive blank spaces and remove
    #         print_in_progress('Fixing excesive blank spaces')
    #         self.text = self.__fix_excesive_blank_spaces(self.text)
    #         print_completed('Excesive blank spaces fixed')

    #         """
    #         # No shortcodes available in text by now

    #         # 2. Check shortcodes are processable
    #         print_in_progress('Fixing shortcodes')
    #         self.text = self.__fix_text_shortcodes()
    #         print_completed('Shortcodes fixed')

    #         # 3. Censor bad words (with censorship sound)
    #         if DO_BAN_WORDS:
    #             print_in_progress('Processing banned words')
    #             self.text = self.__process_banned_words()
    #             print_completed('Banned words processed')

    #         # 4. Enhance content by adding shortcodes next to words in our dictionary
    #         if DO_ENHANCE_WORDS:
    #             print_in_progress('Processing enhanced words')
    #             self.text = self.__process_enhanced_words()
    #             print_completed('Enhanced words processed')

    #         # 5. Check double or triple (or more) consecutive blank spaces and remove again
    #         print_in_progress('Fixing excesive blank spaces')
    #         self.text = self.__fix_excesive_blank_spaces()
    #         print_completed('Excesive blank spaces fixed')

    #         print('@@ == >   Text that will be processed...')
    #         print(self.text)
    #         """

    #     return self.text
        
    # # TODO: Import this from 'yta-general-utils' when available
    # def __fix_excesive_blank_spaces(self, text):
    #     """
    #     Removed blank spaces longer than 1 from the provided 'text' and returns it clean.
    #     """
    #     # TODO: Ok, why am I using not the 'repl' param in re.search?
    #     # I'm applying it in the new method below, please check if
    #     # valid to avoid the while, thank you
    #     filtered = re.search('[ ]{2,}', text)
    #     while filtered:
    #         index_to_replace = filtered.end() - 1
    #         s = list(text)
    #         s[index_to_replace] = ''
    #         text = ''.join(s)
    #         filtered = re.search('[ ]{2,}', text)

    #     return text
    
    # # TODO: Import this from 'yta-general-utils' when available
    # def __fix_unseparated_periods(self, text):
    #     """
    #     This methods fixes the provided 'text' by applying a space
    #     after any period without it.
    #     """
    #     # Thank you: https://stackoverflow.com/a/70394076
    #     return re.sub(r'\.(?!(?<=\d\.)\d) ?', '. ', text)

    # def __fix_text_shortcodes(self):
    #     """
    #     Checks the segment text and fixes the shortcodes that won't be processable.
    #     This means those shortcodes that end with ']x' when 'x' is not a blank
    #     space.
    #     """
    #     if self.text:
    #         filtered = re.search('][^ ]', self.text)
    #         while filtered:
    #             index_to_replace = filtered.end() - 1
    #             s = list(self.text)
    #             s[index_to_replace] = '' # I will delete that 'no white space char', sorry
    #             self.text = ''.join(s)
    #             filtered = re.search('][^ ]', self.text)

    #     return self.text

    # def __check_and_format_effects(self, json):
    #     """
    #     This method checks if the provided effects are valid and also transform those
    #     json effects into 'Effect' objects that are stored in self.effects to process
    #     them better lately.

    #     This method is for the effects that comes in the script, not as shortcodes. 
    #     The ones in shortcodes will be processed later.
    #     """
    #     self.effects = []
    #     if 'effects' in json and (len(json['effects']) > 0):
    #         object_effects = []
    #         for effect in json['effects']:
    #             print_in_progress('Adding "' + effect['effect'] + '" effect')
    #             # TODO: Implement 'sound' parameter
    #             #object_effects.append(segments.building.objects.effect.Effect(effect['effect'], effect.get('start'), effect.get('end'), effect.get('sound', True), effect.get('parameters', {})))
    #             # TODO: Careful with 'start' and 'end'
    #             from segments.building.objects.enums import Origin, Mode
    #             object_effects.append(segments.building.objects.effect.Effect(effect['effect'], effect.get('start'), effect.get('end'), Origin.DEFAULT.value, Mode.DEFAULT.value, effect.get('parameters', {})))

    #         self.effects = object_effects

    #     return self.effects