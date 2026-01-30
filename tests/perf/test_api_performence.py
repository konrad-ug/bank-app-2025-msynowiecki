import requests
import pytest
import time
import uuid

url = "http://127.0.0.1:5000/api"


@pytest.mark.perf
def test_create_delete_account_100_times():
    for i in range(100):
        pesel = str(uuid.uuid4().int)[:11]
        start = time.time()
        response = requests.post(
            f"{url}/accounts",
            json={
                "first_name": f"Perf{i}",
                "last_name": "Account",
                "pesel": pesel
            },
            timeout=0.5
        )
        duration = time.time() - start
        assert response.status_code == 201
        assert duration < 0.5

        start = time.time()
        response = requests.delete(f"{url}/accounts/{pesel}", timeout=0.5)
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 0.5


@pytest.mark.perf
def test_100_ingoing_transfers():
    pesel = str(uuid.uuid4().int)[:11]

    response = requests.post(
        f"{url}/accounts",
        json={"first_name": "Perf", "last_name": "Account", "pesel": pesel},
        timeout=0.5
    )
    assert response.status_code == 201

    for i in range(100):
        start = time.time()
        response = requests.post(
            f"{url}/accounts/{pesel}/transfer",
            json={"type": "ingoing", "amount": 10.0},
            timeout=0.5
        )
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 0.5

    response = requests.get(f"{url}/accounts/{pesel}", timeout=0.5)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 1000.0

    requests.delete(f"{url}/accounts/{pesel}", timeout=0.5)
