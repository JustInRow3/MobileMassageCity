import re
import requests
from bs4 import BeautifulSoup

# Function to extract phone numbers from text
def extract_phone_numbers(text):
    # Use a regular expression to find phone numbers
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    phone_numbers = re.findall(phone_pattern, text)
    return phone_numbers

# Function to extract phone numbers from a website
def extract_phone_numbers_from_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from the website
        text_content = soup.get_text()

        # Extract phone numbers from the text content
        phone_numbers = extract_phone_numbers(text_content)

        return phone_numbers
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return []

# Example usage
website_url = 'https://www.magoose-massage-yoga.de/kontakt'  # Replace with the URL of the website you want to scrape
phone_numbers = extract_phone_numbers_from_website(website_url)

if phone_numbers:
    print("Phone numbers found on the website:")
    for phone_number in phone_numbers:
        print(phone_number)
else:
    print("No phone numbers found on the website.")
