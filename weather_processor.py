from datetime import datetime
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """
    """

    def __init__(self):
        self.db = DBOperations()
        self.plotter = PlotOperations()
        self.scraper = WeatherScraper(start_url="")

        self.db.initialize_db()

    def run(self):
        """
        This function controls the main menu for the WeatherProcessor application giving the user options to
        either download the weather data, update the weather data, generate a boxplot, generate a lineplot and exit the program.
        """
        while True:
            print("\n--- Winnipeg Weather ---")
            print("1. Download All Data")
            print("2. Update Data")
            print("3. Generate Boxplot")
            print("4. Generate Line Plot")
            print("5. Exit")

            choice = input("Please select a option:")

            if choice == "1":
                self.download_data()
            elif choice == "2":
                self.update_data()
            elif choice == "3":
                self.generate_boxplot()
            elif choice == "4":
                self.generate_lineplot()
            elif choice == "5":
                print("Exiting Program.")
                break
            else:
                print("Please select another option")


    def download_data(self):
        """
        download_data updates the weather database and purges the existing data so all the rows are updated.
        """
        print("Downloading All Data")
        self.db.purge_data()
        data = self.scraper.scrape()
        self.db.save_data(data)
        print(f"{len(data)} records downloaded")


    def update_data(self):
        """
        update_data will update all the rows inside the weather database for if the user needs more current information.
        """
        rows = self.db.fetch_data()

        if not rows:
            print("No pre-existing data, please download data first")
            return

        latest_date = max(row[0] for row in rows)
        latest = datetime.strptime(latest_date, "%Y-%m-%d")
        today = datetime.now()


        if latest.date() == today.date():
            print("Database is already up to date")
            return


        print(f"Updating data from {latest_date} to today")
        data = self.scraper.scrape()
        self.db.save_data(data)
        print("Weather Data Update Complete")


    def generate_boxplot(self):
        """
        generate_boxplot will provide the user the choice for which years they would like the boxplot to show data from.
        """
        start_year = int(input("Enter start year: "))
        end_year = int(input("Enter end year: "))

        rows = self.db.fetch_data()
        self.plotter.generate_boxplot(rows, start_year, end_year)


    def generate_lineplot(self):
        """
        generate_lineplot will provide the user the choice for which year and month that they would like to see data for.
        """
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        rows = self.db.fetch_data()
        self.plotter.generate_lineplot(rows, month, year)


if __name__ == "__main__":
    WeatherProcessor().run()
