from datetime import datetime
from typing import List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hw.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import Client, ClientParking, Parking

    with app.app_context():
        db.create_all()  # создать таблицы при старте

    # @app.before_request
    # def before_request_func():
    #     db.create_all()

    @app.route("/clients", methods=["GET"])
    def get_clients():
        """Список всех клиентов"""
        clients: List[Client] = db.session.query(Client).all()

        users_list = [c.to_json() for c in clients]
        return jsonify(users_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_handler(client_id):
        """Получение клиента по id"""
        # client: Client = db.session.query(Client).get(client_id)
        client = db.session.get(Client, client_id)
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=["POST"])
    def create_client():
        """Создание нового клиента"""
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        credit_card = request.form.get("credit_card", type=str)
        car_number = request.form.get("car_number", type=str)

        new_client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )

        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client.to_json()), 201

    @app.route("/parking", methods=["POST"])
    def create_parking():
        """Создание новой парковочной зоны"""
        address = request.form.get("address", type=str)
        opened = request.form.get("opened", type=bool)
        count_places = request.form.get("count_places", type=int)
        count_available_places = request.form.get("count_available_places", type=int)

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )

        db.session.add(new_parking)
        db.session.commit()

        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=["POST"])
    def enter_parking():
        client_id = request.args.get("client_id", type=int)
        parking_id = request.args.get("parking_id", type=int)

        client = db.session.get(Client, client_id)
        if client is None:
            return jsonify({"error": "Client not found"}), 404

        parking = db.session.get(Parking, parking_id)

        if not parking.opened:
            return jsonify({"error": "Parking is closed"}), 400

        if parking.count_available_places <= 0:
            return jsonify({"error": "No available places"}), 400

        active_parking = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()

        if active_parking:
            return jsonify({"error": "Client already parked here"}), 400

        parking.count_available_places -= 1
        new_entry = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.now()
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Client entered parking"}), 201

    @app.route("/client_parkings", methods=["DELETE"])
    def exit_parking():
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)

        client = db.session.get(Client, client_id)
        parking = db.session.get(Parking, parking_id)

        if not client or not parking:
            return jsonify({"error": "Client or Parking not found"}), 404

        if not client.credit_card:
            return (
                jsonify({"error": "Client has no credit card linked for payment"}),
                400,
            )

        active_parking = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()
        if not active_parking:
            return jsonify({"error": "No active parking entry found"}), 404

        active_parking.time_out = datetime.now()
        parking.count_available_places += 1
        db.session.commit()

        return jsonify({"message": "Client exited parking"}), 200

    return app
