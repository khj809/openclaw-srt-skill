# SRT Korean Train Service - OpenClaw Skill

OpenClaw skill for managing Korean SRT (Super Rapid Train) reservations with search, booking, view, and cancellation capabilities.

## Features

- 🔍 **Search trains** between stations with real-time seat availability
- 🎫 **Make reservations** with automatic rate limiting
- 📋 **View bookings** to see all active reservations
- 🗑️ **Cancel bookings** with confirmation prompts
- 🤖 **AI-friendly** JSON output for programmatic access
- 🛡️ **Rate limiting** to prevent account blocking
- ⚠️ **Retry protection** with maximum 10 attempts per session

## Quick Start

### Installation

1. **Install from ClawHub:**
```bash
clawhub install srt
```

2. **Set environment variables:**
```bash
export SRT_PHONE="010-1234-5678"
export SRT_PASSWORD="your_password"
```
Add to your shell profile (`~/.zshrc`, `~/.bashrc`) for persistence.

**Important:** Phone number must include hyphens (e.g., `010-1234-5678`)

### Usage Examples

**Search trains:**
```bash
/srt search --departure "수서" --arrival "부산" --date "20260217" --time "140000"
```

**Make reservation:**
```bash
/srt reserve --train-id "1"
```

**View bookings:**
```bash
/srt list
```

**Cancel booking:**
```bash
/srt cancel --reservation-id "RES123456"
```

## Natural Language Examples

The AI can understand Korean requests:

- "2월 17일에 수서에서 부산 가는 기차 검색해줘"
- "제일 빠른걸로 2장 예약해줘"
- "내 예약 확인해줘"
- "부산 예약 취소해줘"
- "매진이면 다음거 시도해줘"

## Common Korean Stations

- 수서 (Suseo) - Seoul
- 부산 (Busan)
- 동대구 (Dongdaegu)
- 대전 (Daejeon)
- 광주송정 (Gwangju-Songjeong)
- 울산 (Ulsan)
- 포항 (Pohang)

## Rate Limiting

To protect your account:
- Minimum 3 seconds between reservations
- Minimum 5 seconds between searches
- Maximum 10 retry attempts per session
- Exponential backoff after failures

## Important Notes

1. **Payment Required:** Reservations must be paid manually via SRT app/website
2. **Korean Names:** Station names must be in Korean (Hangul)
3. **Date Format:** YYYYMMDD (e.g., 20260217)
4. **Time Format:** HHMMSS (e.g., 140000 for 2:00 PM)

## Documentation

See [SKILL.md](SKILL.md) for complete documentation, including:
- Full command reference
- Error handling guide
- AI orchestration examples
- Troubleshooting tips

## Development

### Local Testing

```bash
# Clone repository
git clone <repository-url>
cd clawhub-srt-skill

# Install dependencies
# Install uv if not already installed
# https://docs.astral.sh/uv/getting-started/installation/

# Configure credentials
export SRT_PHONE="010-1234-5678"
export SRT_PASSWORD="your_password"

# Test commands
uv run --with SRTrain python3 scripts/srt_cli.py search --departure "수서" --arrival "부산" --date "20260203" --time "140000"
```

### Project Structure

```
clawhub-srt-skill/
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── scripts/
    ├── srt_cli.py             # Main CLI router
    ├── search_trains.py       # Search tool
    ├── make_reservation.py    # Reservation tool
    ├── view_bookings.py       # View bookings tool
    ├── cancel_booking.py      # Cancellation tool
    └── utils.py               # Shared utilities
```

## License

MIT

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
- File an issue on GitHub
- Check [SKILL.md](SKILL.md) for troubleshooting
- Visit SRT website: https://etk.srail.kr

## Version

**1.0.0** - Initial release (February 2026)
