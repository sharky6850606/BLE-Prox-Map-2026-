import time
from datetime import timedelta
from flask import Flask
from app.config import Config
from app.db import db
from app.models import Device, Beacon, State, Notification
from app.flespi import fetch
from app.distance import rssi_to_distance

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context(): db.create_all()

def run():
    cfg=Config()
    while True:
        with app.app_context():
            for m in fetch(cfg.FLESPI_TOKEN,cfg.FLESPI_URL):
                if m["type"]=="fmc":
                    d=Device.query.filter_by(imei=m["imei"]).first() or Device(imei=m["imei"])
                    d.lat,d.lon,d.last_seen=m["lat"],m["lon"],m["time"]
                    db.session.add(d); continue
                d=Device.query.filter_by(imei=m["imei"]).first()
                if not d: continue
                b=Beacon.query.filter_by(uid=m["bid"]).first() or Beacon(uid=m["bid"])
                db.session.add(b)
                dist=rssi_to_distance(m["rssi"],cfg.RSSI_AT_1M,cfg.PATH_LOSS_N)
                inr=dist<=cfg.RANGE_METERS
                st=State.query.filter_by(device_id=d.id,beacon_id=b.id).first()
                if not st:
                    st=State(device_id=d.id,beacon_id=b.id)
                    db.session.add(Notification(device_id=d.id,beacon_id=b.id,event="IN" if inr else "OUT",distance=dist,rssi=m["rssi"]))
                elif st.in_range!=inr:
                    db.session.add(Notification(device_id=d.id,beacon_id=b.id,event="IN" if inr else "OUT",distance=dist,rssi=m["rssi"]))
                st.last_seen=m["time"]
                st.expires_at=m["time"]+timedelta(seconds=cfg.TTL_SECONDS)
                st.rssi,st.distance,st.in_range=m["rssi"],dist,inr
                db.session.add(st)
            State.query.filter(State.expires_at < db.func.now()).delete()
            db.session.commit()
        time.sleep(cfg.WORKER_INTERVAL)

run()
