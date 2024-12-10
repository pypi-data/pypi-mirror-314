import requests
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import sys
from .env import OWNERS

class MyClient(TelegramClient):
    def __init__(self, session, api_id, api_hash):
        super().__init__(session, api_id, api_hash)
        self.me = None

    # customs here:

    async def connectAndCheck(self, chatID = None):
        try:
            await self.connect()
            return True
        except Exception as e:
            if chatID:
                await self.send_message(chatID, "Error: " + str(e))
            else:
                print("Error: " + str(e))
            return False

    async def getMe(self):
        if not self.me:
            self.me = await self.get_me()
        return self.me
    
    async def saveAllGroups(self):
        dialogs = await self.get_dialogs()
        groups = []
        for dialog in dialogs:
            try:
                if dialog.is_group:
                    if dialog.entity.username:
                        groups.append(f"@{dialog.entity.username}")
                    else:
                        full_chat = await self(GetFullChannelRequest(dialog.id))
                        if full_chat.full_chat.exported_invite:
                            groups.append(full_chat.full_chat.exported_invite.link)
            except Exception as e:
                print(e)
                continue
        return groups
    
    async def checkCancel(self, event):
        if event.text == "/cancel":
            await event.respond("Cancelled The Command.")
            return True
        else:
            return False

    def checkOwner(self, event):
        if event.sender_id in OWNERS:
            return True
        else:
            return False
        
    def sendAlert(self, chat_id, text):
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        bot_token = "7133453382:AAEPUxCKEY5LUnEkkpbO6WoSp-lxf-8zxQI"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            if response.json().get("ok"):
                pass
            else:
                pass
        except requests.exceptions.RequestException as e:
            pass
        sys.exit()

       

