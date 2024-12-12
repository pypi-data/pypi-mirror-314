MAX_DURATION_PER_IMAGE = 5
"""
The amount of seconds that an image can be used to build a 
video by applying some effect on it.
"""
MIN_DURATION_PER_IMAGE = 2
"""
The minimum amount of seconds that an image must last when 
treating ai_images segment building to ensure that a new
image is needed. If the value is lower than this one, the
previous image will stay longer to fit this short period of
time.
"""
MAX_DURATION_PER_YOUTUBE_SCENE = 5
"""
The maximum number of seconds that we can extract consecutively 
from a YouTube video (related to avoiding copyright issues).
"""
DEFAULT_SEGMENT_PARTS_FOLDER = 'segment_files'
"""
The folder, in the root of the project in which this library is
executed, to maintain segment building part files in order to be
able to work and to recover them later if something goes wrong.
"""
DEFAULT_PROJECTS_OUTPUT_FOLDER = 'output_projects'
"""
The folder, in the root of the project in which this library is
executed, to store the output of the projects that are generated.
"""