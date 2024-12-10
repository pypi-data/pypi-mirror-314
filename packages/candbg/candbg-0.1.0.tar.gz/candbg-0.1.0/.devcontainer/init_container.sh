#!/bin/bash

set -e

# list boards with `circuitpython_setboard --list`
BOARD=feather_m4_can

sudo circuitpython_setboard $BOARD

pip install -e .
