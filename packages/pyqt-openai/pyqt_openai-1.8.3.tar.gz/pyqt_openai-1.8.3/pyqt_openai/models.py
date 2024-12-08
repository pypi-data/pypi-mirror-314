"""
This file is used to store the data classes that are used throughout the application.
"""

from dataclasses import dataclass, fields, field
from typing import List

from pyqt_openai import (
    DB_FILE_NAME,
    DEFAULT_FONT_SIZE,
    DEFAULT_FONT_FAMILY,
    DEFAULT_USER_IMAGE_PATH,
    DEFAULT_AI_IMAGE_PATH,
    MAXIMUM_MESSAGES_IN_PARAMETER,
    TTS_DEFAULT_VOICE,
    TTS_DEFAULT_SPEED,
    TTS_DEFAULT_AUTO_PLAY,
    TTS_DEFAULT_AUTO_STOP_SILENCE_DURATION,
    TTS_DEFAULT_PROVIDER,
)
from pyqt_openai.lang.translations import LangClass


@dataclass
class Container:
    def __init__(self, **kwargs):
        """
        You don't have to call this if you want to use default class variables
        """
        for k in self.__annotations__:
            setattr(self, k, kwargs.get(k, getattr(self, k, "")))
        for key, value in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, value)

    @classmethod
    def get_keys(cls, excludes: list = None):
        """
        Function that returns the keys of the target data type as a list.
        Exclude the keys in the "excludes" list.
        """
        if excludes is None:
            excludes = []
        arr = [field.name for field in fields(cls)]
        for exclude in excludes:
            if exclude in arr:
                arr.remove(exclude)
        return arr

    def get_values_for_insert(self, excludes: list = None):
        """
        Function that returns the values of the target data type as a list.
        """
        if excludes is None:
            excludes = []
        arr = [getattr(self, key) for key in self.get_keys(excludes)]
        return arr

    def get_items(self, excludes: list = None):
        """
        Function that returns the items of the target data type as a list.
        """
        if excludes is None:
            excludes = []
        return {key: getattr(self, key) for key in self.get_keys(excludes)}.items()

    def create_insert_query(self, table_name: str, excludes: list = None):
        if excludes is None:
            excludes = []
        """
        Function to dynamically generate an SQLite insert statement.
        Takes the table name as a parameter.
        """
        field_names = self.get_keys(excludes)
        columns = ", ".join(field_names)
        placeholders = ", ".join(["?" for _ in field_names])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return query


@dataclass
class ChatThreadContainer(Container):
    id: str = ""
    name: str = ""
    insert_dt: str = ""
    update_dt: str = ""


@dataclass
class ChatMessageContainer(Container):
    id: str = ""
    thread_id: str = ""
    role: str = ""
    content: str = ""
    insert_dt: str = ""
    update_dt: str = ""
    finish_reason: str = ""
    model: str = ""
    prompt_tokens: str = ""
    completion_tokens: str = ""
    total_tokens: str = ""
    favorite: int = 0
    favorite_set_date: str = ""
    is_json_response_available: str = 0
    is_g4f: int = 0
    provider: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class ImagePromptContainer(Container):
    id: str = ""
    model: str = ""
    width: str = ""
    height: str = ""
    provider: str = ""
    prompt: str = ""
    negative_prompt: str = ""
    n: str = ""
    quality: str = ""
    data: str = ""
    style: str = ""
    revised_prompt: str = ""
    update_dt: str = ""
    insert_dt: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class SettingsParamsContainer(Container):
    lang: str = LangClass.lang_changed()
    db: str = DB_FILE_NAME
    do_not_ask_again: bool = False
    notify_finish: bool = True
    show_secondary_toolbar: bool = True
    chat_column_to_show: List[str] = field(default_factory=ChatThreadContainer.get_keys)
    image_column_to_show: List[str] = field(
        default_factory=ImagePromptContainer.get_keys
    )
    maximum_messages_in_parameter: int = MAXIMUM_MESSAGES_IN_PARAMETER
    show_as_markdown: bool = True
    apply_user_defined_styles: bool = False
    run_at_startup: bool = True
    manual_update: bool = True

    voice_provider: str = TTS_DEFAULT_PROVIDER
    voice: str = TTS_DEFAULT_VOICE
    voice_speed: int = TTS_DEFAULT_SPEED
    auto_play_voice: bool = TTS_DEFAULT_AUTO_PLAY
    auto_stop_silence_duration: int = TTS_DEFAULT_AUTO_STOP_SILENCE_DURATION


@dataclass
class CustomizeParamsContainer(Container):
    background_image: str = ""
    user_image: str = DEFAULT_USER_IMAGE_PATH
    ai_image: str = DEFAULT_AI_IMAGE_PATH
    font_size: int = DEFAULT_FONT_SIZE
    font_family: str = DEFAULT_FONT_FAMILY


@dataclass
class PromptGroupContainer(Container):
    id: str = ""
    name: str = ""
    insert_dt: str = ""
    update_dt: str = ""
    prompt_type: str = ""


@dataclass
class PromptEntryContainer(Container):
    id: str = ""
    group_id: str = ""
    act: str = ""
    prompt: str = ""
    insert_dt: str = ""
    update_dt: str = ""
