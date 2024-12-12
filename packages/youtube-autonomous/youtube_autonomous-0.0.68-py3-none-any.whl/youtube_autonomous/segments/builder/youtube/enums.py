from yta_general_utils.programming.enum import YTAEnum as Enum


class YoutubeChannelId(Enum):
    """
    Our specific channel ids.
    """
    STOCK = 'UCS49NBDOLkrahf6UgYiL4SQ'
    """
    Stock videos to be used as main part of the video background.
    """
    MEMES = 'UCiz62GOuKsIw3n7i3Cs4pRA'
    """
    Meme videos to enhance the experience by overlaying them or
    putting inline.
    """
    SOUNDS = 'UCF1vrXoRtVfUY05fCnmfNqw'
    """
    Sound videos to be downloaded as audio and used to enhance the
    video experience by using them in different specific situations.
    """
    MUSIC = 'UCDLfH57hn3K7lhmcAAqp9Mw'
    """
    Music videos to be downloaded as audio and used to enhance the
    video experience by using them as background music for the 
    whole video or for some specific moments.
    """
    ALPHA_TRANSITIONS = 'UC8yIzZMJnFsFb40ewuUcKIA'
    """
    Alpha transitions to be downloaded and applied between videos
    with the 'alpha' transition effect. These transitions have no
    sound effect.
    """