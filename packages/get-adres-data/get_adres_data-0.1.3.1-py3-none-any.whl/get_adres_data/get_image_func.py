import requests
from io import StringIO

def get_image(filename: str, sessionKey: str) -> String:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(f"https://www.adres-risa.org/v1/assessment/image/{filename}/", headers=headers)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        data_url = StringIO(csv_response.text)

        return data_url
    else:
        return None

