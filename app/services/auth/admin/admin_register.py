from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from app.helper.helper import get_pg_connection, hash_password

router = APIRouter(prefix="/auth/admin", tags=["Auth"])

class UserRegister(BaseModel):
    nama: str = Field(..., example="Nama Lengkap")
    email: EmailStr = Field(..., example="user@email.com")
    password: str = Field(..., min_length=6)
    alamat: str = Field(..., example="Jl. Sudirman No.1")
    no_hp: str = Field(..., example="08123456789")

@router.post("/register")
def admin_register(user: UserRegister):
    try: 
        conn = get_pg_connection()
        cur = conn.cursor()
        # Check email already exist?
        cur.execute('SELECT user_id FROM users WHERE email = %s', (user.email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        # Hash password
        hashed_pw = hash_password(user.password)
        
        # Insert new user (role=admin)
        cur.execute(
            """
            INSERT INTO users 
            (nama, email, password, alamat, no_hp, role)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING user_id
            """,
            (user.nama, user.email, hashed_pw, user.alamat, user.no_hp, "admin")
        )
        user_id = cur.fetchone()["user_id"]
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Register successful!",
            "user_id": user_id
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
