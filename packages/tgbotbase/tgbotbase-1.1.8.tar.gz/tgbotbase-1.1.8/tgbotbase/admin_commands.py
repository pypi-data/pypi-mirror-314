from typing import Any

from aiogram.filters import Command
from aiogram.types import Message

from tgbotbase.answer import AnswerContext
from tgbotbase.filters import Role
from tgbotbase.utils import SHARED_OBJECTS, check_text_pattern, get_msg_args, logger
from tgbotbase.renv import renv

# for local debugging
try:
    from src.models import User, UserRole  # type: ignore
except ImportError:
    class User(Any): ...
    class BookType(Any): ...

async_redis = SHARED_OBJECTS.get("async_redis")
admin_router = SHARED_OBJECTS.get("admin_router")
renv_value_filters = SHARED_OBJECTS.get("renv_value_filters", {})
if async_redis is None:
    logger.warning(
        "async_redis is not initialized to SHARED_OBJECTS, add it as value to key 'async_redis' to SHARED_OBJECTS"
    )

if admin_router is None:
    logger.warning(
        "admin_router is not initialized to SHARED_OBJECTS, add it as value to key 'admin_router' to SHARED_OBJECTS"
    )

if not renv_value_filters:
    logger.error(
        "renv_value_filters is not filled in SHARED_OBJECTS"
    )
#renv_value_filters = {
#    "commissions": [r"^[\d.]+,[\d.]+,[\d.]+,[\d.]+,[\d.]+$", "10,9,8,6,5"],
#}
class RenvTEXT:
    usage = "<b>Usage:</b>\n/renv KEY\n/renv KEY VALUE"
    get_key = "<b>Key:</b> <code>{key}</code>\n<b>Current value:</b> <code>{value}</code>"
    set_key_value = "<b>Key:</b> <code>{key}</code>\n<b>Set new value:</b> <code>{value}</code> -> <code>{new_value}</code>"
    set_key_filter_error = "Invalid value format.\n\n<b>Key:</b> <code>{key}</code>\nCurrent value: <code>{value}</code>\nYour value: <code>{new_value}</code>\n\nFormat: {pattern}\nExample: {example}"

@admin_router.message(Role(UserRole.OWNER.value), Command("renv", "r"))
async def edit_renv(message: Message, user: User, cxt: AnswerContext):
    ok, args = await get_msg_args(message, 1, RenvTEXT.usage,
        validator = lambda len_args, target: len_args < target
    )
    if not ok:
        return

    key = args[0]

    current_value = await renv(key)
    
    if len(args) == 1:
        await cxt.answer(RenvTEXT.get_key.format(
            key = key, 
            value = current_value
        ), parse_mode = "HTML")
    else:
        key, value = args[:2]
        if pattern_example_list := renv_value_filters.get(key):
            pattern, example = pattern_example_list
            if not check_text_pattern(pattern, value):
                await cxt.answer(RenvTEXT.set_key_filter_error.format(
                    key = key,
                    value = current_value,
                    new_value = value,
                    pattern = pattern,
                    example = example,
                ), parse_mode = "HTML")
                return

        await renv(key, value)
        await cxt.answer(RenvTEXT.set_key_value.format(
            key = key, 
            value = current_value, 
            new_value = value
        ), parse_mode = "HTML")


@admin_router.message(Role(UserRole.OWNER.value), Command("renv_items", "renvs", "renv_list", "renvs_list"))
async def renv_items(message: Message, user: User, cxt: AnswerContext):
    items = await renv()
    text = ""
    for key, value in items.items():
        text += f"<b>{key}</b>: <code>{value}</code>\n"
        if pattern_example_list := renv_value_filters.get(key):
            pattern, example = pattern_example_list
            text += f"Format: {pattern} | Example: {example}\n"
        
        text += "\n"

    await cxt.answer(text, parse_mode = "HTML")