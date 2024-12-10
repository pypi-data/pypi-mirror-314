<a href="https://zoho.com/catalyst/">
    <img width="150" height="150" src="https://www.zohowebstatic.com/sites/default/files/catalyst/catalyst-logo.svg">
</a>

<h1>ZCatalyst Cliq SDK</h1>

<p>
  The official python sdk for integrating Zoho Catalyst with Zoho Cliq.
</p>
<br>

ZCatalyst Cliq SDK helps you to work with Python for handling Zoho Cliq extensions using Zoho Catalyst.

## Prerequisites

To start working with this SDK you need to sign up with [catalyst](https://catalyst.zoho.com/) and [cliq](https://cliq.zoho.com/)

Then you need to install suitable version of [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installation/)

## Installing

The ZCatalyst Cliq SDK is a pip package and can be found as zcatalyst-cliq on PyPI:

```bash
python -m pip install zcatalyst-cliq
```

## Using zcatalyst-cliq

After installing zcatalyst-cliq, you can initialize it in your catalyst's cliq integration functions as:

```python
import zcatalyst_cliq

# your cliq handler files's mapping should be given here
config = {
    "ZohoCliq": {
        "handlers": {
            "bot_handler": "handlers/bot_handler.py",
            "function_handler": "handlers/function_handler.py",
            "command_handler": "handlers/command_handler.py",
            "widget_handler": "handlers/widget_handler.py",
            "messageaction_handler": "handlers/message_action_handler.py",
            "extension_handler": "handlers/extension_handler.py",
            "link_preview_handler": "handlers/link_preview_handler.py"
        }
    },
}

def handler(request, response):
    handler_resp = zcatalyst_cliq.execute(request, config)
    response.set_content_type('application/json')
    response.send(handler_resp)
```

## Documentation

For documentation and further queries kindly contanct [support@zohocatalyst.com](mailto:support@zohocatalyst.com)
