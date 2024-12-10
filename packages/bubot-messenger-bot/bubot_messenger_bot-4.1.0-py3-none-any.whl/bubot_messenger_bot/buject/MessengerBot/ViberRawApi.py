import json
from asyncio import TimeoutError as AsyncioTimeoutError
import hmac
import hashlib

import aiohttp
from bubot_helpers.ExtException import ExtException, NotAvailable, ExtTimeoutError


class ViberRawApi:
    api_url = 'https://chatapi.viber.com/pa/'

    def __init__(self, token, *, api_url=None):
        self._token = token
        if api_url:
            self.api_url = api_url

    async def get_me(self):
        try:
            resp = await self.exec_method('get_account_info', request_type='get', timeout=20)
            resp['title'] = resp['name']
            return resp
        except Exception as err:
            raise ExtException(parent=err, action=f'{self.__class__.__name__}.get_me')

    async def set_webhook(self, url):
        if not url:
            raise ExtException(message='Webhook url not defined')
        data = dict(
            url=url,
            event_types=[
                "failed",
                "subscribed",
                "unsubscribed",
                "conversation_started"
            ],
            send_name=True,
            send_photo=False
        )
        resp = await self.exec_method('set_webhook', json=data)
        a = 1

    def verify_signature(self, request_data, signature):
        return signature == self._calculate_message_signature(request_data)

    def _calculate_message_signature(self, message):
        return hmac.new(
            bytes(self._token.encode('ascii')),
            msg=message,
            digestmod=hashlib.sha256) \
            .hexdigest()

    # async def get_updates(self, *, offset=None, limit=100, timeout=0, allowed_updates=None):
    #     try:
    #         data = dict(offset=offset, limit=limit, timeout=timeout, allowed_updates=allowed_updates)
    #         request_timeout = round(timeout * 1.3) if timeout else None
    #         resp = await self.exec_method('getUpdates', request_type='post', json=data, timeout=request_timeout)
    #         return resp
    #     except Exception as err:
    #         raise ExtException(parent=err, action=f'{self.__class__.__name__}.get_updates')
    #
    # async def delete_message(self, chat_id: int, message_id: int):
    #     data = dict(
    #         chat_id=chat_id,
    #         message_id=message_id,
    #     )
    #     try:
    #         resp = await self.exec_method('deleteMessage', json=data)
    #         return resp
    #     except Exception as err:
    #         raise ExtException(parent=err, action="delete_message", dump=data)
    #
    async def send_message(self, chat_id: int, data):
        try:
            resp = await self.exec_method('send_message', json=data)
            return resp
        except Exception as err:
            raise ExtException(parent=err, action="send_message", dump=data)
    #
    # async def edit_message_text(self, chat_id: int, message_id: int, text: str, *, reply_markup=None,
    #                             parse_mode=None):
    #     # print(f'edit_message_text({chat_id}{text}')
    #
    #     data = dict(
    #         chat_id=chat_id,
    #         message_id=message_id,
    #         text=text,
    #     )
    #     Helper.obj_set_path_value(data, 'reply_markup', reply_markup, skip_if_none=True)
    #     Helper.obj_set_path_value(data, 'parse_mode', parse_mode, skip_if_none=True)
    #     try:
    #         resp = await self.exec_method('editMessageText', json=data)
    #         return resp
    #     except Exception as err:
    #         raise ExtException(parent=err, action="edit_message_text", dump=data)
    #
    async def exec_method(self, method, *, request_type='post', json=None, timeout=None):
        try:
            url = f'{self.api_url}/{method}'
            headers = {'X-Viber-Auth-Token': self._token}
            async with aiohttp.ClientSession() as session:
                async with session.request(request_type, url, headers=headers, json=json, timeout=timeout) as resp:
                    content_type = resp.headers.get('Content-Type')
                    if content_type.find('application/json') >= 0:
                        resp_data = await resp.json()

                        if resp.status in [200]:
                            if resp_data['status'] == 0:
                                return resp_data
                            else:
                                raise ExtException(message=resp_data['status_message'])

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
