from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict, Literal

MessageType = Literal['text', 'file', 'attachment', 'banner', 'message_edit', 'transient_message']
ButtonType = Literal['+', '-']
OrganizationType = Literal['company', 'network']
ChatType = Literal['channel', 'bot', 'dm', 'chat', 'crossproduct_custom_chat', 'entity_chat', 'guests', 'threads', 'thread']
ChannelOperation = Literal['added', 'removed', 'message_sent', 'message_edited', 'message_deleted', 'auto_followed_thread', 'added_in_thread', 'removed_from_thread', 'thread_closed', 'thread_reopened']
BotAlertOperation = Literal['default_state', 'busy', 'ringing', 'answered', 'ended', 'declined', 'missed', 'offline']

@dataclass
class Organization:
    type: OrganizationType
    id: int

@dataclass
class Access:
    zoho_user_id: int
    user_id: int
    user_agent: str
    chat_id: str
    organization: Organization
    message_id: str
    platform_version: Optional[str]
    parent_chat_id: Optional[str]

@dataclass
class AppInfo:
    current_version: str
    existing_version: str
    type: Literal["install", "upgrade"]


@dataclass
class Attachment:
    name: str
    comment: str
    id: str
    url: str
    contenttype: str


@dataclass
class BotDetails:
    name: str
    image: str

@dataclass
class MessageStyles:
    highlight: bool

@dataclass
class ActionData:
    name: Optional[str]
    owner: Optional[str]
    web: Optional[str]
    windows: Optional[str]
    iOS: Optional[str]
    android: Optional[str]
    api: Optional[str]


@dataclass
class Confirm:
    title: Optional[str]
    description: Optional[str]
    input: Optional[str]
    button_text: Optional[str]


@dataclass
class Action:
    type: Optional[str]
    data: Optional[ActionData]
    confirm: Optional[Confirm]


@dataclass
class ButtonObject:
    id: Optional[str]
    button_id: Optional[str]
    label: Optional[str]
    name: Optional[str]
    hint: Optional[str]
    type: Optional[ButtonType]
    key: Optional[str]
    action: Optional[Action]
    url: Optional[str]


@dataclass
class Button:
    type: Literal['button']
    object: ButtonObject


@dataclass
class ButtonArguments:
    key: str


@dataclass
class Member:
    id: str
    first_name: str
    last_name: str
    email: str
    status: str


@dataclass
class Sender:
    name: str
    id: str


@dataclass
class RecentMessage:
    sender: Sender
    time: int
    text: str
    id: str
    type: str


@dataclass
class Chat:
    owner: int
    id: str
    type: str
    title: str
    members: List[Member]
    recent_messages: List[RecentMessage]
    channel_unique_name: str
    chat_type: ChatType
    channel_id: str
    entity_id: str


@dataclass
class Dimension:
    size: int
    width: int
    height: int


@dataclass
class FileContent:
    name: str
    id: str
    type: str
    dimensions: Dimension


@dataclass
class Thumbnail:
    width: str
    blur_data: str
    height: str


@dataclass
class Content:
    thumbnail: Thumbnail
    file: FileContent
    comment: str
    text: str


@dataclass
class DateTimeObject:
    date_time: str
    time_zone_id: str

@dataclass
class ExtensionDetails:
    version: str

@dataclass
class Environment:
    data_center: str
    base_url: str
    tld: str
    extension: ExtensionDetails


@dataclass
class File:
    name: str
    id: str
    type: str
    url: str


@dataclass
class FormRequestParam:
    name: str
    action: str
    values: Any


@dataclass
class FormValue:
    label: Optional[str]
    value: Optional[str]


@dataclass
class FormTarget:
    name: str
    value: Any
    query: str


@dataclass
class Location:
    latitude: int
    longitude: int
    accuracy: int
    altitude: int
    status: Literal['granted', 'prompt', 'denied', 'failed']


@dataclass
class LocationValue:
    latitude: int
    longitude: int


@dataclass
class Mention:
    name: str
    dname: str
    id: str
    type: str


@dataclass
class Message:
    type: str
    mentions: Optional[List[Mention]]
    text: Optional[str]
    file: Optional[File]
    comment: Optional[str]
    status: Optional[str]


@dataclass
class MessageDetails:
    time: int
    message: Message;


@dataclass
class User:
    id: str
    first_name: str
    last_name: str
    email: str
    admin: bool
    organization_id: int
    timezone: str
    country: str
    language: str
    name: str


@dataclass
class MessageObject:
    sender: User
    time: int
    type: MessageType
    text: str
    is_read: bool
    ack_key: str
    id: str
    content: Content

@dataclass
class Messages:
    count: int
    list: List[MessageObject]

@dataclass
class SuggestionObject:
    text: str
    icon: str


@dataclass
class CommandSuggestion:
    title: Optional[str]
    description: Optional[str]
    imageurl: Optional[str]


class ICliqReqHandler(TypedDict):
    type: str
    name: Optional[str]


class ICliqReqBody(TypedDict):
    name: str
    unique_name: str
    handler: ICliqReqHandler
    response_url: str
    type: str
    timestamp: int
    params: Dict[str, Any]

