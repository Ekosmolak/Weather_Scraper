# db_operations.py
from dbcm import DBCM

class DBOperations:
    """
    Handles all weather data in the SQLite database.
    """

    def __init__(self, db_name="weather.db"):
        """
        Initializing the DBOperations class.
        """
        self.db_name = db_name


    def initialize_db(self):
        """
        Initialzes the weather database table if it does not exist already.
        """
        create_sql = """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weather_date TEXT NOT NULL,
            location TEXT NOT NULL,
            min_temp REAL,
            max_temp REAL,
            avg_temp REAL,
            UNIQUE(weather_date, location)
        );
        """

        with DBCM(self.db_name) as cursor:
            cursor.execute(create_sql)


    def purge_data(self):
        """
        purge_data deletes all the rows in the weather table withiout
        dropping the database.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("DELETE FROM weather;")


    def save_data(self, weather_data: dict, location="Winnipeg"):
        """
        save_data saves all the weather data into the weather database.
        """
        sql = """
        INSERT OR IGNORE INTO weather (weather_date, location, min_temp, max_temp, avg_temp)
        VALUES (?, ?, ?, ?, ?);
        """

        with DBCM(self.db_name) as cursor:
            for date, temperatures in weather_data.items():
                try:
                    min_temp = float(temperatures["Min"])
                    max_temp = float(temperatures["Max"])
                    avg_temp = float(temperatures["Mean"])
                except:
                    continue

                cursor.execute(sql, (
                    date,
                    location,
                    min_temp,
                    max_temp,
                    avg_temp
                ))


    def fetch_data(self, start_date=None, end_date=None, location="Winnipeg"):
        """
        fetch_data returns all the rows needed.
        """

        sql = """
        SELECT weather_date, min_temp, max_temp, avg_temp
        FROM weather
        WHERE location = ?
        """

        params = [location]

        if start_date:
            sql += " AND weather_date >= ?"
            params.append(start_date)

        if end_date:
            sql += " AND weather_date <= ?"
            params.append(end_date)

        sql += " ORDER BY weather_date ASC"

        with DBCM(self.db_name) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
