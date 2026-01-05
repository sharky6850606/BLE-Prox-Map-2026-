from flask import Blueprint, jsonify, request, render_template
from app.models import Device, Beacon, State
from app.reports import daily_diagnostics, activity

routes=Blueprint("routes",__name__)

@routes.route("/")
def ui(): return render_template("map.html")

@routes.route("/api/live")
def live():
    out=[]
    for s in State.query.all():
        d=Device.query.get(s.device_id)
        b=Beacon.query.get(s.beacon_id)
        out.append({
            "device":{"id":d.id,"name":d.name or d.imei,"lat":d.lat,"lon":d.lon},
            "beacon":{"id":b.id,"name":b.name or b.uid},
            "distance":s.distance,"in":s.in_range
        })
    return jsonify(out)

@routes.route("/api/rename/device",methods=["POST"])
def rd():
    d=Device.query.get(request.json["id"])
    d.name=request.json["name"]; return ("",204)

@routes.route("/api/rename/beacon",methods=["POST"])
def rb():
    b=Beacon.query.get(request.json["id"])
    b.name=request.json["name"]; return ("",204)

@routes.route("/api/report/daily",methods=["POST"])
def rep(): return jsonify({"file":daily_diagnostics()})

@routes.route("/api/report/activity",methods=["POST"])
def act():
    j=request.json
    return jsonify({"file":activity(j["type"],j.get("device"),j.get("beacon"))})
