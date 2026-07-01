# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This is the home directory of Kyle Mason (masonkr@gmail.com), a Greater Cleveland, OH-based individual. It is tracked as the `machismo0311/dotfiles` git repo (public). Each subdirectory is an independent project — there is no single build system or test runner at this level.

## Repo Structure

### Submodules
| Directory | Remote | Notes |
|---|---|---|
| `Home-Lab/` | `machismo0311/Home-Lab` (public) | Homelab docs + Obsidian vault |
| `kylemason.org/` | `machismo0311/kylemason.org` (public) | Personal site |
| `manstuffco/` | `machismo0311/Manstuffco` (public) | Personal site |
| `claude-desktop-debian/` | `aaddrick/claude-desktop-debian` (public) | Upstream project, not a fork |
| `pacextractor/` | `divinebird/pacextractor` (public) | Upstream project, not a fork |
| `CVE-2022-38694_unlock_bootloader/` | `TomKing062/CVE-2022-38694_unlock_bootloader` (public) | Upstream project, not a fork |
| `spreadtrum_flash/` | `TomKing062/spreadtrum_flash` (public) | Upstream project, not a fork |

After pushing to any submodule's own remote, update the pointer here:
```bash
git submodule update --remote <name>
git add <name>
git commit -m "Update <name> submodule to latest"
git push
```

### Direct files
- `jobscraper/` — single-script Python project with no upstream remote
- `Vaults/homelab-vault/` — Obsidian vault, **mirrored** into `Home-Lab/vault/`. Keep the two copies byte-identical: edit both, then commit `Home-Lab/vault/` inside the submodule (push to its remote + update the pointer here) and `Vaults/homelab-vault/` directly in dotfiles. A `diff -rq` between them should be empty.
- Dotfiles: `.bashrc`, `.bash_aliases`, `.profile`, `.bash_logout`, `.gitconfig`, `.ssh/config`, `CLAUDE.md`

## Key Projects

### `claude-desktop-debian/`
Unofficial Linux build scripts for Claude Desktop, producing `.deb`, `.rpm`, AppImage, AUR, and Nix flake packages. **Has its own detailed `CLAUDE.md`** — read it before working here.

- Build: `./build.sh --build appimage --clean no`
- Lint: `/lint` skill (shellcheck + actionlint)
- Shell style: tabs for indentation, `[[ ]]` conditionals, lowercase variables, no `set -e`

### `Home-Lab/`
Homelab documentation for a 7-node Proxmox VE 9.2.3 cluster (km-cluster) — R730s (QuarkyLab=ML/RTX 6000→RTX 8000 planned, Jarvis=LLM/2× RTX 6000 planned — GPU SW stack staged), SuperMicro Randy (PBS/storage), EliteDesk nodes (pve2–pve5), Juniper switching, and services. **Has its own detailed `CLAUDE.md`** — read it before working in the homelab; it carries the authoritative node/IP/service tables and safety notes. Also contains the Obsidian vault at `Home-Lab/vault/`.

- Proxmox web UI: any cluster node on `:8006`, e.g. pve3 `https://192.168.10.201:8006`. Note `192.168.10.193` / Tailscale `100.116.237.31` is **pve1**, a standalone Mac Mini (Pi-hole host), *not* a km-cluster member.
- Pi-hole admin: `http://192.168.10.177/admin`
- EX3400 management: `192.168.10.50`
- PBS: `https://192.168.10.187:8007`

### `jobscraper/`
Single-file Python script that fetches remote job listings from RemoteOK and We Work Remotely and generates a static `jobs.html`.

- Run: `python3 jobs.py` → writes `jobs.html`

### `kylemason.org/` and `manstuffco/`
Static HTML personal websites. Edit `index.html` directly — no build process. Both deployed via GitHub Pages.

### `pacextractor/`, `spreadtrum_flash/`, `CVE-2022-38694_unlock_bootloader/`
Low-level C tools for working with Spreadtrum/UNISOC Android firmware. Build each with `make`.

## Shell Environment

- Shell: bash, with nvm managing Node.js (loaded from `~/.nvm/nvm.sh`)
- Arduino IDE 2.x configured in `~/.arduino15/`
- VS Code available at `/usr/bin/code`
