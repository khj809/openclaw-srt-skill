# OpenClaw SRT Skill

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
    ├── srt_cli.py            # CLI router — pure dispatcher, no business logic
    ├── train.py              # Train search + fetch_trains_from_cache()
    ├── reserve.py            # All reservation logic (one-shot, retry, list, cancel, status, stop, log)
    └── utils.py              # Shared utilities (credentials, path safety, rate limiting, formatting)
```

## Direct CLI Usage

```bash
# Search
uv run --with SRTrain python3 scripts/srt_cli.py train search \
  --departure "수서" --arrival "부산" --date "20260227" --time "140000"

# Reserve (one-shot)
uv run --with SRTrain python3 scripts/srt_cli.py reserve one-shot --train-id "1"

# Continuous retry (background)
nohup uv run --with SRTrain python3 scripts/srt_cli.py reserve retry \
  --train-id 1 --timeout-minutes 1440 --wait-seconds 10 &

# Check retry log
uv run --with SRTrain python3 scripts/srt_cli.py reserve log -n 30

# View bookings
uv run --with SRTrain python3 scripts/srt_cli.py reserve list

# Cancel
uv run --with SRTrain python3 scripts/srt_cli.py reserve cancel \
  --reservation-id "RES123456" --confirm
```

## Publishing to ClawHub

```bash
clawhub login
clawhub publish . \
  --slug srt \
  --name "SRT" \
  --version 1.1.1 \
  --tags latest
```

## Version History

- **1.1.1** — Fix cron delivery for isolated sessions
  - Replace `--announce` delivery with `--no-deliver` + explicit `message` tool call
  - Avoids `gateway closed (1008): pairing required` error in isolated cron sessions
  - Update SKILL.md Step 3/4 with CLI-based cron examples and delivery guidance
- **1.1.0** — CLI restructure + codebase consolidation
  - Rename `search_trains.py` → `train.py`; consolidate `make_reservation.py`, `view_bookings.py`, `cancel_booking.py`, `check_retry_log.py` → `reserve.py`
  - All reservation logic (`run_one_shot`, `run_retry`, `run_list`, `run_cancel`, `run_status`, `run_stop`, `run_log`) lives in `reserve.py`
  - Extract `fetch_trains_from_cache()` into `train.py`; delegates to `search_trains()` — removes duplicate SRT API call
  - `utils.load_search_results()` replaced by `load_search_cache()` (file I/O only; no SRT calls)
  - `srt_cli.py` is now a pure router with no inline business logic
  - Update SKILL.md: remove `make_reservation.py` references; fix `reserve retry` option table
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
