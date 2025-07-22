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
    current_user: dict = Depends(only_user) # Validate user role
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
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
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "order_id": order_id,
            "message": "Order created successfully"
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


