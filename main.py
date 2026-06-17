from fastapi import FastAPI, status, HTTPException
from settings.db import ping
from routers.products import router as products_router
from routers.files import router as files_router
from routers.auth import router as auth_router
from authx.exceptions import AuthXException
from fastapi.responses import JSONResponse


app = FastAPI()

@app.exception_handler(AuthXException)
def authx_exception_handler(request, exc: AuthXException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )

app.include_router(products_router)
app.include_router(files_router)
app.include_router(auth_router)


@app.get("/")
def index_root():
    return {"message": "Hello World!"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}
