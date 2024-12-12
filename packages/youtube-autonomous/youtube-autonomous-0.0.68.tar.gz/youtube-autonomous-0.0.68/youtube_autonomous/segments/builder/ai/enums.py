from yta_general_utils.programming.enum import YTAEnum as Enum


class ImageEngine(Enum):
    """
    The engine that is capable of generating AI images.
    """
    PRODIA = 'prodia'
    FLUX = 'flux'
    POLLINATIONS = 'pollinations'

    @classmethod
    def get_default(cls):
        return cls.FLUX

class VoiceEngine(Enum):
    """
    The engine that is capable of generation audio voice narrations.
    """
    GOOGLE = 'google'
    MICROSOFT = 'microsoft'
    # TODO: Add more
    
    @classmethod
    def get_default(cls):
        return cls.GOOGLE