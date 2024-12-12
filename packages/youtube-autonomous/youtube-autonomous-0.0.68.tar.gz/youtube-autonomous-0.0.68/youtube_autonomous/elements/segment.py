from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.enums import StringDuration
from youtube_autonomous.segments.enhancement.edition_manual.edition_manual import EditionManual
from youtube_autonomous.elements.enhancement import Enhancement
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from youtube_autonomous.segments.enums import EnhancementMode, EnhancementType
from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
from yta_multimedia.audio.voice.transcription.stt.whisper import get_transcription_with_timestamps
from yta_multimedia.audio.sound.generation.sound_generator import SoundGenerator
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.logger import print_completed, print_in_progress
from moviepy import AudioFileClip, VideoFileClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip


class Segment:
    project_id: int
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

    duration: float = None

    filename: str
    url: str

    music: str

    enhancements: list

    extra_params: dict

    narration_text_sanitized_without_shortcodes: str
    narration_text_with_simplified_shortcodes: str
    narration_text_sanitized: str
    transcription = None
    shortcodes = None
    created_at = None

    def set_audio_filename(self, audio_filename: str):
        self.audio_filename = audio_filename

        if audio_filename:
            self.audio_clip = AudioFileClip(self.audio_filename)
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'audio_filename', self.audio_filename)

    def set_video_filename(self, video_filename: str):
        self.video_filename = video_filename

        if video_filename:
            self.video_clip = VideoFileClip(self.video_filename)
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'video_filename', self.video_filename)

    def set_full_filename(self, full_filename: str):
        self.full_filename = full_filename

        if full_filename:
            self.full_clip = VideoFileClip(self.full_filename)
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'full_filename', self.full_filename)

    def set_transcription(self, transcription):
        self.transcription = transcription

        if transcription:
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'transcription', transcription)

    def set_shortcodes(self, shortcodes):
        self.shortcodes = shortcodes

        if shortcodes:
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'shortcodes', shortcodes)

    def set_as_finished(self):
        self.database_handler.update_project_segment_status(self.project_id, self.index, 'finished')

    def __init__(self, project_id, index: int, data: dict):
        self.project_id = project_id
        self.index = index

        for key in data:
            setattr(self, key, data[key])

        if self.audio_filename:
            self.audio_clip = AudioFileClip(self.audio_filename)
        if self.video_filename:
            self.video_clip = VideoFileClip(self.video_filename)
        if self.full_filename:
            self.full_clip = VideoFileClip(self.full_filename)

        self.rules = ElementRules.get_subclass_by_type(data['type'])()
        self.builder = ElementBuilder.get_subclass_by_type(data['type'])()
        self.rules_checker = RulesChecker(self.rules)

        self.database_handler = DatabaseHandler()
        # TODO: Set shortcode tags please (read Notion)
        self.shortcode_parser = ShortcodeParser([])

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
        self.set_transcription(words)

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
        # TODO: I'm doing nothing with these enhancements
        # TODO: Maybe store in database (?)
        enhancements = [shortcode.to_enhancement_element(self.transcription) for shortcode in self.shortcodes]

    def build_step_3_apply_edition_manual_shortcodes(self):
        # 3. Apply shortcodes from Edition Manual and 'narration_text'
        # TODO: Maybe store in database (?)
        self.apply_edition_manual()

    def build_step_4_build_base_content(self):
        # 4. Build base video
        self.video_clip = self.builder.build_from_segment(self)
        filename = self.create_segment_file('video.mp4')
        self.video_clip.write_videofile(filename)
        self.set_video_filename(filename)

    def build_step_5_update_enhancements_duration(self):
        for index, enhancement in enumerate(self.enhancements):
            if isinstance(enhancement, dict):
                self.enhancements[index] = Enhancement(self.project_id, self.index, self, index + 100, enhancement)
        # TODO: Convert dict enhancements to enhancement objects
        # 5. Update enhancements duration according to base video
        # TODO: What if 'start' is after the end of the base video (?)
        for index, enhancement in enumerate(self.enhancements):
            # With this condition we avoid the None enhancements that are 
            # generated due to the gap between the start indexes and the
            # ones we generate with +100 because of edition manual
            if enhancement is None:
                continue

            if enhancement.duration == StringDuration.SEGMENT_DURATION.name:
                enhancement.duration = self.video_clip.duration

            if enhancement.start >= self.video_clip.duration:
                raise Exception('The enhancement start moment is after the video_clip.duration')
            
            end = enhancement.start + enhancement.duration
            if end > self.video_clip.duration:
                enhancement.duration = self.video_clip.duration - enhancement.start

            if enhancement.mode == EnhancementMode.INLINE.value:
                # If inline and start is after this moment, increase its
                # start as we are enlarging the video when applying this
                # inline enhancement
                for i in range(index + 1, len(self.enhancements)):
                    if self.enhancements[i] is None:
                        continue
                    
                    if self.enhancements[i].start >= enhancement.start:
                        self.enhancements[i].start += enhancement.duration
            
    def build_step_6_build_and_apply_enhancements(self):
        """
        Builds the different Enhancements according to their
        type and parameters and applies them into the main
        video.
        """
        # I obtain them sorted to start from the first one to apply them
        for enhancement in sorted(self.enhancements, key = lambda enhancement: enhancement.start):
            if enhancement is None:
                # TODO: This should not exist if I don't have 100 None segments
                # because of my +100 index identifying strategy
                continue

            enhancement_clip = enhancement.build()
            # TODO: Combine with our segment according to type

            end = enhancement.start + enhancement.duration
            if enhancement.mode == EnhancementMode.INLINE.value:
                if enhancement.type in [EnhancementType.EFFECT.value, EnhancementType.EFFECT]:
                    parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'video', 'duration']
                    parameters_not_from_extra = ['duration']
                    parameters = EffectElementBuilder.get_building_parameters(enhancement, parameters_to_ignore, parameters_not_from_extra)

                    enhancement_clip = enhancement_clip.apply(self.video_clip.with_subclip(enhancement.start, end), **parameters)

                if enhancement.start > 0:
                    self.video_clip = concatenate_videoclips([
                        self.video_clip.with_subclip(0, enhancement.start),
                        enhancement_clip,
                        self.video_clip.with_subclip(enhancement.start, self.video_clip.duration)
                    ])
                elif enhancement.start == 0:
                    self.video_clip = concatenate_videoclips([
                        enhancement_clip,
                        self.video_clip
                    ])
                # TODO: What about start == clip.duration (?)
            elif enhancement.mode == EnhancementMode.OVERLAY.value:
                compound_clip = CompositeVideoClip([
                    self.video_clip.with_subclip(enhancement.start, end),
                    enhancement_clip
                ])

                if enhancement.start == 0 and enhancement.duration == self.video_clip.duration:
                    # TODO: Improve this
                    self.video_clip = compound_clip
                elif enhancement.start == 0:
                    self.video_clip = concatenate_videoclips([
                        compound_clip,
                        self.video_clip.with_subclip(end, self.video_clip.duration)
                    ])
                elif end == self.video_clip.duration:
                    self.video_clip = concatenate_videoclips([
                        self.video_clip.with_subclip(0, enhancement.start),
                        compound_clip
                    ])
                else:
                    self.video_clip = concatenate_videoclips([
                        self.video_clip.with_subclip(0, enhancement.start),
                        compound_clip,
                        self.video_clip.with_subclip(end, self.video_clip.duration)
                    ])
                # TODO: Could happen that duration is longer than self.video_clip.duration (?)
            elif enhancement.mode == EnhancementMode.REPLACE.value:
                # I first build the special ones
                if enhancement.type in [EnhancementType.EFFECT.value, EnhancementType.EFFECT]:
                    parameters_to_ignore = ['self', 'cls', 'args', 'kwargs', 'video', 'duration']
                    parameters_not_from_extra = ['duration']
                    parameters = EffectElementBuilder.get_building_parameters(enhancement, parameters_to_ignore, parameters_not_from_extra)

                    enhancement_clip = enhancement_clip.apply(self.video_clip.with_subclip(enhancement.start, end), **parameters)
                elif enhancement.type in [EnhancementType.GREENSCREEN.value, EnhancementType.GREENSCREEN]:
                    # TODO: Send parameters (I don't know how actually)
                    enhancement_clip = enhancement_clip.from_video_to_video(self.video_clip.with_subclip(enhancement.start, end))

                # Then just push the clip when needed
                if enhancement.start == 0 and enhancement.duration == self.video_clip.duration:
                    self.video_clip = enhancement_clip
                elif enhancement.start == 0:
                    self.video_clip = concatenate_videoclips([
                        enhancement_clip,
                        self.video_clip.with_subclip(end, self.video_clip.duration)
                    ])
                elif enhancement.duration == self.video_clip.duration:
                    self.video_clip = concatenate_videoclips([
                        self.video_clip.with_subclip(0, enhancement.start),
                        enhancement_clip
                    ])
                else:
                    self.video_clip = concatenate_videoclips([
                        self.video_clip.with_subclip(0, enhancement.start),
                        enhancement_clip,
                        self.video_clip.with_subclip(end, self.video_clip.duration)
                    ])

    def build(self):
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
            print_in_progress('Building base content step 4')
            self.build_step_4_build_base_content()
            print_completed('Base content built in step 4')

        # This would be the real duration that could be not the
        # one in the database as this is in real time and it is
        # not updated in the database
        self.duration = self.video_clip.duration

        # Make the base video to apply enhancements on it
        if self.audio_clip:
            # If we have another audio clip we should want to put
            # them togeter, not to replace it
            audio = self.audio_clip
            if self.video_clip.audio:
                # We have another audio, we need to put them together
                audio = CompositeAudioClip([
                    self.video_clip.audio,
                    audio
                ])
                
            # TODO: Should we replace self.audio_clip (?)
            self.video_clip = self.video_clip.with_audio(audio)
        elif not self.video_clip.audio:
            # Premade and other type of video_clip can have audio
            # by themselves, but another type of videos cannot, so
            # we need to put silence audio to have an audio track
            # or we will have issues when concatenating with ffmpeg
            # only in those without audio
            self.video_clip = self.video_clip.with_audio(SoundGenerator().create_silence_audio(self.video_clip.duration))

        self.build_step_5_update_enhancements_duration()
        # TODO: By now I'm omitting this part
        self.build_step_6_build_and_apply_enhancements()

        # TODO: Build the final video
        self.full_clip = self.video_clip
        filename = self.create_segment_file('definitivo.mp4')
        self.full_clip.write_videofile(filename)
        self.set_full_filename(filename)

        self.set_as_finished()


    def apply_edition_manual(self):
        # TODO: I need to dynamically get the edition manual from somewhere
        # By now I'm forcing it
        test_edition_manual = 'C:/Users/dania/Desktop/PROYECTOS/youtube-autonomous/youtube_autonomous/segments/enhancement/edition_manual/example.json'
        edition_manual = EditionManual.init_from_file(test_edition_manual)
        dict_enhancements_found = edition_manual.apply(self.transcription)
        # Turn dict enhancements found into Enhancement objects
        for index, dict_enhancement_found in enumerate(dict_enhancements_found):
            # TODO: What do we do with 'index' here (?)
            index = 100 + index
            self.enhancements.append(Enhancement(self.project_id, self.index, self, index, dict_enhancement_found))
        # TODO: Some enhancements could be incompatible due to collisions
        # or things like that

        # TODO: What about this enhancements (?)
