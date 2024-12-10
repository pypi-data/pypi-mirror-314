import json
from . import _utils
from os import path
from typing import Union
from .request_types import ICliqReqBody
from .error import CatalystError
from . import _constants as Constants

HANDLERS_LIST = [
    'bot_handler',
    'command_handler',
    'messageaction_handler',
    'widget_handler',
    'function_handler',
    'link_preview_handler',
    'extension_handler'
]


class CliqReq:
    def __init__(self, dict_obj):
        self.__dict__.update(dict_obj)


def get_handler_config(config: Union[str, dict]):
    if not isinstance(config, (str, dict)):
        raise CatalystError(
            'handler config expected to be dict or a string file path'
        )
    handler_config = parse_config(config)
    return validate_handler_config(handler_config)


def parse_config(config) -> dict:
    if isinstance(config, dict):
        return config
    fn_root = _utils.get_function_root()
    try:
        with open(path.normpath(path.join(fn_root, config)), encoding="utf-8") as json_file:
            json_dict = json.load(json_file)
    except:
        raise CatalystError(
            f'Unable to parse the config json from the file path: {config}'
        ) from None
    return json_dict


def validate_handler_config(handler_config: dict):
    if not handler_config:
        raise CatalystError(
            'handler config should not be empty'
        )
    cliq_config = handler_config.get(Constants.CLIQ)
    if not cliq_config:
        raise CatalystError(
            'integration_config for service ZohoCliq is not found'
        )

    cliq_handlers: dict = cliq_config.get('handlers')
    if not cliq_handlers:
        raise CatalystError(
            'Handlers is empty'
        )

    fn_root = _utils.get_function_root()
    for handler in cliq_handlers.keys():
        if handler not in HANDLERS_LIST:
            raise CatalystError(
                f'Unknown handler: {handler}'
            )
        handler_file = cliq_handlers.get(handler)
        handler_filepath = path.abspath(path.join(fn_root, handler_file))
        if not path.exists(handler_filepath):
            raise CatalystError(
                f'Handler file {handler_file} provided for {handler} does not exist'
            )
        cliq_handlers[handler] = handler_filepath

    return cliq_handlers


def process_data(cliq_body: ICliqReqBody) -> CliqReq:
    params = cliq_body.get('params')
    req_type = cliq_body.get('type')
    if not params:
        raise CatalystError('No params found in request body', 2)

    if req_type == Constants.BOT:
        params.update({
            'name': cliq_body.get('name'),
            'unique_name': cliq_body.get('unique_name')
        })
        if cliq_body.get('handler').get('type') == Constants.Handlers.BotHandler.ACTION_HANDLER:
            params.update({
                'action_name': cliq_body.get('handler').get('name')
            })
    elif req_type in [Constants.FUNCTION, Constants.COMMAND, Constants.MESSAGEACTION]:
        params.update({
            'name': cliq_body.get('name')
        })
    return json.loads(json.dumps(params), object_hook=CliqReq)
