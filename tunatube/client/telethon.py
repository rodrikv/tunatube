from telethon import TelegramClient


class TunaTubeClient:
    def __init__(self, api_id, api_hash, bot_token, session="default"):
        self.__api_id = api_id
        self.__api_hash = api_hash
        self.__session = session
        self.__bot_token = bot_token
        self.client = None

    async def connect(self):
        self.client = TelegramClient(self.__session, self.__api_id, self.__api_hash)
        self.client.parse_mode("html")
        await self.client.start(bot_token=self.__bot_token)

    async def stop(self):
        if self.client:
            await self.client.disconnect()

    def is_active(self):
        if self.client:
            return self.client.is_connected()

    async def send_file(
        self,
        chat_id: str,
        path: str,
        caption: str,
        reply_to_message: int,
        thumb: str = None
    ):
        if not self.is_active():
            await self.connect()

        return await self.client.send_file(
            chat_id,
            path,
            caption=caption,
            reply_to=reply_to_message,
            force_document=False,
            allow_cache=False,
            thumb=thumb
        )
