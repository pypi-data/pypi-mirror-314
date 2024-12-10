from dataclasses import dataclass
from resource import struct_rusage
from typing import Any, Dict, List, Literal, Union
from .request_types import User

SlideType = Literal['table', 'list', 'images', 'text', 'label']
ButtonType = Literal['+', '-']
ActionType = Literal['invoke.function', 'system.api', 'open.url', 'preview.url']
CardTheme = Literal['basic', 'poll', 'modern-inline', 'prompt']
Allignment = Literal['left', 'center', 'right']
BannerStatus = Literal['success', 'failure']
PreviewType = Literal['page', 'audio', 'video', 'image']
FormFieldType = Literal[
    'text', 'checkbox', 'datetime', 'location', 'radio', 'number',
    'date', 'textarea', 'file', 'select', 'native_select', 'dynamic_select', 'hidden', 'toggle', 'phone_number'
]
FormFormat = Literal['email', 'tel', 'url', 'password']
FormFilter = Literal['organization', 'team', 'private', 'external', 'dm', 'channels', 'adhoc', 'colleagues', 'contacts', 'bots', 'skip_current_user']
FormRenderingMode = Literal['kiosk', 'classic']
FormActionMode = Literal['immediate', 'confirm']
DataSourceType = Literal['channels', 'conversations', 'contacts', 'teams']
MessageType = Literal['text', 'file', 'attachment', 'banner', 'message_edit', 'transient_message']
MessageViewType = Literal['navigation','ephemeral','popup']
FormModificationActionType = Literal['remove', 'clear', 'enable', 'disable', 'update', 'add_before', 'add_after']
WidgetButtonEmotion = Literal['positive', 'neutral', 'negative']
WidgetDataType = Literal['sections', 'info', 'map', 'form', 'web_view']
WidgetElementType = Literal[
    'title', 'text', 'subtext', 'activity', 'user_activity', 'divider', 'buttons', 'table', 'fields', 'cards', 'images', 'percentage_chart', 'graph']
WidgetEvent = Literal['load', 'refresh', 'tab_click']
WidgetType = Literal['applet']
WidgetStyleView = Literal['carousel', 'gallery']
WidgetStyleSize = Literal['small', 'medium', 'large']
WidgetStylePreview = Literal['pie', 'doughnut', 'semi_doughnut', 'vertical_bar', 'horizontal_bar', 'horizontal_stacked_bar', 'vertical_stacked_bar', 'trend']
TickerType = Literal['person', 'bicycle', 'motorcycle', 'car', 'van', 'bus', 'plane', 'home', 'office']
TickerColor = Literal['green', 'red', 'yellow']
ChannelOperation = Literal['added', 'removed', 'message_sent', 'message_edited', 'message_deleted']
SystemApiAction = Literal[
    'audiocall/{{id}}', 'videocall/{{id}}', 'startchat/{{id}}', 'invite/{{id}}', 'locationpermission', 'joinchannel/{{id}}','set_reminder']


@dataclass
class SuggestionObject:
    text: str = None
    icon: str = None


@dataclass
class SuggestionList:
    list: List[SuggestionObject] = None

    @staticmethod
    def new_suggestion(text: str = None, icon: str = None):
        return SuggestionObject(text, icon)

    def add_suggestions(self, *suggestion: SuggestionObject):
        if not self.list:
            self.list = list(suggestion)
            return len(self.list)
        self.list.extend(suggestion)
        return len(self.list)


@dataclass
class ContextParam:
    name: str = None
    question: str = None
    value: Dict[str, str] = None
    suggestions: SuggestionList = None

    def set_value(self, val: str):
        self.value = {'text': val}

    def add_suggestion(self, text: str, icon: str = None):
        if not self.suggestions:
            self.suggestions = SuggestionList()
        self.suggestions.add_suggestions(self.suggestions.new_suggestion(text, icon))


