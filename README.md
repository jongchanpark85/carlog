# Car Log

> Photo-based vehicle record platform — parking, maintenance, accidents, condition, and business handovers, all organized around photos.

Take a photo and tap — the app auto-records date, time, location, and vehicle.

## Features

- **Vehicle Registration** — plate, make, model, year, insurance and inspection schedule
- **Parking Records** — photo + GPS auto-save (Nominatim reverse geocoding), floor/zone selection, active parking banner with photo on home screen
- **Maintenance Records** — type, cost, mileage, photos, next service reminder
- **Accident Response** — scene photos, GPS location, emergency insurer contacts
- **Vehicle Status** — scratches, warning lights, tires, glass — photo-based log
- **Vehicle Timeline** — unified view: parking, maintenance, accidents, status, handovers
- **Personal / Business mode** — onboarding selection, toggle in settings any time
- **Business features**:
  - 운행목적 (work/personal) on parking records
  - 운행일지 — work/personal ratio stats
  - 인수인계 — driver handover records (mileage, fuel, photos)
  - 렌트카 점검 — pickup/return comparison, fuel level, photos, PDF report
  - 외관 체크리스트 — section-by-section 양호/경미/손상 check, photos, PDF report
- **Light/Dark theme** — toggle in settings
- **HUB button** — fixed top-center, links to MetaMoni hub (`/`)
- **PWA** — installable, offline-capable, service worker with update banner
- **Data backup/restore** — JSON export/import for all records

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Single-file `app/index.html` — vanilla HTML + CSS + JS |
| Storage | Browser `localStorage` (no backend) |
| Server | `nginx:alpine` — `$PORT`-aware, `/healthz` endpoint |
| Container | Docker, docker-compose |
| PWA | `manifest.json` + `sw.js` (network-first HTML, cache-first assets) |

## Quick Start

```bash
# Local Docker
docker compose up --build -d
open http://localhost:3403

# Or open app/index.html directly in a browser (no server needed for dev)
```

## Deployment

Car Log is served **via the INO project** at the `/car/` path on Synology NAS (port 3403).
NAS auto-pulls the INO repo every 1 minute via cron.

**To deploy to NAS:**
```bash
cp app/index.html ../ino/app/car/index.html
# commit + push carlog repo
# commit + push ino repo → NAS picks up within 1 min
```

| Stage | Platform |
|-------|---------|
| Active | Synology NAS via INO project (`/car/`) |
| Local dev | `docker compose up --build -d` or open `app/index.html` directly |
| Next | GCP Cloud Run — `gcloud run deploy --source .` |

## Project Structure

```
app/
  index.html        Car Log app (single-file vanilla JS, localStorage, PWA)
  manifest.json     PWA manifest
  sw.js             Service worker
  icon-192.png      PWA icon
  icon-512.png      PWA icon
.claude/
  agents/           Specialized sub-agents (frontend, devops, docs, qa)
docs/
  todo.md           Phase progress with completion %
Dockerfile          nginx:alpine, $PORT-aware
docker-compose.yml  Local dev / NAS deployment
CLAUDE.md           AI assistant guide
```

## Modes

On first launch, select **개인용 (personal)** or **법인/업무용 (business)**.
Toggle any time via the gear icon on the home screen.
