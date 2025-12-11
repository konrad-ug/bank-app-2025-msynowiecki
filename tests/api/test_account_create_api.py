import requests

url = "http://localhost:5000/api"

def test_create_account_request():

    base = {"first_name": "John", "last_name": "Pork", "pesel": "89092909825"}

    post_response = requests.post(f"{url}/accounts", json = base)

    assert post_response.status_code == 201
    assert post_response.json() == {"message": "Account created"}


    get_response = requests.get(f"{url}/accounts/89092909825")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["first_name"] == "John"
    assert data["last_name"] == "Pork"
    assert data["pesel"] == "89092909825"
    assert data["balance"] == 0