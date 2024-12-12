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

async def get_renv_keys() -> dict:
    all_redis_items = await async_redis.keys("*")
    all_keys = [item.decode() for item in all_redis_items]
    # filter FSM and throttle keys
    all_keys = [key for key in all_keys if not key.startswith("throttle_antiflood") and not key.startswith("fsm")]
    all_items = await async_redis.mget(all_keys)
    # convert all_items to dict
    all_items = {key: item.decode() for key, item in zip(all_keys, all_items)}
    return all_items


async def renv(key: str = None, value: str | bool = None) -> str | bool | dict | None:
    if key is None:
        return await get_renv_keys()
    
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
