import requests
from io import StringIO

import pandas as pd
from pandas import DataFrame

from IPython.display import display, HTML
import json

# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

def get_data(csv_url: str, sessionKey: str) -> DataFrame:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(f"https://www.adres-risa.org/v1/dataanalytics/assessmentsubject/{csv_url}", headers=headers)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        csv_data = StringIO(csv_response.text)
        df = pd.read_csv(csv_data)

        return df
    else:
        print(f"Cannot get csv data: {csv_url}")
        return None

def get_image(filename: str, sessionKey: str) -> str:
    # Make the request to download the CSV file
    headers = {
        "adres-analytics-token": sessionKey
    }

    csv_response = requests.get(f"https://www.adres-risa.org/v1/assessment/image/{filename}/", headers=headers)

    if csv_response.status_code == 200:
        # Read the CSV content into a DataFrame
        json_data = json.loads(StringIO(csv_response.text).getvalue())

        return json_data
    else:
        print(f"Cannot get image file: {filename}")
        return None

# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
def get_video(filename, adres_token):
    # Create a custom HTML video element with JavaScript to set headers
    video_url = f"https://www.adres-risa.org/v1/assessment/videostream/{filename}/0/"

    html = f"""
    <video id="video" controls autoplay style="width: 100%; height: auto;">
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <script>
        const video = document.getElementById('video');
        const token = '{adres_token}';
        
        // Fetch video with authentication header
        fetch('{video_url}', {{
            method: 'GET',
            headers: {{
                'adres-analytics-token': token
            }}
        }})
        .then(response => {{
            if (!response.ok) throw new Error('Network response was not ok');
            return response.blob();
        }})
        .then(blob => {{
            const objectURL = URL.createObjectURL(blob);
            video.src = objectURL;
        }})
        .catch(error => console.error('Fetch error:', error));
    </script>
    """
    display(HTML(html))


# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

# def get_uvf(filename: str, sessionKey: str) -> DataFrame:

# def get_pdf(filename: str, sessionKey: str) -> DataFrame:

