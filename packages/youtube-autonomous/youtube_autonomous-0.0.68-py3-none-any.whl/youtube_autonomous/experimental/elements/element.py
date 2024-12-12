from youtube_autonomous.experimental.elements.element_data import ElementData
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from yta_multimedia.audio.voice.transcription.stt.whisper import get_transcription_with_timestamps
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.logger import print_completed
from moviepy import AudioFileClip, VideoFileClip
from typing import Union


class Element:
    _audio_clip = None
    _video_clip = None
    _full_clip = None

    @property
    def type(self):
        return self.data.type

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index: int):
        self._index = index

    @property
    def status(self):
        return self.data.status
    
    @status.setter
    def status(self, status: str):
        self.data.status = status

    @property
    def audio_filename(self):
        audio_filename = self.data.audio_filename

        if audio_filename and not self.audio_clip:
            self.audio_clip = AudioFileClip(audio_filename)

        return audio_filename
    
    @audio_filename.setter
    def audio_filename(self, audio_filename: Union[str, None]):
        self.data.audio_filename = audio_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.data.audio_filename:
            self.audio_clip = AudioFileClip(self.data.audio_filename)

    @property
    def audio_clip(self):
        return self._audio_clip
    
    @audio_clip.setter
    def audio_clip(self, audio_clip):
        self._audio_clip = audio_clip

    @property
    def video_filename(self):
        video_filename = self.data.video_filename

        if video_filename and not self.video_clip:
            self._video_clip = VideoFileClip(video_filename)

        return video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        self.data.video_filename = video_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.data.video_filename:
            self.video_clip = VideoFileClip(self.data.video_filename)

    @property
    def video_clip(self):
        return self._video_clip
    
    @video_clip.setter
    def video_clip(self, video_clip):
        self._video_clip = video_clip

    @property
    def full_filename(self):
        full_filename = self.data.full_filename

        if full_filename and not self.full_clip:
            self.full_clip = VideoFileClip(full_filename)

        return full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        self.data.full_filename = full_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.data.full_filename:
            self.full_clip = VideoFileClip(self.data.full_filename)

    @property
    def full_clip(self):
        return self._full_clip
    
    @full_clip.setter
    def full_clip(self, full_clip):
        self._full_clip = full_clip

    @property
    def audio_narration_filename(self):
        return self.data.audio_narration_filename
    
    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        self.data.audio_narration_filename = audio_narration_filename

    @property
    def transcription(self):
        return self.data.transcription
    
    @transcription.setter
    def transcription(self, transcription: Union[dict, None]):
        self.data.transcription = transcription

    @property
    def shortcodes(self):
        return self.data.shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: Union[list['Shortcode'], None]):
        self.data.shortcodes = shortcodes

    @property
    def calculated_duration(self):
        return self.data.calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[float, int, None]):
        self.data.calculated_duration = calculated_duration

    @property
    def text(self):
        return self.data.text
    
    @property
    def duration(self):
        return self.data.duration

    @duration.setter
    def duration(self, duration):
        self.data.duration = duration

    @property
    def filename(self):
        return self.data.filename
    
    @property
    def url(self):
        return self.data.url
    
    @property
    def voice(self):
        return self.data.voice
    
    @property
    def narration_text(self):
        return self.data.narration_text
    
    @property
    def narration_text_sanitized_without_shortcodes(self):
        return self.data.narration_text_sanitized_without_shortcodes
    
    @narration_text_sanitized_without_shortcodes.setter
    def narration_text_sanitized_without_shortcodes(self, narration_text_sanitized_without_shortcodes: str):
        self.data.narration_text_sanitized_without_shortcodes = narration_text_sanitized_without_shortcodes

    @property
    def narration_text_with_simplified_shortcodes(self):
        return self.data.narration_text_with_simplified_shortcodes
    
    @narration_text_with_simplified_shortcodes.setter
    def narration_text_with_simplified_shortcodes(self, narration_text_with_simplified_shortcodes: str):
        self.data.narration_text_with_simplified_shortcodes = narration_text_with_simplified_shortcodes

    @property
    def narration_text_sanitized(self):
        return self.data.narration_text_sanitized
    
    @narration_text_sanitized.setter
    def narration_text_sanitized(self, narration_text_sanitized: str):
        self.data.narration_text_sanitized = narration_text_sanitized
    
    def __init__(self, index: int, data: dict):
        self.index = index
        self.data = ElementData(data)
        self.rules = ElementRules.get_subclass_by_type(data['type'])()
        self.builder = ElementBuilder.get_subclass_by_type(data['type'])()
        self.rules_checker = RulesChecker(self.rules)

        self.database_handler = DatabaseHandler()
        # TODO: Set shortcode tags please (read Notion)
        self.shortcode_parser = ShortcodeParser([])

    def create_segment_file(self, filename: str):
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

        return f'{DEFAULT_SEGMENT_PARTS_FOLDER}/segment_{self.index}_{temp_filename}'
    
    def validate(self):
        """
        Validates that the main data of the Element is correctly
        set, all required fields are provided, there are no
        unexpected shortcodes and more stuff.

        This method will raise an Exception if something is wrong.
        """
        # TODO: Move this to a external validator (?)
        # If 'text' have shortcodes
        self.shortcode_parser.parse(self.text)

        # If 'narration_text' have invalid shortcodes
        self.shortcode_parser.parse(self.narration_text)

        # If element has not necessary parameters
        self.rules_checker.check_this_need_rules(self.data)

    def create_narration(self):
        """
        Creates the audio narration (if needed) by generating an AI audio
        narration with provided 'voice' and 'audio_narration_text'
        parameters or by using the 'audio_narration_filename'.

        This method will set the 'audio_filename' to be able to build the
        audio clip in a near future.
        """
        if self.audio_narration_filename:
            segment_part_filename = self.create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
            copy_file(self.audio_narration_filename, segment_part_filename)
            print_completed('Original voice narration file copied to segment parts folder')
            self.audio_narration_filename = segment_part_filename
            self.audio_filename = segment_part_filename
        else:
            segment_part_filename = self.create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            self.audio_filename = self.builder.build_narration(self.narration_text_sanitized_without_shortcodes, output_filename = segment_part_filename)
            print_completed('Voice narration created successfully')

    def create_transcription(self):
        """
        Creates the transcription of the generated audio narration
        that would be stored in 'self.audio_filename'.
        
        This method returns a words array containing, for each word,
        a 'text', 'start' and 'end' field to be able to use the 
        transcription timestamps.
        """
        transcription = get_transcription_with_timestamps(self.audio_filename, initial_prompt = self.narration_text_sanitized_without_shortcodes)

        # We join all words together as we don't need segments, just words with time
        words = []
        for transcription_segment in transcription['segments']:
            words += transcription_segment['words']
        self.transcription = words