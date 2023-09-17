import requests
from bs4 import BeautifulSoup
import spacy
from langdetect import detect

# Load spaCy models for multiple languages
nlp_models = {
    'en': spacy.load('en_core_web_sm'),  # English
    'es': spacy.load('es_core_news_sm'),  # Spanish
    # Add more languages and models as needed
}

# Function to extract human names from text in a specific language
def extract_names(text, lang):
    doc = nlp_models[lang](text)
    names = []
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            names.append(entity.text)
    return names

# URL of the website you want to scrape
url = "https://www.lomilomi-sisters.de/about/"

# Send an HTTP GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text content from the website (you may need to refine this based on the website's structure)
    text = soup.get_text()

    # Detect the language of the text
    detected_language = detect(text)

    # Extract human names based on the detected language
    if detected_language in nlp_models:
        names = extract_names(text, detected_language)
        print(f"Names in {detected_language}: {names}")
    else:
        print("No NLP model available for the detected language.")
else:
    print("Failed to retrieve the web page.")
