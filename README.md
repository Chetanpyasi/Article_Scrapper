# Article_Scrapper
This is a python code that automatically scrapes through the website in search for key tags/points such as: headline, description, content, image_url, etc and stores them inside an mongoDB noSQL database.

# Prerequisites
## MongoDB
* Make sure MongoDB is installed, if not install from the official website:
  ```
  https://www.mongodb.com/try/download/community
  ```
* Follow the installation instructions for your operating system.
* Start the MongoDB server:
  ```
  mongod
  ```
  

### Initalise python enviroment
```
python -m venv myenv
```
### Run the enviroment
```
myenv\Scripts\activate
```

### Install the requirments
```
pip install -r requirements.txt
```
### Run the scrapper.py
```
python scrapper.py
```

# Description
This project uses python libraries to scrap throught news webpages and store the relevent data in mongo db in Storage.json file formate. 

> [!NOTE]
> Paste the urls to be scrapped in urls.txt.
