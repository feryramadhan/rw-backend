from fastapi import APIRouter, Depends, HTTPException
from app.helper.helper import get_pg_connection, get_current_user

router = APIRouter(prefix="/product", tags=["Barang"])

@router.get("/", status_code=200)
def get_all_products(current_user: dict = Depends(get_current_user)):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_barang, nama_barang, harga, stok, deskripsi
            FROM barang
            ORDER BY id_barang DESC;
            """
        )
        products = cur.fetchall()
        cur.close()
        conn.close()

        return {
            "status": 200,
            "message": "Successfully fetched all products",
            "data": products
        }

    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
