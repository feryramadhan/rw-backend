from fastapi import APIRouter, Depends, HTTPException, status
from app.helper.helper import get_pg_connection, only_admin
from pydantic import BaseModel

router = APIRouter(prefix="/product", tags=["Barang"])

class BarangCreate(BaseModel):
    nama_barang: str
    harga: int
    stok: int
    deskripsi: str = None  # Optional

@router.post("/", status_code=201)
def create_product(
    barang: BarangCreate,
    current_user: dict = Depends(only_admin)
):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO barang (nama_barang, harga, stok, deskripsi)
            VALUES (%s, %s, %s, %s)
            RETURNING id_barang, nama_barang, harga, stok, deskripsi;
            """,
            (barang.nama_barang, barang.harga, barang.stok, barang.deskripsi)
        )
        new_barang = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Successfully create product",
            "data": new_barang
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
