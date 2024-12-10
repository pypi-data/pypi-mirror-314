import json
from asyncio import TimeoutError as AsyncioTimeoutError

import aiohttp

from bubot_helpers.ExtException import ExtException, NotAvailable, ExtTimeoutError
from bubot_helpers.Helper import Helper


class TelegramRawApi:
    api_url = 'https://api.telegram.org'

    def __init__(self, token, *, api_url=None):
        self._token = token
        self._bot_url = f'{api_url if api_url else self.api_url}/bot{token}'

    async def get_me(self):
        try:
            resp = await self.exec_method('getMe', request_type='get', timeout=20)
            resp['title'] = resp['first_name']
            return resp
        except Exception as err:
            raise ExtException(parent=err, action=f'{self.__class__.__name__}.get_me')

    async def get_updates(self, *, offset=None, limit=100, timeout=0, allowed_updates=None):
        try:
            data = dict(offset=offset, limit=limit, timeout=timeout, allowed_updates=allowed_updates)
            request_timeout = round(timeout * 1.3) if timeout else None
            resp = await self.exec_method('getUpdates', request_type='post', json=data, timeout=request_timeout)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action=f'{self.__class__.__name__}.get_updates')

    async def delete_message(self, chat_id: int, message_id: int):
        data = dict(
            chat_id=chat_id,
            message_id=message_id,
        )
        try:
            resp = await self.exec_method('deleteMessage', json=data)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action="delete_message", dump=data)

    async def send_message(self, chat_id: int, text: str, *, reply_markup=None, reply_to_message_id=None,
                           parse_mode=None):
        # print(f'send_message({chat_id}{text}')
        data = {
            'chat_id': chat_id,
            'text': text
        }
        Helper.obj_set_path_value(data, 'reply_markup', reply_markup, skip_if_none=True)
        Helper.obj_set_path_value(data, 'reply_to_message_id', reply_to_message_id, skip_if_none=True)
        Helper.obj_set_path_value(data, 'parse_mode', parse_mode, skip_if_none=True)
        try:
            resp = await self.exec_method('sendMessage', json=data)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action="send_message", dump=data)

    async def forward_message(self, chat_id: int, from_chat_id: int, message_id: int):
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }
        try:
            resp = await self.exec_method('forwardMessage', json=data)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action="forward_message", dump=data)

    async def edit_message_text(self, chat_id: int, message_id: int, text: str, *, reply_markup=None,
                                parse_mode=None):
        # print(f'edit_message_text({chat_id}{text}')

        data = dict(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
        )
        Helper.obj_set_path_value(data, 'reply_markup', reply_markup, skip_if_none=True)
        Helper.obj_set_path_value(data, 'parse_mode', parse_mode, skip_if_none=True)
        try:
            resp = await self.exec_method('editMessageText', json=data)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action="edit_message_text", dump=data)

    async def exec_method(self, method, *, request_type='post', json=None, timeout=None):
        try:
            url = f'{self._bot_url}/{method}'
            async with aiohttp.ClientSession() as session:
                async with session.request(request_type, url, json=json, timeout=timeout) as resp:
                    content_type = resp.headers.get('Content-Type')
                    if content_type.find('application/json') >= 0:
                        resp_data = await resp.json()

                        if resp.status in [200] and resp_data['ok']:
                            return resp_data['result']
                    if resp.status == 502:
                        raise ExtTimeoutError(message=await resp.text(), action="send_message")
                    raise NotImplementedError(f'{resp.status} {await resp.text()}')
        except AsyncioTimeoutError as err:
            raise NotAvailable(parent=err, action="exec_method")
        except aiohttp.ClientConnectionError as err:
            raise NotAvailable(parent=err, action="exec_method")
        except Exception as err:
            raise ExtException(parent=err, action='exec_method') from err

    @staticmethod
    def validate_web_app_data(init_data, bot_token):
        import hashlib
        import hmac

        from urllib.parse import unquote

        data_check_arr = unquote(init_data).split('&')
        data = {}
        hash_item = None
        for item in data_check_arr:
            key, value = item.split('=')
            data[key] = value
            if key == 'hash':
                hash_item = item
            elif key == 'user':
                data[key] = json.loads(value)
        data_check_arr.remove(hash_item)
        data_check_arr.sort()
        data_check_string = "\n".join(data_check_arr)

        secret_key = hmac.new('WebAppData'.encode(), bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if data['hash'] != calculated_hash:
            return None
        return data
