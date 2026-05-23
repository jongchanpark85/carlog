# CLAUDE.md

Guidance for Claude Code (and other AI coding assistants) working in this repo.

## Project

**Car Log** — a photo-based vehicle record web app.
Users register vehicles and record: parking (GPS auto-save), maintenance history,
accident response, vehicle condition (scratches, warning lights), and
handover records (business mode).

Personal mode: everyday vehicle management, family sharing.
Business mode: driving log with purpose tags (work/personal), handover records,
vehicle inspection reports.

No build step, no backend. All state lives in the browser's `localStorage`,
served as static files behind Nginx in a Docker container.

## Stack

- **Frontend**: single `app/index.html` (vanilla HTML + CSS + JS).
  PWA via `manifest.json` + `sw.js`. Korean UI, light theme by default.
  Bottom nav: 홈/주차/정비/차량 + accident FAB.
  Business mode: adds 운행일지, 인수인계 quick actions on home.
- **Server**: `nginx:alpine`. Listens on `$PORT` (default 3403), `/healthz`.
- **Containers**: Dockerfile + docker-compose for local and NAS.
- **Storage**: browser localStorage — no backend database.

## Run

```bash
# Local
docker compose up --build -d
open http://localhost:3403

# Or open app/index.html directly in a browser (no server required for dev)
```

## Layout

```
app/
  index.html        Car Log app (single-file vanilla JS, localStorage, PWA)
  manifest.json     PWA manifest
  sw.js             Service worker (network-first HTML, cache-first assets)
  icon-192.png      PWA icon
  icon-512.png      PWA icon
Dockerfile          nginx:alpine, $PORT-aware, /healthz
docker-compose.yml  Local dev / NAS deployment
docker-entrypoint.sh  Renders nginx.conf with $PORT at start
nginx.conf          Site template (envsubst replaces ${PORT})
docs/
  todo.md           Phase progress with completion %
CLAUDE.md           This file
README.md           Project overview
```

## localStorage Keys

| Key | Contents |
|-----|----------|
| `car_v` | Vehicles `[{id, name, plate, make, model, year, color, mileage, ...}]` |
| `car_p` | Parking records `[{id, vehicleId, ts, lat, lng, addr, floor, zone, purpose, photos, isActive, exitTime}]` |
| `car_m` | Maintenance records `[{id, vehicleId, type, date, mileage, cost, nextMileage, shop, memo, photos}]` |
| `car_a` | Accident records `[{id, vehicleId, ts, lat, lng, addr, plate, contact, memo, photos}]` |
| `car_s` | Vehicle status records `[{id, vehicleId, category, description, photos, ts}]` |
| `car_h` | Handover records (business) `[{id, vehicleId, type, driver, mileage, fuel, memo, photos, ts}]` |
| `car_cfg` | Settings `{mode:'personal'|'business', theme:'light'|'dark', selectedVehicleId}` |

`purpose` in parking records: `'work'` | `'personal'` | `null` (personal mode records have null).

## Modes

On first launch, user selects **개인용 (personal)** or **법인/업무용 (business)** from the
onboarding screen. Mode is stored in `car_cfg.mode`. Switching mode via Settings sheet
(gear icon on home screen) is always available.

Business mode adds:
- 운행목적 (work/personal) field to parking records
- 운행일지 view with work/personal ratio stats
- 인수인계 recording (인수/반납, driver name, mileage, fuel level, photos)

## Deployment

| Stage | Platform | How |
|-------|----------|-----|
| Now | **Synology NAS** | DSM Container Manager + 1-min `git pull` cron |
| Next | **GCP Cloud Run** | `gcloud run deploy --source .` |

Port default: **3403** (same as INO hub). Keep as-is unless explicitly changed.

## Conventions

- **All file contents in English** (identifiers, comments, variable names).
  UI strings may be Korean.
- **Responses in Korean.** All Claude replies to the user are in Korean.
- **Commit messages**: Korean one-liner in `한글 요약 — 설명` format (em-dash).
  Example: `법인 운행일지 추가 — 업무/개인 통계 바 포함`.
- **Commit + push every change.** No uncommitted files ever.
- **No LFS.** Keep binaries small.
- **Auto-decide.** Don't ask the user clarifying questions; pick a sensible
  default and proceed.
- **Always update** `CLAUDE.md`, `README.md`, and `docs/todo.md` (with refreshed
  completion %) whenever behavior changes.
- **Single-file frontend**: keep all UI in `app/index.html` until it exceeds
  ~3000 lines. Don't split into a build pipeline prematurely.
- **Photo handling**: Canvas resize to 800px wide, JPEG quality 0.72, stored as
  base64 in localStorage. Max 8 photos per record.
- **GPS**: navigator.geolocation → Nominatim reverse geocoding.
- **Cloud-portable Docker**: image must be self-contained. `docker-compose.yml`
  uses bind-mount (`./app` → nginx html) for NAS convenience so `git pull &&
  docker restart carlog` deploys immediately without image rebuild.

## When in doubt

- Read `docs/todo.md` first — it lists what's done and what's next.
- The entire frontend is in `app/index.html`.
- Don't introduce a framework, build step, or backend without asking.
