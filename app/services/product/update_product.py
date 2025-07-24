from fastapi import APIRouter, Depends, HTTPException, status
from app.helper.helper import get_pg_connection, only_admin
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/product", tags=["Barang"])

class BarangUpdate(BaseModel):
    nama_barang: Optional[str] = None
    harga: Optional[int] = None
    stok: Optional[int] = None
    deskripsi: Optional[str] = None


@router.patch("/{id_barang}", status_code=200)
def update_product(
    id_barang: int,
    barang: BarangUpdate,
    current_user: dict = Depends(only_admin)
):
    try:
        data_to_update = barang.dict(exclude_unset=True)
        if not data_to_update:
            raise HTTPException(status_code=400, detail="No data provided for update.")

        set_clause = ", ".join([f"{field} = %s" for field in data_to_update.keys()])
        values = list(data_to_update.values())
        values.append(id_barang)

        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(
            f"""
            UPDATE barang
            SET {set_clause}
            WHERE id_barang = %s
            RETURNING id_barang, nama_barang, harga, stok, deskripsi;
            """,
            values
        )
        updated_barang = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if not updated_barang:
            raise HTTPException(status_code=404, detail="Product not found.")

        return {
            "status": 200,
            "message": "Successfully updated product",
            "data": updated_barang
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
