import os
from typing import List
from dataclasses import dataclass
from pytube import YouTube, StreamQuery
from tunatube.utils.video import call_ffmpeg
from datetime import datetime


@dataclass
class YouTubeDescription:
    title: str
    author: str
    captions: List[str]
    views: int
    description: str
    publish_date: datetime
    rating: str
    thumbnail_url: str

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "views": self.views,
            "description": self.description,
            "rating": self.rating,
            "publish_date": str(self.publish_date),
        }


class TunaTube:
    def __init__(
        self, url, on_progress_callback=None, on_complete_callback=None
    ) -> None:
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        self.__yt = YouTube(
            url=url,
            on_progress_callback=self.on_progress_callback,
            on_complete_callback=self.on_complete_callback,
        )

    @property
    def streams(self) -> StreamQuery:
        return self.__yt.streams

    @property
    def thumbnail_url(self):
        return self.__yt.thumbnail_url

    @property
    def description(self) -> YouTubeDescription:
        return YouTubeDescription(
            thumbnail_url=self.__yt.thumbnail_url,
            title=self.__yt.title,
            author=self.__yt.author,
            captions=self.__yt.captions,
            views=self.__yt.views,
            description=self.__yt.description,
            publish_date=self.__yt.publish_date,
            rating=self.__yt.rating,
        )

    def get_highest_mp4(self):
        return self.streams.filter(
            progressive=False, only_video=True, file_extension="mp4"
        ).first()

    def get_highest_audio(self):
        return self.streams.filter(only_audio=True).first()

    def download_hr(
        self,
        output_path: str = None,
        filename: str = None,
        filename_prefix: str = None,
        skip_existing: bool = True,
        timeout: int = None,
        max_retries: int = 0,
    ):
        audio = self.get_highest_audio()
        video = self.get_highest_mp4()

        filename = f"{video.title}.mp4"
        path = os.path.join(output_path, filename)

        pv = video.download(filename_prefix="video")
        pa = audio.download(filename_prefix="audio")

        err, stdout = call_ffmpeg(
            [
                "-i",
                pv,
                "-i",
                pa,
                f"-c:v copy -c:a {audio.audio_codec}",
                path,
            ]
        )

        print(stdout)
        print(err)

        return path
