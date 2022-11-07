from typing import List
from dataclasses import dataclass
from pytube import YouTube, StreamQuery, Stream
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
            "publish_date": str(self.publish_date)
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
