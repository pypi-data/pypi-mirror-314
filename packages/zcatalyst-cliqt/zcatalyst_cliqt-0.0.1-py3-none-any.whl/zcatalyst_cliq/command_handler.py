from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple, TypedDict
from ._handler import Handler
from . import _constants as Constants
from ._constants import Handlers
from .request_types import (
    Access,
    Chat,
    Environment,
    File,
    Location,
    Mention,
    User,
    CommandSuggestion as CommandSuggestionReq

)
from .handler_response import HandlerResponse
from .response_types import CommandSuggestion


@dataclass
class CommandHandlerRequest:
    name: str
    location: Location
    mentions: List[Mention]
    user: User
    chat: Chat
    environment: Environment
    access: Access
    arguments: str
    options: Dict[str, str]
    selections: List[CommandSuggestionReq]
    attachments: List[File]


def execution_handler(
        func: Callable[
            [CommandHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.COMMAND,
        Handlers.CommandHandler.EXECUTION_HANDLER,
        func,
        HandlerResponse
    )


def suggestion_handler(
        func: Callable[
            [CommandHandlerRequest, List[CommandSuggestion], Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.COMMAND,
        Handlers.CommandHandler.SUGGESTION_HANDLER,
        func,
        list
    )


def new_handler_response():
    return HandlerResponse()


def new_command_suggestion(
        title: str = None,
        desc: str = None,
        image_url: str = None
):
    return CommandSuggestion(title, desc, image_url)
