import datetime
import yaml
from datetime import datetime
from pathlib import Path

DEFAULTS_FILE = Path("/Users/alexastewart/tools/groceries/defaults.yaml")
ITEMS_FILE = Path("/Users/alexastewart/tools/groceries/items.txt")
LOG_FILE = Path("/Users/alexastewart/tools/groceries/grocery.log")

store_synonymns= {"trader joes": ["tj","tjs"],
                  "walmart": ["w+", "w", "walmart plus"],
                  "job lot": ["joblot","jl", "jlot", "ocean state job lot"],
                  "costco": ["costcos"],
                  "marketplace":["facebook marketplace","fb marketplace", "fb market", "marketplace","fb", "fbm"],
                  "savers":["supersavers"],
                  "aldi":["aldis", "aldi's", "aldi natick", "aldi natick"],
                  "thrift":["thriftstore","thrift store","thrifts", "thrifting", "thriftshop", "thrift shop"],
                  "goodwill":["good will","gw"]
}

def normalize(value: str) -> str:
    """
    Normalize text for matching.

    - Capitalizes all first letters, strips whitespace, and removes duplicate spaces.
    - Replaces common store acronymns. 
    """
    value=value.lower()
    for store in store_synonymns.keys():
        for synonymn in store_synonymns[store]:
            value=value.replace(synonymn,store)
    value=value.replace("","")
    value=" ".join(value.strip().split())
    return value.title()


def same(a: str, b: str) -> bool:
    """
    Returns True if the first normalized string is contained in the second.
    """
    na = normalize(a)
    nb = normalize(b)

    return na in nb #or nb in na


def load_defaults() -> dict:
    """Load defaults.yaml."""
    if not DEFAULTS_FILE.exists():
        raise FileNotFoundError(f"Missing: {DEFAULTS_FILE}")
    with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data

def save_defaults(defaults: dict) -> None:
    """Save defaults.yaml."""
    with open(DEFAULTS_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(defaults, f, sort_keys=False)

def load_items() -> dict:
    """Load items.txt data."""
    if not ITEMS_FILE.exists():
        return {"General": []}

    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if "General" not in data:
        data["General"] = []

    return data

def save_items(data: dict) -> None:
    """Save items.txt."""
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def log(message: str) -> None:
    """Append a timestamped log entry."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def today() -> str:
    """Return today's date."""
    return datetime.now().strftime("%m-%d-%Y")


def find_store_name(defaults: dict, supplied_name: str) -> str | None:
    """
    Resolve a store name using defaults.yaml as ground truth.

    Matching is done by containment on normalized strings.
    """
    for store in defaults:
        if same(store, supplied_name):
            return store

    return None


def find_default_store(defaults: dict, item: str) -> str | None:
    item_lower = item.lower()

    for store, default_items in defaults.items():
        for default_item in default_items:
            if default_item.lower() in item_lower:
                return store

    return None


def expand_items(value: str) -> list[str]:
    """
    Split a comma-separated string into individual grocery items.
    """
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def expand_comma_seperated_list(tokens: list[str]) -> list[str]:
    """
    Expand comma-separated arguments.
    """
    expanded = []

    for token in tokens:
        if token.startswith("-"):
            expanded.append(token)
            continue

        expanded.extend(expand_items(token))

    return expanded


def remove_items(
    store: str,
    search_terms: list[str],
    items_data: dict,
) -> list[str]:
    """
    Remove items matching any search term from a store.
    """
    removed = []
    remaining = []

    for item in items_data.get(store, []):
        matched = any(same(term, item) for term in search_terms)
        if matched:
            removed.append(item)
        else:
            remaining.append(item)

    items_data[store] = remaining
    return removed


def ensure_store(defaults: dict, items_data: dict, store_name: str) -> str:
    """
    Ensure a store exists.

    If unknown, add it to defaults.yaml.
    """
    existing = find_store_name(defaults, store_name)

    if existing:
        if existing not in items_data:
            items_data[existing] = []
        return existing

    defaults[store_name] = []
    save_defaults(defaults)

    items_data.setdefault(store_name, [])

    return store_name


def add_item(store: str, item: str, items_data: dict, show=True) -> None:
    """Add an item if not already present."""
    items_data.setdefault(store, [])

    for existing in items_data[store]:
        if same(existing, item):
            return
    if show:
        print("adding ",item," to store:", store)
    items_data[store].append(item)


def clear_store(store: str, items_data: dict) -> None:
    """Clear a store list."""
    items_data[store] = []


def print_shop_list(store: str, items_data: dict) -> None:
    """Print General plus requested store."""
    print("\nGeneral")
    print("-------")
    for item in items_data.get("General", []):
        print(f"- {item}")
    print()
    print(store)
    print("-" * len(store))
    for item in items_data.get(store, []):
        print(f"- {item}")


def print_combined_shop_list(stores: list[str], items_data: dict) -> None:
    seen = set()
    for store in stores:
        for item in items_data.get(store, []):
            key = item.lower()
            if key not in seen:
                print(f"- {item}")
                seen.add(key)