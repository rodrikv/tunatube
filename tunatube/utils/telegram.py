from ctypes import DEFAULT_MODE
from telegram import InlineKeyboardMarkup, MessageEntity
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput
from typing import List, Tuple, Any


def send_message(
    text: str,
    chat_id: str | int = None,
    message_id: int = None,
    inline_message_id: str = None,
    parse_mode: ODVInput[str] = DEFAULT_NONE,
    disable_web_page_preview: bool = DEFAULT_NONE,
    reply_markup: InlineKeyboardMarkup = None,
    entities: List[MessageEntity] | Tuple[MessageEntity, ...] = None,
    *,
    read_timeout: ODVInput[float] = DEFAULT_NONE,
    write_timeout: ODVInput[float] = DEFAULT_NONE,
    connect_timeout: ODVInput[float] = DEFAULT_NONE,
    pool_timeout: ODVInput[float] = DEFAULT_MODE,
    api_kwargs: JSONDict = None,
    rate_limit_args: Any = None
):
    pass
