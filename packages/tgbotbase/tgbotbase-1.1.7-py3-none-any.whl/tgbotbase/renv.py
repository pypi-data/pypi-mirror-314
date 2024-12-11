from tgbotbase.utils import logger, SHARED_OBJECTS

async_redis = SHARED_OBJECTS.get("async_redis")

if async_redis is None:
    logger.warning(
        "async_redis is not initialized to SHARED_OBJECTS, add it as value to key 'async_redis' to SHARED_OBJECTS"
    )


# check default REDIS keys
async def check_renv(default_keys: dict):
    for key, default_value in default_keys.items():
        current_value = await renv(key)
        if current_value is None:
            await renv(key, default_value)
            logger.warning(f"[RENV] Added default key {key} with value {default_value}")


async def renv(key: str, value: str | bool = None) -> str | bool | None:
    if value is None:
        current_value = await async_redis.get(key)
        current_value = current_value.decode() if current_value else None

        if current_value in ["true", "false"]:
            current_value = current_value == "true"

        return current_value
    else:
        if isinstance(value, bool):
            value = "true" if value else "false"

        await async_redis.set(key, value)
        logger.warning(f"[RENV] Set {key}={value}")
