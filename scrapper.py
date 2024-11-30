import requests
from bs4 import BeautifulSoup
import pymongo
import re
from pymongo import MongoClient
from datetime import datetime

def scrape_toi_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the headline
        headline_tag = soup.find("h1")
        headline = headline_tag.text.strip() if headline_tag else "No headline found"
        
        # Extract the publication date from <span> tag
        date_tag = soup.find("span", string=re.compile(r"Updated:.*"))
        if date_tag:
            date_text = date_tag.text.strip()
            # Extract date from "Updated: Nov 30, 2024, 13:59 IST" format
            date_match = re.search(r"Updated:\s*(\w+\s\d{1,2},\s\d{4})", date_text)
            date = date_match.group(1) if date_match else "No date found"
        else:
            date = "No date found"
        
        # Extract the content
        paragraphs = soup.find_all("div", class_="Normal")
        content = " ".join([para.text.strip() for para in paragraphs if para.text.strip()])
        
        # Extract the description (meta description tag)
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag.get("content", "No description found").strip() if description_tag else "No description found"
        
        # Extract the image URL (og:image meta tag)
        image_tag = soup.find("meta", attrs={"property": "og:image"})
        image_url = image_tag.get("content", "No image found").strip() if image_tag else "No image found"
        
        # Get the current time for created_at and updated_at
        current_time = datetime.utcnow().isoformat()  # ISO 8601 format: "2024-11-30T14:00:00Z"
        
        # Prepare article data in the generic format
        article_data = {
            "headline": headline,
            "date": date,
            "description": description,
            "content": content,
            "image_url": image_url,
            "author": "Unknown",  # You can add an author extraction if available
            "tags": [],  # You can implement a way to extract tags if available
            "url": url,
            "source": "Times of India",  # Default to "Times of India" for this case
            "language": "English",  # Assuming the article is in English, adjust as necessary
            "publisher": "Times of India",
            "created_at": current_time,
            "updated_at": current_time
        }

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if different
        db = client['news_database']  # Database name
        collection = db['articles']  # Collection name

        # Use the article's URL as a unique identifier for the document
        collection.update_one({"url": url}, {"$set": article_data}, upsert=True)

        print(f"Article data saved in MongoDB with URL: {url}")
    else:
        print(f"Failed to fetch the article. Status code: {response.status_code}")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def main():
    # Path to the file containing the URLs
    file_path = "urls.txt"
    
    # Read URLs from the file
    urls = read_urls_from_file(file_path)
    
    # Scrape each URL and store the data in MongoDB
    for url in urls:
        scrape_toi_article(url)

# Run the main function
if __name__ == "__main__":
    main()
