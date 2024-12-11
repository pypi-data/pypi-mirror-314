# Good Home API Client

Good Home API Client is a Python client for interacting with the Good Home API. This client allows you to manage authentication, refresh tokens, verify tokens, and retrieve information about users, devices, and homes via the Good Home API.

## Prerequisites

- Python 3.6+
- `requests` package
- `pydantic` package
- `requests-mock` package (for testing)

## Installation

Clone this repository and install the necessary dependencies.

```bash
git clone https://github.com/biker91620/goodhomepy.git
python setup.py install
```

## Example
```python
from good_home_client import GoodHomeClient

# Initialize the client
client = GoodHomeClient()

# Example of logging in
response = client.login("example@example.com", "password")
print(response)

# Update the access token
client.token = response.token

# Verify the token
verify_response = client.verify_token(client.token)
print(verify_response)

# Retrieve the user's devices
devices_response = client.get_devices("user_id")
print(devices_response)

# Retrieve user information
user_response = client.get_user("user_id")
print(user_response)

# Retrieve the user's homes
homes_response = client.get_homes("user_id")
print(homes_response)

```