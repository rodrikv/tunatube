import os
import hashlib

from enum import Enum
from typing import List
from dataclasses import dataclass
from pytube import YouTube, StreamQuery
from tunatube.utils.video import call_ffmpeg
from datetime import datetime
from tunatube.logger import get_logger
from tunatube.utils import convert_size

logger = get_logger(__name__)


class Resolution(Enum):
    SD = "360p"
    RD = "480p"
    HD = "720p"
    FHD = "1080p"
    UHD = "2160p"
    HIGHEST = "highest"
    LOWEST = "lowest"


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
    def title(self):
        return self.__yt.title

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

    @staticmethod
    def stream_repr(stream):
        return f"[{stream.mime_type}] {stream.resolution} {convert_size(stream.filesize)}"

    def get_highest_mp4(self):
        return self.streams.filter(
            progressive=False, only_video=True, file_extension="mp4"
        ).first()

    def get_all_mp4(self):
        return self.streams.filter(
            progressive=False, only_video=True, file_extension="mp4"
        )

    def get_highest_audio(self):
        return (
            self.streams.filter(only_audio=True, mime_type="audio/mp4")
            .order_by("abr")
            .last()
        )

    def get_resolution(self, resolution: str):
        return self.streams.filter(
            res=resolution, only_video=True, file_extension="mp4"
        ).first()

    def get_highest_resolution(self):
        return self.streams.get_highest_resolution()

    def download_resolution(
        self,
        resolution: Resolution,
        output_path: str = None,
        filename: str = None,
        filename_prefix: str = None,
        skip_existing: bool = True,
        timeout: int = None,
        max_retries: int = 0,
    ):

        if resolution == Resolution.HIGHEST:
            video = self.get_highest_mp4()
        elif resolution == Resolution.LOWEST:
            video = self.get_lowest_resolution()
        else:
            video = self.get_resolution(resolution=resolution)

        audio = self.get_highest_audio()

        if video is None:
            return None, "Video resolution is not Valid"

        fn = hashlib.md5(video.title.encode("UTF-8")).hexdigest()

        filename = f"{fn}.mp4"
        output = os.path.join(os.getcwd(), output_path, f"{fn}.mp4")

        pv = video.download(
            filename_prefix="video",
            output_path=output_path,
            filename=filename,
        )
        pa = audio.download(
            filename_prefix="audio",
            output_path=output_path,
            filename=filename,
        )

        try:
            process = call_ffmpeg(
                [
                    "-i",
                    pv,
                    "-i",
                    pa,
                    "-map_metadata:s:v",
                    "0:s:v",
                    "-map_metadata:s:a",
                    "1:s:a",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "copy",
                    output,
                ]
            )
            logger.info(f"FFMPEG: {process.stdout.readlines()}")
            logger.info(f"FFMPEG: {process.stderr.readlines()}")

        except Exception as e:
            return None, f"Error in ffmpeg: {e}"

        os.remove(pv)
        os.remove(pa)

        return output, None

    def download_audio(self, output_path: str = None, filename: str = None):
        audio = self.get_highest_audio()

        if audio is None:
            return None, "Audio resolution is not Valid"

        filename = f"{audio.title}.mp3"
        output = os.path.join(os.getcwd(), output_path, f"{audio.title}.mp3")

        audio.download(
            filename_prefix="audio",
            output_path=output_path,
            filename=filename,
        )

        return output, None