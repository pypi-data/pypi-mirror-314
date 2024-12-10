from bubot_helpers.ActionDecorator import async_action
from bubot.buject.User.User import User
from bubot.core.ObjApi import ObjApi
from bubot_helpers.ActionDecorator import async_action
from bubot_helpers.ExtException import ExtException

from bubot_messenger_bot.buject.MessengerBot.Helper import clear_phone
from bubot_messenger_bot.buject.MessengerBot.TelegramBot import TelegramBot as Bot
from bubot_messenger_bot.buject.MessengerBotChat.MessengerBotChat import MessengerBotChat as Chat
from bubot.buject.Session.Session import Session

# from bubot_messenger_bot.buject.Client.Client import Client
# from bubot_messenger_bot.buject.Order.Order import Order


class MessengerBotApi(ObjApi):
    # client = Client
    # handler: Order = Order

    bot_data = {}

    @async_action
    async def public_api_telegram_webhook(self, view, *, _action=None, **kwargs):
        data = await view.loads_json_request_data(view)
        pass

    @staticmethod
    def get_bot_instance(view, bot_id):
        # todo убрать говнокод
        running_devices = view.app['device'].running_devices
        for uuid in running_devices:
            if running_devices[uuid].__class__.__name__ == 'MessengerBotUpdater':
                if running_devices[uuid].bot.data['token'].startswith(str(bot_id)):
                    return running_devices[uuid].bot
        raise NotImplementedError()

    @async_action
    async def public_api_sign_in_by_web_app(self, view, *, _action=None, **kwargs):
        data = await view.loads_json_request_data(view)
        # todo убрать говнокод
        bot_id = int(data['bot'])
        log = view.app['device'].log
        log.info(data)

        try:
            bot_data = self.bot_data[bot_id]
        except KeyError:
            bot = Bot(view.storage)
            await bot.find_by_id(bot_id, _form=None)
            bot_data = bot.data
            self.bot_data[bot_id] = bot_data
        token = bot_data['token']

        init_data = Bot.raw_api.validate_web_app_data(data['initData'], token)
        if init_data is None:
            log.error(data)
            raise ExtException(message='Bad initData', detail='Что ты вы делаете не то, обратитесь к разработчику')
        user = User(view.storage, lang=view.lang, form='CurrentUser')

        user_id = init_data['user']['id']
        title = f"{init_data['user']['last_name']} {init_data['user']['first_name']}"

        chat = Chat(view.storage, bot_id=int(bot_id))
        await chat.find_by_chat_id(int(user_id))

        phone = clear_phone(chat.data.get('phone'))
        if not phone:
            raise ExtException(message='Not phone')

        auth_type = 'phone'
        try:
            _action.add_stat(await user.add_auth({
                'type': auth_type,
                'id': phone,
                'title': title
            }, **kwargs))
        except ExtException as err:
            pass

        _action.add_stat(await Session.create_from_request(user, view,
                                                           bot_id=bot_id,
                                                           user_id=user_id
                                                           ))
        return self.response.json_response({
            'title': chat.data['title'],
            'bot': bot_data['subtype'],
            'bot_id': int(bot_id),
            'chat_id': int(user_id),
            'phone': phone,
            # 'login': chat.data.get('login'),
            # 'password': chat.data.get('password'),
            # 'access': chat.data.get('access'),
        })
