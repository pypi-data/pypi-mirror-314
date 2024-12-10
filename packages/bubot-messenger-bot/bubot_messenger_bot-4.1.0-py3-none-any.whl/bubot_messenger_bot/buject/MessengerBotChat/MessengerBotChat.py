from bubot.core.Obj import Obj

from bubot_helpers.ActionDecorator import async_action


class MessengerBotChat(Obj):
    name = 'TelegramBotChat'
    file = __file__

    @property
    def db(self):
        return 'ToFirstGrade'

    def __init__(self, storage, *, account_id=None, lang=None, data=None, bot_id=None, **kwargs):
        self.bot_id = bot_id
        super().__init__(storage, account_id=account_id, lang=lang, data=data, **kwargs)

    def init(self):
        self.data = dict(
            bot_id=self.bot_id,
        )

    @property
    def chat_id(self):
        return self.data.get("chat_id")

    @property
    def lang(self):
        return self.data.get("lang")

    @lang.setter
    def lang(self, value):
        self.data['lang'] = value

    @async_action
    async def find_by_chat_id(self, chat_id, *, _form="Item", _action=None, **kwargs):
        return await self.find_one({"bot_id": self.bot_id, "chat_id": chat_id}, _form=_form, **kwargs)
