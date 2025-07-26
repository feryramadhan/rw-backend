from pydantic import BaseModel
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from app.helper.helper import get_pg_connection, only_user

router = APIRouter(prefix="/order/user", tags=["Order User"])

class OrderCreate(BaseModel):
    id_barang: int
    tanggal_order: date
    status_order: str
    total_harga: float

@router.post("/", status_code=201)
def create_order(
    order: OrderCreate,
    current_user: dict = Depends(only_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        # Check stock
        cur.execute(
            "SELECT stok, nama_barang FROM barang WHERE id_barang = %s FOR UPDATE",
            (order.id_barang,)
        )
        barang = cur.fetchone()
        if not barang:
            raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
        if barang["stok"] <= 0:
            raise HTTPException(status_code=400, detail="Stok barang habis")

        # Create order
        cur.execute(
            '''
            INSERT INTO "order" (user_id, id_barang, tanggal_order, status_order, total_harga)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_order
            ''',
            (
                current_user["user_id"],
                order.id_barang,
                order.tanggal_order,
                "pending",
                order.total_harga
            )
        )
        order_id = cur.fetchone()["id_order"]

        cur.execute(
            '''
            UPDATE barang
            SET stok = stok - 1
            WHERE id_barang = %s
            ''',
            (order.id_barang,)
        )

        # log
        cur.execute(
            '''
            INSERT INTO log (user_id, aksi, deskripsi)
            VALUES (%s, %s, %s)
            ''',
            (
                current_user["user_id"],
                "Buat Order",
                f"Order id={order_id}, barang = {barang['nama_barang']} (id={order.id_barang}), total = {order.total_harga}"
            )
        )

        conn.commit()
        cur.close()
        conn.close()

        return {
            "order_id": order_id,
            "message": "Berhasil order barang!"
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )