from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
import os

# =============================
# DATABASE CONNECTION
# =============================

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# =============================
# CREATE TABLES ON STARTUP
# =============================

with engine.connect() as conn:

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS queue (
        id SERIAL PRIMARY KEY,
        reg TEXT,
        service TEXT,
        vehicle TEXT,
        time INTEGER,
        price INTEGER
    );
    """))

    conn.commit()

# =============================
# APP SETUP
# =============================

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# =============================
# LOGIN CREDENTIALS
# =============================

MANAGER_EMAIL = "Kawadzatanakalionel@gmail.com"
MANAGER_PASSWORD = "@123456789"

# =============================
# SERVICE CONFIG
# =============================

services = {
    "Express Wash": {"time": 20, "price": 80},
    "Full Wash": {"time": 45, "price": 180},
    "Interior Cleaning": {"time": 40, "price": 150},
    "Engine Wash": {"time": 35, "price": 200},
}

vehicle_multiplier = {
    "Small": 1.0,
    "Sedan": 1.2,
    "SUV": 1.4,
    "Bakkie": 1.5,
    "Minibus": 1.8,
    "Truck": 2.2,
}

# =============================
# ROUTES
# =============================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "login": True, "error": ""}
    )


@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    if email == MANAGER_EMAIL and password == MANAGER_PASSWORD:
        return RedirectResponse("/dashboard", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "login": True, "error": "Invalid Login"}
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "login": False,
            "services": services.keys(),
            "vehicles": vehicle_multiplier.keys(),
        }
    )


@app.post("/add")
async def add_car(
    reg: str = Form(...),
    service: str = Form(...),
    vehicle: str = Form(...)
):

    base = services[service]
    mult = vehicle_multiplier[vehicle]

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO queue (reg, service, vehicle, time, price)
            VALUES (:reg, :service, :vehicle, :time, :price)
        """), {
            "reg": reg,
            "service": service,
            "vehicle": vehicle,
            "time": int(base["time"] * mult),
            "price": int(base["price"] * mult)
        })
        conn.commit()

    return RedirectResponse("/dashboard", status_code=302)


@app.get("/queue-data")
def get_queue_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM queue ORDER BY id DESC"))
        rows = result.mappings().all()
    return JSONResponse(content=rows)
