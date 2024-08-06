# APIGuard

### Token system to protect your API

#### APIGuard is an API protection system developed to ensure secure access to your web services. Using token-based authentication, APIGuard allows developers to protect sensitive API endpoints in a simple and efficient way.

### Install requirements:
    pip install -r requirements.txt

### create database:
    python3 manage.py cretate_database

### create superuser
    python3 manage.py create_superuser

### run
    python3 main.py

![image](https://github.com/user-attachments/assets/afe56ad9-2dd3-42f1-ae66-7a27d42a40d0)

![image](https://github.com/user-attachments/assets/6421fa4e-ad83-403f-b737-daffb8449f41)

![image](https://github.com/user-attachments/assets/602506a9-ee47-473b-8f24-c0ba7069b308)

![image](https://github.com/user-attachments/assets/e085f8af-e4d4-4a57-b6ac-96b94a2d616d)

![image](https://github.com/user-attachments/assets/939bc425-84d4-4451-b4ac-4e56536f5b46)

![image](https://github.com/user-attachments/assets/641e1c9b-134c-4650-8bae-42f3c32e297e)

![image](https://github.com/user-attachments/assets/016dd469-b76f-409b-8591-8c7319c0464c)








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

