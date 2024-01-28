import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)

def download_images_from_website(url, base_folder):
    # Create a new folder with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Extract the domain name from the URL
    domain = urlparse(url).netloc
    folder_path = os.path.join(base_folder, f"images_{domain} "+timestamp)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Successfully connected to the website")
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Download each image
        for img_tag in img_tags:
            src = img_tag.get('src')
            if src:
                # Join the URL of the webpage with the image URL
                img_url = urljoin(url, src)

                # Check if the URL is an absolute URL
                if urlparse(img_url).scheme:
                    # Get the file name from the URL
                    file_name = os.path.basename(img_url)

                    # Sanitize the file name
                    file_name = sanitize_filename(file_name)

                    # Build the full path to save the image
                    full_path = os.path.join(folder_path, file_name)

                    # Send a GET request to the image URL
                    img_response = requests.get(img_url)

                    # Save the image to the specified folder
                    with open(full_path, 'wb') as img_file:
                        img_file.write(img_response.content)

                    print(f"Downloaded image: {file_name}")

        # Check if the folder is empty
        if not os.listdir(folder_path):
            print("No images downloaded.")
        else:
            print(f"\n--DOWNLOAD COMPLETED--\nImages saved to: {os.path.abspath(folder_path)}")
    
    else:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")

# --INSERT WEBSITE HERE--
website_url = ""
# --Download Location--
base_folder = ""

# Extract the domain name from the URL
domain = urlparse(website_url).netloc

download_images_from_website(website_url, base_folder)
