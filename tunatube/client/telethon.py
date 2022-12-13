from telethon import TelegramClient
from tunatube.utils.video import *


class TunaTubeClient:
    def __init__(self, api_id, api_hash, bot_token, session="default"):
        self.__api_id = api_id
        self.__api_hash = api_hash
        self.__session = session
        self.__bot_token = bot_token
        self.client = None

    async def connect(self):
        self.client = TelegramClient(self.__session, self.__api_id, self.__api_hash)
        self.client.parse_mode = "html"
        await self.client.start(bot_token=self.__bot_token)

    async def stop(self):
        if self.client:
            await self.client.disconnect()

    def is_active(self):
        if self.client:
            return self.client.is_connected()

    async def send_video(
        self,
        chat_id: str,
        path: str,
        caption: str,
        reply_to_message: int = None,
    ):
        if not self.is_active():
            await self.connect()

        video_metadata = get_file_attributes(path)
        thumb = get_video_thumb(path)

        kwargs = dict(
            reply_to=reply_to_message,
            caption=caption,
            force_document=False,
            allow_cache=False,
            attributes=video_metadata,
            thumb=thumb,
        )

        return await self.client.send_file(
            chat_id,
            path,
            **kwargs,
        )

    async def send_audio(
        self, chat_id: str, path: str, caption: str, reply_to_message: int = None
    ):
        if not self.is_active():
            await self.connect()

        kwargs = dict(
            reply_to=reply_to_message,
            caption=caption,
            force_document=False,
            allow_cache=False,
        )

        return await self.client.send_file(
            chat_id,
            path,
            **kwargs,
        )
