import pytest

from ..models import Parking


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_get_endpoints(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client):
    data = {
        "name": "Alice",
        "surname": "Smith",
        "credit_card": "1111-2222-3333-4444",
        "car_number": "XYZ789",
    }
    response = client.post("/clients", data=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == "Alice"


def test_create_parking(client):
    data = {
        "address": "New Parking",
        "opened": "true",
        "count_places": 20,
        "count_available_places": 20,
    }
    response = client.post("/parking", data=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["address"] == "New Parking"


@pytest.mark.parking
def test_enter_parking(client, db_session):
    client_id = 2
    parking_id = 2
    # response = client.post("/client_parkings", data={"client_id": client_id, "parking_id": parking_id})
    response = client.post(
        f"/client_parkings?client_id={client_id}&parking_id={parking_id}"
    )
    assert response.status_code == 201, response.data.decode()
    parking = db_session.get(Parking, parking_id)
    assert parking.count_available_places == 9


@pytest.mark.parking
def test_exit_parking(client, db_session):
    client_id = 1
    parking_id = 1
    response = client.delete(
        "/client_parkings", data={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 200
    parking = db_session.get(Parking, parking_id)
    assert parking.count_available_places >= 1
