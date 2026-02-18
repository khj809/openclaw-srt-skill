# SRT Korean Train Service - OpenClaw Skill

OpenClaw skill for managing Korean SRT (Super Rapid Train) reservations — search, booking, continuous monitoring, and cancellation.

## Features

- 🔍 **Search trains** with real-time seat availability
- 🎫 **One-shot reservation** from search results
- 🔄 **Continuous monitoring** — background retry process for sold-out trains
- 📋 **View bookings**
- 🗑️ **Cancel bookings**
- 🤖 **AI-friendly** JSON output
- 🛡️ **Rate limiting** to protect account

## Installation

```bash
clawhub install srt
```

Set credentials in your shell profile:
```bash
export SRT_PHONE="010-XXXX-XXXX"   # hyphens required
export SRT_PASSWORD="your_password"
```

## Natural Language Examples

- "2월 27일 수서에서 동대구 가는 열차 20시 이후 보여줘"
- "SRT369 2자리 예약해줘"
- "취소표 나오면 잡아줘 — 24시간 동안 돌려줘"
- "내 예약 확인해줘"
- "부산 예약 취소해줘"

## Project Structure

```
openclaw-srt-skill/
├── SKILL.md                  # OpenClaw skill definition (AI reference)
├── README.md                 # This file
├── requirements.txt
└── scripts/
    ├── srt_cli.py            # CLI router (search / reserve / list / cancel)
    ├── search_trains.py      # Search implementation
    ├── make_reservation.py   # Reservation with --retry support
    ├── check_retry_log.py    # Log tail utility for monitoring
    ├── view_bookings.py      # Bookings viewer
    ├── cancel_booking.py     # Cancellation
    └── utils.py              # Shared utilities
```

## Direct CLI Usage

```bash
# Search
uv run --with SRTrain python3 scripts/srt_cli.py search \
  --departure "수서" --arrival "부산" --date "20260227" --time "140000"

# Reserve
uv run --with SRTrain python3 scripts/srt_cli.py reserve --train-id "1"

# Continuous retry (background)
nohup uv run --with SRTrain python3 scripts/make_reservation.py \
  --train-id 1 --retry --timeout-minutes 1440 --wait-seconds 10 \
  > ~/.openclaw/tmp/srt/srt369_retry.log 2>&1 &

# Check retry log
python3 scripts/check_retry_log.py --log-file ~/.openclaw/tmp/srt/srt369_retry.log --lines 30

# View bookings
uv run --with SRTrain python3 scripts/srt_cli.py list

# Cancel
uv run --with SRTrain python3 scripts/srt_cli.py cancel \
  --reservation-id "RES123456" --confirm
```

## Publishing to ClawHub

```bash
clawhub login
clawhub publish . \
  --slug srt \
  --name "SRT Korean Train Service" \
  --version 0.1.3 \
  --tags latest
```

## Version History

- **1.0.0** — Security hardening + SKILL.md refactor
  - Replace `pickle` with JSON for search result caching (removes RCE-class deserialization risk)
  - Add `os.chmod(0o600)` on all created files (log, cache, rate-limit state)
  - Add `get_data_dir()` via `SRT_DATA_DIR` env var — removes hardcoded `~/.openclaw/tmp/srt` path
  - Add `--log-file` arg to `make_reservation.py`; prints `LOG_FILE: <path>` at startup
  - Add `requires.env` metadata for `SRT_PHONE`/`SRT_PASSWORD` (fixes ClawHub security scan mismatch)
  - Add SRTrain PyPI/GitHub source URL to install spec
  - Compact `SKILL.md`: add Continuous Monitoring architecture, remove non-skill content
- **0.1.3** — Add `make_reservation.py --retry` for continuous monitoring; add `check_retry_log.py`
- **0.1.2** — Add `--all` flag for sold-out trains
- **0.1.1** — Use `uv` for dependency management
- **0.1.0** — Initial release (February 2026)

## License

MIT
