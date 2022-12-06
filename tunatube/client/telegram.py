import os
import logging


from dataclasses import dataclass
from tunatube.client.telethon import TunaTubeClient
from tunatube.youtube import Resolution, TunaTube, YouTubeDescription
from tunatube.utils.date import uploaded_at

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TunaTubeBot:
    client: TunaTubeClient = None

    def __init__(self, token):
        self.TOKEN = token

    def run(self):
        application = Application.builder().token(self.TOKEN).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("ping", self.ping))
        application.add_handler(CommandHandler("youtube", self.youtube_command))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, text = update.message.text.split(maxsplit=1)
        await update.message.reply_html(
            f"pong {text}",
        )

    async def youtube_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /help is issued."""

        message = await context.bot.send_message(
            update.message.chat.id,
            text="Sending youtube video description\nPlease wait...",
            reply_to_message_id=update.message.id,
        )

        tt = TunaTube(update.message.text)

        download_path, _ = tt.download_resolution(Resolution.HIGHEST, "./downloads")

        if _:
            return await update.message.reply_text(
                text=f"something bad happend couldn't download file!!!\nErrorMessage: {_}"
            )

        if not download_path:
            return await update.message.reply_text(
                text="Couldn't find the highest resolution :("
            )

        await context.bot.delete_message(message.chat_id, message.id)

        response_text = GenericMessages.youtube_description(tt.description)

        try:
            await update.message.reply_text(text=f"sending video please wait...")

            await self.client.send_file(
                update.message.chat_id,
                download_path,
                caption=response_text.text,
                reply_to_message=update.message.id,
            )

            os.remove(download_path)
        except Exception as e:
            return await update.message.reply_text(
                text=f"something bad happend couldn't send file!!!\nErrorMessage: {e}"
            )


@dataclass
class ResponseMessage:
    text: str
    parse_mode: str = "html"


class GenericMessages:
    @classmethod
    def youtube_description(cls, ytd: YouTubeDescription):
        text = f"""<b>{ytd.title}</b>
{'{:,}'.format(ytd.views)} views

<b>{uploaded_at(ytd.publish_date)}</b>
        """

        return ResponseMessage(text=text, parse_mode="html")

    def fetching_youtube_url(cls):
        text = ""

        return ResponseMessage(text=text, parse_mode="html")
