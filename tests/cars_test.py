from fastapi.testclient import TestClient
from routes.router_cars import router
from main import app


client = TestClient(app)


def test_get_all_cars_success():
    response = client.get(f"{router.prefix}/get_all_cars", params={"skip": 0, "take": 100})
    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["message"] == "get data completed!"
    assert len(response.json()["data"]) > 0


def test_get_all_cars_no_data():
    response = client.get(f"{router.prefix}/get_all_cars", params={"skip": 1000, "take": 1000})
    assert response.status_code == 404
    assert response.json()["message"] == "No car in database"


def test_get_car_by_id():
    response = client.get(f"{router.prefix}/get_car_by_id", params={"car_id": 1})
    assert response.status_code == 200
    assert len(response.json()["data"]) > 1


def test_get_car_by_id_no_data():
    response = client.get(f"{router.prefix}/get_car_by_id", params={"car_id": 999})
    assert response.status_code == 404
    assert response.json()["message"] == "Car not found"
    assert response.json()["data"] is None

