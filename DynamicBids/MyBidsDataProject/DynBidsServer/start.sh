#!/bin/sh

export PYTHONPATH=""
export PYTHONPATH="${PYTHONPATH}:$HOME/eclipse-workspace/DynBidsServer/"
export PYTHONPATH="${PYTHONPATH}:$HOME/eclipse-workspace/DynBidsServer/ApiProvider"
export PYTHONPATH="${PYTHONPATH}:$HOME/eclipse-workspace/DynBidsServer/blockchains"

python3 ./ApiProvider/main.py

