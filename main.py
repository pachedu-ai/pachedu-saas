from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import uuid

app = FastAPI()

MANAGER_EMAIL = "Kawadzatanakalionel@gmail.com"
MANAGER_PASSWORD = "@123456789"

sessions = set()
queue = []

@app.get("/", response_class=HTMLResponse)
async def login_page():
    return """
    <html>
        <head>
            <title>Manager Login</title>
        </head>
        <body style="font-family: Arial; text-align:center; margin-top:100px;">
            <h2>Carwash Manager Portal</h2>
            <form method="post" action="/login">
                <input type="email" name="email" placeholder="Email" required><br><br>
                <input type="password" name="password" placeholder="Password" required><br><br>
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    if email == MANAGER_EMAIL and password == MANAGER_PASSWORD:
        session = str(uuid.uuid4())
        sessions.add(session)
        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie("session", session)
        return response
    return RedirectResponse("/")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body style="font-family: Arial; text-align:center; margin-top:100px;">
            <h2>Manager Dashboard</h2>
            <p>System is working successfully ✅</p>
            <p>Queue Length: {}</p>
        </body>
    </html>
    """.format(len(queue))