import os.path

from bubot.core.BubotHelper import BubotHelper
from bubot_helpers.ExtException import ExtException, NotAvailable
from bubot.buject.OcfDevice.subtype.Device.Device import Device
from bubot.core.DataBase.Mongo import Mongo as Storage
from bubot.buject.OcfDevice.subtype.Device.RedisQueueMixin import RedisQueueMixin


class MessengerBotUpdater(RedisQueueMixin, Device):
    file = __file__
    template = False

    def __init__(self, **kwargs):
        self.storage = None
        Device.__init__(self, **kwargs)
        RedisQueueMixin.__init__(self, **kwargs)
        self.bot = None

    async def on_update_oic_con(self, message):
        pass

    async def on_pending(self):
        try:
            self.storage = await Storage.connect(self)
            await RedisQueueMixin.on_pending(self)
            bot_data = self.get_param('/oic/con', 'bot')
            handler = BubotHelper.get_subtype_class('MessengerBot', bot_data['subtype'])
            self.bot = handler(self.storage, device=self)
            self.bot = self.bot.init_by_data(bot_data)
            await self.bot.initialize()
            await Device.on_pending(self)
        except Exception as err:
            raise ExtException(parent=err)

    async def on_cancelled(self):
        await RedisQueueMixin.on_cancelled(self)
        await Device.on_cancelled(self)

    async def on_idle(self):
        try:
            await self.bot.scheduler()
        except Exception as err:
            await self._process_error(ExtException(parent=err, action='bot.scheduler'))
        try:
            try:
                limit = 100
                timeout = self.get_param('/oic/con', 'BotUpdateTimeout', 60)
                while True:
                    res = await self.bot.get_updates(timeout=timeout, limit=limit)
                    if len(res) < limit:
                        break
            except NotAvailable:
                pass
            finally:
                await self.bot.update()
        except Exception as err:
            await self._process_error(ExtException(parent=err, action='bot.update'))

    async def _process_error(self, err):
        msg = f'MessengerBotUpdater on_idle error: {str(err)}'
        self.log.error(msg)
        try:
            await self.bot.send_message_to_admin(msg)
        except Exception as err:
            self.log.error(f'send to admin {err}, {msg}')
            pass
