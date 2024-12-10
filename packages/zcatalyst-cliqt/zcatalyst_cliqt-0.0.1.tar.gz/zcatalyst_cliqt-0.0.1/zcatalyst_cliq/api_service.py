from io import BufferedReader
from typing import List, Union
from zcatalyst_sdk._http_client import HttpClient
from zcatalyst_sdk.connection import Connector
from . import _constants as ApiConstants


class ApiUtil:
    def __init__(self, connector: Connector):
        self._connection = connector
        self._requester = HttpClient()

    def send_request(self, url, **kwargs):
        resp = self._requester.request(
            'POST',
            url,
            headers={
                'Authorization': ApiConstants.OAUTH_PREFIX + self._connection.get_access_token(),
                'User-Agent': ApiConstants.USER_AGENT
            },
            **kwargs
        )
        return resp


class CliqApiService:
    def __init__(self, connector: Connector):
        self._api = ApiUtil(connector)

    def post_to_channel(
            self,
            channel_unique_name: str,
            payload: Union[str, BufferedReader],
            bot_unique_name: str = None
    ):
        file = None
        message = None
        url = ApiConstants.POST_TO_CHANNEL_URL + channel_unique_name
        if isinstance(payload, str):
            url += ApiConstants.MESSAGE
            message = {
                'text': payload
            }
        elif isinstance(payload, BufferedReader):
            url += ApiConstants.FILES
            file = {
                'file': payload
            }
        query_params = {}
        if bot_unique_name:
            query_params = {
                ApiConstants.BOT_UNIQUE_NAME: bot_unique_name
            }
        resp = self._api.send_request(
            url=url,
            params=query_params,
            files=file,
            json=message
        )
        return resp

    def post_to_channel_as_bot(
            self,
            channel_unique_name: str,
            payload: Union[str, BufferedReader],
            bot_unique_name: str
    ):
        self.post_to_channel(
            channel_unique_name,
            payload,
            bot_unique_name
        )

    def post_to_bot(
            self,
            bot_unique_name: str,
            payload: Union[str, BufferedReader],
            delivery_info: Union[bool, List[str]]
    ):
        file = None
        message = None
        url = ApiConstants.POST_TO_BOT_URL + bot_unique_name
        if isinstance(payload, str):
            url += ApiConstants.MESSAGE
            message = {
                'text': payload
            }
            if isinstance(delivery_info, bool):
                message[ApiConstants.BROADCAST] = delivery_info
            elif isinstance(delivery_info, list):
                message[ApiConstants.BROADCAST] = False
                message[ApiConstants.USERIDS] = ','.join(delivery_info)

        elif isinstance(payload, BufferedReader):
            url += ApiConstants.FILES
            file = {
                'file': payload
            }
        resp = self._api.send_request(
            url=url,
            files=file,
            json=message
        )
        return resp

    def post_to_chat(
            self,
            chat_id: str,
            payload: Union[str, BufferedReader]
    ):
        file = None
        message = None
        url = ApiConstants.POST_TO_CHAT_URL + chat_id
        if isinstance(payload, str):
            url += ApiConstants.MESSAGE
            message = {
                'text': payload
            }
        elif isinstance(payload, BufferedReader):
            url += ApiConstants.FILES
            file = {
                'file': payload
            }
        resp = self._api.send_request(
            url=url,
            files=file,
            json=message
        )
        return resp

    def post_to_user(
            self,
            id: str,
            payload: Union[str, BufferedReader]
    ):
        file = None
        message = None
        url = ApiConstants.POST_TO_CHAT_URL + id
        if isinstance(payload, str):
            url += ApiConstants.MESSAGE
            message = {
                'text': payload
            }
        elif isinstance(payload, BufferedReader):
            url += ApiConstants.FILES
            file = {
                'file': payload
            }
        resp = self._api.send_request(
            url=url,
            files=file,
            json=message
        )
        return resp
