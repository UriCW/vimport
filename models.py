# 0hvfhs_license_num,dispatching_base_num,originating_base_num,request_datetime,on_scene_datetime,pickup_datetime,dropoff_datetime,PULocationID,DOLocationID,trip_miles,trip_time,base_passenger_fare,tolls,bcf,sales_tax,congestion_surcharge,airport_fee,tips,driver_pay,shared_request_flag,shared_match_flag,access_a_ride_flag,wav_request_flag,wav_match_flag
# HV0003,B03404,B03404,2024-01-01 00:21:47,2024-01-01 00:25:06,2024-01-01 00:28:08,2024-01-01 01:05:39,161,158,2.83,2251,45.61,0.0,1.25,4.05,2.75,0.0,0.0,40.18,N,N,N,N,N
# HV0003,B03404,B03404,2024-01-01 00:10:56,2024-01-01 00:11:08,2024-01-01 00:12:53,2024-01-01 00:20:05,137,79,1.57,432,10.05,0.0,0.28,0.89,2.75,0.0,0.0,6.12,N,N,N,N,N
# HV0003,B03404,B03404,2024-01-01 00:20:04,2024-01-01 00:21:51,2024-01-01 00:23:05,2024-01-01 00:35:16,79,186,1.98,731,18.07,0.0,0.5,1.6,2.75,0.0,0.0,9.47,N,N,N,N,N


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class TripRecord(db.Model):
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
