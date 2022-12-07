import os

from dataclasses import dataclass
from tunatube.client.telethon import TunaTubeClient
from tunatube.youtube import Resolution, TunaTube, YouTubeDescription
from tunatube.utils.date import uploaded_at
from tunatube.logger import get_logger

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
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

logger = get_logger(__name__)

filters.BaseFilter


class TunaTubeBot:
    client: TunaTubeClient = None

    def __init__(self, token):
        self.TOKEN = token

    def run(self):
        application = Application.builder().token(self.TOKEN).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("ping", self.ping))
        application.add_handler(CommandHandler("youtube", self.youtube_command))
        application.add_handler(CommandHandler("info", self.youtube_info))
        application.add_handler(CallbackQueryHandler(self.download))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, text = update.message.text.split(maxsplit=1)
        await update.message.reply_html(
            f"pong {text}",
        )

    async def youtube_info(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            tt = TunaTube(update.message.text)
            message = await context.bot.send_message(
                update.message.chat.id,
                text=f"<b>{tt.title}</b>",
                reply_to_message_id=update.message.id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=TunaTube.stream_repr(stream),
                                callback_data=f"{update.message.text} {stream.resolution}",
                            )
                        ]
                        for stream in tt.get_all_mp4()
                    ]
                ),
                parse_mode="HTML",
            )
            logger.info(f"{tt.get_all_mp4()}")
        except Exception as e:
            return await update.message.reply_text(
                text=f"something bad happend!!!\nErrorMessage: {e}"
            )

    async def download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        _, youtube_url, resolution = update.callback_query.data.split()
        tt = TunaTube(youtube_url)
        download_path, _ = tt.download_resolution(resolution, output_path="./downloads")

        await update.callback_query.answer(
            text="sending video"
        )

        response_text = GenericMessages.youtube_description(tt.description)

        try:
            await self.client.send_file(
                update.callback_query.chat_instance,
                download_path,
                caption=response_text.text,
                reply_to_message=update.message.id,
            )

            os.remove(download_path)
        except Exception as e:
            pass

    async def youtube_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Send a message when the command /help is issued."""

        try:
            tt = TunaTube(update.message.text)
            message = await context.bot.send_message(
                update.message.chat.id,
                text="Sending youtube video description\nPlease wait...",
                reply_to_message_id=update.message.id,
            )
        except Exception as e:
            return await update.message.reply_text(
                text=f"something bad happend!!!\nErrorMessage: {e}"
            )

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
