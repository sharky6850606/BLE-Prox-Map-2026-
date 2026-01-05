import os
from reportlab.pdfgen import canvas
from datetime import datetime
from app.models import Device, Beacon, State, Notification
from app.db import db

DIR="reports"
os.makedirs(DIR,exist_ok=True)

def daily_diagnostics():
    name=f"{DIR}/diagnostics_{datetime.utcnow().date()}.pdf"
    c=canvas.Canvas(name)
    y=800
    c.setFont("Helvetica-Bold",14)
    c.drawString(40,y,"Daily Diagnostics Report"); y-=30
    for d in Device.query.all():
        c.setFont("Helvetica-Bold",11)
        c.drawString(40,y,f"Device: {d.name or d.imei}"); y-=15
        for s in State.query.filter_by(device_id=d.id):
            b=Beacon.query.get(s.beacon_id)
            c.setFont("Helvetica",10)
            c.drawString(60,y,f"{b.name or b.uid} | {'IN' if s.in_range else 'OUT'} | {s.distance:.2f}m")
            y-=12
        y-=10
        if y<100: c.showPage(); y=800
    c.save()
    return name

def activity(report_type, did=None, bid=None):
    name=f"{DIR}/{report_type}_activity_{datetime.utcnow().timestamp()}.pdf"
    c=canvas.Canvas(name)
    y=800
    c.setFont("Helvetica-Bold",14)
    c.drawString(40,y,"Activity Report"); y-=30
    q=Notification.query
    if did: q=q.filter_by(device_id=did)
    if bid: q=q.filter_by(beacon_id=bid)
    for n in q.order_by(Notification.time):
        c.setFont("Helvetica",10)
        c.drawString(40,y,f"{n.time} | {n.event} | {n.distance:.2f}m")
        y-=12
        if y<100: c.showPage(); y=800
    c.save()
    return name
