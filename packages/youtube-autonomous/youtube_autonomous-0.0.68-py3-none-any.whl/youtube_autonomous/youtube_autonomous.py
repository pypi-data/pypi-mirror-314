from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.experimental.segments.validation.segment_validator import SegmentValidator
from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTag
from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
from youtube_autonomous.shortcodes.enums import ShortcodeTagType
from youtube_autonomous.elements.validator.element_validator import ElementValidator
from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.project.project import Project
from youtube_autonomous.segments.enums import StringDuration, SegmentType, EnhancementType
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from youtube_autonomous.segments.enums import SegmentField, EnhancementField, ProjectStatus, SegmentStatus
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER, DEFAULT_PROJECTS_OUTPUT_FOLDER
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from yta_general_utils.temp import clean_temp_folder
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.path import create_file_abspath
from yta_general_utils.file.reader import FileReader
from yta_general_utils.logger import print_completed, print_in_progress, print_error
from datetime import datetime
from typing import Union

import copy


class YoutubeAutonomous:
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.

    _This parameter is not manually set by the user._
    """
    __segment_validator: SegmentValidator = None
    """
    Object to validate the segments we want to use to build a project.

    _This parameter is not manually set by the user._
    """
    __segments_abspath: Union[str, None] = None
    """
    The absolute path that points to the segments folder in which this
    software will store the segments related content parts that are
    created during the whole segment building process. This folder 
    allows us recovering a non-finished project in which we generated
    some segments in the past but not all of them.

    _This parameter is not manually set by the user._
    """
    __projects_output_abspath: Union[str, None] = None
    """
    The absolute path that points to the projects output folder in which
    this software will store the final videos generated.

    _This parameter is not manually set by the user._
    """

    def __init__(self):
        """
        Initializes the object and creates the segment part building
        folder in which segment parts will be stored.
        """
        self.__database_handler = DatabaseHandler()
        self.__segment_validator = SegmentValidator()

        self.__segments_abspath = get_project_abspath() + DEFAULT_SEGMENT_PARTS_FOLDER + '/'
        self.__projects_output_abspath = get_project_abspath() + DEFAULT_PROJECTS_OUTPUT_FOLDER + '/'

        # We force to create the folder if it doesn't exist
        create_file_abspath(self.__segments_abspath + 'toforce')
        create_file_abspath(self.__projects_output_abspath + 'toforce')

    def purge(self, do_remove_segments_files = False):
        """
        Cleans the temporary folder removing all previous generated 
        temporary files, and also the segment files if the
        'do_remove_segments_files' parameter is set to True.
        """
        clean_temp_folder()
        if do_remove_segments_files:
            # TODO: Remove all files in self.__segments_abspath folder
            pass

    def check_config(self):
        # TODO: Check that he config is ok
        pass
     
    def insert_project_in_database_from_file(self, filename: str):
        """
        Reads the provided project content 'filename' and creates a new 
        project in the database if the provided 'filename' contains a new
        project and is valid. If the information belongs to an already
        registered project, it will raise an exception.

        This method returns the new stored project mongo ObjectId if 
        successfully stored, or raises an Exception if anything went wrong.
        """
        ElementParameterValidator.validate_filename(filename, None)
        
        json_data = self.__read_project_from_file(filename)

        # If a project with the same content exists, it is the same project
        db_project = self.__database_handler.get_database_project_from_json(json_data)
        if db_project:
            raise Exception('There is an existing project in the database with the same content.')

        # Process the information to store it parsed
        json_data = self.validate_and_prepare_data_for_database(json_data)

        db_project = self.__database_handler.insert_project(json_data)

        print_completed('Project created in database with ObjectId = "' + str(db_project['_id']) + '"')

        return str(db_project['_id'])
    
    def validate_data(self, json_data: dict):
        segments = json_data.get('segments', [])

        if not segments:
            raise Exception('No "segments" in the provided "json_data" parameter.')

        # TODO: Check main structure and validate fields
        # TODO: This shortcode parser must have the definitive shortcodes
        # TODO: Shortcode handlers must be working, check Notion (https://www.notion.so/ShortcodeParser-personalizado-10ff5a32d462804d9253e9cb782e5540?pvs=4)
        # TODO: This shortcode parser must be instantiated once, and this is
        # being instantiated twice in this file
        shortcode_parser = ShortcodeParser([ShortcodeTag('meme', ShortcodeTagType.SIMPLE)])

        for index, segment in enumerate(segments):
            print_in_progress(f'Handling segment [{index}]')

            # Check all fields are set (no more, no less)
            ElementValidator.validate_segment_fields(segment)

            type = ElementParameterValidator.validate_segment_type(segment.get(SegmentField.TYPE.value, '')).value

            # Check if 'text' has any shortcode
            try:
                ShortcodeParser([]).parse(segment.get(SegmentField.TEXT.value, ''))
            except Exception:
                print_error(f'Field "{SegmentField.TEXT.value}" not found or shortcodes found on it.')
                exit()

            # Check if 'narration_text' has unaccepted shortcodes
            try:
                shortcode_parser.parse(segment.get(SegmentField.NARRATION_TEXT.value, ''))
            except Exception:
                print_error(f'Field "{SegmentField.NARRATION_TEXT.value}" not found or unregistered shortcodes found on it.')
                exit()

            # Check 'duration' is valid segment duration string or 
            # positive numeric value
            duration = ElementValidator.validate_segment_duration_field(segment.get(SegmentField.DURATION.value, None))

            # We can only accept 'FILE_DURATION' for some specific types
            ElementValidator.validate_segment_duration_field_for_type(duration, type)

            # TODO: Validate, if premade or effect, that 'extra_data' has
            # needed fields
            keywords = segment.get(SegmentField.KEYWORDS.value, None)
            if type == SegmentType.PREMADE.value:
                # We avoid 'duration' because we obtain it from main fields
                PremadeElementBuilder.extract_extra_params(segment, PremadeElementBuilder.premade_name_to_class(keywords).generate, ['self', 'cls', 'args', 'kwargs', 'duration'])
            elif type == SegmentType.TEXT.value:
                # We avoid 'text' and 'duration' because we obtain them from main fields
                TextElementBuilder.extract_extra_params(segment, TextElementBuilder.text_premade_name_to_class(keywords).generate, ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration', 'text'])
            # TODO: Validate for another types
            
            for index, enhancement in enumerate(segment.get(SegmentField.ENHANCEMENTS.value, [])):
                print_in_progress(f'   Handling enhancement [{index}]')

                # We let the user know if any unaccepted field has been given
                # and we raise and Exception if that happen
                ElementValidator.validate_enhancement_fields(enhancement)

                # Check enhancement type is allowed as enhancement
                enhancement_type = ElementParameterValidator.validate_enhancement_type(enhancement.get(EnhancementField.TYPE.value, '')).value
                
                # Check if 'text' has any shortcode
                try:
                    ShortcodeParser([]).parse(enhancement.get(EnhancementField.TEXT.value, ''))
                except Exception:
                    print_error(f'Field "{EnhancementField.TEXT.value}" not found or shortcodes found on it.')
                    exit()

                # Check if 'narration_text' has unaccepted shortcodes
                try:
                    shortcode_parser.parse(enhancement.get(EnhancementField.NARRATION_TEXT.value, ''))
                except Exception:
                    print_error(f'Field "{EnhancementField.NARRATION_TEXT.value}" not found or unregistered shortcodes found on it.')
                    exit()

                # Check 'duration' is valid enhanacement duration string or
                # positive numeric value
                duration = ElementValidator.validate_enhancement_duration_field(enhancement.get(EnhancementField.DURATION.value, None))
                mode = ElementValidator.validate_enhancement_mode_field(enhancement.get(EnhancementField.MODE.value, None)).value

                # We can only accept 'FILE_DURATION' for some specific types
                ElementValidator.validate_enhancement_duration_field_for_type(duration, enhancement_type)

                # We can only accept the mode if its type accepts it
                ElementValidator.validate_enhancement_mode_field_for_type(mode, enhancement_type)

                RulesChecker.check_need_rules(enhancement, ElementRules.get_subclass_by_type(enhancement_type)())
                # TODO: We should check any other thing that is here (frames, etc.)

                # TODO: Validate, if premade or effect, that 'extra_data' has
                # needed fields
                keywords = enhancement.get(EnhancementField.KEYWORDS.value, None)
                if enhancement_type == EnhancementType.PREMADE.value:
                    # We avoid 'duration' because we obtain it from main fields
                    PremadeElementBuilder.extract_extra_params(enhancement, PremadeElementBuilder.premade_name_to_class(keywords).generate, ['self', 'cls', 'args', 'kwargs', 'duration'])
                elif enhancement_type == EnhancementType.EFFECT.value:
                    EffectElementBuilder.extract_extra_params(enhancement, EffectElementBuilder.effect_name_to_class(keywords).apply, params_to_ignore = ['self', 'cls', 'args', 'kwargs', 'video'])
                elif enhancement_type == EnhancementType.TEXT.value:
                    # We avoid 'text' and 'duration' because we obtain them from main fields
                    TextElementBuilder.extract_extra_params(enhancement, TextElementBuilder.text_premade_name_to_class(keywords).generate, ['self', 'cls', 'args', 'kwargs', 'output_filename', 'duration', 'text'])
                # TODO: Validate for another types

            # 4. If doesn't have necessary fields for its type
            RulesChecker.check_need_rules(segment, ElementRules.get_subclass_by_type(type)())
    
    def prepare_data_for_database(self, json_data: dict):
        """
        This method prepares the project data that has been previously
        verified so it has the structure with it will be stored in the
        database.

        This method will parse the 'narration_text' and generate the
        some processed and sanitized fields (it processes the 
        shortcodes). It will also transform any string type duration
        to its actual numeric value that will be dynamically processed
        later when building the content.

        The result of this method will be a dict containing 'status',
        'script' and 'segments' fields.
        """
        # This is the structure the project must have in database
        data = {
            'status': ProjectStatus.TO_START.value,
            'script': copy.deepcopy(json_data),
            'segments': None
        }

        # TODO: This shortcode parser must be instantiated once, and this is
        # being instantiated twice in this file
        shortcode_parser = ShortcodeParser([ShortcodeTag('meme', ShortcodeTagType.SIMPLE)])
        segments = []
        for segment in json_data['segments']:
            # Manually handle 'narration_text'
            if segment.get(SegmentField.NARRATION_TEXT.value, ''):
                shortcode_parser.parse(segment[SegmentField.NARRATION_TEXT.value])
                segment['narration_text_sanitized_without_shortcodes'] = shortcode_parser.text_sanitized_without_shortcodes
                segment['narration_text_with_simplified_shortcodes'] = shortcode_parser.text_sanitized_with_simplified_shortcodes
                segment['narration_text_sanitized'] = shortcode_parser.text_sanitized

            # Manually handle string duration
            if segment.get(SegmentField.DURATION.value, None) and isinstance(segment[SegmentField.DURATION.value], str):
                segment[SegmentField.DURATION.value] = StringDuration.convert_duration(segment[SegmentField.DURATION.value])
                    
            segment['status'] = SegmentStatus.TO_START.value
            segment['created_at'] = datetime.now()

            for enhancement in segment.get(SegmentField.ENHANCEMENTS.value, []):
                # Manually handle 'narration_text'
                if enhancement.get(EnhancementField.NARRATION_TEXT.value, ''):
                    shortcode_parser.parse(enhancement[EnhancementField.NARRATION_TEXT.value])
                    enhancement['narration_text_sanitized_without_shortcodes'] = shortcode_parser.text_sanitized_without_shortcodes
                    enhancement['narration_text_with_simplified_shortcodes'] = shortcode_parser.text_sanitized_with_simplified_shortcodes
                    enhancement['narration_text_sanitized'] = shortcode_parser.text_sanitized

                # Manually handle string duration
                if enhancement.get('duration', None) and isinstance(enhancement['duration'], str):
                    enhancement['duration'] = StringDuration.convert_duration(enhancement['duration'])

                enhancement['status'] = SegmentStatus.TO_START.value
                enhancement['created_at'] = datetime.now()

            segments.append(segment)

        data['segments'] = segments

        return data

    def validate_and_prepare_data_for_database(self, json_data: dict):
        """
        This method will validate the 'json_data' provided and raise
        an Exception if anything is wrong. If it is ok, it will 
        process the data and turn it into the expected data to be 
        stored in the database.
        """
        self.validate_data(json_data)
        return self.prepare_data_for_database(json_data)
    
    def process_unfinished_projects(self):
        db_projects = self.get_unfinished_projects()

        for db_project in db_projects:
            print_in_progress(f'Processing project "{db_project["_id"]}"')
            self.process_project(db_project)
            print_completed(f'Project "{db_project["_id"]}" processed succesfully!')

    def process_project(self, db_project):
        project = Project(db_project['_id'])
        project.build(f'{self.__projects_output_abspath}project_{project.id}.mp4')
    
    # TODO: This below is for testing, remove it
    def get_unfinished_project(self):
        """
        Returns the first unfinished project that exists in the
        database, or None if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_project()

    def get_unfinished_projects(self):
        """
        Returns a list containing all the existing projects in the 
        database that have not been finished yet, or an empty list
        if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_projects()
    
    def __read_project_from_file(self, filename: str):
        """
        Reads the provided 'filename', that should contain the information of
        a project, and validates its content and structure. This method will
        return the data read as a dict or will raise an Exception if something
        is not ok.
        """
        if not filename:
            raise Exception('No "filename" provided.')
        
        if not isinstance(filename, str):
            raise Exception('The "filename" parameter provided is a str.')
        
        json_data = FileReader.read_json_from_file(filename)

        if not 'segments' in json_data:
            raise Exception('The provided "filename" does not contain the expected data structure.')

        # We validate each segment to be able to store the project
        # This will raise an Exception if something is not ok
        # for segment in json_data['segments']:
        #     self.__segment_validator.validate(segment)

        return json_data

    # TODO: Apply ObjectId type to 'project_id'
    def __get_project_from_database_by_id(self, project_id):
        """
        Gets the project with the provided 'project_id' if existing, or
        None if not.
        """
        return self.__database_handler.get_database_project_from_id(project_id)
    
    # TODO: Apply json type to 'json'
    def __get_project_from_database_by_json(self, json):
        """
        Gets the project with the provided 'json' if existing, or None if
        not. This 'json' will be compared with the 'script' field stored
        in database to check if there is a similar project previously 
        stored that must be recovered instead of duplicating it.
        """
        return self.__database_handler.get_database_project_from_json(json)
