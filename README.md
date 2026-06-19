# dotfiles

Personal dotfiles and project index for Kyle Mason (`machismo0311`).

## Dotfiles

| File | Purpose |
|---|---|
| `.bashrc` | Interactive shell config, aliases, nvm init |
| `.profile` | Login shell config, PATH setup |
| `.bash_logout` | Clears screen on logout |
| `.gitconfig` | Git user config, GitHub credential helper |

## Projects

### My repos (submodules)

| Directory | Description |
|---|---|
| [`Home-Lab/`](https://github.com/machismo0311/Home-Lab) | Homelab docs — Proxmox cluster, Juniper switching, Obsidian vault |
| [`kylemason.org/`](https://github.com/machismo0311/kylemason.org) | Personal website |
| [`manstuffco/`](https://github.com/machismo0311/Manstuffco) | Personal website |

### Third-party repos (submodules)

| Directory | Description |
|---|---|
| [`claude-desktop-debian/`](https://github.com/aaddrick/claude-desktop-debian) | Unofficial Claude Desktop Linux packaging |
| [`pacextractor/`](https://github.com/divinebird/pacextractor) | Spreadtrum PAC firmware extractor |
| [`spreadtrum_flash/`](https://github.com/TomKing062/spreadtrum_flash) | Spreadtrum/UNISOC device flash tool |
| [`CVE-2022-38694_unlock_bootloader/`](https://github.com/TomKing062/CVE-2022-38694_unlock_bootloader) | Bootloader unlock tool |

### Local projects

| Directory | Description |
|---|---|
| `jobscraper/` | Python script that scrapes remote job listings and generates a static HTML page |
| `Vaults/homelab-vault/` | Obsidian vault with homelab notes (also in `Home-Lab/vault/`) |
| `quarkylab/gpu-fan-control/` | temperature-driven chassis fan control for QuarkyLab's R730 + RTX 6000; replaces iDRAC's panic-ramp on the non-Dell GPU and fails safe to iDRAC auto |

## Cloning

```bash
git clone --recurse-submodules https://github.com/machismo0311/dotfiles.git
```
