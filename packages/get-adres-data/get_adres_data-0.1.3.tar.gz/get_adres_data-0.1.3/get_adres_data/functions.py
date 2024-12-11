import requests
from io import StringIO

import pandas as pd
from pandas import DataFrame

# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

def get_uvf(filename: str, sessionKey: str) -> DataFrame:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(f"https://www.adres-risa.org/v1/assessment/uvfstream/{filename}/", headers=headers)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        csv_data = StringIO(csv_response.text)
        df = pd.read_csv(csv_data)

        return df
    else:
        return None

def get_pdf(filename: str, sessionKey: str) -> DataFrame:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(f"https://www.adres-risa.org/v1/assessment/pdf/{filename}/", headers=headers)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        csv_data = StringIO(csv_response.text)
        df = pd.read_csv(csv_data)

        return df
    else:
        return None

