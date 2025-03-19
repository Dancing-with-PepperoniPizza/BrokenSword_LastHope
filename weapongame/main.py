import time
import random
import sys

try:
    import msvcrt

    def getch():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def weapon_enhancement(current_level):
    delay = max(0.05, 0.2 - current_level * 0.01)
    gauge_length = 30

    if current_level <= 3:
        success_zone_width = 4
    elif current_level <= 6:
        success_zone_width = 3
    else:
        success_zone_width = 2

    success_start = random.randint(0, gauge_length - success_zone_width)
    success_end = success_start + success_zone_width - 1

    print(f"\n현재 무기 강화 단계: {current_level}")
    print("게이지에 표시된 성공 구간에 스페이스바를 눌러 강화하세요!")

    gauge_visual = "".join(["=" if success_start <= i <= success_end else "-" for i in range(gauge_length)])
    print("성공 구간: [" + gauge_visual + "]")
    print("스페이스바를 눌러 멈추세요!")

    pos = 0
    direction = 1

    while True:
        gauge_line = "".join([">" if i == pos else " " for i in range(gauge_length)])
        sys.stdout.write("\r[" + gauge_line + "]")
        sys.stdout.flush()

        if 'msvcrt' in sys.modules:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
                if key == " ":
                    break
        else:
            import select
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if dr:
                key = sys.stdin.read(1)
                if key == " ":
                    break

        pos += direction
        if pos >= gauge_length - 1:
            direction = -1
            pos = gauge_length - 1
        elif pos <= 0:
            direction = 1
            pos = 0

        time.sleep(delay)

    print()
    print(f"게이지 멈춘 위치: {pos}")

    if success_start <= pos <= success_end:
        new_level = current_level + 1
        print("강화 성공!")
        if new_level in [5, 8, 10]:
            print(f"{new_level}강 보너스 옵션 획득!")
    else:
        if current_level > 0:
            if random.random() < 0.3:
                new_level = 0
                print("강화 실패! 무기가 초기화되었습니다.")
            else:
                new_level = current_level - 1
                print("강화 실패! 무기 강화 단계가 감소했습니다.")
        else:
            new_level = 0
            print("강화 실패! 무기 강화 단계 유지.")

    return new_level

def main():
    current_level = 0
    while True:
        input("\n엔터를 눌러 무기 강화를 시작하세요...")
        current_level = weapon_enhancement(current_level)
        print(f"현재 무기 강화 단계: {current_level}")
        if current_level >= 10:
            print("최종 강화 단계에 도달했습니다! 게임 클리어!")
            break

if __name__ == "__main__":
    main()
