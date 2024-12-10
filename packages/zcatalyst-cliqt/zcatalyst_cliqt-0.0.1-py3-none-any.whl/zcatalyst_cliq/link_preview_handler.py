from dataclasses import dataclass
from typing import Any, Callable, Tuple, Dict, List
from ._handler import Handler
from .handler_response import HandlerResponse
from . import _constants as Constants
from ._constants import Handlers
from .request_types import (
    Access,
    Environment,
    User,
    Chat
)

@dataclass
class LinkPreviewHandlerRequest:
    user: User
    chat: Chat
    environment: Environment
    access: Access
    url: str
    domain: str
    target: Dict[str,Any]

def preview_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.PREVIEW_HANDLER,
        func,
        HandlerResponse
    )

def action_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.ACTION_HANDLER,
        func,
        HandlerResponse
    )

def menu_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.MENU_HANDLER,
        func,
        HandlerResponse
    )

def after_send_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.AFTER_SEND_HANDLER,
        func,
        HandlerResponse
    )