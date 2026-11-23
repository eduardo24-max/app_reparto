import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .routers import productos, trabajadores, platillos, inventario

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kraken Rolls API",
    description="Backend de Kraken Rolls: productos, platillos, trabajadores e inventario.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router)
app.include_router(trabajadores.router)
app.include_router(platillos.router)
app.include_router(inventario.router)


@app.get("/api")
def api_info():
    return {"mensaje": "Kraken Rolls API funcionando. Ve a /docs para probar los endpoints."}


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/ui", StaticFiles(directory=STATIC_DIR, html=True), name="ui")


@app.get("/")
def root():
    return {"mensaje": "Kraken Rolls API funcionando. Ve a /ui para el panel visual, o a /docs para probar los endpoints."}
