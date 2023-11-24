import os
from datetime import date
from calendar import Calendar

import sqlite3
from sqlite3 import Error


DB_FILE = os.path.join(
    os.getcwd(),
    'escala.db'
)


def create_tables():
    """ create the tables if they don't exist
    :return:
    """
    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor
    
    # create vigilants table
    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS vigilants (
                letter text PRIMARY KEY,
                name text NOT NULL
            );
            """
        )
    except Error as e:
        print(e)

    # create days table
    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS days (
                id integer PRIMARY KEY AUTOINCREMENT,
                date datetime,
                vigilant_night1 text NOT NULL,
                vigilant_night2 text NOT NULL,
                vigilant_day1 text,
                vigilant_day2 text,
                is_holiday boolean,
                FOREIGN KEY (vigilant_night1) REFERENCES vigilants (letter),
                FOREIGN KEY (vigilant_night2) REFERENCES vigilants (letter),
                FOREIGN KEY (vigilant_day1) REFERENCES vigilants (letter),
                FOREIGN KEY (vigilant_day2) REFERENCES vigilants (letter)
            );
            """
        )
    except Error as e:
        print(e)
    
    conn.commit() # commit our changes
    conn.close() # close our nonnection


def insert_letters():
    """Insert first five letters to vigilats table
    :return:
    """
    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor

    values = [(letter, '') for letter in 'ABCDE']
    try:
        c.executemany("""
            INSERT INTO vigilants VALUES (?, ?)
            """,
            values
        )
    except Error as e:
        print(e)

    conn.commit() # commit our changes
    conn.close() # close our nonnection


def get_vigilants_names() -> [(str, )]:
    """ 
    :return: list of vigilants names
    """
    names = 5 * [('', )]

    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor

    try:
        c.execute("""
        SELECT name
        FROM vigilants
        ORDER BY letter
        """)
        names = c.fetchall()
    except Error as e:
        print(e)

    conn.commit() # commit our changes
    conn.close() # close our nonnection

    return names


def get_vigilants_by_date(mdate: date):
    """ 
    :param mdate: a date object
    :return: list with letters and names from `mdate`
    """
    date_data = None

    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor

    try:
        c.execute("""
            SELECT
                night_vig1.letter,
                night_vig1.name,
                night_vig2.letter,
                night_vig2.name,
                day_vig1.letter,
                day_vig1.name,
                day_vig2.letter,
                day_vig2.name,
                days.is_holiday
            FROM days
            LEFT JOIN vigilants night_vig1 ON days.vigilant_night1 = night_vig1.letter
            LEFT JOIN vigilants night_vig2 ON days.vigilant_night2 = night_vig2.letter
            LEFT JOIN vigilants day_vig1 ON days.vigilant_day1 = day_vig1.letter
            LEFT JOIN vigilants day_vig2 ON days.vigilant_day2 = day_vig2.letter
            WHERE days.date = ?
            """, 
            (date.strftime(mdate, format = '%Y-%m-%d'), )
        )
        date_data = c.fetchone()
    except Error as e:
        print(e)

    conn.commit() # commit our changes
    conn.close() # close our nonnection

    return date_data


def update_names(names: [str]):
    """Update first five names to vigilats table
    :param names: list of strings with vigilants names
    :return:
    """
    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor

    letters = ['A', 'B', 'C', 'D', 'E']
    try:
        for letter, name in zip(letters, names):
            c.execute("""
                UPDATE vigilants SET name = ? WHERE letter = ?
                """,
                (name, letter)
            )
    except Error as e:
        print(e)

    conn.commit() # commit our changes
    conn.close() # close our nonnection


def set_vigilants_by_date(
        mdate: date,
        vigilant_night1: str,
        vigilant_night2: str,
        vigilant_day1: str,
        vigilant_day2: str,
        is_holiday: bool
    ):
    """Insert/update the month vigilants by date
    :param mdate: date that will be modified
    :param vigilant_night1: night vigilant
    :param vigilant_night2: night vigilant letter
    :param vigilant_day1: day vigilant letter
    :param vigilant_day2: day vigilant letter
    :param is_holiday: true if it is a holiday
    :return:
    """
    conn = sqlite3.connect(DB_FILE)  # connect to the database (and create it if not exists)
    c = conn.cursor() # create a cursor

    c.execute("""
        SELECT COUNT(*) FROM days WHERE days.date = ?
        """,
        (date.strftime(mdate, format = '%Y-%m-%d'), )
    )
    exists_date = c.fetchone()[0]

    if exists_date:
        try:
            c.execute("""
                UPDATE days 
                SET
                    vigilant_night1 = ?,
                    vigilant_night2 = ?,
                    vigilant_day1 = ?,
                    vigilant_day2 = ?,
                    is_holiday = ?
                WHERE days.date = ?
                """,
                (vigilant_night1, vigilant_night2,
                 vigilant_day1, vigilant_day2,
                 is_holiday,
                 date.strftime(mdate, format = '%Y-%m-%d'))
            )
        except Error as e:
            print(e)
    else:
        try:
            c.execute("""
                INSERT INTO days (date, vigilant_night1, vigilant_night2, vigilant_day1, vigilant_day2)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date.strftime(mdate, format = '%Y-%m-%d'),
                 vigilant_night1, vigilant_night2,
                 vigilant_day1, vigilant_day2)
            )
        except Error as e:
            print(e)


    conn.commit() # commit our changes
    conn.close() # close our nonnection