from datetime import datetime
from app.db import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    last_seen = db.Column(db.DateTime)

class Beacon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, unique=True)
    name = db.Column(db.String)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"))
    beacon_id = db.Column(db.Integer, db.ForeignKey("beacon.id"))
    last_seen = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    rssi = db.Column(db.Float)
    distance = db.Column(db.Float)
    in_range = db.Column(db.Boolean)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    beacon_id = db.Column(db.Integer)
    event = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    distance = db.Column(db.Float)
    rssi = db.Column(db.Float)
