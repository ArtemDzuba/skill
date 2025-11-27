import factory

from .app import db
from .models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=50),
        factory.Faker("credit_card_number"),
        None,
    )
    car_number = factory.Faker("bothify", text="???-###")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=5, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
