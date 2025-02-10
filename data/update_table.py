import psycopg2
import os

C = 0.1


def update():
    db = psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                          user=os.environ['POSTGRES_USER'],
                          password=os.environ['POSTGRES_PASSWORD'],
                          host=os.environ['POSTGRES_CONTAINER_NAME'],  # Это имя контейнера с базой данных
                          port="5432")

    sql = db.cursor()
    with db:
        # Обновляем winrate
        sql.execute(f'UPDATE words SET winrate = CASE WHEN total=0 THEN 0 ELSE'
                    f' CAST(successful AS FLOAT) / CAST(total AS FLOAT) END')

        # Обновляем coef
        sql.execute(f'UPDATE words SET coef = SQRT(winrate)*'
                    f"(1 - TANH({C}))")

    sql.close()
    db.close()
