import requests
from bs4 import BeautifulSoup

def get_telegram_user_details(username):
    url = f"https://telegram.dog/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Name
        name_tag = soup.find("div", class_="tgme_page_title")
        name = name_tag.text.strip() if name_tag else "Unknown Name"

        # Extract Bio
        bio_tag = soup.find("div", class_="tgme_page_description")
        bio = bio_tag.text.strip() if bio_tag else "No Bio"

        # Extract Profile Picture URL
        profile_img_tag = soup.find("img", class_="tgme_page_photo_image")
        profile_img = profile_img_tag["src"] if profile_img_tag else "No Profile Picture"

        return {"username": username, "name": name, "bio": bio, "profile_image": profile_img}
    else:
        return {"error": "User not found or profile is private."}

# Example usage
username = "itzAsuraa"  # Replace with the desired username
user_details = get_telegram_user_details(username)
print(user_details)