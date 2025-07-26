from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.helper.helper import get_pg_connection, only_user

router = APIRouter(prefix="/order/user", tags=["Order User"])

class OrderStatusUpdate(BaseModel):
    status_order: str

@router.put("/{id_order}/status", status_code=200)
def update_order_status(
    id_order: int,
    payload: OrderStatusUpdate = ...,
    current_user: dict = Depends(only_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute(
            'SELECT * FROM "order" WHERE id_order = %s AND user_id = %s',
            (id_order, current_user["user_id"])
        )
        order = cur.fetchone()
        if not order:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Order id not found")

        status_lama = order["status_order"]

        # Update status
        cur.execute(
            'UPDATE "order" SET status_order = %s WHERE id_order = %s',
            (payload.status_order, id_order)
        )

        # Log
        cur.execute(
            '''
            INSERT INTO log (user_id, aksi, deskripsi)
            VALUES (%s, %s, %s)
            ''',
            (
                current_user["user_id"],
                "Update Status Order",
                f"Order id={id_order}: update status dari '{status_lama}' menjadi '{payload.status_order}'"
            )
        )
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Status order berhasil diupdate"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

