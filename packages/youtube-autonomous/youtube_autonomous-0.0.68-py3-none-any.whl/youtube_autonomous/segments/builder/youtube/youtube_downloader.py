from youtube_autonomous.segments.builder.youtube.enums import YoutubeChannelId
from youtubeenhanced.objects.youtube_video import YoutubeVideo
from youtubeenhanced.enums import Quality, Language
from youtubeenhanced.utils.youtube_api import YoutubeAPI
from yta_general_utils.temp import create_temp_filename
from random import randint

import requests


class YoutubeDownloader:
    """
    Singleton class.

    This object simplifies the access to our Youtube provider channels.
    It uses the Google Youtube Data V3 API and, if not available, uses
    a community API to obtain the videos.

    This object is used to download memes, stock videos, sounds, music,
    etc. from our specific Youtube channels.
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not YoutubeDownloader.__instance:
            YoutubeDownloader.__instance = object.__new__(cls)
        
        return YoutubeDownloader.__instance

    def __init__(self, ignore_repeated = True):
        # TODO: Maybe implement the other 'Singleton' pattern method, I don't
        # know if this one is actually working
        if not hasattr(self, 'ignore_ids'):
            if not YoutubeAPI.is_youtube_token_valid():
                print('Youtube token is not valid. Please, login to get a new valid token.')
                YoutubeAPI.start_youtube_auth_flow()

            self.service = YoutubeAPI.create_youtube_service()
            # This is to avoid using the same video again in the whole video. This can be
            # modified to avoid repeated videos only in each segment
            self.ignore_ids = []
            self.ignore_repeated = ignore_repeated

    def activate_ignore_repeated(self):
        """
        Sets the 'ignore_repeated' flag as True. This flag checks that a video
        that has been returned once is not returned again. This method will
        activate it, so any video can be returned only once.
        """
        self.ignore_repeated = True

    def deactivate_ignore_repeated(self):
        """
        Sets the 'ignore_repeated' flag as False. This flag checks that a video
        that has been returned once is not returned again. This method will
        deactivate it, so any video can be returned unlimited times if found.
        """
        self.ignore_repeated = False

    def add_ignored_id(self, ignore_id):
        # TODO: Maybe do any more check (?)
        if ignore_id not in self.ignore_ids:
            self.ignore_ids.append(ignore_id)

    def __search(self, keywords: str, max_results: int = 25, channel_id: str = None):
        """
        Searchs videos in the provided 'channel_id' channel, using the 'keywords'
        keywords, and returning 'max_results' results as maximum.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')
        
        if not max_results:
            max_results = 25

        if not channel_id:
            raise Exception('No "channel_id" provided.')

        try:
            response_videos_list = self.service.search().list(
                part = 'snippet',
                channelId = channel_id,
                maxResults = max_results,
                order = 'relevance',  # This is the most interesting by far, using the youtube search engine
                type = 'video',
                q = keywords
            ).execute()
        except Exception as e:
            print(e)
            # We try the collaborative known alternative that should work
            no_key_url = 'https://yt.lemnoslife.com/noKey/search?part=snippet&channelId=' + channel_id + '&maxResults=' + str(max_results) + '&order=relevance&type=video&q=' + keywords + '&alt=json'
            try:
                response_videos_list = requests.get(no_key_url).json()
            except Exception as e:
                print(e)
                return []

        if response_videos_list['pageInfo']['totalResults'] == 0:
            return []
        
        return response_videos_list['items']
    
    def get_video(self, url: str):
        """
        Returns the Youtube video from the 'url' provided as a YoutubeVideo
        object.
        """
        if not url:
            raise Exception('No "url" provided.')
        
        if not isinstance(url, str):
            raise Exception('The "url" parameter provided is not a str.')
        
        return YoutubeVideo(url)

    # TODO: Maybe the '__get_videos' (?)
    
    def __get_video(self, keywords: str, channel_id: str, do_randomize: bool = False) -> YoutubeVideo:
        """
        Looks for videos in the provided 'channel_id' channel according to the also
        provided 'keywords'. This method will return a video, if found, or None if 
        not. The 'do_randomize' parameter will return a random video if True and
        more than one video is found.

        This method will ignore any repeated video if 'ignore_repeated' is True in 
        this class instance.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')

        if not channel_id:
            raise Exception('No "channel_id" provided.')

        youtube_videos = self.__search(keywords, 25, channel_id)

        # We look for repeated videos to eliminate from the ones found
        if self.ignore_repeated and len(self.ignore_ids) > 0:
            index = 0
            while index < len(youtube_videos):
                video = youtube_videos[index]
                if video['id']['videoId'] in self.ignore_ids:
                    del youtube_videos[index]
                    index -= 1
                index += 1

        if len(youtube_videos) == 0:
            return None

        url = 'https://www.youtube.com/watch?v=' + youtube_videos[0]['id']['videoId']
        if do_randomize:
            url = 'https://www.youtube.com/watch?v=' + youtube_videos[randint(0, len(youtube_videos) - 1)]['id']['videoId']

        return YoutubeVideo(url)

    def __download_video(self, keywords: str, channel_id: str, include_audio = False, do_randomize: bool = False, output_filename = 'output.mp4'):
        """
        Looks for the videos in the channel with provided 'channel_id' id and that match
        the also provided 'keywords'. This method will download, if any video is found, 
        the first one (or a random one if 'do_randomize' is True).

        This method will return None if no video found nor downloaded.

        This method forces the download to FULL HD quality (1920x1080).

        This method returns the locally stored 'output_filename' (that could change due to video
        extension), or None if something went wrong.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')

        if not channel_id:
            raise Exception('No "channel_id" provided.')
        
        youtube_video = self.__get_video(keywords, channel_id, do_randomize)

        if not youtube_video:
            return None

        if include_audio:
            output_filename = youtube_video.download_with_audio(Quality.FULL_HD, Language.DEFAULT, output_filename)
        else:
            output_filename = youtube_video.download(Quality.FULL_HD, output_filename)

        if self.ignore_repeated:
            self.add_ignored_id(youtube_video.id)

        return output_filename
    
    def download_this_video(self, youtube_video: YoutubeVideo, output_filename: str = None, do_include_sound: bool = True, language: Language = Language.DEFAULT):
        """
        Downloads the provided 'youtube_video' and stores it locally as 
        'output_filename' if this parameter is provided, or in a temporary file
        (that is returned by this method) if not. The 'do_include_sound' parameter
        allows the user to include the audio or not. If 'do_include_sound' is True,
        the 'language' parameter is needed to decide the audio language.
        """
        if not youtube_video:
            raise Exception('No "youtube_video" provided.')
        
        if not output_filename:
            output_filename = create_temp_filename('youtube_video.mp4')

        if not isinstance(output_filename, str):
            raise Exception('The "output_filename" provided is not a str.')

        if not language:
            language = Language.DEFAULT

        if not isinstance(language, Language):
            raise Exception('The "language" parameter provided is not a Language.')

        if do_include_sound:
            output_filename = youtube_video.download_with_audio(Quality.FULL_HD, language, output_filename)
        else:
            output_filename = youtube_video.download(Quality.FULL_HD, output_filename)

        return output_filename
    
    def download_video(self, url: str, output_filename: str = None, do_include_sound: bool = True, language: Language = Language.DEFAULT):
        """
        Downloads the Youtube video from the provided 'url' and stores it locally
        as 'output_filename' if this parameter is provided, or in a temporary file
        (that is returned by this method) if not. The 'do_include_sound' parameter
        allows the user to include the audio or not. If 'do_include_sound' is True,
        the 'language' parameter is needed to decide the audio language.
        """
        if not url:
            raise Exception('No "url" provided.')
        
        if not isinstance(url, str):
            raise Exception('The "url" parameter provided is not a str.')
        
        if not output_filename:
            output_filename = create_temp_filename('youtube_video.mp4')

        if not isinstance(output_filename, str):
            raise Exception('The "output_filename" provided is not a str.')

        if not language:
            language = Language.DEFAULT

        if not isinstance(language, Language):
            raise Exception('The "language" parameter provided is not a Language.')


        # TODO: Validate url (?)
        video = YoutubeVideo(url)
        
        if not video.is_available():
            raise Exception('Provided "url" is not a valid and/or available Youtube video.')
        
        return self.download_this_video(video, output_filename, do_include_sound, language)
    
    def __download_audio(self, keywords: str, channel_id: str, do_randomize: bool = False, output_filename = 'output.mp3'):
        """
        Looks for the videos in the channel with provided 'channel_id' id and that match
        the also provided 'keywords'. This method will download, if any video is found, 
        the first one (or a random one if 'do_randomize' is True).

        This method will return None if no video found nor downloaded.

        This method forces the download to DEFAULT LANGUAGE (the first one in the list).

        This method returns the locally stored 'output_filename' (that could change due to video
        extension), or None if something went wrong.
        """
        youtube_video = self.__get_video(keywords, channel_id, do_randomize)

        if not youtube_video:
            return None
        
        if self.ignore_repeated:
            self.add_ignored_id(youtube_video.id)

        return youtube_video.download_audio(Language.DEFAULT, output_filename)

    def download_audio(self, url: str, output_filename: str = None, language: Language = Language.DEFAULT):
        """
        Downloads the Youtube video audio from the provided 'url' and stores it 
        locally as 'output_filename' if this parameter is provided, or in a 
        temporary file (that is returned by this method) if not. The 'language' 
        parameter is needed to decide the audio language.
        """
        if not url:
            raise Exception('No "url" provided.')
        
        if not isinstance(url, str):
            raise Exception('The "url" parameter provided is not a str.')
        
        if not output_filename:
            output_filename = create_temp_filename('youtube_video.mp3')

        if not isinstance(output_filename, str):
            raise Exception('The "output_filename" provided is not a str.')

        if not language:
            language = Language.DEFAULT

        if not isinstance(language, Language):
            raise Exception('The "language" parameter provided is not a Language.')

        # TODO: Validate url (?)
        video = YoutubeVideo(url)
        output_filename = video.download_audio(language, output_filename)

        return output_filename

    def download_meme_video(self, keywords: str, include_audio: bool = True, do_randomize: bool = False, output_filename: str = create_temp_filename('meme.mp4')):
        """
        Downloads a meme from the specific Youtube channel configured as Meme channel. It will
        include the audio if 'include_audio' is True, and will return the first result (based 
        on Youtube search relevance) or a random one if 'do_randomize' is True. It will be 
        stored locally as 'output_filename' if found.

        This method returns the 'output_filename' of the locally stored video, or None if not
        downloaded.
        """
        return self.__download_video(keywords, YoutubeChannelId.MEMES.value, do_randomize = do_randomize, include_audio = include_audio, output_filename = output_filename)

    def download_stock_video(self, keywords: str, include_audio: bool = True, do_randomize: bool = False, output_filename: str = create_temp_filename('stock.mp4')):
        """
        Downloads a stock video from the specific Youtube channel configured as Stock videos 
        channel. It will include the audio if 'include_audio' is True, and will return the 
        first result (based on Youtube search relevance) or a random one if 'do_randomize' is
        True. It will be stored locally as 'output_filename' if found.

        This method returns the 'output_filename' of the locally stored video, or None if not
        downloaded.
        """
        return self.__download_video(keywords, YoutubeChannelId.STOCK.value, do_randomize = do_randomize, include_audio = include_audio, output_filename = output_filename)
    
    def download_sound_audio(self, keywords: str, output_filename: str = create_temp_filename('sound.mp3')):
        """
        Downloads a sound from the specific Youtube channel configured as Sounds channel. It 
        will be stored locally as 'output_filename' if found.

        This method returns the 'output_filename' of the locally stored audio, or None if not
        downloaded.
        """
        return self.__download_audio(keywords, YoutubeChannelId.SOUNDS.value, do_randomize = False, output_filename = output_filename)
    
    def download_music_audio(self, keywords: str, output_filename: str = create_temp_filename('music.mp3')):
        """
        Downloads a song from the specific Youtube channel configured as Music channel. It 
        will be stored locally as 'output_filename' if found.

        This method returns the 'output_filename' of the locally stored audio, or None if not
        downloaded.
        """
        return self.__download_audio(keywords, YoutubeChannelId.MUSIC.value, do_randomize = False, output_filename = output_filename)
    
    def get_stock_video(self, keywords: str, do_randomize: bool = False) -> YoutubeVideo:
        """
        Searches for the provided 'keywords' in the Stock Videos Youtube channel and gets,
        if available, a video matching those 'keywords'. It will return the first one or a
        random one if 'do_randomize' is True.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')
        
        return self.__get_video(keywords, YoutubeChannelId.STOCK.value, do_randomize)
    

"""
    Pay attention to this yt-dlp link, it is interesting: 
    https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#download-options
"""