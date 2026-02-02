#!/usr/bin/env python3
"""
Make reservation tool for SRT skill.
Reserves a specific train from search results.
"""

import sys
import argparse
from utils import (
    load_credentials,
    handle_error,
    output_json,
    format_reservation_info,
    load_search_results,
    RateLimiter,
    wait_with_message,
    check_attempt_limit
)


def make_reservation(credentials, args):
    """
    Make a reservation for a specific train.

    Args:
        credentials: dict with phone and password
        args: argparse namespace with reservation parameters

    Returns:
        Reservation object
    """
    from SRT import SRT

    # Load search results
    trains = load_search_results()
    if not trains:
        raise Exception(
            "검색 결과를 찾을 수 없습니다. 먼저 'search' 명령으로 열차를 검색해주세요."
        )

    # Get train by ID (1-based index)
    try:
        train_idx = int(args.train_id) - 1
        if train_idx < 0 or train_idx >= len(trains):
            raise ValueError
        train = trains[train_idx]
    except (ValueError, IndexError):
        raise Exception(
            f"잘못된 열차 번호입니다. 1부터 {len(trains)} 사이의 번호를 입력해주세요."
        )

    # Rate limiting
    limiter = RateLimiter()
    attempts = check_attempt_limit(limiter, max_attempts=10)
    can_reserve, wait_time = limiter.check_reserve_rate()

    if not can_reserve:
        wait_with_message(wait_time, "예약 요청 대기 중")

    # Calculate backoff for retries
    if attempts > 0:
        backoff = limiter.calculate_backoff(attempts)
        wait_with_message(backoff, f"재시도 {attempts+1}회째 - 서버 보호 대기")

    # Login and reserve
    print(f"🎫 예약 진행 중... (열차 {train.train_number})")
    srt = SRT(credentials['phone'], credentials['password'])

    reservation = srt.reserve(train)

    # Record reservation attempt
    limiter.record_reserve()

    return reservation


def _display_result(reservation):
    """Display reservation result."""
    print("\n✅ 예약이 완료되었습니다!\n")
    print("📋 예약 정보:")
    print(f"  예약번호: {getattr(reservation, 'reservation_number', 'N/A')}")
    print(f"  열차번호: {getattr(reservation, 'train_number', 'N/A')}")
    print(f"  출발: {getattr(reservation, 'dep_station_name', 'N/A')} {getattr(reservation, 'dep_time', 'N/A')}")
    print(f"  도착: {getattr(reservation, 'arr_station_name', 'N/A')} {getattr(reservation, 'arr_time', 'N/A')}")
    print(f"  좌석: {getattr(reservation, 'seat_number', 'N/A')}")
    print("\n⚠️  중요: 결제는 SRT 앱 또는 웹사이트에서 직접 완료해주세요!")
    print("   결제 기한을 확인하세요.")

    info = format_reservation_info(reservation)
    info['success'] = True
    info['payment_required'] = True
    output_json(info, success=True)


def run(args):
    """Run reservation with pre-parsed args from srt_cli.py."""
    try:
        credentials = load_credentials()
        reservation = make_reservation(credentials, args)
        _display_result(reservation)
        sys.exit(0)
    except Exception as e:
        error_info = handle_error(e, context="reserve")
        output_json(error_info, success=False)
        if "NoSeatsAvailable" in error_info.get("error", ""):
            sys.exit(1)
        else:
            sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="SRT 열차 예약")
    parser.add_argument('--train-id', required=True, help="열차 번호 (검색 결과의 순번)")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
