"""
This file contains some constants that are useful for validation.
"""
from youtube_autonomous.segments.enums import SegmentType


# Valid segment types for validation
NARRATION_SEGMENT_TYPES = [SegmentType.CUSTOM_STOCK.value, SegmentType.STOCK.value, SegmentType.AI_IMAGE.value, SegmentType.IMAGE.value, SegmentType.YOUTUBE_VIDEO.value, SegmentType.TEXT.value]
URL_SEGMENT_TYPES = [SegmentType.IMAGE.value, SegmentType.YOUTUBE_VIDEO.value]
CUSTOM_SEGMENT_TYPES = [SegmentType.MEME.value, SegmentType.PREMADE.value]
VALID_SEGMENT_TYPES = NARRATION_SEGMENT_TYPES + URL_SEGMENT_TYPES + CUSTOM_SEGMENT_TYPES

# Arrays for validation
NEED_KEYWORDS_SEGMENT_TYPES = [SegmentType.CUSTOM_STOCK.value, SegmentType.STOCK.value, SegmentType.AI_IMAGE.value, SegmentType.MEME.value]
NEED_TEXT_SEGMENT_TYPES = [SegmentType.PREMADE.value, SegmentType.TEXT.value]