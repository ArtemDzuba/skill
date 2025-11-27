import pytest

from ..factories import ClientFactory, ParkingFactory
from ..models import Client, Parking


@pytest.mark.parking
def test_create_client(db_session):
    initial_count = db_session.query(Client).count()
    client = ClientFactory()
    db_session.commit()
    assert client.id is not None
    assert db_session.query(Client).count() == initial_count + 1


@pytest.mark.parking
def test_create_parking(db_session):
    initial_count = db_session.query(Parking).count()
    parking = ParkingFactory()
    db_session.commit()
    assert parking.id is not None
    assert db_session.query(Parking).count() == initial_count + 1
