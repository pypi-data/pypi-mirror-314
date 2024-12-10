from dataclasses import dataclass
from typing import Any, Callable, Tuple, TypedDict, List
from .response_types import WidgetEvent, WidgetResponse, ChannelTabResponse, WidgetTarget
from ._handler import Handler
from . import _constants as Constants
from ._constants import Handlers
from .request_types import (
    Access,
    Environment,
    User,
    Chat,
    Location
)


@dataclass
class WidgetRequest:
    user: User
    environment: Environment
    access: Access
    chat: Chat

@dataclass
class WidgetExecutionHandlerRequest(WidgetRequest):
    target: WidgetTarget
    event: WidgetEvent
    location: Location



def view_handler(
        func: Callable[
            [WidgetExecutionHandlerRequest, WidgetResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.WIDGET,
        Handlers.WidgetHandler.VIEW_HANDLER,
        func,
        WidgetResponse
    )

def channel_tab_handler(
        func: Callable[
            [WidgetRequest, List[ChannelTabResponse], Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.WIDGET,
        Handlers.WidgetHandler.CHANNEL_TAB_HANDLER,
        func,
        list
    )

def new_widget_response():
    return WidgetResponse()

def new_channel_tab_handler(label: str = None,id: str = None,description: str = None):
    return ChannelTabResponse(label,id,description)
