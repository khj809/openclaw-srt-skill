---
name: srt
description: Korean SRT (Super Rapid Train) search, reservation, and booking management
homepage: https://github.com/khj809/openclaw-srt-skill
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🚅",
        "requires": { "bins": ["python3", "uv"] },
        "install": [
          {"id": "uv", "kind": "uv", "package": "SRTrain", "label": "Install SRTrain (uv)"}
        ]
      },
  }
---

# SRT Korean Train Service Skill

OpenClaw skill for managing Korean SRT (Super Rapid Train) reservations with search, booking, view, and cancellation capabilities.

## Features

- 🔍 **Search trains** between stations with real-time seat availability
- 🎫 **Make reservations** with automatic rate limiting to protect your account
- 📋 **View bookings** to see all active reservations
- 🗑️ **Cancel bookings** with confirmation prompts
- 🤖 **AI-friendly** JSON output for programmatic access
- 🛡️ **Rate limiting** to prevent account blocking (3s between reservations, 5s between searches)
- ⚠️ **Retry protection** with maximum 10 attempts per session

## Prerequisites

1. **Python 3.10+** installed
2. **SRT account** with phone number and password
3. **OpenClaw** installed and configured

## Configuration

Set your SRT credentials as environment variables:

```bash
export SRT_PHONE="010-1234-5678"
export SRT_PASSWORD="your_password"
```

Add these to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) for persistence.

**Security Note:** Avoid committing credentials to version control.

**Important:** Phone number must include hyphens in the format `010-XXXX-XXXX`

## Usage

### User-Invocable Command

Use the `/srt` slash command in OpenClaw:

```
/srt search --departure "수서" --arrival "부산" --date "20260217" --time "140000"
/srt reserve --train-id "1"
/srt list
/srt cancel --reservation-id "RES123456"
```

### Natural Language (AI-Orchestrated)

The AI can invoke this skill based on user intent:

**Examples:**
- "2월 17일에 수서에서 부산 가는 기차 검색해줘" *(Search trains)*
- "제일 빠른걸로 예약해줘" *(Reserve first available)*
- "내 예약 확인해줘" *(List bookings)*
- "부산 예약 취소해줘" *(Cancel booking)*

### Direct CLI Usage

```bash
# Search trains
uv run --with SRTrain python3 scripts/srt_cli.py search \
  --departure "수서" \
  --arrival "부산" \
  --date "20260217" \
  --time "140000" \
  --passengers "adult=2"

# Make reservation (uses train ID from search results)
uv run --with SRTrain python3 scripts/srt_cli.py reserve --train-id "1"

# View bookings
uv run --with SRTrain python3 scripts/srt_cli.py list --format json

# Cancel booking
uv run --with SRTrain python3 scripts/srt_cli.py cancel \
  --reservation-id "RES123456" \
  --confirm
```

## Common Korean Station Names

**Main SRT Stations:**
- 수서 (Suseo) - Seoul SRT station
- 부산 (Busan)
- 동대구 (Dongdaegu) - Daegu
- 대전 (Daejeon)
- 천안아산 (Cheonan-Asan)
- 오송 (Osong)
- 광주송정 (Gwangju-Songjeong)
- 울산 (Ulsan)
- 포항 (Pohang)
- 경주 (Gyeongju)
- 김천구미 (Gimcheon-Gumi)
- 익산 (Iksan)
- 전주 (Jeonju)
- 목포 (Mokpo)
- 신경주 (Singyeongju)

**Important:** Station names MUST be in Korean (Hangul) for the SRT API to work correctly.

## Date and Time Formats

- **Date:** YYYYMMDD (e.g., `20260217` for February 17, 2026)
- **Time:** HHMMSS (e.g., `140000` for 2:00 PM, `093000` for 9:30 AM)

## Tools for AI Agent

This skill provides 4 tools for managing SRT train reservations:

### 1. search_trains
Search for available trains between stations.

**Usage:**
```bash
uv run --with SRTrain python3 scripts/srt_cli.py search \
  --departure "수서" \
  --arrival "부산" \
  --date "20260217" \
  --time "120000"
```

**Returns:** JSON array of available trains with seat availability

