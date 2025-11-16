"""

Final Project
Student ID: 0390523
Name: Eric Kosmolak
Date: November 05, 2025
Version 1.0
Group 10

The scrape_weather.py module is designed to scrape weather from Winnipeg, MB as far back as possible using the
provided URL from the rubric. This module is step 1 of the final project for ADEV 3005.
"""

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
import time
from db_operations import DBOperations

class WeatherHTMLParser(HTMLParser):
    """
    WeatherHTMLParser is a HTML Parser for pulling daily weather data from
    a Environment Canada URL. This parser looks for data rows and collects
    the values for days, max temp, min temp and mean temperature.
    """

    def __init__(self):
        """
        Initializing the parser.
        """
        super().__init__()
        self.in_row = False
        self.current_row = []
        self.data_rows = []

    def handle_starttag(self, tag, attrs):
        """
        handle_starttag begins when the HTML parser begins when a opening
        HTML tag is found.
        """
        if tag == "tr":
            self.in_row = True
            self.current_row = []

    def handle_endtag(self, tag):
        """
        handle_endtag begins when the HTML parser notices a closing HTML tag.
        """
        if tag == "tr" and self.in_row:
            self.in_row = False

            # Makes sure each row contains 4 values
            if len(self.current_row) >= 4:
                self.data_rows.append(self.current_row)

    def handle_data(self, data):
        """
        handle_data begins when text is found inside <tr> tags.
        """
        if self.in_row:
            cleaned = data.strip()
            if cleaned:
                self.current_row.append(cleaned)


class WeatherScraper:
    """
    WeatherScraper handles the scraping of the daily temperature data from Winnipeg
    from Enviroment Canada. It uses HTMLParser to pull temperature readings month by month
    until no more data is found.
    """

    BASE_URL = (
        "https://climate.weather.gc.ca/climate_data/daily_data_e.html"
        "?StationID=27174&timeframe=2&Day=1&Year={year}&Month={month}"
    )

    def __init__(self, start_url: str):
        """
        Initializing the WeatherScraper class.
        """
        self.start_url = start_url

    def _fetch(self, url: str) -> str | None:
        """
        _fetch attempts to fetch and return the HTML content from the URL.
        """
        try:
            with urlopen(url, timeout=10) as r:
                return r.read().decode("utf-8", errors="ignore")
        except (HTTPError, URLError):
            return None

    def _parse_weather(self, html: str) -> dict:
        """
        _parse_weather parses the data tables and pulls the temperature data.
        """
        parser = WeatherHTMLParser()
        parser.feed(html)

        results = {}

        # Each row will contain day, max temp, min temp and mean temperature
        for row in parser.data_rows:

            date = f"{self.current_year}-{self.current_month:02d}-{row[0]:0>2}"
            try:
                max_temp = float(row[1])
                min_temp = float(row[2])
                mean_temp = float(row[3])

                results[date] = {
                    "Max": max_temp,
                    "Min": min_temp,
                    "Mean": mean_temp,
                }
            except:
                # Skips rows if there is invalid or missing data
                pass

        return results

    def scrape(self) -> dict:
        """
        scrape will scrape the monthly weather data backwards from today until no more data is found.
        """
        all_data = {}

        today = datetime.now()
        year = today.year
        month = today.month

        # Scrapes moving backwards going month by month
        while True:
            url = self.BASE_URL.format(year=year, month=month)
            print(f"Checking {year}-{month:02d}")

            html = self._fetch(url)
            if not html:
                break

            # Storing current month and year
            self.current_year = year
            self.current_month = month

            # Parses the months data
            page_data = self._parse_weather(html)

            if not page_data:
                break

            all_data.update(page_data)

            # Moves to previous month while scraping
            month -= 1
            if month < 1:
                month = 12
                year -= 1

            time.sleep(0.3)

        return all_data


if __name__ == "__main__":
    scraper = WeatherScraper(start_url="")
    weather = scraper.scrape()

    db = DBOperations()
    db.initialize_db()

    db.save_data(weather)

    print("Saved", len(weather), "records to database.")