@dataclass
class Context:
    id: str = None
    timeout: int = None
    params: List[ContextParam] = None

    @staticmethod
    def new_param():
        return ContextParam()

    def add_params(self, *param: ContextParam):
        if not self.params:
            self.params = list(param)
            return len(self.params)
        self.params.extend(param)
        return len(self.params)


@dataclass
class ActionDataParams:
    content: str
    date_time: str #Expected format of dateTime is YYYY-MM-DDTHH:MM

@dataclass
class ActionData:
    name: str = None
    owner: str = None
    web: str = None
    windows: str = None
    iOS: str = None
    android: str = None
    api: str = None
    params: ActionDataParams = None


@dataclass
class Confirm:
    title: str = None
    description: str = None
    input: str = None
    buttontext: str = None
    emotion: WidgetButtonEmotion = None
    mandatory: bool = False
    button_label: str = None
    cancel_button_label: str = None



@dataclass
class Action:
    type: ActionType = None
    data: ActionData = None
    confirm: Confirm = None

    @staticmethod
    def new_action_data_obj():
        return ActionData()

    @staticmethod
    def new_confirm_object():
        return Confirm()


@dataclass
class ButtonObject:
    id: str = None
    button_id: str = None
    label: str = None
    name: str = None
    hint: str = None
    type: ButtonType = None
    key: str = None
    action: Action = None
    url: str = None
    arguments: str = None
    icon: str = None
    section_id: str = None

    @staticmethod
    def new_action_object():
        return Action()


@dataclass
class WidgetTarget:
    label: str
    id: str
    tab_id: str
    section_id: str

@dataclass
class Slide:
    type: SlideType = None
    title: str = None
    data: Any = None
    buttons: List[ButtonObject] = None
    styles: Any  = None;

    @staticmethod
    def new_button_obj():
        return ButtonObject()

    def add_buttons(self, *button: ButtonObject):
        if not self.buttons:
            self.buttons = list(button)
            return len(self.buttons)
        self.buttons.extend(button)
        return len(self.buttons)


@dataclass
class CardDetails:
    title: str = None
    icon: str = None
    thumbnail: str = None
    theme: CardTheme = None
    color: str = None
    preview: str = None


@dataclass
class FormAction:
    type: ActionType = 'invoke.function'
    name: str = None
    mode: FormActionMode = 'immediate'


@dataclass
class FormActionsObject:
    submit: FormAction = None
    cancel: FormAction = None

    @staticmethod
    def new_form_action(name: str = None):
        return FormAction(name=name)


@dataclass
class FormValue:
    label: str = None
    value: str = None


@dataclass
class Boundary:
    latitude: int = None
    longitude: int = None
    radius: int = None

@dataclass
class PhoneNumberFilter:
    country_code: List[str]

    def __init__(self, country_code: List[str]):
        self.country_code = country_code

@dataclass
class FormError:
    type = 'form_error'
    text: str = None
    inputs: Dict[str,Dict[str,str]] = None

@dataclass
class FormInput:
    type: FormFieldType = None
    trigger_on_change: bool = None
    name: str = None
    label: str = None
    hint: str = None
    placeholder: str = None
    mandatory: bool = None
    value: Any = None
    options: List[FormValue] = None
    format: FormFormat = None
    filter: Union[List[FormFilter], PhoneNumberFilter] = None
    max_length: str = None
    min_length: str = None
    max_selections: str = None
    boundary: Boundary = None
    max: int = None
    min: int = None
    multiple: bool = None
    data_source: DataSourceType = None
    auto_search_min_results: int = None
    min_characters: int = None

    @staticmethod
    def new_form_value(label: str = None, value: str = None):
        return FormValue(label, value)

    @staticmethod
    def new_boundary(latitude: int = None, longitude: int = None, radius: int = None):
        return Boundary(latitude, longitude, radius)

    def add_options(self, *form_value: FormValue):
        if not self.options:
            self.options = list(form_value)
            return len(self.options)
        self.options.extend(form_value)
        return len(self.options)

    @staticmethod
    def new_phone_number_filter(country_code: List[str]):
        return PhoneNumberFilter(country_code)


