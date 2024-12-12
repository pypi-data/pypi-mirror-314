from youtube_autonomous.segments.enums import EnhancementField, SegmentBuildingField, EnhancementOrigin
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode
from youtube_autonomous.experimental.elements.element import Element
from yta_general_utils.logger import print_completed
from bson.objectid import ObjectId
from typing import Union


class Enhancement(Element):
    @property
    def segment_index(self):
        return self._segment_index
    
    @segment_index.setter
    def segment_index(self, segment_index: int):
        self._segment_index = segment_index

    @property
    def origin(self):
        return self._origin
    
    @origin.setter
    def origin(self, origin: EnhancementOrigin):
        self._origin = origin

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, 'origin', origin)
        # TODO: This should be stored in database

    @property
    def status(self):
        return super().status
    
    @status.setter
    def status(self, status: str):
        super().status = status

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, 'status', status)

    @property
    def audio_filename(self):
        return super().audio_filename
    
    @audio_filename.setter
    def audio_filename(self, audio_filename: Union[str, None]):
        audio_filename = audio_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.AUDIO_FILENAME.value, audio_filename)

    @property
    def video_filename(self):
        return super().video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        super().video_filename = video_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.VIDEO_FILENAME.value, video_filename)

    @property
    def full_filename(self):
        return super().full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        super().full_filename = full_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.FULL_FILENAME.value, full_filename)

    @property
    def audio_narration_filename(self):
        return super().audio_narration_filename
    
    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        super().audio_narration_filename = audio_narration_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, EnhancementField.AUDIO_NARRATION_FILENAME.value, audio_narration_filename)

    @property
    def transcription(self):
        return super().transcription
    
    @transcription.setter
    def transcription(self, transcription: Union[dict, None]):
        super().transcription = transcription

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.TRANSCRIPTION.value, transcription)

    @property
    def shortcodes(self):
        return super().shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: Union[list[Shortcode], None]):
        super().shortcodes = shortcodes

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.SHORTCODES.value, shortcodes)

    @property
    def start(self):
        return self.data.start
    
    @start.setter
    def start(self, start):
        self.data.start = start

    @property
    def calculated_duration(self):
        return super().calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[float, int, None]):
        super().calculated_duration = calculated_duration

        if self._do_update_database:
            self.database_handler.update_project_segment_enhancement_field(self.project_id, self.segment_index, self.index, SegmentBuildingField.CALCULATED_DURATION.value, calculated_duration)

    def __init__(self, project_id: Union[str, ObjectId], segment_index: int, index: int, data: dict):
        super().__init__(index, data)

        self._do_update_database = False

        self.project_id = str(project_id)
        self.segment_index = segment_index
        
        # By now, we are not accepting shortcodes nor other
        # enhancements in enhancement elements

        self._do_update_database = True

    # TODO: Remove this method below
    def prepare(self):
        # Check duration
        if self.data.duration and not self.calculated_duration:
            self.calculated_duration = self.data.duration

        # Generate narration audio
        if self.rules_checker.should_build_narration_rule(self.data) and not self.audio_clip:
            self.handle_narration()

        # Generate video
        if not self.video_clip:
            self.video_clip = self.builder.build_segment(self)
            # We write this video part to be able to recover it in the future
            segment_part_filename = self.create_segment_file('video.mp4')
            self.video_clip.write_videofile(segment_part_filename)
            self.video_filename = segment_part_filename
            print_completed('Created basic video part and stored locally and in database.')

    # TODO: This below has to be in the common Object from wich Segment
    # and Enhancement will inherit
    def build_step_1_create_narration(self):
        # 1. Generate narration if needed
        self.create_narration()

    def build_step_2_build_base_content(self, segment):
        # 2. Build base video
        if not self.video_clip:
            self.video_clip = self.builder.build_from_segment(self)
            filename = self.create_segment_file('video.mov')
            self.video_clip.write_videofile(filename)
            self.video_filename = filename

        # TODO: In the future we could add enhancements to this
        if self.audio_clip:
            self.video_clip = self.video_clip.with_audio(self.audio_clip)
        self.full_clip = self.video_clip
        filename = self.create_segment_file('video.mov')
        self.full_clip.write_videofile(filename)
        self.full_filename = filename
    
    def build(self, segment):
        """
        Builds this enhancement to be applied in the provided 'segment'.
        """
        self.build_step_1_create_narration()
        self.build_step_2_build_base_content(segment)

        return self.full_clip