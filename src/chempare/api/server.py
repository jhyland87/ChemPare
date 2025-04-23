from __future__ import annotations

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import UJSONResponse

from .routers import supplier_routes


# from enum import Enum
# import json
# import os


# app = FastAPI()

# app.include_router(supplier_routes)


app = FastAPI()


def start_api():

    app.include_router(supplier_routes)


@app.get("/")
def get_all_urls():

    return [
        {
            "path": route.path,
            "name": route.name,
            "methods": route.methods if route.methods else None,
        }
        for route in supplier_routes
    ]


def init():
    print("Starting server")

    uvicorn.run(
        "chempare.api.server:start_api", host="0.0.0.0", port=8000, reload=True
    )


if __name__ == "__main__":
    init()
