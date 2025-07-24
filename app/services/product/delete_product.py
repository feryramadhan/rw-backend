from fastapi import APIRouter, Depends, HTTPException
from app.helper.helper import get_pg_connection, only_admin

router = APIRouter(prefix="/product", tags=["Barang"])

@router.delete("/{id_barang}", status_code=200)
def delete_product(
    id_barang: int,
    current_user: dict = Depends(only_admin)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        # Check if product exists
        cur.execute(
            "SELECT id_barang FROM barang WHERE id_barang = %s;", (id_barang,)
        )
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Product not found.")

        # Delete product
        cur.execute(
            "DELETE FROM barang WHERE id_barang = %s;", (id_barang,)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": 200,
            "message": "Successfully deleted product"
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
