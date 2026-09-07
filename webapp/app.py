from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
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

@app.post("/{store}/additem")
def add_to_list(
    store: str,
    item: str = Form(""),
):
    items = load_items()
    add_item(store, item, items, show=False)
    save_items(items)
    return RedirectResponse(
        url=f"/{store}",
        status_code=303,
    )

@app.post("/{store}/delitem")
def del_from_list(
    store: str,
    item: str = Form(""),
):
    items = load_items()
    remove_items(store, [item], items)
    save_items(items)
    return RedirectResponse(
        url=f"/{store}",
        status_code=303,
    )