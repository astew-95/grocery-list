#!/usr/bin/env bash
# Wrapper script to call the Python tool todo

usage() {
echo "Usage:"
echo
echo "grocery-list milk bananas                                             # add to default list"
echo 'grocery-list milk -tjs bananas -walmart "ice Cream" -costco   # add groceries to specific stores'
echo "grocery-list -shopped 'tjs'                                   # clear the grocery list for a store"
echo "grocery-list -shop tjs'                                       # get the list for a store"
echo
echo "grocery-list -add  # good for adding items to one store in bulk  "
}

# ---- groceries quick help  ----
if [[ "${1:-}" == "-quickhelp" || "${1:-}" == "--quickhelp" || "${1:-}" == "--qhelp" ]]; then
    usage
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/main.py"

python3 "$PY_SCRIPT" "$@" 

# # ---- helper  ----
# if [[ "${1:-}" == "-help" || "${1:-}" == "--help" ]]; then
#     echo "------------------- global tool shop help -----------------"
#     usage
#     echo ""
#     echo "For global tool help, use -globalhelp instead of -help ."
#     # specify a README here for this specific tool
#     README_FILE=""
#     if [[ -e "$README_FILE" ]]; then
#         echo "-------------------- README -------------------------"
#         cat "$README_FILE"
#         echo "-------------------- END OF README -------------------------"
#         echo
#         exit 0
#     fi
#     exit 0
# fi