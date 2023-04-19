import requests

# set up the base URL of your Flask application
base_url = 'http://127.0.0.1:5000'

# define the users to be created
users = [
  {
    "email": "abc@gmail.com",
    "password1": "123",
    "password2": "123",
    "username": "abc",
    "role": "admin"
  },
  {
    "email": "def@gmail.com",
    "password1": "456",
    "password2": "456",
    "username": "def",
    "role": "user"
  },
  {
    "email": "ghi@gmail.com",
    "password1": "789",
    "password2": "789",
    "username": "ghi",
    "role": "user"
  },
  {
    "email": "jkl@gmail.com",
    "password1": "101112",
    "password2": "101112",
    "username": "jkl",
    "role": "user"
  },
  {
    "email": "mno@gmail.com",
    "password1": "131415",
    "password2": "131415",
    "username": "mno",
    "role": "user"
  }
]

# loop through each user and send a POST request to the Flask endpoint to create the user
for user in users:
    response = requests.post(f'{base_url}/signup', data=user)
    print(response.status_code)