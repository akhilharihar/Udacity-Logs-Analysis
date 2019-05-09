#!usr/bin/env python3

"""
analytics.py:
"""

import os
from sys import exit
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # load variables to the os environment declared in .env


class Config:
    """
    Application seetings file.
    """

    @classmethod
    def db_credentials(cls, string_format=True):
        """
        Returns db credentials declared in os environment.
        params:
        string_format(bool): if true, the credentials are returns as a string
        object else dict
        """

        credentials = {
            'dbname': os.getenv('DB_NAME').strip(),
            'user': os.getenv('DB_USERNAME').strip(),
            'password': os.getenv('DB_PASSWORD').strip(),
            'port': str(os.getenv('DB_PORT', 5432).strip()),
            'host': os.getenv('DB_HOST', 'localhost').strip()
        }

        if not string_format:
            return credentials

        cred_str_format = ''
        for key, value in credentials.items():
            cred_str_format += " {}={} ".format(key, value)

        return cred_str_format


class DB:
    """
    Universal db class. Create an instance of the db connection to perform \
    any queries.
    Extend this class if you want to include additional methods.
    """

    def __init__(self):
        try:
            self.__connection = psycopg2.connect(Config.db_credentials())
        except psycopg2.Error as e:
            print(e)
            exit(1)

    @property
    def query(self):
        """
        returns cursor object.
        """
        return self.__connection.cursor()

    def close(self):
        """
        Close connection to db establised via db object
        """
        self.__connection.close()

    def commit(self):
        """
        Commit changes made to db
        """
        self.__connection.commit()


def top_articles(cursor, total=3, stdout=False):
    """
    Prints top viewed articles.
    params:
    total(int): Nunber of top viewed articles to be returned.
    """

    popular_three_articles = cursor

    popular_three_articles.execute("select split_part(path, '/', 3), \
    count(path) from log where path != '/' group by path order by \
    count(path) desc limit %s;", (total,))
    if stdout:
        print('{} {} {}'.format('*' * 5, 'Top Three articles', '*' * 5))

        for index, article in enumerate(popular_three_articles):
            article_name = ' '.join(map(lambda x: x.capitalize(),
                                    article[0].split('-')))
            print("{}. {} - {} views".format(index + 1, article_name,
                                             article[1]))

    data = popular_three_articles.fetchall()
    popular_three_articles.close()
    return data


def popular_authors(cursor, stdout=False):
    """
    list authors with top viewed articles
    """

    sorted_authors = cursor

    sorted_authors.execute("select authors.name, count(log.path) from \
        log right join articles on substring(log.path, 10) = articles.slug \
        right join authors on authors.id = articles.author \
        group by authors.id order by count(log.path) desc;")

    if stdout:
        print('{} {} {}'.format('*' * 5, 'popular authors', '*' * 5))

        for index, author in enumerate(sorted_authors):
            print("{}. {} - {} views".format(index + 1, author[0], author[1]))

    data = sorted_authors.fetchall()
    sorted_authors.close()
    return data


def error_requests_per_day(cursor, stdout=False):
    """
    Prints percentage of error responses generated per day
    """

    error_requests = cursor

    error_requests.execute("select cast(log.time as date), count(log.status), \
        count(errors.status) from log left join (select error.id, error.status\
         from log error where error.status != '200 OK') as errors on \
        errors.id = log.id group by cast(log.time as date) having \
        (count(errors.status)*100.0)/count(log.status) > 1")

    if stdout:
        print('{} {} {}'.format('*' * 5, 'Error requests', '*' * 5))

        for errors in error_requests:
            formated_date = errors[0].strftime("%B %d, %Y")
            error_percentage = round((errors[2]/errors[1])*100, 2)
            print("{} - {}% errors".format(formated_date, error_percentage))

    data = error_requests.fetchall()
    error_requests.close()
    return data


if __name__ == "__main__":
    conn = DB()
    top_articles(conn.query, stdout=True)
    print('\n')
    popular_authors(conn.query, stdout=True)
    print('\n')
    error_requests_per_day(conn.query, stdout=True)
    print('\n')
    conn.close()
