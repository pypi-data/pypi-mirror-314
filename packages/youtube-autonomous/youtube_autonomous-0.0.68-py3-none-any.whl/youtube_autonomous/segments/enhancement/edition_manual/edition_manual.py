from youtube_autonomous.segments.enhancement.edition_manual.edition_manual_term import EditionManualTerm
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_general_utils.file.reader import FileReader
from typing import Union


class EditionManual:
    @property
    def terms(self):
        return self._terms
    
    @terms.setter
    def terms(self, terms: list[EditionManualTerm]):
        if not terms:
            terms = []

        if any(not isinstance(term, EditionManualTerm) for term in terms):
            raise Exception('At least one of the provided "terms" is not an EditionManualTerm.')

        self._terms = terms

    @staticmethod
    def init_from_file(filename: str):
        """
        Initializes an Edition Manual from the given file
        'filename' that must have a valid structure.
        """
        ElementParameterValidator.validate_filename(filename, None)

        terms_dictionary = FileReader.read_json_from_file(filename)

        terms = terms_dictionary.get('terms', None)

        if terms is None:
            raise Exception('No "terms" field found in the provided json filename {filename}.')
        
        # Terms will be validated in the '__init__' method

        return EditionManual(terms)

    def __init__(self, terms: Union[list[dict], list[EditionManualTerm]]):
        # TODO: We need an ID or something maybe
        # TODO: Look for a better way to iterate
        term_objects = []
        for term in terms:
            if not isinstance(term, EditionManualTerm):
                obj = {term: terms[term]}

                ElementParameterValidator.validate_edition_manual_term(obj)

                term_objects.append(EditionManualTerm(term, terms[term]['mode'], terms[term]['context'], terms[term]['enhancements']))
            else:
                term_objects.append(term)

        self.terms = term_objects

    def apply(self, transcription: list[dict]):
        """
        Applies this edition manual to the provided 'segment' parameter.
        This method will search all the terms in the edition manual and
        will return all the enhancements found according to those terms
        based on the segment transcription.
        """
        # We only accept segments by now, enhancements in a future
        
        # Search for the terms according to the search mode
        # of each term
        enhancements_found = []
        for term in self.terms:
            enhancements_found += term.search(transcription)

        # Enhancements are, by now, dicts
        # TODO: Maybe we should append enhancements as objects to
        # the segment
        return enhancements_found