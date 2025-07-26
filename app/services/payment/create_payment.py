from fastapi import APIRouter, Depends, HTTPException
from app.helper.helper import get_pg_connection, only_user
from pydantic import BaseModel
from datetime import date

class PaymentCreate(BaseModel):
    id_order: int
    tanggal_bayar: date
    jumlah_bayar: float
    metode_bayar: str
    status_bayar: str

router = APIRouter(prefix="/payment/user", tags=["Payment"])

@router.post("/", status_code=201)
def create_payment(
    payment: PaymentCreate,
    current_user: dict = Depends(only_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(
            '''
            INSERT INTO payment (id_order, tanggal_bayar, jumlah_bayar, metode_bayar, status_bayar)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_payment
            ''',
            (
                payment.id_order,
                payment.tanggal_bayar,
                payment.jumlah_bayar,
                payment.metode_bayar,
                payment.status_bayar
            )
        )
        id_payment = cur.fetchone()["id_payment"]

        # Log
        cur.execute(
            '''
            INSERT INTO log (user_id, aksi, deskripsi)
            VALUES (%s, %s, %s)
            ''',
            (
                current_user["user_id"],
                "Create Payment",
                f"Payment id={id_payment}, order id={payment.id_order}, jumlah = {payment.jumlah_bayar}, metode = {payment.metode_bayar}, status = {payment.status_bayar}"
            )
        )

        conn.commit()
        cur.close()
        conn.close()

        return {
            "id_payment": id_payment,
            "message": "Berhasil melakukan pembayaran!"
        }

    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

