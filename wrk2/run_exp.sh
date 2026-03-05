#!/usr/bin/env bash
set -euo pipefail

# USAGE: ./run_exp.sh > sweep.log 2>&1 & echo $! > sweep.pid

# SUT address (remote server)
HOST="localhost"
PORT_NUM=8080

URL="http://${HOST}:${PORT_NUM}"
THREADS=2
DURATION="30s"

for C in 4 16 64 256 1024 4096 16384; do
  for RPS in 500 1000 2000 4000 8000; do
    echo "========================================"
    echo "Running wrk with -c $C and -R $RPS"
    echo "========================================"

    ./wrk -t"$THREADS" -c"$C" --requests -R"$RPS" -d"$DURATION" "$URL" --csv || true

    echo
    echo "Sleeping 5 seconds before next run..."
    sleep 5
  done
done