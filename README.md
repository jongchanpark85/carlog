# Car Log

> 사진 기반 차량 상태기록 플랫폼 — 주차·정비·사고·상태·인수인계를 사진 중심으로 빠르게 기록.

사용자는 사진을 찍고 간단히 선택만 하면 되고, 앱은 날짜·시간·위치·차량을 자동 정리합니다.

## 핵심 기능

- 🚗 **차량 등록** — 번호판, 제조사, 연식, 보험·검사 일정 관리
- 🅿 **주차 기록** — 사진 + GPS 자동저장 (Nominatim 역지오코딩) + 층수/구역 선택
- 🔧 **정비 기록** — 종류·비용·주행거리·사진, 다음 교체 알림
- ⚠ **사고 대응** — 현장사진·위치 즉시 기록 + 보험사 긴급연락처
- 📷 **차량 상태 기록** — 긁힘·경고등·타이어·유리 등 사진 기반 기록
- 🏢 **법인/업무용 모드** — 운행목적(업무/개인) 기록, 운행일지, 인수인계 기록
- 🌗 **라이트/다크 테마** — 설정에서 토글

## 기술 구성

| 레이어 | 기술 |
|--------|------|
| Frontend | Single-file HTML + Vanilla CSS/JS |
| Storage | 브라우저 `localStorage` |
| Server | `nginx:alpine` — `$PORT` 동적 바인딩, `/healthz` |
| Container | Docker, docker-compose |

## 빠른 시작

```bash
docker compose up --build -d
open http://localhost:3403
```

또는 `app/index.html` 을 브라우저로 직접 열어도 동작합니다.

## 모드

첫 실행 시 **개인용** / **법인/업무용** 선택. 설정(톱니바퀴)에서 언제든 변경 가능.

## 프로젝트 구조

```
app/index.html        Car Log 앱 (단일 파일)
docs/todo.md          기능 진행률
Dockerfile            nginx:alpine
docker-compose.yml    로컬 / NAS 배포
CLAUDE.md             AI 어시스턴트 가이드
```
