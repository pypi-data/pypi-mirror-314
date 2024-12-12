# TODO: Remove this in a near future

from youtube_autonomous.segments.enums import EnhancementType, EnhancementMode
from youtube_autonomous.experimental.segments.enhancements.validation.segment_enhancement_validator import SegmentEnhancementValidator
from youtube_autonomous.experimental.shortcodes.consts import FILE_DURATION, SEGMENT_DURATION
from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips, concatenate_audioclips
from typing import Union


class EnhancementElement:
    """
    Class that represents an element that will be used to enhance a 
    segment video by applying it. It could be an effect, a sound, a
    sticker, etc.

    This class can be built directly from a json file that is read
    as a dict, or by a previously detected shortcode that is converted
    into this.
    """
    @classmethod
    def get_class_from_type(cls, type: Union[EnhancementType, str]):
        """
        This method returns the EnhancementElement class that is
        equivalent of the provided 'type' EnhancementType.
        """
        SegmentEnhancementValidator.validate_type(type)

        if isinstance(type, str):            
            type = EnhancementType(type)

        from youtube_autonomous.experimental.segments.enhancements.objects.meme_enhancement_element import MemeEnhancementElement
        from youtube_autonomous.experimental.segments.enhancements.objects.sound_enhancement_element import SoundEnhancementElement
        from youtube_autonomous.experimental.segments.enhancements.objects.image_enhancement_element import ImageEnhancementElement
        from youtube_autonomous.experimental.segments.enhancements.objects.sticker_enhancement_element import StickerEnhancementElement
        from youtube_autonomous.experimental.segments.enhancements.objects.greenscreen_enhancement_element import GreenscreenEnhancementElement
        from youtube_autonomous.experimental.segments.enhancements.objects.effect_enhancement_element import EffectEnhancementElement

        if type == EnhancementType.MEME:
            return MemeEnhancementElement
        if type == EnhancementType.SOUND:
            return SoundEnhancementElement
        if type == EnhancementType.IMAGE:
            return ImageEnhancementElement
        if type == EnhancementType.STICKER:
            return StickerEnhancementElement
        if type == EnhancementType.GREENSCREEN:
            return GreenscreenEnhancementElement
        if type == EnhancementType.EFFECT:
            return EffectEnhancementElement
        
        raise Exception('The provided "type" does not have a related EnhancementElement class.')

    _type: EnhancementType
    """
    The enhancement element type that determines the way it will be
    built and applied.
    """
    _start: float
    """
    The time moment of the current segment in which this element is
    expected to be applied.
    """
    _duration: float
    """
    The duration of the element that the user wants to be applied.
    """
    _keywords: str = ''
    """
    The keywords that will be used to look for the resource in the 
    platform that the type of element needs, if provided.
    """
    _url: str = ''
    """
    The url from which the resource will be obtained, if set, to
    use as source of this enhancement element.
    """
    _filename: str = ''
    """
    The filename that will be used as source of this enhancement 
    element if provided.
    """
    _mode: EnhancementMode = EnhancementMode.INLINE
    """
    The mode in which the enhancement element will be applied, that could be inline
    or as overview.
    """

    def __init__(self, type: EnhancementType, start: float, duration: float, keywords: str, url: str, filename: str, mode: EnhancementMode):
        self.type = type
        self.start = start
        self.duration = duration
        self.keywords = keywords
        self.url = url
        self.filename = filename
        self.mode = mode

    @property
    def valid_modes(self):
        """
        The EnhancementMode enums accepted for this type of
        EnhancementElement.
        """
        return EnhancementMode.get_all()
    
    @valid_modes.setter
    def valid_modes(self, value):
        raise Exception('You cannot modify the "valid_modes" parameter.')

    @property
    def type(self):
        """
        The enhancement element type that determines the way it will be
        built and applied.
        """
        return self._type
    
    @type.setter
    def type(self, type: Union[EnhancementType, str]):
        SegmentEnhancementValidator.validate_type(type)
            
        if isinstance(type, str):
            type = EnhancementType(type)

        self._type = type

    @property
    def start(self):
        """
        The time moment of the current segment in which this element is
        expected to be applied.
        """
        return self.start
    
    @start.setter
    def start(self, start: float):
        SegmentEnhancementValidator.validate_start(start)
        
        self._start = start

    @property
    def duration(self):
        """
        The duration of the element that the user wants to be applied.
        """
        return self._duration
    
    @duration.setter
    def duration(self, duration: float):
        SegmentEnhancementValidator.validate_duration(duration)
        
        self._duration = duration

    @property
    def keywords(self):
        """
        The keywords that will be used to look for the resource in
        the platform that the type of element needs, if provided.
        """
        return self._keywords
    
    @keywords.setter
    def keywords(self, keywords: Union[str, None]):
        if keywords is not None and keywords != '':
            if not keywords:
                raise Exception('No "keywords" provided.')
            
            if not isinstance(keywords, str):
                raise Exception(f'The "keywords" parameter provided {str(keywords)} is not a string.')
        else:
            keywords = ''
        
        self._keywords = keywords

    @property
    def url(self):
        """
        The url from which the resource will be obtained, if set, to
        use as source of this enhancement element.
        """
        return self._url
    
    @url.setter
    def url(self, url: Union[str, None]):
        if url is not None and url != '':
            if not url:
                raise Exception('No "url" provided.')
            
            if not isinstance(url, str):
                raise Exception(f'The "url" parameter provided {str(url)} is not a string.')
        else:
            url = ''
        
        self._url = url

    @property
    def filename(self):
        """
        The filename that will be used as source of this enhancement 
        element if provided.
        """
        return self._filename
    
    @filename.setter
    def filename(self, filename: Union[str, None]):
        if filename is not None and filename != '':
            if not filename:
                raise Exception('No "filename" provided.')
            
            if not isinstance(filename, str):
                raise Exception(f'The "filename" parameter provided {str(filename)} is not a string.')
        else:
            filename = ''
        
        self._filename = filename

    @property
    def mode(self):
        """
        The mode in which the enhancement element will be applied, that could be inline
        or as overview.
        """
        return self._mode
    
    @mode.setter
    def mode(self, mode: Union[EnhancementMode, str]):
        SegmentEnhancementValidator.validate_mode(mode, self.valid_modes)
        
        if isinstance(mode, str):
            mode = EnhancementMode(mode)

        self._mode = mode


    def recalculate_duration(self, enhancement_clip: Union[AudioFileClip, CompositeAudioClip, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        This method recalculates the 'self.duration' field according to
        its value, the 'self.mode' parameter value we have, and also the
        'enhancement_clip' and 'video' parameters provided.
        """
        if self.duration == FILE_DURATION:
            self.duration = enhancement_clip.duration

        if self.duration == SEGMENT_DURATION:
            self.duration = video.duration

        if self.mode in [EnhancementMode.INLINE, EnhancementMode.OVERLAY]:
            if self.duration > enhancement_clip.duration:
                self.duration = enhancement_clip.duration

        if self.mode == [EnhancementMode.OVERLAY, EnhancementMode.REPLACE]:
            end = self.start + self.duration
            if end > video.duration:
                self.duration = video.duration - self.start

    def apply(self, enhancement_clip: Union[AudioFileClip, CompositeAudioClip, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], video: Union[VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        This method adjusts the 'enhancement_clip' duration and make the
        necessary cuts to fit in the base provided 'video' according to
        its parameters. It will consider the mode to cut the 'video' and
        insert the 'enhancement_clip' in some specific position, or will
        put it as an overlay video if requested.

        This method returns the provided 'video' with the 
        'enhancement_clip' applied on it.
        """
        if isinstance(enhancement_clip, (AudioFileClip, CompositeAudioClip)):
            audio = video.audio
            if self.mode == EnhancementMode.INLINE:
                if self.start == 0:
                    audio = concatenate_audioclips([
                        enhancement_clip.with_duration(self.duration),
                        audio
                    ])
                elif self.start == video.duration:
                    audio = concatenate_audioclips([
                        audio,
                        enhancement_clip.with_duration(self.duration)
                    ])
                else:
                    audio = concatenate_audioclips([
                        audio.with_subclip(0, self.start),
                        enhancement_clip.with_duration(self.duration),
                        audio.with_subclip(self.start, video.duration)
                    ])
            elif self.mode in [EnhancementMode.OVERLAY, EnhancementMode.REPLACE]:
                audio = CompositeAudioClip([
                    audio,
                    enhancement_clip.with_start(self.start).with_duration(video.duration)
                ])
            # TODO: Implement self.mode == EnhancementMode.REPLACE (?)

            video = video.with_audio(audio)
        elif isinstance(enhancement_clip, (VideoFileClip, CompositeVideoClip, ImageClip, ColorClip)):
            if self.mode == EnhancementMode.INLINE:
                if self.start == 0:
                    video = concatenate_videoclips([
                        enhancement_clip.with_duration(self.duration),
                        video
                    ])
                elif self.start == video.duration:
                    video = concatenate_videoclips([
                        video,
                        enhancement_clip.with_duration(self.duration)
                    ])
                else:
                    video = concatenate_videoclips([
                        video.with_subclip(0, self.start),
                        enhancement_clip.with_duration(self.duration),
                        video.with_subclip(self.start, video.duration)
                    ])
            elif self.mode == EnhancementMode.OVERLAY:
                video = CompositeVideoClip([
                    video,
                    enhancement_clip.with_start(self.start).with_duration(video.duration)
                ])
            elif self.mode == EnhancementMode.REPLACE:
                end = self.start + self.duration
                if self.start == 0:
                    if end == video.duration:
                        video = enhancement_clip
                    else:
                        video = concatenate_videoclips([
                            enhancement_clip,
                            video.with_subclip(end, video.duration)
                        ])
                elif end == video.duration:
                    video = concatenate_videoclips([
                        video.with_subclip(0, self.start),
                        enhancement_clip
                    ])
                else:
                    video = concatenate_videoclips([
                        video.with_subclip(0, self.start),
                        enhancement_clip,
                        video.with_subclip(end, video.duration)
                    ])

        return video
        