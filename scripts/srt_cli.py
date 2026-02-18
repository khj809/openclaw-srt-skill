#!/usr/bin/env python3
"""
Main CLI router for SRT skill.
Routes commands to appropriate tool modules.
"""

import os
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="SRT (Korean Train Service) CLI",
        epilog="예시:\n"
               "  검색: python3 scripts/srt_cli.py search --departure 수서 --arrival 부산 --date 20260217 --time 140000\n"
               "  예약 (단일): python3 scripts/srt_cli.py reserve --train-id 1\n"
               "  예약 (재시도): python3 scripts/srt_cli.py reserve --retry --timeout-minutes 60\n"
               "  로그 확인: python3 scripts/srt_cli.py log -n 30\n"
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

    # Reserve command
    reserve_parser = subparsers.add_parser('reserve', help='열차 예약')
    reserve_parser.add_argument('--train-id', 
                                help='열차 번호 (검색 결과의 순번, 쉼표로 복수 지정 가능, 생략 시 모든 열차 시도)')
    reserve_parser.add_argument('--retry', action='store_true',
                                help='실패 시 자동 재시도 (백그라운드 실행 권장)')
    reserve_parser.add_argument('--timeout-minutes', type=int, default=60,
                                help='최대 시도 시간 (분, 기본값: 60)')
    reserve_parser.add_argument('--wait-seconds', type=int, default=10,
                                help='재시도 대기 시간 (초, 기본값: 10)')

    # List command
    list_parser = subparsers.add_parser('list', help='예약 목록 조회')
    list_parser.add_argument('--format', choices=['table', 'json'], default='table',
                             help='출력 형식')

    # Cancel command
    cancel_parser = subparsers.add_parser('cancel', help='예약 취소')
    cancel_parser.add_argument('--reservation-id', required=True, help='예약번호')
    cancel_parser.add_argument('--confirm', action='store_true', help='확인 없이 바로 취소')

    # Check retry log command
    log_parser = subparsers.add_parser('log', help='예약 재시도 로그 확인')
    log_parser.add_argument('--lines', '-n', type=int, default=20,
                            help='표시할 라인 수 (기본값: 20)')

    # Stop retry process command (safe alternative to shell kill $(cat pid_file))
    stop_parser = subparsers.add_parser('stop', help='백그라운드 예약 재시도 프로세스 종료')
    stop_parser.add_argument('--pid-file', required=True,
                             help='PID 파일 경로 (make_reservation.py --retry 실행 시 저장한 파일)')

    # Status check command (safe alternative to kill -0 $(cat pid_file))
    status_parser = subparsers.add_parser('status', help='백그라운드 예약 재시도 프로세스 상태 확인')
    status_parser.add_argument('--pid-file', required=True,
                               help='PID 파일 경로')

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

        elif args.command == 'status':
            import signal
            from utils import validate_safe_path
            pid_file = validate_safe_path(Path(args.pid_file))
            if not pid_file.exists():
                print("NOT_RUNNING (PID 파일 없음)")
                sys.exit(0)
            raw = pid_file.read_text().strip()
            if not raw.isdigit():
                print(f"ERROR: PID 파일 내용이 유효하지 않습니다: {raw!r}")
                sys.exit(1)
            pid = int(raw)
            try:
                os.kill(pid, 0)  # signal 0 = existence check only, no kill
                print(f"RUNNING ({pid})")
            except ProcessLookupError:
                print(f"NOT_RUNNING (PID {pid} 종료됨)")
            except PermissionError:
                print(f"RUNNING ({pid}, 권한 없음으로 신호 전송 불가)")

        elif args.command == 'stop':
            import signal
            from utils import validate_safe_path
            pid_file = validate_safe_path(Path(args.pid_file))
            if not pid_file.exists():
                print(f"❌ PID 파일이 없습니다: {pid_file}")
                sys.exit(1)
            raw = pid_file.read_text().strip()
            if not raw.isdigit():
                print(f"❌ PID 파일 내용이 유효하지 않습니다: {raw!r}")
                sys.exit(1)
            pid = int(raw)
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"✅ 프로세스 {pid} 종료 요청 완료")
            except ProcessLookupError:
                print(f"⚠️  프로세스 {pid}는 이미 종료되어 있습니다")
            except PermissionError:
                print(f"❌ 프로세스 {pid} 종료 권한 없음")
                sys.exit(1)

        elif args.command == 'log':
            from check_retry_log import tail_log
            from utils import get_data_dir
            log_dir = get_data_dir()
            candidates = sorted(log_dir.glob('reserve_*.log'), key=lambda p: p.stat().st_mtime, reverse=True)
            if not candidates:
                print(f"❌ 로그 파일이 없습니다. ({log_dir}/reserve_*.log)")
                sys.exit(1)
            log_file = candidates[0]
            print(f"📄 로그 파일: {log_file}")
            tail_log(log_file, args.lines)

    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
