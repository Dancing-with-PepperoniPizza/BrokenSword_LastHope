import sys
import time
import random
import select

# Windows용 비동기 입력 처리
try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False

# ★ data.py에서 강화 확률 및 비용 불러오기
from data import STARFORCE_TABLE, STARFORCE_COST

def get_key_nonblocking():
    """Windows/macOS/Linux 비동기 입력 처리"""
    if WINDOWS:
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        else:
            return None
    else:
        import select
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        else:
            return None

def get_star_width(level: int) -> int:
    """강화 단계(level)에 따라 인디케이터 길이 결정"""
    if level >= 9:
        return 1
    elif level >= 7:
        return 2
    elif level >= 5:
        return 3
    else:
        return 4

def starforce_game(level: int) -> str:
    """
    인디케이터 맞추기:
    - 최대 3번 시도
    - 성공 시 'success', 3번 모두 실패 시 확률 테이블에 따라 'downgrade'/'destroy'/'fail'
    """
    gauge_length = 30
    star_width = get_star_width(level)
    success_width = star_width
    success_start = random.randint(0, gauge_length - success_width)

    data = STARFORCE_TABLE.get(level, {'success': 5, 'downgrade': 0, 'destroy': 0})
    success_rate = data['success']
    downgrade_rate = data['downgrade']
    destroy_rate = data['destroy']

    print(f"\n★ 스타포스 모드 (현재 {level}강) ★")
    print(f"성공 {success_rate}% | 하락 {downgrade_rate}% | 파괴 {destroy_rate}%")
    print(f"인디케이터 길이: {star_width}칸, 성공 구간: {success_width}칸")
    print("3번의 기회 안에 정확히 맞추면 성공!")
    print("(엔터로 정지)")

    star_pos = 0
    direction = 1

    for attempt in range(1, 4):
        print(f"\n시도 {attempt}/3\n")
        while True:
            gauge = ["-"] * gauge_length
            for i in range(success_start, success_start + success_width):
                gauge[i] = "S"
            for i in range(star_width):
                idx = star_pos + i
                if 0 <= idx < gauge_length:
                    gauge[idx] = "="

            gauge_str = "".join(gauge)
            sys.stdout.write(f"\r| {gauge_str} |")
            sys.stdout.flush()

            key = get_key_nonblocking()
            if key in ["\n", "\r"]:
                break

            star_pos += direction
            if star_pos <= 0:
                star_pos = 0
                direction = 1
            elif star_pos + star_width - 1 >= gauge_length - 1:
                star_pos = gauge_length - star_width
                direction = -1

            time.sleep(0.05)

        sys.stdout.write("\n")

        if star_pos == success_start:
            print(f">>> ★ 강화 성공! (시도 {attempt}/3) ★\n")
            return "success"
        else:
            print(f">>> 강화 실패! (시도 {attempt}/3)\n")
            time.sleep(1)

    print("★★★ 3번 모두 실패... 강화 실패! ★★★\n")

    degrade = downgrade_rate
    destroy = destroy_rate
    keep = 100 - degrade - destroy

    r = random.random() * 100
    if r < destroy:
        return "destroy"
    elif r < (destroy + degrade):
        return "downgrade"
    else:
        return "fail"

def starforce_attempt(level: int, gold: int) -> (int, int):
    """
    - 강화 시도 비용 표시 → 골드 부족 시 시도 불가
    - starforce_game 실행 후 결과 처리
    """
    cost = STARFORCE_COST.get(level, 10000)
    if gold < cost:
        print(f"골드가 부족합니다! (필요: {cost} / 보유: {gold})")
        return level, gold

    print(f"{cost}G가 소모됩니다. 강화 시도를 진행하시겠습니까?")
    confirm = input("(Y/N): ").lower()
    if confirm != 'y':
        print("강화 시도를 취소합니다.")
        return level, gold

    gold -= cost
    print(f"{cost}G를 지불하고 강화 시도를 진행합니다! (남은 골드: {gold})")

    result = starforce_game(level)
    if result == "success":
        level += 1
        print(f"강화 결과: {level}강 달성!")
    elif result == "downgrade":
        if level >= 1:
            print(f"🔽 단계 하락! {level}강 → {level - 1}강")
            level -= 1
        else:
            print("강화 실패... 현재 0강 유지.")
    elif result == "destroy":
        print("💥 무기가 파괴되었습니다! 초기화됩니다. 💥")
        level = 0
    else:
        print(f"강화 실패... 현재 {level}강 유지.")

    return level, gold

def main():
    level = 0
    gold = 0

    while True:
        cost = STARFORCE_COST.get(level, 10000)
        print(f"\n[현재] 무기 강화: {level}강 / 보유 골드: {gold}G")
        print(f"1. 강화 시도 ({cost}G가 소모됩니다.)")
        print("2. 골드 추가 (테스트용)")
        print("0. 종료")

        cmd = input("선택: ")
        if cmd == "1":
            level, gold = starforce_attempt(level, gold)
        elif cmd == "2":
            gold += 500
            print(f"골드를 500G 추가했습니다! (보유 골드: {gold}G)")
        elif cmd == "0":
            print("강화 시스템 종료!")
            break
        else:
            print("잘못된 입력입니다.")

        if level >= 10:
            print("🎉 축하합니다! 10강 달성! 🎉")
            break

if __name__ == "__main__":
    main()