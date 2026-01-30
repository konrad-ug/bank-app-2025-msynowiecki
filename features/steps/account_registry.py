from behave import *
import requests

URL = "http://localhost:5000"

@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        requests.delete(URL + f"/api/accounts/{account['pesel']}")

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {"first_name": name, "last_name": last_name, "pesel": pesel}
    response = requests.post(URL + "/api/accounts", json=json_body)
    assert response.status_code == 201

@step('Number of accounts in registry equals: "{count}"')
def check_account_count(context, count):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    assert len(accounts) == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_not_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_account_field(context, field, pesel, value):
    if field == "surname":
        json_body = {"last_name": value}
    elif field == "name":
        json_body = {"first_name": value}
    else:
        raise ValueError("Invalid field: must be 'name' or 'surname'")
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def check_account_field(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    data = response.json()
    if field == "surname":
        assert data["last_name"] == value
    elif field == "name":
        assert data["first_name"] == value
