import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract article text from a given URL
def extract_article_text(url, url_id):
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract article title
        article_title = soup.title.text.strip() if soup.title else "No Title Found"

        # Extract article text
        article_text = ""
        article_body = soup.find('body')  # Assume article is contained within the <body> tag
        if article_body:
            for paragraph in article_body.find_all('p'):  # Extract paragraphs
                article_text += paragraph.text.strip() + "\n"

        # Save the extracted article text into a text file
        with open(f"articles/{url_id}.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {article_title}\n\n{article_text}")

        print(f"Article text extracted and saved for URL_ID: {url_id}")
    except Exception as e:
        print(f"Error extracting article text for URL_ID: {url_id}. Error: {e}")

# Read the input.xlsx file
input_data = pd.read_excel("D:\Projects\Intern\Intern\Input.xlsx")

# Create a folder to save the extracted article text files
if not os.path.exists("articles"):
    os.makedirs("articles")

# Iterate through each row in the input data
for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    extract_article_text(url, url_id)