@dataclass
class Form:
    type: str
    title: str = None
    hint: str = None
    name: str = None
    version: int = None
    button_label: str = None
    trigger_on_cancel: bool = None
    actions: FormActionsObject = None
    action: FormAction = None
    inputs: List[FormInput] = None
    mode: FormRenderingMode = 'classic'


    def __init__(self,isWidget: bool = False):
        if not isWidget:
           self.type = 'form'

    @staticmethod
    def new_form_actions_obj():
        return FormActionsObject()

    @staticmethod
    def new_form_action(name: str = None):
        return FormAction(name=name)

    @staticmethod
    def new_form_input():
        return FormInput()

    def add_inputs(self, *input: FormInput):
        if not self.inputs:
            self.inputs = list(input)
            return len(self.inputs)
        self.inputs.extend(input)
        return len(self.inputs)


@dataclass
class Mention:
    name: str = None
    dname: str = None
    id: str = None
    type: str = None


@dataclass
class File:
    name: str
    id: str
    type: str
    url: str


@dataclass
class Message:
    type: MessageType = None
    mentions: List[Mention] = None
    text: str = None
    file: File = None
    comment: str = None
    status: BannerStatus = None

    @staticmethod
    def new_mention():
        return Mention()

    def add_mentions(self, *mention: Mention):
        if not self.mentions:
            self.mentions = list(mention)
            return len(self.mentions)
        self.mentions.extend(mention)
        return len(self.mentions)


@dataclass
class CommandSuggestion:
    title: str = None
    description: str = None
    imageurl: str = None

@dataclass
class ChannelTabResponse:
    label: str = None
    id: str = None
    description: str = None

@dataclass
class FormModificationAction:
    type: FormModificationActionType = None
    name: str = None
    input: FormInput = None

    @staticmethod
    def new_form_input():
        return FormInput()


@dataclass
class FormChangeResponse:
    type: str = 'form_modification'
    actions: FormModificationAction = None

    @staticmethod
    def new_form_modification_action():
        return FormModificationAction()

    def add_actions(self, *action: FormModificationAction):
        if not self.actions:
            self.actions = list(action)
            return len(self.actions)
        self.actions.extend(action)
        return len(self.actions)


@dataclass
class FormDynamicFieldResponse:
    options: List[FormValue] = None

    @staticmethod
    def new_form_value(label: str = None, value: str = None):
        return FormValue(label, value)

    def add_options(self, *option: FormValue):
        if not self.options:
            self.options = list(option)
            return len(self.options)
        self.options.extend(option)
        return len(self.options)


@dataclass
class WidgetButton:
    label: str = None
    emotion: WidgetButtonEmotion = None
    disabled: bool = None
    type: ActionType = None
    name: str = None
    url: str = None
    api: str = None
    id: str = None
    confirm: Confirm = None

    def set_api(self, api: SystemApiAction, id: str):
        self.api = api.replace('{{id}}', id)

@dataclass
class AxisInfo:
    title: str

    def __init__(self,title: str):
        self.title = title

@dataclass
class WidgetElementStyle:
    widths: List[str] = None
    alignments: List[Allignment] = None
    short: bool = None
    view: WidgetStyleView = None
    size: WidgetStyleSize = None
    preview: WidgetStylePreview = None
    x_axis: AxisInfo = None
    y_axis: AxisInfo = None

    def add_widths(self, *width: str):
        if not self.widths:
            self.widths = list(width)
            return len(self.widths)
        self.widths.extend(width)
        return len(self.widths)

    def add_alignments(self, *alignment: Allignment):
        if not self.alignments:
            self.alignments = list(alignment)
            return len(self.alignments)
        self.alignments.extend(alignment)
        return len(self.alignments)

    @staticmethod
    def new_axis_info(title: str):
        return AxisInfo(title)

