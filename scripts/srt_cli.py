#!/usr/bin/env python3
"""
Main CLI router for SRT skill.
Routes commands to appropriate tool modules.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="SRT (Korean Train Service) CLI",
        epilog="예시:\n"
               "  검색: python3 scripts/srt_cli.py search --departure 수서 --arrival 부산 --date 20260217 --time 140000\n"
               "  예약: python3 scripts/srt_cli.py reserve --train-id 1\n"
               "  조회: python3 scripts/srt_cli.py list\n"
               "  취소: python3 scripts/srt_cli.py cancel --reservation-id RES123",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='사용 가능한 명령')

    # Search command
    search_parser = subparsers.add_parser('search', help='열차 검색')
    search_parser.add_argument('--departure', required=True, help='출발역 (한글)')
    search_parser.add_argument('--arrival', required=True, help='도착역 (한글)')
    search_parser.add_argument('--date', required=True, help='날짜 (YYYYMMDD)')
    search_parser.add_argument('--time', required=True, help='시간 (HHMMSS)')
    search_parser.add_argument('--passengers', help='승객 수 (예: adult=2)')
    search_parser.add_argument('--all', action='store_true', help='매진 포함 전체 열차 표시')

    # Reserve command
    reserve_parser = subparsers.add_parser('reserve', help='열차 예약')
    reserve_parser.add_argument('--train-id', required=True, help='열차 번호 (검색 결과의 순번)')

    # List command
    list_parser = subparsers.add_parser('list', help='예약 목록 조회')
    list_parser.add_argument('--format', choices=['table', 'json'], default='table',
                             help='출력 형식')

    # Cancel command
    cancel_parser = subparsers.add_parser('cancel', help='예약 취소')
    cancel_parser.add_argument('--reservation-id', required=True, help='예약번호')
    cancel_parser.add_argument('--confirm', action='store_true', help='확인 없이 바로 취소')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Route to appropriate tool with parsed args
        if args.command == 'search':
            from search_trains import run
            run(args)

        elif args.command == 'reserve':
            from make_reservation import run
            run(args)

        elif args.command == 'list':
            from view_bookings import run
            run(args)

        elif args.command == 'cancel':
            from cancel_booking import run
            run(args)

    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
