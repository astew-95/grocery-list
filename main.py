#!/usr/bin/env python3
"""
Simple grocery list manager.

Stores defaults in:
    /Users/alexastewart/tools/groceries/defaults.yaml

Stores active grocery lists in:
    items.txt

Stores activity log in:
    grocery.log
"""

from __future__ import annotations
import sys
from pathlib import Path
from utils import *


# include lists: online, grocery, produce, thrift
INCLUDE_LISTS = {
    "Amazon": [ "online","grocery"],
    "costco": ["produce","grocery"],
    "Walmart": ["grocery", "online", "produce"],
    "Aldi": ["grocery"],
    "Target": ["grocery", "online", "produce"],
    "Trader Joes": ["grocery", "produce"],
    "Job Lot": ["grocery", "thrift"],
    "Savers": ["thrift"],
    "fb": ["thrift"],
    "ikea": ["online"],
    "ikea": ["online"],
    "grocery": ["produce"],
}

DEFAULTS_FILE = Path("/Users/alexastewart/tools/groceries/defaults.yaml")
ITEMS_FILE = Path("/Users/alexastewart/tools/groceries/items.txt")
LOG_FILE = Path("/Users/alexastewart/tools/groceries/grocery.log")

HELP_TEXT = """
Usage:

grocery-list milk bananas                                            # add groceries to default lists
grocery-list main.py milk -tjs bananas -walmart "ice Cream" -costco  # add groceries to specific stores
grocery-list main.py -shopped "tjs"                                  # clear the grocery list for a store
grocery-list main.py -shop "tjs"                                     # get the list for a store
grocery-list -add                                                    # useful for adding in bulk to one store"
"""

SKIP_INCLUDE_ON_SHOPPED = {"thrift", "job lot","ikea","target"}

def handle_shopped(store_arg, item_arg = None):
    """
    Handle -shooped argument which clears the list for a store and all of its linked stores.
    """
    defaults = load_defaults()
    items_data = load_items()
    store = find_store_name(defaults, store_arg)

    if not store:
        print(f"Unknown store: {store_arg}")
        return

    included = [] if store in SKIP_INCLUDE_ON_SHOPPED else INCLUDE_LISTS.get(store, [])
    stores_to_clear = ["General", *included, store]

    if not item_arg:
        for list_name in stores_to_clear:
            clear_store(list_name, items_data)
        save_items(items_data)
        log(f"Store '{store}' shopped on {today()}")
        return

    search_terms = expand_items(item_arg)
    removed = []
    for list_name in stores_to_clear:
        removed.extend(remove_items(list_name, search_terms, items_data))

    save_items(items_data)

def handle_shop(store_arg):
    """Handle -shop argument """
    defaults = load_defaults()
    items_data = load_items()
    store = find_store_name(defaults, store_arg)
    if not store:
        print(f"Unknown store: {store_arg}")
        return

    # print_shop_list(store, items_data)
    stores_to_print = [store, *INCLUDE_LISTS.get(store, [])]
    print_combined_shop_list(stores_to_print, items_data)

def main():
    args = expand_comma_seperated_list(sys.argv[1:])

    if not args:
        print(HELP_TEXT)
        return

    if args[0] in {"-help", "--help"}:
        print(HELP_TEXT)
        return

    if args[0] == "-shopped":
        if len(args) < 2:
            print("Missing store name.")
            return

        item_arg = args[2] if len(args) > 2 else None

        handle_shopped(
            args[1],
            item_arg,
        )
        return

    if args[0] == "-shop":
        if len(args) < 2:
            print("Missing store name.")
            return
        handle_shop(args[1])
        return
    
    # CASE WHERE I USE "-add"
    if args[0] == "-add":
        defaults = load_defaults()
        items_data = load_items()

        if len(args) > 1:
            store_input = args[1]
        else:
            store_input = input(
                "What store would you like to add to? "
            ).strip()

        store = ensure_store( defaults,items_data, store_input,)
        print(f"Adding to store: {store}")
        item_input = input("(comma separated, use quit to stop). What items would you like to add? ").strip()

        all_inputs=item_input+store_input
        if "quit" in all_inputs.lower() or "exit" in all_inputs.lower() or "stop" in all_inputs.lower():
            print("Exitting input. Items not added. Try again! ")
            return None

        items = expand_items(item_input)
        for item in items:
            add_item(store, item, items_data)
            log(
                f"Grocery Item '{item}' added to "
                f"store '{store}' on {today()}")

        save_items(items_data)
        return None

    defaults = load_defaults()
    items_data = load_items()

    pending_item = None
    for token in args:
        if token.startswith("-"):
            if pending_item is None:
                continue
            requested_store = token[1:]
            store = ensure_store(defaults,items_data,requested_store,)
            add_item(store, pending_item, items_data)

            log(
                f"Grocery Item '{pending_item}' added to "
                f"store '{store}' on {today()}"
            )

            pending_item = None
            continue

        if pending_item is not None:
            default_store = find_default_store(defaults, pending_item)

            store = default_store or "General"

            add_item(store, pending_item, items_data)

            log(
                f"Grocery Item '{pending_item}' added to "
                f"store '{store}' on {today()}"
            )

        pending_item = token

    if pending_item is not None:
        default_store = find_default_store(defaults, pending_item)

        store = default_store or "General"

        add_item(store, pending_item, items_data)

        log(
            f"Grocery Item '{pending_item}' added to "
            f"store '{store}' on {today()}"
        )

    save_items(items_data)


if __name__ == "__main__":
    main()