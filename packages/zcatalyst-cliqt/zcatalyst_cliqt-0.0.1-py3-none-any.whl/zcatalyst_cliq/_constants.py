import os
from os import path


def env_override(env_name: str, default_value: str):
    env_value = os.getenv(env_name)
    if not env_value:
        return default_value
    return env_value


meta_file = path.join(path.dirname(path.abspath(__file__)), '__version__.py')
meta = {}
with open(meta_file, encoding="utf-8") as fp:
    exec(fp.read(), meta)  # pylint: disable=exec-used

# SDK constants
SDK_VERSION = meta['__version__']
USER_AGENT = 'zcatalyst-integ-python/'
CONFIG_JSON = 'catalyst-config.json'
CLIQ = 'ZohoCliq'
BOT = 'bot'
COMMAND = 'command'
MESSAGEACTION = 'messageaction'
WIDGET = 'widget'
FUNCTION = 'function'
LINKPREVIEW = 'link_preview'
EXTENSION = 'extension'


class Handlers:
    class BotHandler:
        WELCOME_HANDLER = 'welcome_handler'
        MESSAGE_HANDLER = 'message_handler'
        CONTEXT_HANDLER = 'context_handler'
        MENTION_HANDLER = 'mention_handler'
        ACTION_HANDLER = 'action_handler'
        INCOMING_WEBHOOK_HANDLER = 'incomingwebhook_handler'
        PARTICIPATION_HANDLER = 'participation_handler'
        CALL_HANDLER = 'alert_handler'

    class CommandHandler:
        EXECUTION_HANDLER = 'execution_handler'
        SUGGESTION_HANDLER = 'suggestion_handler'

    class MessageActionHandler:
        EXECUTION_HANDLER = 'execution_handler'

    class WidgetHandler:
        VIEW_HANDLER = 'view_handler'
        CHANNEL_TAB_HANDLER = 'channel_tab_handler'

    class function_handler:
        BUTTON_HANDLER = 'button_handler'
        FORM_HANDLER = 'form_handler'
        FORM_CHANGE_HANDLER = 'form_change_handler'
        FORM_VALUES_HANDLER = 'form_values_handler'
        FORM_VIEW_HANDLER = 'form_view_handler'
        WIDGET_FUNCTION_HANDLER = 'applet_button_handler'

    class LinkPreviewHandler:
        PREVIEW_HANDLER = 'unfurl_handler'
        ACTION_HANDLER = 'unfurl_button_action_handler'
        MENU_HANDLER = 'unfurl_dynamic_action_handler'
        AFTER_SEND_HANDLER = 'unfurl_post_message_handler'

    class ExtensionHandler:
        INSTALLATION_HANDLER = 'installation_handler'
        INSTALLATION_VALIDATOR = 'installation_validator'
        UNINSTALLATION_HANDLER = 'uninstallation_handler'


# API Constants
DOMAIN = env_override('INTEG_CLIQ_DOMAIN', 'https://cliq.zoho.com')
VERSION = '/v2'
API = '/api'
MESSAGE = '/message'
FILES = '/files'
OAUTH_PREFIX = 'Zoho-oauthtoken '
BOT_UNIQUE_NAME = 'bot_unique_name'
BROADCAST = 'broadcast'
USERIDS = 'userids'
API_URL = DOMAIN + API + VERSION
POST_TO_CHANNEL_URL = API_URL + '/channelsbyname/'
POST_TO_BOT_URL = API_URL + '/bots/'
POST_TO_CHAT_URL = API_URL + '/chats/'
POST_TO_USER_URL = API_URL + '/buddies/'