**JSON Format:**
```json
{
  "success": true,
  "data": [
    {
      "train_id": "1",
      "train_number": "301",
      "train_name": "SRT301",
      "departure_time": "120500",
      "arrival_time": "143000",
      "departure_station": "수서",
      "arrival_station": "부산",
      "seat_available": true,
      "general_seat": "예약가능",
      "special_seat": "예약가능"
    }
  ]
}
```

### 2. make_reservation
Reserve a specific train from search results.

**Usage:**
```bash
uv run --with SRTrain python3 scripts/srt_cli.py reserve --train-id "1"
```

**Returns:** Reservation details with payment deadline

**JSON Format:**
```json
{
  "success": true,
  "data": {
    "reservation_id": "RES123456",
    "journey_date": "20260217",
    "journey_time": "120500",
    "departure": "수서",
    "arrival": "부산",
    "train_number": "301",
    "seat_number": "3A",
    "payment_required": true
  }
}
```

**Note:** Payment must be completed manually by user via SRT app/website.

### 3. view_bookings
List all current reservations.

**Usage:**
```bash
uv run --with SRTrain python3 scripts/srt_cli.py list --format json
```

**Returns:** JSON array of active reservations

**JSON Format:**
```json
{
  "success": true,
  "data": [
    {
      "reservation_id": "RES123456",
      "journey_date": "20260217",
      "journey_time": "120500",
      "departure": "수서",
      "arrival": "부산",
      "train_number": "301",
      "seat_number": "3A",
      "payment_required": true
    }
  ]
}
```

### 4. cancel_booking
Cancel a reservation by ID.

**Usage:**
```bash
uv run --with SRTrain python3 scripts/srt_cli.py cancel \
  --reservation-id "RES123456" \
  --confirm
```

**Returns:** Cancellation confirmation

