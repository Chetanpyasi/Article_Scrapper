from pymongo import MongoClient
import json
from bson import ObjectId

def display_all_data():
    client = MongoClient('mongodb://localhost:27017/')  # MongoDB URI
    db = client['news_database']  # database name
    collection = db['articles']  # collection name

    articles = collection.find()

    def convert_objectid_to_str(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert_objectid_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid_to_str(i) for i in obj]
        else:
            return obj

    for article in articles:
        article = convert_objectid_to_str(article)
        print(json.dumps(article, indent=4)) 

if __name__ == "__main__":
    display_all_data()
