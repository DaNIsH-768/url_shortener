from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, name='home.html')

@app.get("/signin")
async def signin(request: Request):
    return templates.TemplateResponse(request, name='signin.html')

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse(request, name='signup.html')
