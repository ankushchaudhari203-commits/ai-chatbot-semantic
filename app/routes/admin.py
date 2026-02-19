from fastapi import APIRouter
from app.db.database import get_connection



router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/orders")
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()

    conn.close()

    return {"orders": rows}

