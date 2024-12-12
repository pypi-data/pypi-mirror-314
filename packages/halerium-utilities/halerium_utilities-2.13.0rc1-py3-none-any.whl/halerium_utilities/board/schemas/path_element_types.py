from typing import Dict, List, Literal, Optional
from pydantic.v1 import BaseModel


# Define the ActionType as a Literal
ActionType = Literal["run", "run-tree"]


class TaskAction(BaseModel):
    nodeId: str
    type: ActionType


class NoteLinkTypeSpecific(BaseModel):
    title: str = ""
    message: str = ""
    attachments: Dict[str, Dict[str, str]] = {}
    linkedNodeId: Optional[str] = None


class BotLinkTypeSpecific(BaseModel):
    prompt_input: str = ""
    prompt_output: str = ""
    attachments: Dict[str, Dict[str, str]] = {}
    linkedNodeId: Optional[str] = None


class ActionChainTypeSpecific(BaseModel):
    actions: List[TaskAction]
    actionLabel: Optional[str] = None


ELEMENTS = {
    "note": NoteLinkTypeSpecific,
    "bot": BotLinkTypeSpecific,
    "action-chain": ActionChainTypeSpecific,
}
