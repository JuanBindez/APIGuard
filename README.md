# API Token System

Token system to protect your API

### Install requirements:
    pip install -r requiments.txt

### install sqlite:
    sudo apt install sqlite3

### create database:
    sqlite3 database.db < schema.sql

# Deploy in GCP

### How to initialize the gcloud CLI in project path
    gcloud init

### deploy
    gcloud run deploy --source .


### Example of a script consuming data from a token-protected api

```python
>>> import requests
>>> 
>>> TOKEN = 'f20e94eb-d573-444a-86fb-1dd1e359008b'
>>> 
>>> url = 'http://127.0.0.1:5000/api/data'
>>> headers = {'Authorization': TOKEN}
>>> response = requests.get(url, headers=headers)
>>> 
>>> print(response.json())
{'data': 'here is the protected data'}
>>> 

```
### If the token is wrong it will not receive the data and will return an error

```python
>>> import requests
>>> 
>>> TOKEN = 'f20e94eb-d573-44fsdfdsf6f56sdfdsfb'
>>> 
>>> url = 'http://127.0.0.1:5000/api/data'
>>> headers = {'Authorization': TOKEN}
>>> response = requests.get(url, headers=headers)
>>> 
>>> print(response.json())
{'message': 'Invalid token'}
>>> 

```
