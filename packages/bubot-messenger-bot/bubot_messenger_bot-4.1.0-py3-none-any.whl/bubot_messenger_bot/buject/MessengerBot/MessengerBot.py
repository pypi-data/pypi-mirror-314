import json
import logging
from datetime import datetime

from bubot.core.Obj import Obj
from bubot_helpers.ArrayHelper import ArrayHelper
from bubot_helpers.ExtException import KeyNotFound, ExtException
from bubot_helpers.Helper import get_tzinfo
# from bubot_messenger_bot.buject.MessengerBot.MessengerBotUpdate import BotUpdate
# from bubot_messenger_bot.buject.ViberBot.RawViberApi import RawViberApi as Api
# from bubot_messenger_bot.buject.ViberBotChat.ViberBotChat import ViberBotChat as Chat

tz_info = get_tzinfo()


class MessengerBot(Obj):
    file = __file__  # должен быть в каждом файле наследнике для чтения форм
    name = 'TelegramBot'
    raw_api = None

    def __init__(self, storage, *, device=None, account_id=None, lang=None, data=None, **kwargs):
        self.device = device
        self.storage = storage
        self.api = None
        self.log = logging.getLogger(f'{self.__class__.__name__}')
        super().__init__(self.storage, account_id=account_id, lang=lang, data=data, **kwargs)

    @property
    def db(self):
        return 'ToFirstGrade'

    def init(self):
        self.data = dict(
            subtype=self.__class__.__name__,
            title=self.__class__.__name__
        )

    def init_by_data(self, data):
        obj_class = super().init_by_data(data)
        obj_class.api = obj_class.raw_api(data['token'])
        return obj_class

    async def initialize(self):
        try:
            me = await self.api.get_me()
            self.obj_id = me['id']
            self.data['title'] = me['title']
            await self.update()
        except Exception as err:
            raise ExtException(parent=err)

