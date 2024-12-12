from yta_stock_downloader.videos.pexels import download_first as download_pexels_first_video, download_random as download_pexels_random_video
from yta_stock_downloader.videos.pixabay import download_first as download_pixabay_first_video
from yta_general_utils.temp import create_temp_filename


class StockDownloader:
    """
    Singleton class.

    This object simplifies the access to our Stock provider platforms.
    It uses our stock library to connecto with different stock 
    platforms directly to download the content.

    This object is used to download stock videos to build the 
    main images that are shown in the videos.

    TODO: Is this actually a singleton class (?)
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not StockDownloader.__instance:
            StockDownloader.__instance = object.__new__(cls)
        
        return StockDownloader.__instance

    def __init__(self, ignore_repeated = True):
        if not hasattr(self, 'ignore_repeated'):
            self.ignore_repeated = ignore_repeated
            self.pexels_used_video_ids = []
            self.pexels_used_image_ids = []
            self.pexels_ignore_ids = []
            self.pixabay_used_video_ids = []
            self.pixabay_used_image_ids = []
            self.pixabay_ignore_ids = []

    def download_video(self, keywords: str, do_randomize: bool = False, output_filename: str = create_temp_filename('stock.mp4')):
        """
        Searches the provided 'keywords' in the different stock platforms we have 
        looking for videos. This method will download, if any video is found, a 
        video that could be the first one or a random one if 'do_randomize' is
        True.

        This method will return the locally stored filename when downloaded, or
        None if no video is found.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')
        
        if not output_filename:
            output_filename = create_temp_filename('stock.mp4')

        # TODO: What about the sound?
        if do_randomize:
            download = download_pexels_random_video(keywords, self.pexels_used_video_ids, output_filename)
            if not download:
                # TODO: Implement 'download_pixabay_random_video' (check task)
                download = download_pixabay_first_video(keywords, output_filename)
        else:
            download = download_pexels_first_video(keywords, self.pexels_used_video_ids, output_filename)
            if not download:
                download = download_pixabay_first_video(keywords, output_filename)

        if not download:
            return None

        if self.ignore_repeated:
            if isinstance(download, str):
                self.pixabay_used_video_ids.append(download)
            else:
                self.pexels_used_video_ids.append(download['id'])

        if isinstance(download, str):
            output_filename = download
        else:
            output_filename = download['output_filename']

        return output_filename
    