@dataclass
class WidgetWebView:
    url: str

    def __init__(self,url: str):
        self.url = url

@dataclass
class MapTicker:
    title: str = None
    type: TickerType = None
    color: TickerColor = None
    info: str = None
    latitude: int = None
    longitude: int = None
    last_modified_time: int = None

@dataclass
class WidgetMap:
    title: str = None
    id: str =None
    tickers: Dict[str,MapTicker] = None

    @staticmethod
    def new_map_ticker():
        return MapTicker()

@dataclass
class WidgetInfo:
    title: str = None
    image_url: str = None
    description: str = None
    button: WidgetButton = None

    @staticmethod
    def new_widget_button():
        return WidgetButton()


@dataclass
class WidgetElement:
    type: WidgetElementType = None
    text: str = None
    description: str = None
    image_url: str = None
    buttons: List[WidgetButton] = None
    button_references: Dict[str, WidgetButton] = None
    preview_type: PreviewType = None
    user: User = None
    headers: List[str] = None
    rows: List[Dict[str, ButtonObject]] = None
    style: WidgetElementStyle = None
    styles: WidgetElementStyle = None
    data: List[Dict[str, ButtonObject]] = None

    @staticmethod
    def new_widget_button():
        return WidgetButton()

    def add_widget_buttons(self, *button: WidgetButton):
        if not self.buttons:
            self.buttons = list(button)
            return len(self.buttons)
        self.buttons.extend(button)
        return len(self.buttons)

    @staticmethod
    def new_button_object():
        return ButtonObject()

    def add_button_reference(self, name: str, button: WidgetButton):
        if not self.button_references:
            self.button_references = {}
        self.button_references[name] = button

    @staticmethod
    def new_widget_element_style():
        return WidgetElementStyle()


@dataclass
class WidgetSection:
    id: str = None
    elements: List[WidgetElement] = None
    type: str = None

    @staticmethod
    def new_widget_element():
        return WidgetElement()

    def add_elements(self, *element: WidgetElement):
        if not self.elements:
            self.elements = list(element)
            return len(self.elements)
        self.elements.extend(element)
        return len(self.elements)


@dataclass
class WidgetTab:
    id: str = None
    label: str = None


@dataclass
class WidgetResponse:
    type: WidgetType = 'applet'
    tabs: List[WidgetTab] = None
    active_tab: str = None
    data_type: WidgetDataType = None
    sections: List[WidgetSection] = None
    info: WidgetInfo = None
    web_view: WidgetWebView = None
    map: WidgetMap = None

    @staticmethod
    def new_widget_info():
        return WidgetInfo()

    @staticmethod
    def new_widget_map():
        return WidgetMap()

    @staticmethod
    def new_widget_form():
        return Form(True)

    @staticmethod
    def new_widget_web_view(url: str):
        return WidgetWebView(url)

    @staticmethod
    def new_widget_tab(
            id: str = None,
            label: str = None
    ):
        return WidgetTab(id, label)

    @staticmethod
    def new_widget_section():
        return WidgetSection()

    def add_tab(self, *tab: WidgetTab):
        if not self.tabs:
            self.tabs = list(tab)
            return len(self.tabs)
        self.tabs.extend(tab)
        return len(self.tabs)

    def add_sections(self, *widget_section: WidgetSection):
        if not self.sections:
            self.sections = list(widget_section)
            return len(self.sections)
        self.sections.extend(widget_section)
        return len(self.sections)


@dataclass
class InstallationResponse:
    status: int = 200
    title: str = None
    message: str = None
    note: List[str] = None
    footer: str = None

    def add_notes(self, *note: str):
        if not self.notes:
            self.note = list(note)
            return len(self.note)
        self.note.extend(note)
        return len(self.note)
