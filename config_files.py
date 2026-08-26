from pathlib import Path
import yaml

DEFAULTS_FILE = Path("defaults.yaml")
ITEMS_FILE = Path("items.txt")
LOG_FILE = Path("grocery.log")

# include lists: online, grocery, produce, thrift
INCLUDE_FILE = Path("include.yaml")
include_lists: dict[str, str]
with INCLUDE_FILE.open("r", encoding="utf-8") as f:
    include_lists = yaml.safe_load(f)