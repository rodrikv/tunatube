from dataclasses import dataclass
import logging
from tunatube.youtube import TunaTube, YouTubeDescription
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
            reply_to_message_id=update.message.id
        )

        tt = TunaTube(update.message.text)

        response_text = GenericMessages.youtube_description(tt.description)

        await context.bot.delete_message(
            message.chat_id,
            message.id
        )

        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=tt.thumbnail_url,
            caption=response_text.text,
            reply_to_message_id=update.message.id,
            parse_mode=response_text.parse_mode,
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
