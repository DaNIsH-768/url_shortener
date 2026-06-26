from fastapi import FastAPI
from .database import initialise_db
from contextlib import asynccontextmanager
from .routers import auth
from .routers import urls
from .rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_db()
    yield

app = FastAPI(
    title="URL Shortener API",
    description="A URL shortening service with analytics",
    version="0.1.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(urls.router)
