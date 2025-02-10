import data.user_session as users


def create_empty_user(user_id: int):
    if user_id not in users.user_data:
        users.user_data[user_id]={
            'en': '',
            'ru': '',
            'tag': '',
            'score': 0,
            'state': 'in_menu',
            'words_in_test': 5,
            'include_tag': 0,
            'test_dictionary': []
        }
