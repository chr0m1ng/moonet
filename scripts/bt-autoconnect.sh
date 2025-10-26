#!/usr/bin/env bash
set -euo pipefail

MAC="${1:-C0:28:8D:10:6A:ED}"  # Default MAC address
RETRIES=8
SLEEP=4

# Ensure BT is unblocked and up
rfkill unblock bluetooth || true
hciconfig hci0 up || true

# Wait for bluetoothd to be active
for i in {1..10}; do
  systemctl is-active --quiet bluetooth && break || true
  sleep 1
done

# Try multiple times (useful at boot)
i=0
while [ $i -lt $RETRIES ]; do
  bluetoothctl <<BTCTL
power on
agent on
default-agent
trust $MAC
connect $MAC
BTCTL

  # Check if connected
  if bluetoothctl info "$MAC" | grep -q "Connected: yes"; then
    exit 0
  fi

  sleep "$SLEEP"
  i=$((i+1))
done

# If we got here, connection failed
exit 1
