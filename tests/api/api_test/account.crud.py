import requests

url = "http://localhost:5000/api"


class TestAccountAPI:

    def test_get_account_request_found(self):
        requests.post(f"{url}/accounts", json={
            "first_name": "John",
            "last_name": "Pork",
            "pesel": "12345678901"
        })

        response = requests.get(f"{url}/accounts/12345678901")
        assert response.status_code == 200

        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Pork"
        assert data["pesel"] == "12345678901"
        assert data["balance"] == 0


    def test_get_account_request_not_found(self):
        response = requests.get(f"{url}/accounts/00000000000")
        assert response.status_code == 404
        assert response.json() == {"message": "Account not found"}


    def test_update_account_request(self):
        requests.post(f"{url}/accounts", json={
            "first_name": "John",
            "last_name": "Pork",
            "pesel": "12345678902"
        })

        response = requests.patch(f"{url}/accounts/12345678902", json={
            "first_name": "Jane"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "Account updated"}

        response = requests.get(f"{url}/accounts/12345678902")
        data = response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Pork"


    def test_delete_account_request(self):
        requests.post(f"{url}/accounts", json={
            "first_name": "John",
            "last_name": "Pork",
            "pesel": "12345678903"
        })

        response = requests.delete(f"{url}/accounts/12345678903")
        assert response.status_code == 200
        assert response.json() == {"message": "Account deleted"}

        response = requests.get(f"{url}/accounts/12345678903")
        assert response.status_code == 404
        assert response.json() == {"message": "Account not found"}