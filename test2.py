import requests
from bs4 import BeautifulSoup
import os

def download_images(query, num_images=5):
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all("img", limit=num_images + 1)  # First image is the Google logo
    img_urls = []
    for img in img_tags[1:num_images + 1]:  # Skip the first image (Google logo)
        img_url = img.get('data-src') or img.get('src')
        if img_url:
            img_urls.append(img_url)

    if not os.path.exists('downloaded_images'):
        os.makedirs('downloaded_images')

    for i, img_url in enumerate(img_urls):
        try:
            img_response = requests.get(img_url, headers=headers)
            with open(f'downloaded_images/image_{i + 1}.jpg', 'wb') as f:
                f.write(img_response.content)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

    print(f"Downloaded {len(img_urls)} images.")

# Example usage
download_images("military trucks in forest", num_images=50)
