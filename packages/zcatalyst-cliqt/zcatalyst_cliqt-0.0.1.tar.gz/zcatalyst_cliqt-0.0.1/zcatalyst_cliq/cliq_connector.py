from typing import Dict, Union
from .error import CatalystError
from ._handler_util import parse_config
import zcatalyst_sdk


class CliqConnector:
    def __init__(self, properties: Union[str, Dict[str, Dict[str, str]]]):
        self.config = self._get_connection_json(properties)

    def get_connector(self, name: str):
        app = zcatalyst_sdk.initialize()
        return app.connection(self.config).get_connector(name)

    @staticmethod
    def _get_connection_json(properties):
        if not properties or not isinstance(properties, (str, dict)):
            raise CatalystError(
                'Connection properties must be passed '
                'as dict or string path to json file', 2
            )
        if isinstance(properties, dict):
            return properties
        return parse_config(properties)
