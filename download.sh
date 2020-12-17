#!/bin/bash
#while read p; do
#    wget -c --tries=2 "$p" &
#done<output.txt
#aria2c -c -j10 --connect-timeout=60 --max-connection-per-server=16 --split=16 --min-split-size=1M --human-readable=true --file-allocation=none --enable-rpc
source meuenv/bin/activate
python3 ./main.py
