from functools import partial
from sys import stderr
from typing import Any
import os
import ruamel.yaml
from loguru import logger
from pywebio import config, start_server
from pywebio.output import (
    put_button,
    put_collapse,
    put_info,
    put_markdown,
    put_scope,
    put_table,
    toast,
    clear,
    put_text,
)
from pywebio.pin import pin_on_change, put_textarea
from pywebio.session import set_env
from pywebio_battery.web import basic_auth

# for local debugging
try:
    from src.models import ProductPart  # type: ignore
except ImportError:
    class ProductPart(Any): ...

undefined = object()
# https://stackoverflow.com/questions/72732098/keeping-comments-in-ruamel-yaml
def my_pop(self, key, default=undefined):
    if key not in self:
        if default is undefined:
            raise KeyError(key)
        return default
    keys = list(self.keys())
    idx = keys.index(key)
    if key in self.ca.items:
        if idx == 0:
            raise NotImplementedError('cannot handle moving comment when popping the first key', key)
        prev = keys[idx-1]
        # print('prev', prev, self.ca)
        comment = self.ca.items.pop(key)[2]
        if prev in self.ca.items:
            self.ca.items[prev][2].value += comment.value
        else:
            self.ca.items[prev] = self.ca.items.pop(key)
    res = self.__getitem__(key)
    self.__delitem__(key)
    return res

ruamel.yaml.comments.CommentedMap.pop = my_pop

yaml = ruamel.yaml.YAML()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
COOKIE_SECRET = os.getenv("COOKIE_SECRET")
if not COOKIE_SECRET or not ADMIN_PASSWORD:
    logger.critical(f"[Uniserver init error] COOKIE_SECRET or ADMIN_PASSWORD is None | {COOKIE_SECRET=}, {ADMIN_PASSWORD=}")
    exit(1)

class UniServerHelper:
    locales = {
        "ru": "./locales/bot.ru.yml",
        "en": "./locales/bot.en.yml",
    }
    locale_data = {}
    memory_areas = {}
    old_values = {}

    @staticmethod
    def load_locales():
        for locale, path in UniServerHelper.locales.items():
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.load(f)

            UniServerHelper.locale_data[locale] = {
                "data": data,
                "normalized": UniServerHelper.normalize_locale_data(data),
            }

    @staticmethod
    # normalize to just key: value
    def normalize_locale_data(data: dict, prev_key: str = "") -> dict:
        # normalize dict like
        # {key1: {key2: value}}
        # to
        # {key1.key2: value}
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result.update(UniServerHelper.normalize_locale_data(value, (prev_key + "-" if prev_key else "") + key))
            else:
                result[f"{prev_key}-{key}"] = value
        return result

    @staticmethod
    def update_value(data: dict, setting_id: str, new_value: str):
        # Разбиваем setting_id на части
        keys = setting_id.split('-')
        
        # Проверяем, есть ли ключи в словаре
        current_level = data
        for key in keys[:-1]:
            if key not in current_level:
                current_level[key] = {}  # Создаем новый уровень, если его нет
            current_level = current_level[key]
        
        # Обновляем значение
        current_level[keys[-1]] = new_value

    @staticmethod
    def change_memory_area_value(key, _, value):
        logger.info(f"Updated {key} {value}")
        UniServerHelper.memory_areas[key] = value

    @staticmethod
    def save_locale_value_to_db(setting_id: str):
        for locale, path in UniServerHelper.locales.items():
            old_value = UniServerHelper.old_values.get(f"area_{setting_id}_{locale}", "")
            new_value = UniServerHelper.memory_areas.get(f"area_{setting_id}_{locale}", "")
            logger.info(f"[{locale.upper()}] Save {setting_id=} from `{old_value}` to `{new_value}`")

            UniServerHelper.update_value(UniServerHelper.locale_data[locale]["data"], f"{locale}-{setting_id[3:]}", new_value)

            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(UniServerHelper.locale_data[locale]["data"], f)

            if len(new_value) < 15:
                toast(f"[{locale.upper()}] Saved: `{old_value}` -> `{new_value}`")
            else:
                toast(f"[{locale.upper()}] Saved: `{old_value[:12]}...` -> `{new_value[:12]}...`")

            UniServerHelper.old_values[f"area_{setting_id}_{locale}"] = new_value

    @staticmethod
    def put_block_locales():
        first_locale_name = list(UniServerHelper.locales.keys())[0]

        header = ["Name"] + [f"Text {locale}" for locale in UniServerHelper.locales.keys()] + ["Save"]

        content = [
            put_text("Add new locale key", scope = "new_text"),
            put_scope("new_text"),
            put_scope("edit_new_text"),
        ]

        for key, value in UniServerHelper.locale_data[first_locale_name]["normalized"].items():
            content.append([key.replace(f'{first_locale_name}-', '')] + 
                [put_scope(f"area_{key}_{locale}") for locale in UniServerHelper.locales.keys()] +
                [put_scope(f"edit_{key}")])

        content.append([" "] + [" "*150 for _ in UniServerHelper.locales.keys()] + [" "])
        
        put_collapse("Текста",
            content = [
                put_table([
                    header,
                    *content
                ])
        ], open = True)


        for key, value in UniServerHelper.locale_data[first_locale_name]["normalized"].items():
            # count all lines len > 150 
            extra_rows = [lc:= 0, [lc := lc + 1 for x in str(value).split('\n') if len(x) > 150], lc][-1]
            put_textarea(f"area_{key}_{first_locale_name}", rows = str(value).count('\n') + extra_rows, value = str(value), readonly = False, scope = f"sarea_{key}_{first_locale_name}")
            
            for locale, path in UniServerHelper.locales.items():
                if locale == first_locale_name:
                    continue

                other_value = str(UniServerHelper.locale_data[locale]["normalized"].get(key.replace(f"{first_locale_name}-", f"{locale}-"), "-"))
                put_textarea(f"area_{key}_{locale}", rows = other_value.count('\n') + extra_rows, value = other_value, readonly = False, scope = f"sarea_{key}_{locale}")
                
            put_button("Save", onclick = partial(save_new_area_value, key), scope = f"edit_{key}", color = "info")

        for key, value in UniServerHelper.locale_data[first_locale_name]["normalized"].items():
            name = f"area_{key}"
            UniServerHelper.memory_areas[f"{name}_{first_locale_name}"] = value
            UniServerHelper.old_values[f"{name}_{first_locale_name}"] = value
            pin_on_change(f"{name}_{first_locale_name}", onchange = partial(UniServerHelper.change_memory_area_value, f"{name}_{first_locale_name}", value))
            
            
            for locale, value in UniServerHelper.locale_data.items():
                if locale == first_locale_name:
                    continue

                UniServerHelper.memory_areas[f"{name}_{locale}"] = UniServerHelper.locale_data[locale]["normalized"].get(key.replace(f"{first_locale_name}-", f"{locale}-"), "-")
                UniServerHelper.old_values[f"{name}_{locale}"] = UniServerHelper.locale_data[locale]["normalized"].get(key.replace(f"{first_locale_name}-", f"{locale}-"), "-")
                pin_on_change(f"{name}_{locale}", onchange = partial(UniServerHelper.change_memory_area_value, f"{name}_{locale}", value))

        put_textarea("new_text", rows = 1, value = "", readonly = False, scope = "new_text")
        put_button("Save", 
                onclick = partial(save_new_area_value, "add_new_text"), 
                scope = "edit_new_text", color = "info")
        pin_on_change("new_text", onchange = partial(UniServerHelper.change_memory_area_value, "new_text", ""))


    @staticmethod
    def put_on(row_id: int, handler_on, handler_off, initial: bool = True):
        scope = f"enable_{row_id}"
        clear(scope=scope)
        put_button("ON", scope=scope, color = "success",
                onclick=lambda: UniServerHelper.put_off(row_id, handler_on, handler_off, False))  

        if not initial:
            handler_off(row_id)

    @staticmethod
    def put_off(row_id: int, handler_on, handler_off, initial: bool = True):
        scope = f"enable_{row_id}"
        clear(scope=scope)
        put_button("OFF", scope=scope, color = "danger",
                onclick=lambda: UniServerHelper.put_on(row_id, handler_on, handler_off, False))

        if not initial:
            handler_on(row_id)

