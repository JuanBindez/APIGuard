# APIGuard

### Token system to protect your API

#### APIGuard is an API protection system developed to ensure secure access to your web services. Using token-based authentication, APIGuard allows developers to protect sensitive API endpoints in a simple and efficient way.

### Install requirements:
    pip install -r requirements.txt

### create database:
    python3 manage.py cretate-database

### create superuser
    python3 manage.py create-superuser

### run
    python3 main.py

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

### Deploy in GCP

### How to initialize the gcloud CLI in project path
    gcloud init

### deploy
    gcloud run deploy --source .

