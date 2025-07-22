from fastapi import APIRouter, Depends, Query, HTTPException
from app.helper.helper import get_pg_connection, only_admin

router = APIRouter(prefix="/order/admin", tags=["Order Admin"])

@router.delete("/{order_id}", status_code=200)
def delete_order(
    order_id: int,
    current_user: dict = Depends(only_admin)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        query = 'DELETE FROM "order" WHERE id_order = %s'
        cur.execute(query, (order_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "message": "Order deleted successfully"
            }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
        