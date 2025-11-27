from datetime import datetime, timedelta

import pytest

from .app import create_app
from .app import db as _db
from .models import Client, ClientParking, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with _app.app_context():
        _db.create_all()

        client = Client(
            id=1,
            name="John",
            surname="Doe",
            credit_card="1234-5678-9876-5432",
            car_number="ABC-123",
        )
        parking = Parking(
            id=1,
            address="123 Main St",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        client_parking = ClientParking(
            id=1,
            client_id=1,
            parking_id=1,
            time_in=datetime.now() - timedelta(hours=1),
            time_out=None,
        )

        _db.session.add_all([client, parking, client_parking])
        _db.session.commit()

        client2 = Client(
            id=2,
            name="Depts",
            surname="Doe",
            credit_card="2345-5678-9876-5432",
            car_number="ABC-126",
        )
        parking2 = Parking(
            id=2,
            address="124 Main St",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        _db.session.add_all([client2, parking2])
        _db.session.commit()

    yield _app

    with _app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield _db.session
