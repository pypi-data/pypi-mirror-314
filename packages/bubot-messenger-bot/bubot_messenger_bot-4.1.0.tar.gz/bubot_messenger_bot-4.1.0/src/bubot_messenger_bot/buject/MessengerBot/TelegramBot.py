import json
from datetime import datetime

from bubot_helpers.ArrayHelper import ArrayHelper
from bubot_helpers.ExtException import KeyNotFound, ExtException
from bubot_helpers.Helper import get_tzinfo
from bubot_messenger_bot.buject.MessengerBot.MessengerBot import MessengerBot
from bubot_messenger_bot.buject.MessengerBot.Helper import clear_phone
from bubot_messenger_bot.buject.MessengerBot.TelegramBotUpdate import TelegramBotUpdate as BotUpdate
from bubot_messenger_bot.buject.MessengerBot.TelegramRawApi import TelegramRawApi as Api
from bubot_messenger_bot.buject.MessengerBotChat.MessengerBotChat import MessengerBotChat as Chat

tz_info = get_tzinfo()


class TelegramBot(MessengerBot):
    file = __file__  # должен быть в каждом файле наследнике для чтения форм
    selenium_scenario = None
    raw_api = Api

    async def get_updates(self, *, timeout=0, limit=100):
        last_update_id = self.data.get('last_update_id', 0)
        if last_update_id:
            last_update_id += 1
        updates = await self.api.get_updates(offset=last_update_id, timeout=timeout, limit=limit)
        try:
            for _update in updates:
                update = BotUpdate(_update)
                await self.process_update(update)
                self.data['last_update_id'] = update.update_id
        except Exception as err:
            raise ExtException(parent=err, action='TelegramBot.get_updates') from err
        return updates

    async def process_update(self, update: BotUpdate):
        if update.chat_id:
            if update.chat_id < 0:
                # resp = await self.api.send_message(
                #     update.chat_id,
                #     'Бот не работает в группах.'
                # )
                return
            chat = Chat(self.storage, bot_id=self.obj_id)
            try:
                await chat.find_by_chat_id(update.chat_id)
                if not chat.lang:
                    chat.lang = update.language
            except KeyNotFound:
                chat_data = update.get_chat()
                title = f"{chat_data.get('last_name', '')} {chat_data.get('first_name', '')}".strip()
                chat.init_by_data({
                    'chat_id': update.chat_id,
                    'title': title,
                    'username': chat_data.get('username'),
                    'lang': update.language
                })
                await self.send_message_to_admin(f'New chat {self.__class__.__name__} {update.chat_id} {title}')

            await self.process_chat_update(update, chat=chat)
            await chat.update()
        else:
            await self.send_message_to_admin(f'Unsupported update {json.dumps(update.data, ensure_ascii=False)}')

    async def process_chat_update(self, update: BotUpdate, *, chat=None):
        try:
            if update.callback_query:
                try:
                    command = update.message['text'][1:]
                    await getattr(self, f'process_callback_{command}')(update, chat=chat)
                except Exception as err:
                    self.log.error(err)
            elif update.is_bot_command():
                try:
                    await getattr(self, f'process_command_{update.bot_command_name}')(update, chat=chat)
                except Exception as err:
                    self.log.error(err)
            elif update.is_user_contact():
                await self.process_command_set_phone(update, chat=chat)
            else:
                if chat:
                    my_chat_member = update.data.get('my_chat_member')
                    if my_chat_member:
                        new_chat_member = my_chat_member.get('new_chat_member')
                        if new_chat_member.get('status') == 'member':
                            await getattr(self, 'process_command_start')(update, chat=chat)
                        return

                    next_update = chat.data.get('next_update')
                    if next_update:
                        if next_update['type'] == 'command_param':
                            update.bot_command_name = next_update['command']
                            update.bot_command_params = update.get_message().get('text', '')
                            command_handler = f'process_command_{update.bot_command_name}'
                            try:
                                await getattr(self, command_handler)(update, chat=chat)
                            except Exception as err:
                                err = ExtException(parent=err, action=command_handler)
                                self.log.error(err)
                        chat.data['next_update'] = None
                    else:
                        if update.message_id:
                            await self.process_message(chat, update)
                        else:
                            await self.send_message_to_admin(
                                f'Unsupported update {json.dumps(update.data, ensure_ascii=False)}')
                else:
                    await self.send_message_to_admin(
                        f'Unsupported update {json.dumps(update.data, ensure_ascii=False)}')
                pass
        except Exception as err:
            err1 = ExtException(parent=err, dump=update.data)
            chat.data['last_error'] = err1.to_dict()
            await self.send_message_to_admin(
                f'Unsupported update {err1} {json.dumps(update.data, ensure_ascii=False)}')

    async def process_message(self, chat, update):
        try:
            if 'messages' not in chat.data:
                chat.data['messages'] = []
                index = -1
            else:
                index = ArrayHelper.find_by_key(chat.data['messages'], update.message_id, '_id')
            # _raw_json = json.dumps(update.data, ensure_ascii=False)
            _message = {
                'text': update.data['message'].get('text'),
                'date': datetime.fromtimestamp(update.data['message']['date'], tz=tz_info),
                '_id': update.data['message']['message_id']
            }
            # _message.pop('chat', None)
            # _message.pop('from', None)
            # _message['_id'] = _message.pop('message_id')
            # _message['__update_id'] = update.update_id
            # _message['date'] = datetime.fromtimestamp(_message['date'], tz=tz_info)
            try:
                if update.message['reply_to_message'] and update.message['reply_to_message'].get('forward_from') \
                        and update.message['reply_to_message']['from']['id'] == self.data['_id']:
                    original_chat_id = update.message['reply_to_message']['forward_from']['id']
                    original_chat = Chat(self.storage, bot_id=self.obj_id)
                    await original_chat.find_by_chat_id(original_chat_id)
                    res = await self.api.send_message(original_chat_id, _message['text'])
                    _message['_id'] = res['message_id']
                    _message['bot'] = True
                    original_chat.data['messages'].append(_message)
                    await original_chat.update()
                    return
            except Exception as err:
                pass
            if index < 0:
                if _message['text']:
                    chat.data['messages'].append(_message)
                await self.forward_message_to_admin(update)
                # await self.send_message_to_admin(f'Message {_raw_json}', from_chat=chat.chat_id)
            else:
                chat.data['messages'][index] = _message
        except Exception as err:
            raise ExtException(parent=err) from err

    async def get_list_admin_chat(self):
        filter = {
            "bot_id": self.obj_id,
            "admin": True
        }
        chat = Chat(self.storage, bot_id=self.obj_id)
        chats = await chat.list(filter=filter)
        return chats.result['rows']

    async def send_message_to_admin(self, text, *, reply_to_message_id=None, parse_mode=None, from_chat=None):
        self.log.error(f'send_message_to_admin: {text}')
        admin_chats = await self.get_list_admin_chat()
        for admin_data in admin_chats:
            if from_chat and from_chat == admin_data['chat_id']:
                continue
            await self.api.send_message(admin_data['chat_id'], text, reply_to_message_id=reply_to_message_id,
                                        parse_mode=parse_mode)

    async def forward_message_to_admin(self, update):
        try:
            # self.log.error(f'forward_message_to_admin: {text}')
            from_chat_id = update.message['chat']['id']
            message_id = update.message_id
            admin_chats = await self.get_list_admin_chat()
            for admin_data in admin_chats:
                if from_chat_id and from_chat_id == admin_data['chat_id']:
                    continue
                await self.api.forward_message(admin_data['chat_id'], from_chat_id, message_id)
        except Exception as err:
            raise ExtException(parent=err)

    async def process_command_start(self, update: BotUpdate, *, chat: Chat = None):
        await self.process_command_help(update, chat=chat)

    async def process_command_help(self, update: BotUpdate, *, chat: Chat = None):
        await self.api.send_message(update.chat_id, self.t('start', update.language),
                                    reply_to_message_id=update.message_id,
                                    parse_mode='Markdown')

    async def process_command_set_phone(self, update: BotUpdate, *, chat: Chat = None):
        message = update.get_message()
        contact = message.get('contact')
        if contact and contact['user_id'] == message['from']['id']:
            chat.data['phone'] = clear_phone(contact['phone_number'])

    async def scheduler(self):
        pass
