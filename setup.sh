#!/bin/bash

command -v python3 > /dev/null 2>&1 || { echo "python3 binary not found" >&2; exit 1; }
mkdir -p venv
python3 -m venv venv && {
    source venv/bin/activate
    python -m pip install -r requirements.txt
}

echo "done"