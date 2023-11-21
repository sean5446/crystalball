#!/bin/bash

# install with:
# sudo systemctl edit --force --full crystalball.service
# paste the contents of bootservice
# run: sudo systemctl enable crystalball
# then startup on power-on should work

sudo /usr/bin/env python3 /home/queso/src/crystalball/server.py

