import pathlib
import sqlite3


class DbReader:
    def __init__(self):
        self.path_db = pathlib.Path().resolve().joinpath('netflix.db')

    def db_request(self, query):
        with sqlite3.connect(self.path_db) as con:
            result = con.cursor().execute(query).fetchall()
        return result

    def convert_single_to_dict(self, data_tupple, keys):
        result: dict = {}
        for data, key in zip(data_tupple, keys):
            result.update({key: data})
        return result

    def convert_results_to_view(self, data_tupple, *keys):
        result: list[dict] = []
        for items in data_tupple:
            one_item_dict: dict = {}
            for column, key in zip(items, keys):
                one_item_dict.update({key: column})
            result.append(one_item_dict)

        return result


#get
    def get_film_by_title(self, title: str):
        query = f"""
            SELECT 
                title, country, release_year, listed_in, description
            FROM 
                netflix
            WHERE
                LOWER(title) = LOWER("{title}")
            ORDER BY release_year desc        
        """
        result = self.db_request(query)
        convert_result = self.convert_results_to_view(result, 'title', 'country', 'release_year', 'genre', 'description')
        return convert_result

    def get_films_from_year_to_year(self, from_year: int, to_year: int):
        query = f"""
            SELECT 
                title, release_year
            FROM 
                netflix
            WHERE release_year BETWEEN {from_year} AND {to_year}
            ORDER BY release_year DESC
            LIMIT 100
        """
        result = self.db_request(query)
        convert_result = self.convert_results_to_view(result, "title", "release_year")
        return convert_result

    def get_films_by_rating(self, rating: str):
        ratings = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'G', 'PG', 'PG-13', 'R', 'NC-17'"
        }
        rating_for_query = ratings.get(rating.lower())

        query = f"""
            SELECT 
                title, rating, description
            FROM 
                netflix
            WHERE
                rating in {tuple(rating_for_query)}
        """


        result = self.db_request(query)
        convert_result = self.convert_results_to_view(result, 'title', 'rating', 'description')
        return convert_result

    def get_films_by_genre(self, genre):
        query = f"""
            SELECT 
                title, description
            FROM 
                netflix
            WHERE
                LOWER(listed_in) = LOWER("{genre}")
            ORDER BY release_year desc 
            LIMIT 10       
        """
        result = self.db_request(query)
        convert_result = self.convert_results_to_view(result, 'title', 'description')
        return convert_result

    def get_films_by_type_year_genre(self, type, year, genre):
        query = f"""
            SELECT 
                title, description
            FROM 
                netflix
            WHERE
                LOWER(type) = LOWER("{type}") AND
                release_year = {year} AND
                LOWER(listed_in) = LOWER("{genre}") 
            ORDER BY title ASC 
        """
        result = self.db_request(query)

        convert_result = self.convert_results_to_view(result, 'title', 'description')
        return convert_result

    def get_companions_of_two_actors(self, actor_one, actor_two):
        # получил касты всех фильмов, где снимались актер1 и актер2
        query = f"""
                    SELECT 
                        "cast"
                    FROM 
                        netflix
                    WHERE
                        LOWER("cast") LIKE  LOWER('%{actor_one}%') AND
                        LOWER("cast") Like LOWER('%{actor_two}%')
                    ORDER BY title ASC 
                """
        all_casts = self.db_request(query)


        all_actors: dict = {}
        for cast in all_casts:
            #разделил и отформатировал актеров
            actors_list = str(cast).split(', ')
            actors_set = set(map(lambda element: ''.join(char for char in element if char.isalpha() or char.isspace()), actors_list))
            #убрал двух искомых актеров из сета
            companions = actors_set - {actor_one, actor_two}

            for companion in companions:
                if count:=all_actors.get(companion):
                    all_actors.update({companion: count+1})
                else:
                    all_actors.update({companion: 1})

        twice_or_more_actors = []
        for actor, count in all_actors.items():
            if count >=2:
                twice_or_more_actors.append(actor)

        return twice_or_more_actors
