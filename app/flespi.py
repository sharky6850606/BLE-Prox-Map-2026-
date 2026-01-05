import requests
from datetime import datetime

def fetch(token, url):
    r = requests.get(url, headers={"Authorization": f"FlespiToken {token}"}, timeout=20)
    r.raise_for_status()
    out = []
    for m in r.json():
        ts = m.get("timestamp") or m.get("server.timestamp")
        t = datetime.utcfromtimestamp(ts)
        imei = m.get("ident")
        if "ble.beacons" not in m:
            out.append({"type":"fmc","imei":imei,"lat":m.get("position.latitude"),"lon":m.get("position.longitude"),"time":t})
        else:
            for b in m.get("ble.beacons",[]):
                out.append({"type":"beacon","imei":imei,"bid":b.get("id"),"rssi":b.get("rssi"),"time":t})
    return out
