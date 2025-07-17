from fastapi import FastAPI
from app.services.auth.user import user_register

app = FastAPI(
    title="Pembelian Barang",
    description="Backend untuk aplikasi pembelian barang (pencatatan, pembayaran, dan pengelolaan data pengiriman).",
    version="1.0.0"
)

# default
@app.get("/")
async def health_check():
    return {"status": "ok"}

# auth user
app.include_router(user_register.router)