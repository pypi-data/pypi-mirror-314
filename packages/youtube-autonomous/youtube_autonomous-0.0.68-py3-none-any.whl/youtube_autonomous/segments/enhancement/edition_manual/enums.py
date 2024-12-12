from yta_general_utils.programming.enum import YTAEnum as Enum


class EditionManualTermMode(Enum):
    """
    This is the mode in which we will look for the terms
    of our edition manual book in the given segment text
    to find any coincidences.
    """
    EXACT = 'exact'
    """
    The term found must be exactly matching one term of
    our edition manual book.
    """
    IGNORE_CASE_AND_ACCENTS = 'ignore_case_and_accents'
    """
    The term found must match, in lower case and ignoring
    the accents, one term of our edition manual book.
    """
    @classmethod
    def get_default(cls):
        """
        Returns the item that acts as the one by default.
        """
        return cls.EXACT

class EditionManualTermContext(Enum):
    """
    This is the context we will be able to apply to our
    edition terms to be applied only on those segments
    related to that context.
    """
    ANY = 'any'
    """
    The term will be applied always, in any context.
    """
    @classmethod
    def get_default(cls):
        """
        Returns the item that acts as the one by default.
        """
        return cls.ANY