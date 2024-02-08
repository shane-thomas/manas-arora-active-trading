import os
from zipfile import ZipFile
from datetime import datetime, timedelta
import urllib.request
import socket
import constants as c


def setup(three_months_date, one_month_date, five_days_date, end_date, path):
    delta = end_date - three_months_date
    date_range = []

    for i in range(delta.days + 1):
        date = three_months_date + timedelta(days=i)
        if date.weekday() < 5:
            date_range.append(date)

    for date in date_range:
        # url = c.URL + "{}/{}".format(
        #     date.strftime("%Y"), date.strftime("%b").upper())
        url = f"{c.URL}{date.strftime('%Y')}/{date.strftime('%b').upper()}"
        date_str = date.strftime("%d%b%Y").upper()
        filename = "cm{}bhav.csv.zip".format(date_str)
        url = "{}/{}".format(url, filename)
        try:
            get_file(url, path, one_month_date, five_days_date, end_date)
        except Exception:
            continue


def get_file(url, destination, one_month_date, five_days_date, end_date):
    socket.setdefaulttimeout(1)
    # Downloading
    zip_filename = os.path.basename(url)
    zip_path = os.path.join(destination, zip_filename)
    urllib.request.urlretrieve(url, zip_path)

    # Extracting and Renaming
    with ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith("bhav.csv"):
                date_str = file_info.filename[2:11]
                date_obj = datetime.strptime(date_str, "%d%b%Y")
                new_name = date_obj.strftime(c.DATE_FORMAT) + "-NSE-EQ.csv"
                file_info.filename = new_name
                zip_ref.extract(file_info, destination)
                if one_month_date <= date_obj <= end_date:
                    path = os.path.join(destination, "../1 MONTH")
                    zip_ref.extract(file_info, path)
                if five_days_date <= date_obj <= end_date:
                    path = os.path.join(destination, "../5 DAYS")
                    zip_ref.extract(file_info, path)

    os.remove(zip_path)


def rm_zips(directory):
    filelist = [f for f in os.listdir(directory) if (
        f.endswith(".csv") or f.endswith(".zip"))]
    for f in filelist:
        os.remove(os.path.join(directory, f))
