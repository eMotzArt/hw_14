import pathlib
import sqlite3


class DbReader:
    def __init__(self):
        self.path_db = pathlib.Path().resolve().joinpath('netflix.db')

    def db_request(self, query):
        con = sqlite3.connect(self.path_db)
        cur = con.cursor()
        result = cur.execute(query).fetchall()

        con.close()
        return result

    def get_film_by_title(self, title: str):
        query = f"""
            SELECT 
                title, country, release_year, listed_in, description
            FROM 
                netflix
            WHERE
                title = "{title}"
            ORDER BY release_year desc        
        """
        result = self.db_request(query)
        pass

DbReader().get_film_by_title('100 Humans')