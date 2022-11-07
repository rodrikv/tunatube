from telethon import TelegramClient


class TunaTubeClient:
    _clients = {}

    def __init__(self, api_id, api_hash, session="default"):
        self.__api_id = api_id
        self.__api_hash = api_hash
        self._clients[session]: TelegramClient = TelegramClient(
            session, self.__api_id, self.__api_hash
        )
        self.client = self.clients[session]

    def stop(self):
        self.client.disconnect()

    def is_active(self):
        return self.client.is_connected()

    async def send_file(self):
        self.client.send_file()
