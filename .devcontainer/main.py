import sys
import time
import random

# 즉시 키 입력 (Windows & Mac/Linux 겸용)
try:
    import msvcrt
    def getch():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

def get_star_width(level: int) -> int:
    """
    현재 강화 단계(level)에 따라 인디케이터 길이 결정
    9강 이상 → 1칸
    7강 이상 → 2칸
    5강 이상 → 3칸
    그 외    → 4칸
    """
    if level >= 9:
        return 1
    elif level >= 7:
        return 2
    elif level >= 5:
        return 3
    else:
        return 4

def starforce_game(level: int) -> bool:
    """
    - 최대 3번 시도
    - 인디케이터(==== 등)와 성공 구간(SSSS 등)이 "정확히" 겹치면 성공
    - 정지 키: 엔터(Enter)
    - 도중 한 번이라도 성공하면 즉시 True
    - 3번 모두 실패하면 False
    """

    gauge_length = 30
    star_width = get_star_width(level)  # 현재 강화 단계에 따른 인디케이터 길이
    success_width = star_width          # 성공 구간 길이 = 인디케이터 길이

    # 성공 구간 시작 위치 (0 ~ gauge_length - success_width 사이 무작위)
    success_start = random.randint(0, gauge_length - success_width)

    print(f"\n★ 스타포스 모드 (현재 {level}강) ★")
    print(f"인디케이터 길이: {star_width}칸, 성공 구간: {success_width}칸")
    print("3번의 기회 안에 정확히 맞추면 강화 성공!")
    print("(엔터로 정지, 정확히 일치해야 성공)")

    # 인디케이터(스타포스) 초기 위치
    star_pos = 0
    direction = 1  # 1: 오른쪽, -1: 왼쪽

    for attempt in range(1, 4):
        # 시도 안내
        print(f"\n시도 {attempt}/3 | 현재 강화 상태: {level}강 (Enter로 정지)\n")

        while True:
            # 게이지 배열: 성공 구간 S, 나머지 -
            gauge = ["-"] * gauge_length
            for i in range(success_start, success_start + success_width):
                gauge[i] = "S"

            # 인디케이터(==== 등) 배치
            for i in range(star_width):
                idx = star_pos + i
                if 0 <= idx < gauge_length:
                    gauge[idx] = "="

            # 한 줄에서 깜빡이도록 출력
            gauge_str = "".join(gauge)
            sys.stdout.write(f"\r| {gauge_str} |")
            sys.stdout.flush()

            # 키 입력 체크 (엔터를 만나면 break)
            if 'msvcrt' in sys.modules:
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    # Windows 환경에서 엔터는 b'\r'로 읽히는 경우가 많음
                    if key in [b'\r', b'\n']:
                        break
            else:
                import select
                dr, dw, de = select.select([sys.stdin], [], [], 0)
                if dr:
                    key = sys.stdin.read(1)
                    # Mac/Linux에서는 엔터가 '\n'
                    if key in ["\n", "\r"]:
                        break

            # 인디케이터 이동
            star_pos += direction
            # 범위 체크
            if star_pos <= 0:
                star_pos = 0
                direction = 1
            elif star_pos + star_width - 1 >= gauge_length - 1:
                star_pos = gauge_length - star_width
                direction = -1

            time.sleep(0.05)

        # 엔터 눌러 정지 후 줄바꿈
        sys.stdout.write("\n")

        # 성공 판정: 인디케이터 시작 == 성공 구간 시작
        if star_pos == success_start:
            print(f">>> ★ 강화 성공! (시도 {attempt}/3) ★\n")
            return True
        else:
            print(f">>> 강화 실패! (시도 {attempt}/3)\n")
            time.sleep(1)

        # 다음 시도를 위해 인디케이터 초기화
        star_pos = 0
        direction = 1

    # 3번 모두 실패
    print("★★★ 3번 모두 실패... 강화 실패! ★★★\n")
    return False

def main():
    current_level = 0
    while True:
        # 강화 시작: 엔터
        input("\n[엔터]를 눌러 스타포스를 시작하세요...")

        success = starforce_game(current_level)
        if success:
            current_level += 1
            print(f"강화 결과: {current_level}강 달성!\n")
        else:
            print(f"강화 실패... 현재 {current_level}강 유지.")

        # 10강 달성 시 종료 (예시)
        if current_level >= 10:
            print("축하합니다! 최종 강화 단계(10강)에 도달했습니다!")
            break

if __name__ == "__main__":
    main()
