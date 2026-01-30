import requests
import pytest
import uuid

url = "http://localhost:5000/api"

@pytest.fixture
def create_account():
    base_account = {
        "first_name": "John",
        "last_name": "Test",
        "pesel": str(uuid.uuid4().int)[:11],
    }

    response = requests.post(f"{url}/accounts", json=base_account)
    assert response.status_code == 201

    response = requests.post(
        f"{url}/accounts/{base_account['pesel']}/transfer",
        json={"type": "ingoing", "amount": 1000.0}
    )

    assert response.status_code == 200

    yield base_account

    requests.delete(f"{url}/accounts/{base_account['pesel']}")


class TestAccountAPI:

    def test_get_account_request_found(self, create_account):
        account = create_account

        response = requests.get(f"{url}/accounts/{account['pesel']}")
        assert response.status_code == 200

        data = response.json()
        assert data["first_name"] == account["first_name"]
        assert data["last_name"] == account["last_name"]
        assert data["pesel"] == account["pesel"]


    def test_get_account_request_not_found(self, create_account):
        account = create_account

        response = requests.get(f"{url}/accounts/0000000000X")
        assert response.status_code == 404
        assert response.json() == {"message": "Account not found"}


    def test_update_account_request(self, create_account):
        account = create_account

        response = requests.patch(f"{url}/accounts/{account['pesel']}", json={"first_name": "Jane"})

        assert response.status_code == 200
        assert response.json() == {"message": "Account updated"}

        response = requests.get(f"{url}/accounts/{account['pesel']}")
        data = response.json()

        assert response.status_code == 200
        assert data["first_name"] == "Jane"
        assert data["last_name"] == account["last_name"]


    def test_delete_account_request(self, create_account):
        account = create_account

        response = requests.delete(f"{url}/accounts/{account['pesel']}")
        assert response.status_code == 200
        assert response.json() == {"message": "Account deleted"}

        response = requests.get(f"{url}/accounts/{account['pesel']}")
        assert response.status_code == 404
        assert response.json() == {"message": "Account not found"}


    @pytest.mark.parametrize(
        "transfer_type, amount, expected_status, expected_message",
        [
            ("ingoing", 100.0, 200, "Transfer commissioned"),
            ("outgoing", 50.0, 200, "Transfer commissioned"),
            ("express", 10.0, 200, "Transfer commissioned"),
            ("invalid", 10.0, 400, "Invalid transfer type"),
            ("outgoing", -10000.0, 422, "Transfer failed"),
        ]
    )

    def test_transfer_requests(self, create_account, transfer_type, amount, expected_status, expected_message):
        account = create_account

        response = requests.post(
            f"{url}/accounts/{account['pesel']}/transfer",
            json={"type": transfer_type, "amount": amount}
        )

        assert response.status_code == expected_status
        assert response.json()["message"] == expected_message