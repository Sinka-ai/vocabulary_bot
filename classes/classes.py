import psycopg2
import os
from data.update_table import update


class Word:
    en: str
    ru: str
    total: int
    success: int
    coef: int
    definition: str

    def __init__(self, en, ru, definition, total, success, coef):
        self.en = en
        self.ru = ru
        self.total = total
        self.success = success
        self.coef = coef
        self.definition = definition

    def __str__(self):
        return ('Ваше слово - ' + self.en + ', перевод: ' + self.ru + ' total ' + str(self.total) + ' successful ' +
                str(self.success) + ' coef ' + str(self.coef))


class Dictionary:
    words: list[Word]
    words_copy: list[Word]

    def __init__(self, count: int, user_id: int):
        db = psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                              user=os.environ['POSTGRES_USER'],
                              password=os.environ['POSTGRES_PASSWORD'],
                              host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                              port="5432")
        sql = db.cursor()
        self.words = []
        sql.execute(f'SELECT en,ru, definition, total,successful,coef FROM words WHERE user_id = {user_id} '
                             f'ORDER BY coef ASC')

        for i in range(count):
            word = sql.fetchone()
            if word is not None:
                self.words.append(Word(word[0], word[1], word[2], word[3], word[4], word[5]))
        self.words_copy = self.words.copy()
        sql.close()
        db.close()

    def __str__(self):
        ans = ''
        for i in range(len(self.words)):
            ans += str(self.words[i])
            ans += '         ,           '
        return ans

    def __call__(self):
        i = - 1
        while len(self.words) > 0:
            i = (i + 1) % len(self.words)
            yield self.words[i]



    def delete_word(self, ru: str):
        for i in range(len(self.words)):
            if self.words[i].ru == ru:
                del self.words[i]
                return
        return

    def update(self, user_id, rat_dif):
        db = psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                              user=os.environ['POSTGRES_USER'],
                              password=os.environ['POSTGRES_PASSWORD'],
                              host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                              port="5432")
        sql = db.cursor()
        for i in range(len(self.words_copy)):
            word_i = self.words_copy[i]
            print(f'UPDATE words SET total = {word_i.total}, successful = {word_i.success}, '
                  f"date = CURRENT_DATE WHERE en = '{word_i.en}' AND user_id={user_id}")
            sql.execute(f'UPDATE words SET total = {word_i.total}, successful = {word_i.success}, '
                        f"date = CURRENT_DATE WHERE en = '{word_i.en}' AND user_id={user_id}")

        sql.execute(f'UPDATE users SET rating=rating+{rat_dif}')
        db.commit()
        sql.close()
        db.close()
        update()
