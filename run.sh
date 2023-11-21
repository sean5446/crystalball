#!/bin/bash

# install with:
# sudo systemctl edit --force --full crystalball.service
# paste the contents of bootservice
# run: sudo systemctl enable crystalball
# then server.py should start on power-on

# cd so the database is created in the same place as the server
cd /home/queso/src/crystalball/ && sudo /usr/bin/env python3 server.py
