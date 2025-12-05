#!/bin/bash
set -e
cd "$(dirname "$0")"

TARGET=${1:-all}

# validate input
if [[ ! $TARGET =~ ^(attacker|vuln|hard|all)$ ]]; then
  echo "invalid target $TARGET"
  echo "usage: $0 [ attacker | vuln | hard | all ]"
  exit 1
fi

# for podman & docker compatibility
if command -v podman &> /dev/null; then
    TOOL=podman
elif command -v docker &> /dev/null; then
    TOOL=docker
else
    echo "Error: podman or docker is not installed." >&2
    exit 1
fi

echo
echo "--- Stopping containers ---"
$TOOL compose down -v

echo
if [[ $TARGET =~ ^(all)$ ]]; then
  echo "--- Rebuilding all apps ---"
  $TOOL compose build --no-cache 1>/dev/null
else
  echo "--- Rebuilding $TARGET-app ---"
  $TOOL compose build --no-cache "$TARGET-app"
fi

echo
echo " ✔ REBUILD COMPLETED"

echo
echo "--- Starting containers ---"
$TOOL compose up -d

sleep 0.25

echo
echo "---"
sleep 0.25
$TOOL compose ps
