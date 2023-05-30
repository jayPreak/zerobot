import requests

# This URL is a direct link to the image file in your GitHub repository
url = 'https://raw.githubusercontent.com/jaypreak/zerobot/main/frames/S01/01x1.jpg'

response = requests.get(url, stream=True)

# Ensure the request was successful
response.raise_for_status()

# Open a new file in binary mode and save the image data to it
with open('path_to_local_image.jpg', 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)
