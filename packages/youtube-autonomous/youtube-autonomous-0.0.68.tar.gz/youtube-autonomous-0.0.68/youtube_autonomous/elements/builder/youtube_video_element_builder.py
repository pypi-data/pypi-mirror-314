from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from youtube_autonomous.segments.builder.config import MAX_DURATION_PER_YOUTUBE_SCENE
from moviepy import VideoFileClip, concatenate_videoclips
from typing import Union


class YoutubeVideoElementBuilder(ElementBuilder):
    @classmethod
    def build_from_enhancement(cls, enhancement: dict):
        # TODO: Is always an object (?)
        return cls.build(enhancement.url, enhancement.duration)

    @classmethod
    def build_from_segment(cls, segment: dict):
        # TODO: Is always an object (?)
        return cls.build(segment.url, segment.duration)

    @classmethod
    def build(cls, url: str, duration: Union[float, int]):
        ElementParameterValidator.validate_url(url)
        ElementParameterValidator.validate_duration(duration)

        # Get the youtube video
        youtube_downloader = YoutubeDownloader()
        youtube_video = youtube_downloader.get_video(url)

        if not youtube_video.is_available():
            raise Exception(f'The youtube video with url "{str(url)}" is not available.')

        scenes_number = duration / MAX_DURATION_PER_YOUTUBE_SCENE
        if (duration + MAX_DURATION_PER_YOUTUBE_SCENE) > 0:
            scenes_number += 1
        scenes_number = int(scenes_number)
        scene_duration = duration / scenes_number

        youtube_video_scenes = []
        if youtube_video.heatmap:
            youtube_video_scenes = youtube_video.get_hottest_scenes(scenes_number, scene_duration)
        else:
            youtube_video_scenes = youtube_video.get_scenes(scenes_number, scene_duration)

        # Now we have all scenes, subclip the youtube clip
        youtube_clip = VideoFileClip(youtube_downloader.download_this_video(youtube_video))
        scene_clips = []
        for scene in youtube_video_scenes:
            scene_clips.append(youtube_clip.with_subclip(scene['start'], scene['end']))

        return concatenate_videoclips(scene_clips)