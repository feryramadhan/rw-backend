from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.helper.helper import get_pg_connection, verify_password, create_access_token

router = APIRouter(prefix="/auth/user", tags=["Auth"])

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def user_login(user: UserLogin):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cur.fetchone()
    cur.close()
    conn.close()

    # Check user available & verification password
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password invalid")

    # Generate JWT
    token = create_access_token({
        "sub": user.email,
        "role": db_user["role"],
        "user_id": db_user["user_id"]
    })
    return {
        "status": "Success",
        "access_token": token 
    }