file_log = './logs/uniserver.log'
log_format = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <level>{message}</level>"
logger.remove()
logger.add(stderr, format = log_format)
logger.add(file_log, format = log_format, rotation="7days", compression="zip", backtrace=True, diagnose=True)
logger.level("DEBUG", color='<magenta>')

def save_new_area_value(setting_id):
    logger.info(f"save new area value {setting_id}")
    if setting_id.startswith("edit_price_"):
        part_id = setting_id.replace("edit_price_", "")
        part: ProductPart = ProductPart.get(
            ProductPart.id == int(part_id))
        toast(f"`{part.name.replace('buttons.', '').capitalize()}` price was changed: {part.price} -> {UniServerHelper.memory_areas[f'price_{part_id}']}")
        part.price = UniServerHelper.memory_areas[f"price_{part_id}"]
        part.save()
        return
    
    if setting_id == "add_new_text":
        UniServerHelper.save_locale_value_to_db(f"ru-{UniServerHelper.memory_areas['new_text']}")
        toast(f"New text was added: {UniServerHelper.memory_areas['new_text']} | Refresh page")
        return

    if "ru-" in setting_id:
        UniServerHelper.save_locale_value_to_db(setting_id)

#("default", "dark", "sketchy", "minty", "yeti")
@config(theme = "minty")
def main():
    basic_auth(lambda username, password: username == 'admin' and password == ADMIN_PASSWORD,
                      secret=COOKIE_SECRET)
    #put_text("Hello, %s. You can refresh this page and see what happen" % user_name)

    UniServerHelper.load_locales()

    set_env(
        title = "UniServerEditor by @abuztrade",
        output_animation = False,
        output_max_width = "90%"
    )

    put_markdown("# UniServerEditor by @abuztrade")

    UniServerHelper.put_block_locales()

    put_info("Any error? Send feedback: https://abuztrade.t.me")

if __name__ == '__main__':
    logger.info("UniServerEditor by @abuztrade.")

    PORT = 3055

    try:
        start_server(
            main, 
            port = PORT, 
            auto_open_webbrowser = True
        )
    except OSError:
        logger.error("OSError: Server already running")
        input()
