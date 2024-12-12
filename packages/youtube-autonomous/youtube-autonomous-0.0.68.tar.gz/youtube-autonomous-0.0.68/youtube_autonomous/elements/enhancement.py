from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.segments.enums import EnhancementType
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from yta_multimedia.audio.voice.transcription.stt.whisper import get_transcription_with_timestamps
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.logger import print_completed
from moviepy import AudioFileClip, VideoFileClip


class Enhancement:
    project_id: int
    segment_index: int
    segment = None
    index: int
    status = ''
    type = ''

    audio_filename: str = ''
    audio_clip = None
    video_filename: str = ''
    video_clip = None
    full_filename: str = ''
    full_clip = None

    audio_narration_filename: str
    voice: str
    narration_text: str

    text: str

    keywords: str

    start: float = None
    duration: float = None

    filename: str
    url: str

    mode: str

    music: str

    enhancements: list

    extra_params: dict

    narration_text_sanitized_without_shortcodes: str = ''
    narration_text_with_simplified_shortcodes: str = ''
    narration_text_sanitized: str = ''
    transcription = None
    shortcodes = None
    created_at = None

    def set_audio_filename(self, audio_filename: str):
        self.audio_filename = audio_filename

        if audio_filename:
            self.audio_clip = AudioFileClip(self.audio_filename)
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, 'audio_filename', self.audio_filename)

    def set_video_filename(self, video_filename: str):
        self.video_filename = video_filename

        if video_filename:
            self.video_clip = VideoFileClip(self.video_filename)
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index,  'video_filename', self.video_filename)

    def set_full_filename(self, full_filename: str):
        self.full_filename = full_filename

        if full_filename:
            self.full_clip = VideoFileClip(self.full_filename)
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index,  'full_filename', self.full_filename)

    def set_as_finished(self):
        self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, 'status', 'finished')

    def __init__(self, project_id, segment_index: int, segment, index: int, data: dict):
        self.project_id = str(project_id)
        self.segment_index = segment_index
        self.segment = segment
        self.index = index

        print(f'Enhancement __init__ with index ({index})')

        for key in data:
            setattr(self, key, data[key])

        # I parse shortcodes here because not coming from the 'youtube_autonomous'
        # TODO: Set shortcode tags please (read Notion)
        self.shortcode_parser = ShortcodeParser([])
        if self.narration_text:
            self.shortcode_parser.parse(self.narration_text)
            self.narration_text_sanitized_without_shortcodes = self.shortcode_parser.text_sanitized_without_shortcodes
            self.narration_text_with_simplified_shortcodes = self.shortcode_parser.text_sanitized_with_simplified_shortcodes
            self.narration_text_sanitized = self.shortcode_parser.text_sanitized
            self.shortcodes = self.shortcode_parser.shortcodes

        self.rules = ElementRules.get_subclass_by_type(data['type'])()
        self.builder = ElementBuilder.get_subclass_by_type(data['type'])()
        self.rules_checker = RulesChecker(self.rules)

        self.database_handler = DatabaseHandler()

    # TODO: This below has been moved because inheritance is working strangely

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
            self.set_audio_filename(segment_part_filename)
        else:
            segment_part_filename = self.create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            self.set_audio_filename(self.builder.build_narration(self.narration_text_sanitized_without_shortcodes, output_filename = segment_part_filename))
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

    # TODO: This above has been moved because inheritance is working strangely

    # TODO: This below has to be in the common Object from wich Segment
    # and Enhancement will inherit
    def build_step_1_create_narration(self):
        # 1. Generate narration if needed
        self.create_narration()

    def build_step_2_create_transcription(self):
        # 2. Generate narration transcription
        self.create_transcription()

    def build_step_2_extract_user_shortcodes(self):
        # 2. Extract manually written shortcodes in 'narration_text'
        self.shortcode_parser.parse(self.narration_text)
        self.shortcodes = self.shortcode_parser.shortcodes
        # TODO: Turn shortcodes into enhancements
        enhancements = [shortcode.to_enhancement_element(self.transcription) for shortcode in self.shortcodes]
        print(enhancements)

    def build_step_3_apply_edition_manual_shortcodes(self):
        # 3. Apply shortcodes from Edition Manual and 'narration_text'
        # TODO: By now I'm not applying it
        #self.apply_edition_manual()
        pass

    def build_step_4_build_base_content(self):
        # 2. Build base video
        if not self.video_clip:
            print(self.segment)
            self.video_clip = self.builder.build_from_enhancement(self)
            filename = self.create_segment_file('video.mp4')
            self.video_clip.write_videofile(filename)
            self.set_video_filename(filename)

        # TODO: In the future we could add enhancements to this
        if self.audio_clip:
            self.video_clip = self.video_clip.with_audio(self.audio_clip)
        self.full_clip = self.video_clip
        filename = self.create_segment_file('video.mp4')
        self.full_clip.write_videofile(filename)
        self.set_full_filename(filename)
    
    def build(self):
        """
        Builds this enhancement to be applied in the provided 'segment'.
        """
        if self.type in [EnhancementType.GREENSCREEN.value, EnhancementType.EFFECT.value]:
            self.full_clip = self.builder.build_from_enhancement(self)
        else:
            if self.rules_checker.should_build_narration_rule(self):
                if not self.audio_filename:
                    self.build_step_1_create_narration()

                # We are forcing duration here
                self.duration = self.audio_clip.duration

                if not self.transcription:
                    self.build_step_2_create_transcription()

                # TODO: Handle this (maybe status (?))
                self.build_step_2_extract_user_shortcodes()

                self.build_step_3_apply_edition_manual_shortcodes()

            # TODO: What about duration here that is not set (?)
            if self.audio_clip:
                self.duration = self.audio_clip.duration

            if not self.video_clip:
                print('Building base content step 4')
                self.build_step_4_build_base_content()

            # Make the base video to apply enhancements on it
            if self.audio_clip:
                self.video_clip = self.video_clip.with_audio(self.audio_clip)

            #self.build_step_5_update_enhancements_duration()
            # TODO: By now I'm omitting this part
            #self.build_step_6_build_and_apply_enhancements()

            # TODO: Build the final video
            self.full_clip = self.video_clip
            filename = self.create_segment_file('definitivo.mp4')
            self.full_clip.write_videofile(filename)
            self.set_full_filename(filename)

            self.set_as_finished()

        return self.full_clip