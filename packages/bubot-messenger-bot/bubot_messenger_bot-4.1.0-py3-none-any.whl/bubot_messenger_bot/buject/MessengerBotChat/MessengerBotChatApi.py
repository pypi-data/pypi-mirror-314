from datetime import datetime

from bubot.core.ObjApi import ObjApi
from bubot_helpers.ActionDecorator import async_action
from bubot_messenger_bot.buject.MessengerBot.MessengerBotApi import MessengerBotApi
from .MessengerBotChat import MessengerBotChat


class MessengerBotChatApi(ObjApi):
    handler = MessengerBotChat

    @async_action
    async def api_read(self, view, *, _action=None, **kwargs):
        handler, data = await self.prepare_json_request(view)
        await self.check_right(view, handler, 11)
        result = _action.add_stat(await handler.find_one(data, _form=None))
        return self.response.json_response(result)

    @async_action
    async def api_send_message(self, view, *, _action=None, **kwargs):
        handler, data = await self.prepare_json_request(view)
        await self.check_right(view, handler, 11)
        await self.send_message(view, handler, data, _action=_action)
        return self.response.json_response(handler.data)

    async def send_message(self, view, handler, data, *, _action=None):
        bot_id = data['bot_id']
        chat_id = data['chat_id']
        message = data['message']
        _action.add_stat(await handler.find_one(dict(
            bot_id=bot_id,
            chat_id=chat_id
        ), _form=None))

        bot = MessengerBotApi.get_bot_instance(view, bot_id)
        res = await bot.api.send_message(
            chat_id,
            message
        )
        if 'messages' not in handler.data:
            handler.data['messages'] = []

        handler.data['messages'].append(dict(
            date=datetime.fromtimestamp(res['date']),
            text=message,
            bot=True
        ))
        _action.add_stat(await handler.update())
