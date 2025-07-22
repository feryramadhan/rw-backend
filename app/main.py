from fastapi import FastAPI
from app.services.auth.admin import admin_register, admin_login
from app.services.auth.user import user_register, user_login
from app.services.order.user import create_order, get_orders, update_order_status
from app.services.order.admin import admin_get_orders, admin_delete_order

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
app.include_router(user_login.router)

# auth admin
app.include_router(admin_register.router)
app.include_router(admin_login.router)

# order user
app.include_router(create_order.router)
app.include_router(get_orders.router)
app.include_router(update_order_status.router)

# order admin
app.include_router(admin_get_orders.router)
app.include_router(admin_delete_order.router)
