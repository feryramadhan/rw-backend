from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.helper.helper import get_pg_connection, only_admin

class LogSchema(BaseModel):
    id_log: int
    user_id: int
    aksi: str
    waktu: datetime
    deskripsi: str

router = APIRouter(prefix="/log", tags=["Log (Admin)"])

@router.get("/", response_model=List[LogSchema])
def get_logs(current_user: dict = Depends(only_admin)):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_log, user_id, aksi, waktu, deskripsi
            FROM log
            ORDER BY waktu DESC
            """
        )
        logs = cur.fetchall()
        cur.close()
        conn.close()

        return [dict(log) for log in logs]
        
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
