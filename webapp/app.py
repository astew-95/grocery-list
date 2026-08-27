from fastapi import FastAPI
from fastapi.requests import Request
from webapp import dependencies

from utils import *

app = FastAPI(title="Shopping List")

@app.get("/")
def index(
    request: Request,
):
    return dependencies.templates.TemplateResponse(
        request,
        "list_viewer.html",
        {
            "stores": load_defaults().keys(),
            "selected_store": None,
            "items": None,
        }
    )

@app.get("/{store}")
def store_list(
    request: Request,
    store: str
):
    return dependencies.templates.TemplateResponse(
        request,
        "list_viewer.html",
        {
            "stores": load_defaults().keys(),
            "selected_store": store,
            "items": get_expanded_shop_list(store, load_items()),
        }
    )