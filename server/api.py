from fastapi import APIRouter
from datetime import datetime
from server.database import db

router=APIRouter(prefix="/api")

@router.get("/status")
def status():
    return {"status":"ok"}

@router.post("/orders")
def create_order():
    number=db.create_order(datetime.now().isoformat())
    return {"number":number}

@router.get("/orders/waiting")
def waiting():
    return db.get_waiting_orders()
