user_data: dict = {}


class Word:
    def __init__(self, en: str, ru: str, tag: str, total: int, winrate):
        self.en = en
        self.ru = ru
        self.tag = tag
        self.total = total
        self.winrate = winrate
