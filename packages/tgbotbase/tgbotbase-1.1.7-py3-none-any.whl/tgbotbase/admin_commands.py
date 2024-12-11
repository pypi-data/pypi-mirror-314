from typing import Any

from aiogram.filters import Command
from aiogram.types import Message

from tgbotbase.answer import AnswerContext
from tgbotbase.filters import Role
from tgbotbase.utils import SHARED_OBJECTS, check_text_pattern, get_msg_args, logger

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


@admin_router.message(Role(UserRole.OWNER.value), Command("renv"))
async def edit_renv(message: Message, user: User, cxt: AnswerContext):
    ok, args = await get_msg_args(message, 1, (
        "Usage:\n"
        "/renv KEY\n"
        "/renv KEY VALUE\n"
        ),
        validator = lambda len_args, target: len_args < target
    )
    if not ok:
        return

    current_value = await async_redis.get(args[0])
    current_value = current_value.decode() if current_value else None
    
    if len(args) == 1:
        await cxt.answer(f"Текущее значение: {current_value}")
    else:
        key, value = args[:2]
        if key in renv_value_filters:
            pattern, example = renv_value_filters[key]
            if not check_text_pattern(pattern, value):
                await cxt.answer(f"Неверный формат значения.\nТекущее значение: {current_value}\nВаше значение: {value}\n\nФормат: {pattern}\nПример: {example}")
                return

        await async_redis.set(key, value)
        await cxt.answer(f"Установлено значение: {current_value} -> {value}")
