import json
from datetime import datetime

from bubot_helpers.ArrayHelper import ArrayHelper
from bubot_helpers.ExtException import KeyNotFound, ExtException
from bubot_helpers.Helper import get_tzinfo

from bubot_messenger_bot.buject.MessengerBot.MessengerBot import MessengerBot
from bubot_messenger_bot.buject.MessengerBot.ViberBotUpdate import ViberBotUpdate as BotUpdate
from bubot_messenger_bot.buject.MessengerBot.ViberRawApi import ViberRawApi as Api
from bubot_messenger_bot.buject.MessengerBotChat.MessengerBotChat import MessengerBotChat as Chat

tz_info = get_tzinfo()


class ViberBot(MessengerBot):
    file = __file__  # должен быть в каждом файле наследнике для чтения форм
    raw_api = Api

    async def initialize(self):
        await super().initialize()
        await self.api.set_webhook(self.get_webhook_url())

    def get_webhook_url(self):
        raise NotImplementedError()

    async def on_webhook(self, data):
        return {}

    async def on_message(self, data):

        return {}

    async def get_updates(self, *, timeout=0, limit=100):
        return []

    async def scheduler(self):
        pass
