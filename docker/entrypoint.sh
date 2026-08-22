#!/bin/sh
set -e

chown -R appuser:appuser /app/logs /app/static /app/media /app/assets

exec gosu appuser "$@"
