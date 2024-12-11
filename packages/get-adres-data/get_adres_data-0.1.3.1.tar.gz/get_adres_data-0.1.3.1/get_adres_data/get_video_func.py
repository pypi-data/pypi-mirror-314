from IPython.display import display, HTML
import json


# Ref: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
def get_video(filename, pos, adres_token):
    # Create a custom HTML video element with JavaScript to set headers
    video_url = f"https://www.adres-risa.org/v1/assessment/videostream/{filename}/{pos}/"

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

