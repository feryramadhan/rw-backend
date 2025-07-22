from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.helper.helper import get_pg_connection, only_user

router = APIRouter(prefix="/order/user", tags=["Order User"])

@router.get("/", status_code=200)
def get_orders(
    sort_by: Optional[str] = Query("tanggal_order", description="Sort by"),
    sort_order: Optional[str] = Query("desc", description="asc/desc"),
    current_user: dict = Depends(only_user)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        # Validate sort_by to prevent SQL injection, only allow certain columns!
        allowed_sort_fields = ["tanggal_order", "total_harga", "status_order", "id_order"]
        if sort_by not in allowed_sort_fields:
            raise HTTPException(status_code=400, detail=f"sort_by must be one of {allowed_sort_fields}")

        # Validate sort_order
        sort_order = sort_order.lower()
        if sort_order not in ["asc", "desc"]:
            sort_order = "desc"

        query = f'''
            SELECT * FROM "order"
            WHERE user_id = %s
            ORDER BY {sort_by} {sort_order}
        '''
        cur.execute(query, (current_user["user_id"],))
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return {
            "orders": orders,
            "total": len(orders)
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
