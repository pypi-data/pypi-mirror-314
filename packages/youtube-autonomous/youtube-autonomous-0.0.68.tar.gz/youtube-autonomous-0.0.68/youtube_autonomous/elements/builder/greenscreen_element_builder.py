from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from yta_multimedia.greenscreen.custom.greenscreen import Greenscreen


class GreenscreenElementBuilder(ElementBuilder):
    """
    This builders allows you to generate 'GREENSCREEN' content.
    """
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        """
        Returns an ImageGreenscreen or VideoGreenscreen instance
        initialized with the provided filename or url (filename
        has priority) or raises an Exception if something goes
        wrong.
        """
        filename = enhancement.filename
        url = enhancement.url

        if not url and not filename:
            # TODO: Can this happen (?)
            raise Exception('No "url" nor "filename" provided and at least one is needed.')

        if url and not filename:
            return Greenscreen.init(url)

        return Greenscreen.init(filename)