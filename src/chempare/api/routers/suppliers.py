import os
import sys
from pathlib import Path

# Annotation imports
from typing import TYPE_CHECKING
from typing import Annotated
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from fastapi import APIRouter
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


supplier_routes = APIRouter(prefix="/suppliers", tags=["Supplier routes"])


@supplier_routes.get("/")
def compare_index():
    # /compare-files?file=foo&file=bar
    return {"Hello": "World"}