**JSON Format:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "reservation_id": "RES123456",
    "message": "Reservation cancelled successfully"
  }
}
```

## Error Handling

The skill provides clear, actionable error messages:

**Common Errors:**

1. **AuthenticationFailed**
   - Invalid credentials
   - **Solution:** Check phone number and password in config

2. **NoSeatsAvailable**
   - Train is sold out
   - **Solution:** Try next train or different time
   - **Exit code:** 1 (retryable)

3. **StationNotFound**
   - Invalid station name
   - **Solution:** Use Korean station names from the list above

4. **NoTrainsFound**
   - No trains for specified route/time
   - **Solution:** Try different date or time

5. **RateLimitExceeded**
   - Too many retry attempts (max 10 per session)
   - **Solution:** Wait a few minutes before trying again

6. **NetworkError**
   - Connection timeout or failure
   - **Solution:** Check internet connection and retry

**Exit Codes:**
- `0` - Success
- `1` - Retryable error (e.g., no seats available)
- `2` - Fatal error (e.g., authentication failed, invalid input)

## ⚠️ Rate Limiting and Account Protection

To protect your SRT account from being blocked by the server:

- **Automatic delays** between requests:
  - Minimum 3 seconds between reservation attempts
  - Minimum 5 seconds between search requests
- **Maximum 10 retry attempts** per session
- **Exponential backoff** after failures (3s → 5s → 10s → 15s → 20s → 30s)

**What this means for users:**
- The skill will automatically wait between requests
- You'll see waiting messages like "⏳ SRT 서버 보호를 위해 대기 중 (3초)"
- If you hit the retry limit, wait a few minutes before trying again

**For AI orchestration:**
- The AI should inform users about delays during retries
- Example: "재시도 중입니다. 서버 보호를 위해 3초 대기합니다..."
- After 10 failed attempts, suggest alternatives like different times or dates

## Natural Language Handling

When users make requests in Korean, the AI should:

1. **Extract parameters** from natural language:
   - Stations (must convert to Korean if given in English)
   - Date (relative dates like "내일", "다음주 금요일" → YYYYMMDD)
   - Time (relative times like "오후 2시", "12시 이후" → HHMMSS)
   - Passenger count (default to 1 if not specified)

2. **Call tools in correct sequence:**
   - Search before reserving
   - List before canceling
   - Handle retry logic with rate limiting

3. **Handle errors gracefully:**
   - If no seats available, try next train (with delays)
   - If station not found, suggest correct Korean name
   - Inform user about waiting times during rate limiting

4. **Confirm actions in Korean:**
   - "예약이 완료되었습니다" (Reservation completed)
   - "3초 후 다음 열차를 시도합니다" (Trying next train in 3 seconds)
   - "결제는 SRT 앱에서 완료해주세요" (Complete payment in SRT app)

## Real-World Usage Scenarios

### Scenario 1: Simple Reservation
**User:** "2월 17일에 수서에서 동대구 가는거 12시이후 제일 빠른걸로 2장 예약해줘"

**AI Actions:**
1. Parse: departure=수서, arrival=동대구, date=20260217, time=120000, passengers=adult:2
2. Search trains
3. Select first available train
4. Reserve train
5. Confirm with payment reminder

### Scenario 2: Retry Until Success
**User:** "매진이면 성공할때까지 반복해"

**AI Actions:**
1. Search trains
2. Loop through available trains:
   - Try to reserve
   - If sold out, wait 3-5 seconds (rate limiting)
   - Try next train
   - Max 10 attempts
3. Report success or exhaustion

### Scenario 3: Check and Cancel
**User:** "내 예약 확인해주고 제일 빠른거 취소해줘"

**AI Actions:**
1. List reservations
2. Parse JSON, find earliest by date/time
3. Cancel reservation
4. Confirm cancellation

### Scenario 4: Modify Booking
**User:** "부산 예약 취소하고 동대구로 다시 예약해줘"

**AI Actions:**
1. List reservations
2. Find Busan reservation
3. Cancel Busan reservation
4. Search for trains to 동대구 (same date/time)
5. Reserve new train
6. Confirm both actions

## Payment Notes

**IMPORTANT:** This skill can search and reserve trains, but **cannot process payments**.

After making a reservation:
1. You'll receive a reservation number
2. Payment must be completed via:
   - SRT mobile app (iOS/Android)
   - SRT website (https://etk.srail.kr)
3. Check payment deadline (usually 20 minutes after reservation)
4. Unpaid reservations will be automatically cancelled

## Troubleshooting

### "SRT 인증 정보를 찾을 수 없습니다"
- Verify `SRT_PHONE` and `SRT_PASSWORD` environment variables are set
- Check your shell profile (`~/.zshrc`, `~/.bashrc`) has `export` keyword
- Example: `export SRT_PHONE="010-1234-5678"`

### "검색 결과를 찾을 수 없습니다"
- Run `search` command before `reserve`
- Search results are cached in `~/.openclaw/tmp/srt/last_search.pkl`

### "재시도 한도 초과"
- You've made 10 reservation attempts
- Wait 5-10 minutes before trying again
- Try different trains or times

### Login failures
- Verify credentials are correct
- Check if SRT service is available
- Ensure phone number format includes hyphens (010-1234-5678)

## Development

### Testing Locally

```bash
# Install dependencies
# Install uv if not already installed
# https://docs.astral.sh/uv/getting-started/installation/

# Configure credentials
export SRT_PHONE="010-1234-5678"
export SRT_PASSWORD="your_password"

# Test commands
uv run --with SRTrain python3 scripts/srt_cli.py search --departure "수서" --arrival "부산" --date "20260203" --time "140000"
uv run --with SRTrain python3 scripts/srt_cli.py list
```

### Publishing to ClawHub

```bash
# Authenticate
clawhub login

# Publish
clawhub publish . \
  --slug srt \
  --name "SRT Korean Train Service" \
  --version 0.1.2 \
  --tags latest
```

## License

MIT

## Support

For issues or questions:
- File an issue on GitHub
- Check SRT service status: https://etk.srail.kr

## Version History

- **0.1.2** - Add `--all` flag for sold-out trains
  - Search now supports `--all` to include sold-out trains (passes `available_only=False`)
- **0.1.1** - Use `uv` for dependency management
  - Replace venv/pip with `uv run --with SRTrain`
  - Environment variables only for credentials (remove config file support)
- **0.1.0** - Initial release
  - Search trains
  - Make reservations
  - View bookings
  - Cancel bookings
  - Rate limiting protection
  - AI-friendly JSON output
