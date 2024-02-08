import os
import sys
from datetime import datetime, timedelta
import xlsxwriter

from data_operations import setup, rm_zips
from watchlist_operations import watchlist, closingFilter
import constants as c

def main():
    directories = [c.ONE_MONTH_PATH, c.FIVE_DAYS_PATH, c.THREE_MONTHS_PATH]
    destination = os.getcwd()
    rm_zips(destination)
    file_path = c.RESULTS_FILE
    workbook = xlsxwriter.Workbook(file_path)
    workbook.add_worksheet('1 MONTH')
    workbook.add_worksheet('5 DAYS')
    workbook.add_worksheet('3 MONTHS')
    workbook.close()
    for index, directory in enumerate(directories):
        path = os.path.join(destination, directory)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            if any(os.listdir(path)):
                rm_zips(path)
    else:
        setup(three_months_date, one_month_date, five_days_date, end_date, path)
    watchlist(os.path.join(destination, c.THREE_MONTHS_PATH), 0)
    watchlist(os.path.join(destination, c.ONE_MONTH_PATH), 1)
    watchlist(os.path.join(destination, c.FIVE_DAYS_PATH), 2)
    closingFilter(destination)


if __name__ == "__main__":
    
    three_months_date = datetime.strptime(
        (datetime.now() - timedelta(weeks=12)).strftime(c.DATE_FORMAT), c.DATE_FORMAT)
    one_month_date = datetime.strptime(
        (datetime.now() - timedelta(weeks=4)).strftime(c.DATE_FORMAT), c.DATE_FORMAT)
    five_days_date = datetime.strptime(
        (datetime.now() - timedelta(days=5)).strftime(c.DATE_FORMAT), c.DATE_FORMAT)
    end_date = datetime.strptime(
        (datetime.now() + timedelta(days=1)).strftime(c.DATE_FORMAT), c.DATE_FORMAT)
    main()

    sys.exit()