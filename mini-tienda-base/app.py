"""
MiniTienda — aplicación base (SUT) para el Reto AI-First · Track QA.

App full-stack mínima y autocontenida:
  - Backend: FastAPI
  - Base de datos: SQLite (archivo local, se crea y siembra solo)
  - Web service: API REST bajo /api
  - Integración: servicio de precios/impuestos (/api/pricing/quote),
    con simulación de caída vía la variable de entorno PRICING_FAIL=1
  - Frontend: página estática servida en /

Ejecutar:
    pip install -r requirements.txt
    uvicorn app:app --reload --port 8000
Luego abrir http://localhost:8000
"""
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "minitienda.db")

# Tasas de impuesto por país (la "integración" de precios)
TAX_RATES = {"CO": 0.19, "US": 0.0}
DEFAULT_TAX_RATE = 0.10

SEED_PRODUCTS = [
    ("Café 500g", 25000, 20),
    ("Mug cerámico", 18000, 15),
    ("Cuaderno A5", 12000, 30),
    ("Bolígrafo gel", 4000, 100),
    ("Termo 750ml", 60000, 8),
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_conn()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price_cents INTEGER NOT NULL,
                   stock INTEGER NOT NULL)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS orders (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   country TEXT NOT NULL,
                   subtotal_cents INTEGER NOT NULL,
                   tax_cents INTEGER NOT NULL,
                   total_cents INTEGER NOT NULL,
                   created_at TEXT NOT NULL)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS order_items (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   order_id INTEGER NOT NULL,
                   product_id INTEGER NOT NULL,
                   qty INTEGER NOT NULL,
                   unit_price_cents INTEGER NOT NULL)"""
        )
        count = conn.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
        if count == 0:
            conn.executemany(
                "INSERT INTO products (name, price_cents, stock) VALUES (?, ?, ?)",
                SEED_PRODUCTS,
            )


def price_quote(subtotal_cents: int, country: str) -> dict:
    """Servicio de precios/impuestos. Lanza RuntimeError si se simula caída."""
    if os.environ.get("PRICING_FAIL") == "1":
        raise RuntimeError("pricing service unavailable")
    rate = TAX_RATES.get(country, DEFAULT_TAX_RATE)
    tax_cents = int(subtotal_cents * rate)
    return {
        "subtotal_cents": subtotal_cents,
        "tax_rate": rate,
        "tax_cents": tax_cents,
        "total_cents": subtotal_cents + tax_cents,
    }


class OrderItemIn(BaseModel):
    product_id: int
    qty: int


class OrderIn(BaseModel):
    country: str = "CO"
    items: list[OrderItemIn]


app = FastAPI(title="MiniTienda", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def list_products():
    with closing(get_conn()) as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
        return [dict(r) for r in rows]


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    with closing(get_conn()) as conn:
        row = conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return dict(row)


@app.get("/api/pricing/quote")
def pricing_quote(subtotal_cents: int, country: str = "CO"):
    try:
        return price_quote(subtotal_cents, country)
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Servicio de precios no disponible")


@app.post("/api/orders", status_code=201)
def create_order(order: OrderIn):
    if not order.items:
        raise HTTPException(status_code=400, detail="La orden no tiene items")

    with closing(get_conn()) as conn, conn:
        subtotal = 0
        resolved = []
        for item in order.items:
            product = conn.execute(
                "SELECT * FROM products WHERE id = ?", (item.product_id,)
            ).fetchone()
            if product is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Producto {item.product_id} no existe",
                )
            if item.qty > product["stock"]:
                raise HTTPException(
                    status_code=409,
                    detail=f"Stock insuficiente para producto {item.product_id}",
                )
            subtotal += product["price_cents"] * item.qty
            resolved.append((product, item.qty))

        try:
            quote = price_quote(subtotal, order.country)
        except RuntimeError:
            raise HTTPException(
                status_code=503, detail="Servicio de precios no disponible"
            )

        cur = conn.execute(
            """INSERT INTO orders (country, subtotal_cents, tax_cents, total_cents, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                order.country,
                quote["subtotal_cents"],
                quote["tax_cents"],
                quote["total_cents"],
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        order_id = cur.lastrowid
        for product, qty in resolved:
            conn.execute(
                """INSERT INTO order_items (order_id, product_id, qty, unit_price_cents)
                   VALUES (?, ?, ?, ?)""",
                (order_id, product["id"], qty, product["price_cents"]),
            )
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (qty, product["id"]),
            )

    return get_order(order_id)


@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    with closing(get_conn()) as conn:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        if order is None:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        items = conn.execute(
            "SELECT product_id, qty, unit_price_cents FROM order_items WHERE order_id = ?",
            (order_id,),
        ).fetchall()
    result = dict(order)
    result["items"] = [dict(i) for i in items]
    return result


# El frontend estático se monta al final para no tapar las rutas /api
app.mount("/", StaticFiles(directory="static", html=True), name="static")
