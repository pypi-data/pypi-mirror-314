import requests
import pandas as pd
from io import StringIO

# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

def get_data(csv_url: String, sessionKey: String) -> DataFrame:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(csv_url, headers=headers, verify=False)

    if csv_response.status_code == 200:
        # Save CSV content to a file or process it
        print("CSV file downloaded successfully.")

    else:
        print("Failed to retrieve CSV file:", csv_response.text)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        csv_data = StringIO(csv_response.text)
        df = pd.read_csv(csv_data)

        # Display the DataFrame
        print("data frame:", df)

        # Display the DataFrame
        print("header: ", df.columns)

        return df
