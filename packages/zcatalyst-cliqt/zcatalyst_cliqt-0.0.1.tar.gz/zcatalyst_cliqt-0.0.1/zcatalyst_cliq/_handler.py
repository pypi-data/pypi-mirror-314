from typing import Any, Callable, Dict


class Handler:
    handler_map: Dict[str, Dict[str, Dict[Callable, Any]]] = {}

    @staticmethod
    def register_hanlder(
            component_type: str,
            name: str,
            callback: Callable,
            res: Any
    ):
        if not Handler.handler_map.get(component_type):
            Handler.handler_map[component_type] = {
                name: {
                    'func': callback,
                    'resp': res
                }
            }

        Handler.handler_map[component_type][name] = {
            'func': callback,
            'resp': res
        }
