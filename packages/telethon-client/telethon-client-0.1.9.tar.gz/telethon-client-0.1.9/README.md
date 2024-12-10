# Telethon Custom Client

This is a custom Telethon client package that I have created for my own usage. It is open source and available on GitHub. Feel free to explore the repository and use it if it fits your needs.

## Installation

You can install this package from PyPI using pip:

```shell
pip install telethon-client
```

## Usage

To use this custom Telethon client, you need to import it in your Python code:

```python
from TeleClient import MyClient

# Create an instance of the custom client
bot = MyClient(api_id, api_hash, token) # if u wanna use user client use StringSession from telethon.sessions just like telethon

# Use the client to interact with the Telegram API
# ...
```

Make sure to replace `api_id` and `api_hash` with your own Telegram API credentials.


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
