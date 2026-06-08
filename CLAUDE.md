# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This is the home directory of Kyle Mason (masonkr@gmail.com), a Greater Cleveland, OH-based individual with several personal projects here. Each subdirectory is its own independent project — there is no single build system or test runner at this level.

## Key Projects

### `claude-desktop-debian/`
The primary active development project. Unofficial Linux build scripts for Claude Desktop, producing `.deb`, `.rpm`, AppImage, AUR, and Nix flake packages. **Has its own detailed `CLAUDE.md`** — read it before working in this directory.

- Build: `./build.sh --build appimage --clean no`
- Lint: `/lint` skill (shellcheck + actionlint)
- Shell style: tabs for indentation, `[[ ]]` conditionals, lowercase variables, no `set -e`

### `jobscraper/`
A single-file Python script (`jobs.py`) that fetches remote job listings from RemoteOK and We Work Remotely APIs and generates a static `jobs.html` output.

- Run: `python3 jobs.py` → opens `jobs.html`

### `kylemason.org/` and `manstuffco/`
Static HTML personal websites with no build process. Edit `index.html` directly.

- `kylemason.org` is deployed via GitHub Pages (CNAME set to `kylemason.org`)

### `Home-Lab/`
Documentation for a Proxmox home lab setup on an Intel Mac Mini, with Tailscale VPN and Pi-hole DNS in LXC containers.

- Proxmox web UI: `https://192.168.1.193:8006` (local) or `https://100.116.237.31:8006` (Tailscale)
- Pi-hole admin: `http://192.168.1.47/admin` (primary), `192.168.1.170` (backup Raspberry Pi 4)

### `pacextractor/`
A C tool for extracting Spreadtrum PAC firmware archives.

- Build: `make` (produces `pacextractor` binary)

### `spreadtrum_flash/` and `CVE-2022-38694_unlock_bootloader/`
Low-level C tools for flashing and unlocking Spreadtrum/UNISOC Android devices over USB.

- Build: `make` in each directory

## Shell Environment

- Shell: bash, with nvm managing Node.js (loaded from `~/.nvm/nvm.sh`)
- Arduino IDE 2.x configured in `~/.arduino15/`
- VS Code available at `/usr/bin/code`
