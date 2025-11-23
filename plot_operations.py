import matplotlib.pyplot as plot
from datetime import datetime
from collections import defaultdict

class PlotOperations:
    """
    """

    def generate_boxplot(self, rows, start_year, end_year):
        """
        generate_boxplot will generate a box plot displaying the average temperature
        for each month between the choosen start_year and end_year.
        """
        month = defaultdict(list)

        for date_str, min_temp, max_temp, avg_temp in rows:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                avg_temp = float(avg_temp)
            except ValueError:
                continue

            if start_year <= date.year <= end_year:
                month[date.month].append(avg_temp)

        data = [month[m] for m in range(1, 13)]

        plot.figure()
        plot.boxplot(data)
        plot.title(f"Mean Monthly Temperatures ({start_year}--{end_year})")
        plot.xlabel("Month")
        plot.ylabel("Temperature (Celcsius)")
        plot.xticks(range(1, 13))
        plot.grid(True)
        plot.show()


    def generate_lineplot(self, rows, month, year):
        """
        generate_lineplot will generate a lineplot displaying the the average temperatures
        from the choosen year and month.
        """

        days = []
        temps = []

        for date_str, min_temp, max_temp, avg_temp in rows:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                avg_temp = float(avg_temp)
            except ValueError:
                continue

            if date.month == month and date.year == year:
                days.append(date.day)
                temps.append(avg_temp)

        plot.figure()
        plot.plot(days, temps)
        plot.title(f"Daily Mean Temperatures - {month}/{year}")
        plot.xlabel("Day")
        plot.ylabel("Temperature (Celcsius)")
        plot.grid(True)
        plot.show()
