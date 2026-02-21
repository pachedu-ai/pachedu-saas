from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Simple login credentials
MANAGER_EMAIL = "Kawadzatanakalionel@gmail.com"
MANAGER_PASSWORD = "@123456789"

# In-memory queue
queue = []

# Service presets
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
            "queue": queue,
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

    queue.append({
        "reg": reg,
        "service": service,
        "vehicle": vehicle,
        "time": int(base["time"] * mult),
        "price": int(base["price"] * mult)
    })

    return RedirectResponse("/dashboard", status_code=302)