# ######******######
# #new formats starts
# SlideType = Literal['table', 'list', 'images', 'text', 'label']
# ButtonType = Literal['+', '-']
# ActionType = Literal['invoke.function', 'system.api', 'open.url', 'preview.url']
# CardTheme = Literal['default', 'poll', 'modern-inline', 'prompt']
# Allignment = Literal['left', 'center', 'right']
# BannerStatus = Literal['success', 'failure']
# PreviewType = Literal['page', 'audio', 'video', 'image']
# FormFieldType = Literal[
#     'text', 'checkbox', 'datetime', 'location', 'radio', 'number', 
#     'date', 'textarea', 'file', 'select', 'native_select', 'dynamic_select', 'hidden'
#     ]
# FormFormat = Literal['email', 'tel', 'url', 'password']
# DataSourceType = Literal['channels', 'conversations', 'contacts', 'teams']
# MessageType = Literal['text', 'file', 'attachment', 'banner', 'message_edit', 'transient_message']
# FormModificationActionType = Literal['remove', 'clear', 'enable', 'disable', 'update', 'add_before', 'add_after']
# WidgetButtonEmotion = Literal['positive', 'neutral', 'negative']
# WidgetDataType = Literal['sections', 'info']
# WidgetElementType = Literal['title', 'text', 'subtext', 'activity', 'user_activity', 'divider', 'buttons', 'table', 'fields']
# WidgetEvent = Literal['load', 'refresh', 'tab_click']
# WidgetType = Literal['applet']
# ChannelOperation = Literal['added', 'removed', 'message_sent', 'message_edited', 'message_deleted']
# SystemApiAction = Literal['audiocall/{{id}}', 'videocall/{{id}}', 'startchat/{{id}}', 'invite/{{id}}', 'locationpermission', 'joinchannel/{{id}}']

# ##handler response starts
# class CardDetails(TypedDict):
#     title: str
#     icon: str
#     thumbnail: str
#     theme: CardTheme

# class ButtonObject(TypedDict):
#     id: str
#     button_id: str
#     label: str
#     name: str
#     hint: str
#     type: ButtonType
#     key: str
#     action: Action
#     url: str

# class Slide(TypedDict):
#     type: SlideType
#     title: str
#     data: Any
#     buttons: List[ButtonObject]

# class SuggestionList(TypedDict):
# 	list: List[SuggestionObject]

# class ContextParam(TypedDict):
#     name: str
#     question: str
#     value: Dict[str,str]
#     suggestions: SuggestionList

# class Context(TypedDict):
#     id: str
#     timeout: int
#     params: List[ContextParam]

# class HandlerResponse(TypedDict):
# 	text: str
# 	context: Context
# 	bot: BotDetails
# 	suggestions: SuggestionList
# 	slides: List[Slide]
# 	buttons: List[ButtonObject]
# 	card: CardDetails
# #handler response ends

# #handler cs resp starts
# class CommandSuggestion(TypedDict):
#     title: str
#     description: str
#     imageurl: str
# #handler cs resp ends

# #form change response starts
# class Boundary(TypedDict):
#     latitude: int
#     longitude: int
#     radius: int

# class FormInput(TypedDict):
#     type: FormFieldType
#     trigger_on_change: bool
#     name: str
#     label: str
#     hint: str
#     placeholder: str
#     mandatory: bool
#     value: Any
#     options: List[FormValue]
#     format: FormFormat
#     max_length: str
#     min_length: str
#     max_selections: str
#     boundary: Boundary
#     max: int
#     min: int
#     multiple: bool
#     data_source: DataSourceType
#     auto_search_min_results: int
#     min_characters: int

# class FormModificationAction(TypedDict):
# 	type: FormModificationActionType
# 	name: str
# 	input: FormInput

# class FormChangeResponse(TypedDict):
#     type: Literal['form_modification']
#     actions: FormModificationAction
# #form change response ends


# #form dynamic response starts
# class FormDynamicFieldResponse(TypedDict):
#     options: List[FormValue]
# #form dynamic response ends


# #form widget response starts
# class WidgetButton(TypedDict):
# 	label: str
# 	emotion: WidgetButtonEmotion
# 	disabled: bool
# 	type: ActionType
# 	name: str
# 	url: str
# 	api: str
# 	id: str


# class WidgetElementStyle(TypedDict):
#     widths: List[str]
#     alignments: List[Allignment]
#     short: bool


# class WidgetInfo(TypedDict):
# 	title: str
# 	image_url: str
# 	description: str
# 	button: WidgetButton


# class WidgetElement(TypedDict):
#     type: WidgetElementType
#     text: str
#     description: str
#     image_url: str
#     buttons: List[WidgetButton]
#     button_references: Dict[str,ButtonObject]
#     preview_type: PreviewType
#     user: User
#     headers: List[str]
#     rows: List[Dict[str,ButtonObject]]
#     style: WidgetElementStyle
#     data: List[Dict[str,ButtonObject]]


# class WidgetSection(TypedDict):
#     elements: List[WidgetElement]
#     type: str

# class WidgetTab(TypedDict):
# 	id: str
# 	label: str

# class WidgetResponse(TypedDict):
#     type: WidgetType
#     tabs: List[WidgetTab]
#     active_tab: str
#     data_type: WidgetDataType
#     sections: List[WidgetSection]
#     info: WidgetInfo
# #form widget response ends
