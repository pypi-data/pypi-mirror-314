from youtube_autonomous.segments.enums import ProjectStatus, SegmentStatus, ProjectBuildingField
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.elements.segment import Segment
from youtube_autonomous.elements.validator.element_parameter_validator import ParameterValidator
from yta_multimedia.video.utils.ffmpeg_handler import FfmpegHandler
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.programming.parameter_validator import PythonValidator
from bson.objectid import ObjectId
from typing import Union


class Project:
    """
    Class that represents a whole video Project, containing different
    segments that are used to build consecutively to end being a whole
    video that is this project video.
    """
    _id: str = None
    """
    The stringified mongo ObjectId that identifies this project in the
    database.
    """
    _status: ProjectStatus = None
    """
    The current project status that allows us to know if this project
    has started or not, or even if it has been finished.
    """
    _segments: list[Segment] = None
    """
    The array that contains this project segments that are used to build
    the whole project video.
    """
    _do_update_database: bool = True
    """
    Internal variable to know if we should update the database value.

    _This parameter is not manually set by the user._
    """
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.

    _This parameter is not manually set by the user._
    """
    def __init__(self, id: Union[str, ObjectId]):
        self.id = id
        self._database_handler = DatabaseHandler()
        self.refresh()

    def refresh(self):
        """
        Refreshes the Project data reading from the database.
        """
        project_data = self._database_handler.get_database_project_from_id(self.id)

        if not project_data:
            raise Exception(f'There is no project in the database with the provided "{str(self.id)}" id.')

        self._do_update_database = False

        self.status = project_data['status']
        self.segments = [Segment(self.id, index, segment) for index, segment in enumerate(project_data['segments'])]

        self._do_update_database = True

    @property
    def unfinished_segments(self) -> list[Segment]:
        """
        Returns all this project segments that has not been built at
        all (they are unfinished).
        """
        return [segment for segment in self.segments if segment.status != SegmentStatus.FINISHED.value]
    
    @property
    def id(self):
        """
        The stringified mongo ObjectId that identifies this project in the
        database.
        """
        return self._id

    @id.setter
    def id(self, id: Union[ObjectId, str]):
        ParameterValidator.validate_mandatory_parameter('id', id)
        ParameterValidator.validate_is_class(id, ['str', 'ObjectId'])
        
        if PythonValidator.is_instance(id, ObjectId):
            id = str(id)

        self._id = id

    @property
    def status(self):
        """
        The current project status that allows us to know if this project
        has started or not, or even if it has been finished.
        """
        return self._status

    @status.setter
    def status(self, status: Union[ProjectStatus, str] = ProjectStatus.TO_START):
        """
        Updates the 'status' property and also updates it in the database.
        """
        status = ProjectStatus.to_enum(status)

        if status is not None:
            status = status.value

        self._status = status
        if self._do_update_database:
            self._database_handler.update_project_field(self.id, ProjectBuildingField.STATUS, status)

    @property
    def segments(self):
        """
        The array that contains this project segments that are used to build
        the whole project video.
        """
        return self._segments

    @segments.setter
    def segments(self, segments: list[Segment]):
        """
        Updates the 'segments' property with the provided 'segments' parameter.
        This method will check that any of the provided segments are Segment
        objects.
        """
        ParameterValidator.validate_mandatory_parameter('segments', segments)
        for segment in segments:
            ParameterValidator.validate_is_class('segment', segment, 'Segment')

        self._segments = segments

    @property
    def _database_handler(self):
        """
        Object to interact with the database and get and create projects.

        _This parameter is not manually set by the user._
        """
        return self.__database_handler
    
    @_database_handler.setter
    def _database_handler(self, database_handler: DatabaseHandler):
        ParameterValidator.validate_mandatory_parameter('database_handler', database_handler)
        ParameterValidator.validate_is_class('database_handler', database_handler, 'DatabaseHandler')
        
        self.__database_handler = database_handler
        
    def build(self, output_filename: str):
        """
        This method will make that all the segments contained in this
        project are built. It will build the unfinished ones and them
        concatenate them in a final video that is stored locally as
        'output_filename'.
        """
        # I make, by now, 'output_filename' mandatory for this purpose
        ParameterValidator.validate_mandatory_parameter('output_filename', output_filename)

        self.status = ProjectStatus.IN_PROGRESS

        for segment in self.unfinished_segments:
            segment.build()

        self.refresh()

        unfinished_segments_len = len(self.unfinished_segments)
        if unfinished_segments_len > 0:
            raise Exception(f'There are {str(unfinished_segments_len)} segments that have not been completely built (unfinished).')
        
        # I put them together in a whole project clip
        abspath = get_project_abspath()
        full_abspath_filenames = [f'{abspath}{segment.full_filename}' for segment in self.segments]
        output_abspath = output_filename
        FfmpegHandler.concatenate_videos(full_abspath_filenames, output_abspath)

        self.status = ProjectStatus.FINISHED