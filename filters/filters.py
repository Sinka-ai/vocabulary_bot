from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    admins_list: list[int] = []

    def __init__(self, admins_list):
        self.admins_list = admins_list

    async def __call__(self, message: Message):
        txt = message.text.split()
        del txt[0]
        if message.from_user.id in self.admins_list:
            return {'text': " ".join(txt)}

class InAiMode(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_ai':
                return 1
            else:
                return 0


class InAddEn(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_add_en':
                return 1
            else:
                return 0


class InAddRu(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_add_ru':
                return 1
            else:
                return 0


class InAddTag(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_add_tag':
                return 1
            else:
                return 0


class InSettings(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_settings':
                return 1
            else:
                return 0


class InDelete(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_delete':
                return 1
            else:
                return 0


class InTest(BaseFilter):
    users_dictionary: dict

    def __init__(self, users_dict):
        self.users_dictionary = users_dict

    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if user_id not in self.users_dictionary:
            return 0
        else:
            if self.users_dictionary[user_id]['state'] == 'in_test':
                return 1
            else:
                return 0
