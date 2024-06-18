#! /bin/sh

# A helper script that can be executed off docker, just so that
# uvicorn will print the right port number.  Docker will not do
# environment variable substitution in CMD lines, so this script
# became necessary.

set -eu

python3 -m uvicorn sdx_lc.app:asgi_app --host 0.0.0.0 --port "$SDXLC_PORT"
