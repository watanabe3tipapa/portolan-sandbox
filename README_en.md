# portolan-sandbox

**The end of "distributing map data"—bringing the AI-readable spatial infrastructure "Portolan" to everyone.**

portolan-sandbox is an experimental repository for developing ways to make the open specification "Portolan" more accessible. It aims for a setup where authentication and deployment can be handled with just a Google account, while managing the LP, concept notes, and summary articles in one place.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/watanabe3tipapa/portolan-sandbox/releases)
[![GitHub](https://img.shields.io/github/issues/watanabe3tipapa/portolan-sandbox.svg)](https://github.com/watanabe3tipapa/portolan-sandbox/issues)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-blue.svg)](https://watanabe3tipapa.github.io/portolan-sandbox/)

[Japanese](README.md) | [English](README_en.md)

---

## Overview

Portolan is an open specification that lets geospatial data be published "in a form that AI can read directly," while staying on the publisher's own storage. This repository is dedicated to raising awareness of Portolan and exploring concrete ways to use it.

Key initiatives:

- Outreach through a landing page built with ASTRO (`portolan-lp/`)
- Exploring integration with Google Colaboratory and using the Colab MCP server as a personal development server
- Developing authentication and deployment flows that work with only a Google account
- Organizing ideas and plans in `DEV-MEMO.md`

---

## Concept (why "sandbox")

A sandbox is a place where you can safely experiment and play. Likewise, this repository serves as an experimental field to try out and grow methods for making Portolan more accessible.

---

## Key Features

- Summary article covering the basics of Portolan (`Portolan_要約.html`)
- ASTRO-based LP with automatic GitHub Pages deployment (published on every push to `main`)
- Centralized management of ideas and plans (`DEV-MEMO.md`)
- Aiming toward a deployment setup that can be completed with only a Google account

---

## Prerequisites

| Tool | Required Version | Check Command |
|---|---:|---|
| Node.js | >= 22 | `node --version` |
| npm | >= 10 | `npm --version` |

---

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/watanabe3tipapa/portolan-sandbox.git
```

2. Run the LP locally:

```bash
cd portolan-lp
npm install
npm run dev
```

3. Build:

```bash
npm run build
```

---

## Repository Structure (main files and directories)

- `DEV-MEMO.md` — concept, ideas, and development notes
- `Portolan_要約.html` — summary of the GeoAI #16 article, "The end of the era of distributing map data"
- `portolan-lp/` — ASTRO-based landing page
- `.github/workflows/deploy.yml` — GitHub Pages auto-deploy workflow
- `README.md` / `README_en.md` — this documentation (Japanese / English)
- `LICENSE` — MIT License

---

## Contributing

Contributions are welcome. For significant changes, please open an issue first.

Basic workflow:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your change'`)
4. Push the branch and create a Pull Request

For details, see the repository's Issues page.

---

## Contact / Live Sites

- GitHub: https://github.com/watanabe3tipapa/portolan-sandbox
- LP (GitHub Pages): https://watanabe3tipapa.github.io/portolan-sandbox/

---

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---

## Development / Maintenance Status

- The repository is not archived.
- Last updated: 2026-09-11 (as of this document / v0.1.0)