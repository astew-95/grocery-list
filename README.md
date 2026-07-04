# To do 
- create functionality for "-shopped" "search string" where I can easily remove single items that contain the search string. "-shopped" "tjs" "cook,broc" should remove cookies and brocolli from the trader joes list and the log should say "shopped brocolli and cookies at trader joes on DATE".

- comma seperateed functioanlity, any string that comes in as a grocery item can be comma seperated and applies the same command to all the items.


# Grocery List Manager

A simple command-line grocery list manager that:

* Automatically sorts grocery items into store-specific shopping lists.
* Uses a YAML file as the source of truth for default item locations.
* Maintains active shopping lists in `items.txt`.
* Logs all activity to `grocery.log`.
* Supports interactive bulk entry.
* Supports shopping workflows that clear completed store lists.

## Files

### defaults.yaml

Default store assignments.

Example:

```yaml
ALDI:
  - stevia
  - splenda

Trader Joes:
  - arugula
  - kale
  - blueberries

Walmart:
  - milk
  - frozen salmon

Costco:
  - toilet paper
  - eggs
```

This file is the source of truth for store names.

### items.txt

Contains the current grocery lists organized by store.

Example:

```yaml
General:
  - bananas

Trader Joes:
  - blueberries

Walmart:
  - milk
```

### grocery.log

Activity log.

Example:

```text
Grocery Item 'milk' added to store 'Walmart' on 06-10-2026
Grocery Item 'mint tea' added to store 'General' on 06-10-2026
Store 'Trader Joes' shopped on 06-14-2026
```

## Installation

Install PyYAML:

```bash
pip install pyyaml
```

## Usage

### Add grocery items

```bash
grocery-list milk bananas
```

Items are automatically added to their default store if one exists.

Result:

```yaml
General:
  - bananas

Walmart:
  - milk
```

### Add items to specific stores

```bash
grocery-list milk -tjs bananas -walmart "ice cream" -costco
```

Result:

```yaml
Trader Joes:
  - milk

Walmart:
  - bananas

Costco:
  - ice cream
```

### View shopping list for a store

```bash
grocery-list -shop tjs
```

Displays:

* General list
* Requested store list

### Mark a store as shopped

```bash
grocery-list -shopped tjs
```

This:

* Clears the General list
* Clears the Trader Joes list
* Writes a log entry

Example:

```text
Store 'Trader Joes' shopped on 06-14-2026
```

## Interactive Bulk Add

Prompt for a store and multiple items.

```bash
grocery-list -add
```

Example:

```text
What store would you like to add to? walmart
Adding to store: Walmart
(comma separated) what would you like to add? bananas, apples, yogurt
```

### Skip store prompt

```bash
grocery-list -add walmart
```

Example:

```text
Adding to store: Walmart
(comma separated) what would you like to add? bananas, apples, yogurt
```

All items entered are treated as though they were added individually to that store.

## Store Matching

Store names are matched using normalized containment.

Examples that match `Trader Joes`:

```text
tjs
trader
Trader Joes
TRADER JOES
```

Examples that match `Walmart`:

```text
wal
mart
walmart
WALMART
```

Matching is case-insensitive.

## Unknown Stores

If a store does not exist:

```bash
grocery-list apples -wholefoods
```

The store is automatically created and added to `defaults.yaml`.

Example:

```yaml
WholeFoods: []
```

The item is then added to that store's active list.

## Duplicate Prevention

Duplicate grocery items are not added to the same store list.

Example:

```bash
grocery-list milk
grocery-list milk
```

Only one `milk` entry will appear in the store list.

## Help

```bash
grocery-list [--help/-help]
```

Displays:

```text
Usage:

grocery-list milk bananas
grocery-list milk -tjs bananas -walmart "ice Cream" -costco
grocery-list -shopped "tjs"
grocery-list -shop "tjs"
grocery-list -add
grocery-list -add walmart
```
