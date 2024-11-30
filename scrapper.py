import requests
from bs4 import BeautifulSoup
import pymongo
import re
from pymongo import MongoClient
from datetime import datetime

def scrape_news_article(url):
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
        
        # Extract the description 
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag.get("content", "No description found").strip() if description_tag else "No description found"
        
        # Extract the image URL 
        image_tag = soup.find("meta", attrs={"property": "og:image"})
        image_url = image_tag.get("content", "No image found").strip() if image_tag else "No image found"
        
        # Get the current time for created_at and updated_at
        current_time = datetime.utcnow().isoformat()  
        
        # Prepare article data in the generic format
        article_data = {
            "headline": headline,
            "date": date,
            "description": description,
            "content": content,
            "image_url": image_url,
            "author": "Unknown",  
            "tags": [], 
            "url": url,
            "source": "Times of India", 
            "language": "English",  
            "publisher": "Times of India",
            "created_at": current_time,
            "updated_at": current_time
        }

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # MongoDB URI
        db = client['news_database']  # Database name
        collection = db['articles']  # Collection name

        collection.update_one({"url": url}, {"$set": article_data}, upsert=True)

        print(f"Article data saved in MongoDB with URL: {url}")
    else:
        print(f"Failed to fetch the article. Status code: {response.status_code}")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def main():
    file_path = "urls.txt"
    
    urls = read_urls_from_file(file_path)
    
    for url in urls:
        scrape_news_article(url)

if __name__ == "__main__":
    main()
