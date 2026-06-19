# GPU-Aware Chassis Fan Control (Dell R730 + Quadro RTX 6000)

Dynamic fan control for a Dell PowerEdge R730 running a non-Dell GPU under
Proxmox VE. A small daemon reads the GPU temperature and drives the chassis
fans to match it, replacing iDRAC's broken default behavior. Fails safe to
iDRAC automatic control on any error.

Deployed on QuarkyLab (R730 #1, dual E5-2699 v4, 512 GB LRDIMM, RTX 6000 24 GB).

## The problem this solves

Dell's iDRAC reads temperatures from Dell-supported components only. When it
detects an unrecognized PCIe card — like a Quadro RTX 6000 — it has no thermal
sensor for it, assumes the worst case, and ramps every chassis fan to a high
fixed speed as a safety default. At idle this parked the fans around 55%:
needlessly loud, and completely unresponsive to what the GPU is actually doing.

The naive fix (manual fan control at a fixed low speed) is worse — it removes
the only thing protecting the GPU. If the card heats up under load, fixed-speed
fans won't ramp, and the GPU can throttle or overheat with nobody watching.

This daemon solves both: quiet at idle, automatic ramp under load, and a
fail-safe that hands control back to iDRAC if anything goes wrong.

## How it works

Every 10 seconds the daemon:

1. Reads the hottest GPU temperature via `nvidia-smi`.
2. Maps that temperature to a fan duty cycle (see curve below).
3. Sets the chassis fans over in-band IPMI (`/dev/ipmi0`) — no network, no
   credentials, more reliable than IPMI-over-LAN.

### Fan curve

| GPU Temp | Fan Duty | Hex  |
|----------|----------|------|
| < 50 °C  | 15 %     | 0x0f |
| 50–59 °C | 20 %     | 0x14 |
| 60–64 °C | 25 %     | 0x19 |
| 65–69 °C | 30 %     | 0x1e |
| 70–74 °C | 40 %     | 0x28 |
| 75–79 °C | 50 %     | 0x32 |
| 80–84 °C | 65 %     | 0x41 |
| ≥ 85 °C  | 100 %    | 0x64 |

The RTX 6000 (Turing) throttles its own clocks around 89 °C and hard-shuts-down
near 95 °C as a final hardware backstop, independent of this script.

### Safety design

- Fail-safe on exit. A `trap` on SIGTERM/SIGINT/EXIT restores iDRAC automatic
  fan control whenever the daemon stops or crashes. The box is never left stuck
  at a low fixed speed.
- Fail-safe on sensor loss. If `nvidia-smi` ever fails to return a numeric
  temperature, the loop hands control back to iDRAC auto and keeps retrying.
- Startup preflight. The script refuses to touch the fans unless it can reach
  the local BMC first.
- iDRAC third-party-PCIe override (`raw 0x30 0xce ...`) is applied at startup so
  that even when the fail-safe auto mode takes over, iDRAC does not panic-ramp
  on the unrecognized GPU.

## Files

| File                      | Installs to                                   |
|---------------------------|-----------------------------------------------|
| `gpu-fan-control.sh`      | `/usr/local/sbin/gpu-fan-control.sh`          |
| `gpu-fan-control.service` | `/etc/systemd/system/gpu-fan-control.service` |

## Prerequisites

- A Dell R730 (or similar iDRAC-based PowerEdge) with `ipmitool`
- NVIDIA driver installed on the Proxmox host (`nvidia-smi` working)
- In-band IPMI kernel modules loaded

```bash
apt install ipmitool -y
modprobe ipmi_si ipmi_devintf
echo -e "ipmi_si\nipmi_devintf" >> /etc/modules
ipmitool mc info
```

## Installation

```bash
sudo install -m 755 gpu-fan-control.sh     /usr/local/sbin/gpu-fan-control.sh
sudo install -m 644 gpu-fan-control.service /etc/systemd/system/gpu-fan-control.service
sudo systemctl daemon-reload
sudo systemctl enable --now gpu-fan-control.service
```

## Verification

```bash
systemctl status gpu-fan-control.service
journalctl -t gpu-fan -n 20
ipmitool sdr type Fan
```

A healthy install logs a line like `GPU 30C -> fan duty 0x0f` and shows the fans
below their loud auto-mode speed. Stopping the service logs
`stopping - restoring iDRAC automatic fan control`, confirming the fail-safe.

## Tuning

- Edit `duty_for_temp()` in the script to adjust the curve.
- Change `POLL_INTERVAL` (seconds) to poll more or less often.
- iDRAC will not monitor the GPU while the daemon runs, so watch temps with
  `nvidia-smi` directly.
