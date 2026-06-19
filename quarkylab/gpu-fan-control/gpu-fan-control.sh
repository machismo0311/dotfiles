#!/usr/bin/env bash
#
# gpu-fan-control.sh — dynamic R730 chassis fan control driven by GPU temp.
# Runs on the Proxmox host. Fails safe to iDRAC automatic control on any error.

set -u
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

POLL_INTERVAL=10
LOG_TAG="gpu-fan"

ipmi() { ipmitool "$@"; }   # in-band: talks to local BMC via /dev/ipmi0

enable_manual() { ipmi raw 0x30 0x30 0x01 0x00 >/dev/null 2>&1; }
enable_auto()   { ipmi raw 0x30 0x30 0x01 0x01 >/dev/null 2>&1; }
set_fan()       { ipmi raw 0x30 0x30 0x02 0xff "$1" >/dev/null 2>&1; }

# Preflight: refuse to touch fans if we can't reach the BMC.
if ! ipmi mc info >/dev/null 2>&1; then
    logger -t "$LOG_TAG" "ERROR: cannot reach local BMC (is ipmi_devintf loaded?)"
    exit 1
fi

# Fail-safe: on ANY exit, restore iDRAC automatic control so the box is never
# left stuck at a low fixed speed.
failsafe() {
    trap - SIGTERM SIGINT EXIT
    logger -t "$LOG_TAG" "stopping - restoring iDRAC automatic fan control"
    enable_auto
    exit 0
}
trap failsafe SIGTERM SIGINT EXIT

# Stop iDRAC from panic-ramping fans over the unrecognized GPU, so that our
# fail-safe (auto mode) also behaves sanely.
ipmi raw 0x30 0xce 0x00 0x16 0x05 0x00 0x00 0x00 0x05 0x00 0x01 0x00 0x00 >/dev/null 2>&1

duty_for_temp() {
    local t=$1
    if   (( t >= 85 )); then echo 0x64
    elif (( t >= 80 )); then echo 0x41
    elif (( t >= 75 )); then echo 0x32
    elif (( t >= 70 )); then echo 0x28
    elif (( t >= 65 )); then echo 0x1e
    elif (( t >= 60 )); then echo 0x19
    elif (( t >= 50 )); then echo 0x14
    else                     echo 0x0f
    fi
}

enable_manual
last_duty=""

while true; do
    temp=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits 2>/dev/null \
           | sort -rn | head -1)

    if ! [[ "$temp" =~ ^[0-9]+$ ]]; then
        logger -t "$LOG_TAG" "WARNING: cannot read GPU temp - handing to iDRAC auto"
        enable_auto
        sleep "$POLL_INTERVAL"
        enable_manual
        continue
    fi

    duty=$(duty_for_temp "$temp")
    if [[ "$duty" != "$last_duty" ]]; then
        set_fan "$duty"
        logger -t "$LOG_TAG" "GPU ${temp}C -> fan duty ${duty}"
        last_duty="$duty"
    fi

    sleep "$POLL_INTERVAL"
done
