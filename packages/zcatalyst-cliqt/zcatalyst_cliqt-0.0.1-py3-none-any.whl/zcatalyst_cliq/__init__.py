# Copyright (c) 2023, ZOHO CORPORATION PRIVATE LIMITED
# All rights reserved.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


""" SDK for integrating Zoho Catalyst with Zoho Cliq """
import json
import time
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable, Union
from .error import CatalystError
from ._utils import send_request
from ._handler_util import get_handler_config, process_data
from ._handler import Handler
from .request_types import ICliqReqBody


def execute(
        integ_request,
        config: Union[str, dict],
        *args
):
    cliq_body: ICliqReqBody = integ_request.get_request_body()
    print(f'I AM INSIDE')
    print(f'ENTERED THE MAIN EXECUTE FUNCTION {integ_request}')
    print(f'IT IS CONFIG {config}')
    # handling for cli
    if isinstance(cliq_body, str):
        cliq_body = json.loads(cliq_body)

    handler_type = cliq_body.get('handler').get('type')
    if not handler_type:
        raise CatalystError('Unknown request body', 2)
    component_handler_name = cliq_body.get('type') + '_handler' if cliq_body.get('type') else handler_type
    component_type = cliq_body.get('type') if cliq_body.get('type') else handler_type

    handler_config = get_handler_config(config)
    handler_file = handler_config.get(component_handler_name)
    if not handler_file:
        raise CatalystError('Handler file missing', 2)

    if not Handler.handler_map.get(component_type):
        spec = spec_from_file_location('', handler_file)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

    if not Handler.handler_map.get(component_type):
        raise CatalystError(
            f'No handler function found for {handler_type}', 2
        )
    cliq_handler = Handler.handler_map.get(component_type).get(handler_type)
    handler_fn: Callable = cliq_handler.get('func')
    response = cliq_handler.get('resp')

    if not handler_fn or handler_fn.__class__.__name__ != 'function':
        raise CatalystError(
            f'No handler function found for {handler_type}', 2
        )

    cliq_params = process_data(cliq_body)

    handler_resp = handler_fn(cliq_params, response(), *args)

    try:
        integ_resp = json.dumps({'output': handler_resp or ''},
                                default=lambda o: dict((k, v) for k, v in o.__dict__.items() if v))
    except:
        raise CatalystError(
            f'Unable to process the response for {handler_type} ', 2
        )

    if (time.time() * 1000 - cliq_body.get('timestamp') >= 15000 and cliq_body.get('response_url')):
        resp = send_request(
            'POST',
            cliq_body['response_url'],
            json=integ_resp
        )
        if resp.status_code not in range(200, 300):
            raise CatalystError(
                'Failed to send timeout request'
            )

    return integ_resp
