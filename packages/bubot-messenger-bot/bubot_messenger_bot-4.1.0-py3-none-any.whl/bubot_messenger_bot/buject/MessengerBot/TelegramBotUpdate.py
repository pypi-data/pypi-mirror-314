class TelegramBotUpdate:
    def __init__(self, data):
        self.data = data
        self.bot_command = None
        self.bot_command_name = None
        self.bot_command_params = None

    @property
    def message(self):
        try:
            return self.data['message']
        except (AttributeError, TypeError, KeyError):
            pass
        try:
            return self.data['callback_query']['message']['reply_to_message']
        except (AttributeError, TypeError, KeyError):
            pass
        try:
            return self.data['callback_query']['message']
        except (AttributeError, TypeError, KeyError):
            pass
        return None

    @property
    def update_id(self):
        return self.data['update_id']

    @property
    def chat_id(self):
        try:
            return self.message['chat']['id']
        except (AttributeError, TypeError, KeyError):
            pass
        try:
            return self.data['my_chat_member']['chat']['id']
        except (AttributeError, TypeError, KeyError):
            pass
        return None

    @property
    def language(self):
        try:
            return self.message['from']['language_code']
        except (AttributeError, TypeError, KeyError):
            return None

    @property
    def message_id(self):
        try:
            return self.message['message_id']
        except (AttributeError, TypeError, KeyError):
            return None

    @property
    def callback_query(self):
        return self.data.get('callback_query')

    def is_user_contact(self):
        message = self.get_message()
        try:
            contact = message.get('contact')
        except (AttributeError, TypeError, KeyError):
            return False
        return contact and contact['user_id'] == message['from']['id']

    def is_bot_command(self):
        if self.bot_command is None:
            self.bot_command = False
            try:
                entities = self.message['entities']
            except (AttributeError, TypeError, KeyError):
                return None
            if entities[0].get('type') == 'bot_command':
                self.bot_command = True
                len_command_name = entities[0]['length']
                self.bot_command_name = self.message['text'][entities[0]['offset'] + 1: len_command_name]
                if len(self.message['text']) > len_command_name:
                    self.bot_command_params = self.message['text'][len_command_name + 1:]
        return self.bot_command

    def get_message(self):
        return self.message

    def get_chat(self):
        message = self.get_message()
        return message['chat']

    def is_change_member_status(self):
        if 'my_chat_member' not in self.data:
            return None
        event = self.data['my_chat_member']
        event['old_status'] = event['old_chat_member']['status']
        event['new_status'] = event['new_chat_member']['status']
