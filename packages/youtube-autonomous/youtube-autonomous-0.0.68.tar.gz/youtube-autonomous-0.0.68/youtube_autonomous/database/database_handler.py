from youtube_autonomous.segments.enums import SegmentStatus, SegmentBuildingField, ProjectStatus, ProjectField, SegmentField, ProjectBuildingField
from youtube_autonomous.elements.validator.element_parameter_validator import ParameterValidator
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
from typing import Union


class DatabaseHandler:
    """
    This class is used to interact with the database in which the
    projects are stored and its information and status is handled.

    The projects are stored in the database containing the mongo
    '_id'', a 'status', the 'script' (that is the whole json used
    to generate it and to compare other json files to check if
    existing), and the 'segments' field that is the one the app
    uses to handle the building data and this process.

    The 'script' must be preserved as it is, to be able to compare
    jsons and avoid duplicated projects, and the 'segments' field
    must be used by the app to keep the building process progress.
    """
    DATABASE_NAME = 'youtube_autonomous'
    CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false/' + DATABASE_NAME  # previous: youtubeautonomo
    client = None

    def __init__(self):
        # Initialize database connection
        # TODO: I think this should be a Singleton
        self.get_database()

    def get_database(self):
        """
        Returns the client connected to the database.
        """
        if not self.client:
            self.client = MongoClient(self.CONNECTION_STRING)

        return self.client[self.DATABASE_NAME]
    
    def get_database_projects_table(self):
        """
        Returns the database 'projects' table
        """
        return self.get_database()['projects']
    
    def get_unfinished_project(self):
        """
        Returns the first unfinished project existing in database,
        or None if there are no unfinished projects.

        TODO: Is it actually the first or the last one (?)
        """
        db_projects_table = self.get_database_projects_table()

        db_unfinished_projects = db_projects_table.find({
            "status": { "$ne": ProjectStatus.FINISHED.value }
        })

        try:
            return db_unfinished_projects.next()
        except:
            return None
    
    def get_unfinished_projects(self):
        """
        Returns the unfinished projects that exist in the
        database or an empty array if there are no unfinished
        projects.
        """
        db_projects_table = self.get_database_projects_table()

        db_unfinished_projects = db_projects_table.find({
            "status": { "$ne": ProjectStatus.FINISHED.value }
        })

        # Build a projects array
        # TODO: Improve this, please
        projects = []
        do_finish = False
        while not do_finish:
            try:
                projects.append(db_unfinished_projects.next())
            except:
                do_finish = True
                pass

        return projects
    
    # TODO: Apply 'json' type
    def get_database_project_from_json(self, json):
        """
        Returns the project with the provided 'json' that is stored
        in the database if it actually exists. The 'json' is the 
        whole script that builds the video segments.
        """
        db_projects = self.get_database_projects_table()

        db_project = db_projects.find({
            'script': json
        })

        # TODO: Improve this if possible
        try:
            return db_project.next()
        except:
            return None
        
    # TODO: Apply the 'id' type
    def get_database_project_from_id(self, db_project_id: Union[ObjectId, str]):
        """
        Returns the project with the given 'id' if available, or None
        if not.
        """
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        db_projects = self.get_database_projects_table()

        db_project = db_projects.find({
            '_id': db_project_id
        })

        # TODO: Improve this if possible
        try:
            return db_project.next()
        except:
            return None
        
    def insert_project(self, data: dict):
        """
        Creates a new project with the provided 'data' structure
        that is made of 'status', 'script' and 'segments' fields.

        The 'data' provided here is always valid so I don't check 
        it.
        """
        # TODO: Make some checkings (?)
        db_projects_table = self.get_database_projects_table()
        db_project_id = db_projects_table.insert_one(data).inserted_id
        
        return self.get_database_project_from_id(db_project_id)
    
    def update_project_segment_field(self, db_project_id: Union[ObjectId, str], segment_index: int, field: Union[SegmentField, SegmentBuildingField, str], value):
        """
        Updates a segment field from the provided project (identified by 
        'project_id').
        """
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')

        if segment_index < 0:
            raise Exception('In valid "segment_index" provided')

        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        if not field:
            raise Exception('No "field" provided.')
        
        if not isinstance(field, (SegmentField, SegmentBuildingField, str)):
            raise Exception('The "field" parameter is not a SegmentField nor a SegmentBuildingField nor a string.')
        
        # I let this 'field' to be not strict and accept any string
        if isinstance(field, (SegmentField, SegmentBuildingField)):
            field = field.value
        
        # TODO: Improve checkings
        query = { '_id': db_project_id }
        new_values = { "$set": { 'segments.' + str(segment_index) + '.' + field: value } }
        # TODO: Do you see this below more clear than the one above (?)
        #new_values = { "$set": { f'segments.{str(segment_index)}.{field: value}' } }

        db_projects_table = self.get_database_projects_table()
        db_projects_table.update_one(query, new_values)

    def update_project_segment_enhancement_field(self, db_project_id: Union[ObjectId, str], segment_index: int, enhancement_index: int, field: Union[SegmentField, str], value):
        ParameterValidator.validate_mandatory_parameter('db_project_id', db_project_id)
        ParameterValidator.validate_positive_number_mandatory_parameter('segment_index', segment_index)
        ParameterValidator.validate_positive_number_mandatory_parameter('enhancement_index', enhancement_index)
        # TODO: Only these field type enums (?)
        ParameterValidator.validate_is_class('field', field, ['SegmentField', 'SegmentBuildingField', 'str'])
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        if isinstance(field, (SegmentField, SegmentBuildingField)):
            field = field.value

        # TODO: Improve checkings
        query = { '_id': db_project_id }
        field_str = f'segments.{str(segment_index)}.enhancements.{str(enhancement_index)}.{field}'
        new_values = { "$set": {field_str: value} }

        db_projects_table = self.get_database_projects_table()
        db_projects_table.update_one(query, new_values)

    def update_project_segment_status(self, db_project_id: Union[ObjectId, str], segment_index: int, status: Union[SegmentStatus, str]):
        """
        Updates, in the project with the provided 'db_project_id'
        id, the segment in 'segment_index' index, setting the also
        provided 'status'.
        """
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        if not status:
            raise Exception('No "status" provided.')

        if not isinstance(status, (SegmentStatus, str)):
            raise Exception('The "status" parameter provided is not a SegmentStatus nor a string.')
        
        if isinstance(status, str):
            if not SegmentStatus.is_valid(status):
                raise Exception('The "status" provided is not a valid SegmentStatus value.')
            
            status = SegmentStatus(status)
        
        self.update_project_segment_field(db_project_id, segment_index, ProjectBuildingField.STATUS.value, status.value)

    def set_project_segment_as_in_progress(self, db_project_id: Union[ObjectId, str], segment_index: int):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_status(db_project_id, segment_index, SegmentStatus.IN_PROGRESS.value)

    def set_project_segment_as_finished(self, db_project_id: Union[ObjectId, str], segment_index: int):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_status(db_project_id, segment_index, SegmentStatus.FINISHED)
        
        # TODO: Maybe SegmentBuildingField.FINISHED_AT (?)
        self.update_project_segment_field(db_project_id, segment_index, 'finished_at', datetime.now())

    def set_project_segment_transcription(self, db_project_id: Union[ObjectId, str], segment_index: int, transcription):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_field(db_project_id, segment_index, SegmentBuildingField.TRANSCRIPTION.value, transcription)

    def set_project_segment_audio_filename(self, db_project_id: Union[ObjectId, str], segment_index: int, audio_filename):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_field(db_project_id, segment_index, SegmentBuildingField.AUDIO_FILENAME.value, audio_filename)

    def set_project_segment_video_filename(self, db_project_id: Union[ObjectId, str], segment_index: int, video_filename):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_field(db_project_id, segment_index, SegmentBuildingField.VIDEO_FILENAME.value, video_filename)

    def set_project_segment_full_filename(self, db_project_id: Union[ObjectId, str], segment_index: int, full_filename):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)
        
        if not segment_index and segment_index != 0:
            raise Exception('No "segment_index" provided.')
        
        self.update_project_segment_field(db_project_id, segment_index, SegmentBuildingField.FULL_FILENAME.value, full_filename)

    def update_project_field(self, db_project_id: Union[ObjectId, str], field: Union[ProjectField, ProjectBuildingField, str], value):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        if not field:
            raise Exception('No "field" provided.')
        
        if not isinstance(field, (ProjectField, ProjectBuildingField, str)):
            raise Exception('The "field" parameter provided is not a ProjectField nor a ProjectBuildingField nor a string.')
        
        if isinstance(field, (ProjectField, ProjectBuildingField)):
            field = field.value
        
        db_project = self.get_database_project_from_id(db_project_id)

        if not db_project:
            return None
        
        db_projects_table = self.get_database_projects_table()
        query = { '_id': db_project_id }
        new_values = { "$set": { field: value } }
        db_projects_table.update_one(query, new_values)

    def set_project_music_filename(self, db_project_id: Union[ObjectId, str], music_filename: str):
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        # TODO: Maybe SegmentBuildingField.MUSIC_FILENAME (?)
        self.update_project_field(db_project_id, 'music_filename', music_filename)

    def set_project_as_in_progress(self, db_project_id: Union[ObjectId, str]):
        """
        Sets the project (identified by 'db_project_id') status as 
        'in_progress'.
        """
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        self.update_project_field(db_project_id, ProjectBuildingField.STATUS, ProjectStatus.IN_PROGRESS.value)

    def set_project_as_finished(self, db_project_id: Union[ObjectId, str]):
        """
        Sets the project (identified by 'db_project_id') status as
        'finished'.
        """
        if not db_project_id:
            raise Exception('No "db_project_id" provided.')
        
        if isinstance(db_project_id, str):
            db_project_id = ObjectId(db_project_id)

        self.update_project_field(db_project_id, ProjectBuildingField.STATUS, ProjectStatus.FINISHED.value)
