import sqlite3
import pandas as pd
import os


db_file = 'movies_data.db'


if os.path.exists(db_file):
    os.remove(db_file)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

print("Tworzę strukturę bazy i ładuję dane...")


def import_csv_to_sqlite(csv_name, table_name, connection):
    try:

        df = pd.read_csv(csv_name)

        df.to_sql(table_name, connection, if_exists='replace', index=False)
        print(f"Tabela '{table_name}' gotowa (wierszy: {len(df)})")
    except Exception as e:
        print(f"Błąd przy pliku {csv_name}: {e}")


import_csv_to_sqlite('movies.csv', 'movies', conn)
import_csv_to_sqlite('links.csv', 'links', conn)
import_csv_to_sqlite('ratings.csv', 'ratings', conn)
import_csv_to_sqlite('tags.csv', 'tags', conn)

print("Baza gotowa! Plik 'movies_data.db' został utworzony.\n")



print("--- DEMONSTRACJA NOWEGO PODEJŚCIA (SQL) ---")


query = """
SELECT m.title, AVG(r.rating) as srednia_ocena
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.title
HAVING count(r.rating) > 10  -- tylko filmy z więcej niż 10 głosami
ORDER BY srednia_ocena DESC
LIMIT 5
"""


wynik = pd.read_sql_query(query, conn)

print("Wynik zapytania SQL (Top 5 filmów):")
print(wynik)

conn.close()