from fastapi import APIRouter, Depends, HTTPException, Query
from app.helper.helper import get_pg_connection, only_user
from typing import List
from pydantic import BaseModel
from datetime import date

class PaymentSchema(BaseModel):
    id_payment: int
    id_order: int
    tanggal_bayar: date
    jumlah_bayar: float
    metode_bayar: str
    status_bayar: str

router = APIRouter(prefix="/payment/user", tags=["Payment"])

@router.get("/", response_model=List[PaymentSchema])
def get_user_payment(
    order: str = Query("desc", description="Sort by tanggal_bayar: asc/desc"),
    current_user: dict = Depends(only_user)
):
    try:
        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"

        conn = get_pg_connection()
        cur = conn.cursor()
        query = f"""
            SELECT p.id_payment, p.id_order, p.tanggal_bayar, p.jumlah_bayar, p.metode_bayar, p.status_bayar
            FROM payment p
            JOIN "order" o ON p.id_order = o.id_order
            WHERE o.user_id = %s
            ORDER BY p.tanggal_bayar {order}
        """
        cur.execute(query, (current_user["user_id"],))
        payments = cur.fetchall()
        cur.close()
        conn.close()

        return [dict(payment) for payment in payments]

    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )