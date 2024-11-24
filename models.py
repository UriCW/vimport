""" Defines the ORM Model for the application """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class TripRecord(db.Model):  # pylint: disable=R0903
    """Trip record model"""

    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    hvfhs_license_num = db.Column(db.String)
    dispatching_base_num = db.Column(db.String)
    originating_base_num = db.Column(db.String, nullable=True)
    request_datetime = db.Column(db.DateTime)
    on_scene_datetime = db.Column(db.DateTime, nullable=True)
    pickup_datetime = db.Column(db.DateTime)
    dropoff_datetime = db.Column(db.DateTime)
    PULocationID = db.Column(db.Integer)
    DOLocationID = db.Column(db.Integer)
    trip_miles = db.Column(db.Float)
    trip_time = db.Column(db.Integer)
    base_passenger_fare = db.Column(db.Float)
    tolls = db.Column(db.Float)
    bcf = db.Column(db.Float)
    sales_tax = db.Column(db.Float)
    congestion_surcharge = db.Column(db.Float)
    airport_fee = db.Column(db.Float)
    tips = db.Column(db.Float)
    driver_pay = db.Column(db.Float)
    shared_request_flag = db.Column(db.String(1))
    shared_match_flag = db.Column(db.String(1))
    access_a_ride_flag = db.Column(db.String(1))
    wav_request_flag = db.Column(db.String(1))
    wav_match_flag = db.Column(db.String(1))

    @validates(
        "request_datetime", "on_scene_datetime", "pickup_datetime", "dropoff_datetime"
    )
    def validate_datetime_fields(self, key, value):  # pylint: disable=W0613
        """Ensures empty date strings are converted to python None"""
        if value == "":
            return None
        return value
