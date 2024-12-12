from pydantic.v1 import BaseModel, conlist, validator
from typing import Any, Dict, Literal


NOTECOLORS = ["note-color-1", "note-color-2", "note-color-3",
              "note-color-4", "note-color-5", "note-color-6",
              "note-color-7", "note-color-8"]


bot_states = ('initial', 'queued', 'processing', 'streaming',
              'success', 'incomplete', 'canceled', 'error')


class NoteTypeSpecific(BaseModel):
    title: str = ""
    message: str = ""
    color: Literal[tuple(NOTECOLORS)] = NOTECOLORS[0]
    auto_size: bool = True
    attachments: Dict[str, Dict[str, str]] = {}


class SetupTypeSpecific(BaseModel):
    bot_type: str = "chat-gpt-35"
    setup_args: Dict[str, Any] = {"system_setup": ""}
    auto_size: bool = True


class BotTypeSpecific(BaseModel):
    prompt_input: str = ""
    prompt_output: str = ""
    auto_size: bool = True
    split_size: conlist(float, min_items=2, max_items=2) = [16.73, 83.27]
    state: Literal[bot_states] = "initial"
    attachments: Dict[str, Dict[str, str]] = {}

    @validator("split_size")
    def check_split_size(cls, s):
        sum_s = sum(s)

        if not (
            s[0] >= 0 and
            s[1] >= 0 and
            sum_s > 0
        ):
            return [16.73, 83.27]

        return [s[0] * 100 / sum_s, s[1] * 100 / sum_s]


class VectorStoreTypeSpecific(BaseModel):
    vector_store_file: str = ""
    vector_store_file_type: str = ""
    state: Literal[bot_states] = "queued"


class FrameTypeSpecific(BaseModel):
    color: Literal[tuple(NOTECOLORS)] = NOTECOLORS[0]


NODES = {
    "note": NoteTypeSpecific,
    "setup": SetupTypeSpecific,
    "bot": BotTypeSpecific,
    "vector-store-file": VectorStoreTypeSpecific,
    "frame": FrameTypeSpecific,
}
