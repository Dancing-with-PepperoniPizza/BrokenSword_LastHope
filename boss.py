import sys
import time
import random
import select

BOSS_KEYS = ["Q", "W", "E", "R", "A", "S", "D", "F"]

class Player:
    def __init__(self, name="용사", hp=200, attack=50):
        self.name = name
        self.hp = hp
        self.attack = attack

class Boss:
    def __init__(self, name="어둠의 드래곤", hp=500, phase=1):
        self.name = name
        self.hp = hp
        self.phase = phase

def boss_attack_phase_singlechar(boss, player, base_time_limit=2.0):
    """
    보스가 1~3개의 키를 요구하되, 연속해서 같은 키는 나오지 않는다.
    플레이어는 각 키를 '한 번에 한 글자'씩 제한 시간 내에 입력해야 함.
    - 시간 초과 or 오타 시 즉시 실패
    - 모든 키를 순서대로 맞추면 성공
    - 게이지 형태로 남은 시간 표시
    """

    # (1) 패턴 생성 (1~3글자), 연속 문자 금지
    num_keys = random.randint(1, 3)
    pattern = []
    for _ in range(num_keys):
        c = random.choice(BOSS_KEYS)
        while pattern and c == pattern[-1]:
            c = random.choice(BOSS_KEYS)
        pattern.append(c)

    print(f"\n[보스 패턴] {pattern} → 각 글자를 {base_time_limit}초 안에 순서대로 입력하세요!\n")

    # 패턴을 순서대로 검사
    for idx, required_key in enumerate(pattern, start=1):
        # 개별 키 입력 제한 시간
        start_time = time.time()
        typed_char = None

        # 화면 준비: 게이지 줄, 입력 안내 줄
        print("[====================] 남은 시간: 0.00s")
        print(f"{idx}/{len(pattern)} 번째 키 입력: ( {required_key} )")

        while True:
            remain = base_time_limit - (time.time() - start_time)
            if remain <= 0:
                # 시간 초과
                break

            # 게이지 표시
            fraction = remain / base_time_limit
            bar_len = 20
            fill_len = int(fraction * bar_len)
            gauge_str = "[" + "=" * fill_len + "-" * (bar_len - fill_len) + "]"

            # 2줄 위로 이동
            sys.stdout.write("\033[2F")
            # 게이지 갱신
            sys.stdout.write(f"\r{gauge_str} 남은 시간: {remain:.2f}s\n")
            # 입력 안내 줄
            prompt_str = f"{idx}/{len(pattern)} 번째 키 입력: ( {required_key} ) → 현재 입력: {typed_char or ''}"
            sys.stdout.write(f"\r{prompt_str}\n")
            sys.stdout.flush()

            # 논블로킹 입력 (한 글자씩)
            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if r:
                ch = sys.stdin.read(1)
                if ch in ["\n", "\r"]:
                    # 엔터는 무시 (다음 키 입력)
                    continue
                else:
                    # 입력한 문자를 대문자로 변환
                    typed_char = ch.upper()
                    break

        # 화면 정리 (마지막 출력)
        sys.stdout.write("\033[2F")
        remain = max(remain, 0)
        gauge_str = "[" + "=" * fill_len + "-" * (bar_len - fill_len) + "]"
        sys.stdout.write(f"\r{gauge_str} 남은 시간: {remain:.2f}s\n")
        final_str = f"{idx}/{len(pattern)} 번째 키 입력: ( {required_key} ) → 현재 입력: {typed_char or ''}"
        sys.stdout.write(f"\r{final_str}\n")
        sys.stdout.flush()

        if remain <= 0:
            # 시간 초과 → 실패
            print("\n★ 시간 초과! 입력 실패!")
            dmg = random.randint(10, 30)
            player.hp -= dmg
            print(f"{boss.name}의 공격! {player.name}가 {dmg}의 피해를 입었다!")
            return  # 페이즈 종료

        # 입력 문자가 없는 경우 (예: 엔터만 누름)
        if not typed_char:
            # 오타로 처리
            dmg = random.randint(10, 30)
            player.hp -= dmg
            print(f"\n★ 입력이 없었습니다! {boss.name}의 공격! {player.name}가 {dmg}의 피해를 입었다!")
            return

        # 틀린 문자인 경우
        if typed_char != required_key:
            dmg = random.randint(10, 30)
            player.hp -= dmg
            print(f"\n★ 오타! {boss.name}의 공격! {player.name}가 {dmg}의 피해를 입었다!")
            return

        # 여기까지 오면 해당 키는 성공
        print(f"\n★ {idx}번째 키 '{typed_char}' 성공!")

    # 모든 키를 맞췄다면 전체 성공
    dmg = player.attack
    boss.hp -= dmg
    print(f"\n★★★ 패턴 {pattern} 완벽 성공! {boss.name}에게 {dmg}의 피해를 주었다! ★★★")

def boss_phase_check(boss: Boss):
    """ 보스 체력에 따른 페이즈 전환 (예시) """
    if boss.hp <= 300 and boss.phase == 1:
        boss.phase = 2
        print(f"\n{boss.name}이(가) 분노했다! [페이즈 2 진입]")
    if boss.hp <= 100 and boss.phase == 2:
        boss.phase = 3
        print(f"\n{boss.name}이(가) 최후의 발악을 시작했다! [페이즈 3 진입]")

def boss_raid(player: Player, boss: Boss):
    """
    플레이어와 보스가 체력이 0 이하가 될 때까지 전투.
    매 턴 boss_attack_phase_singlechar 호출 → 성공/실패로 체력 변동.
    보스 체력 따라 페이즈 전환.
    """
    print(f"\n===== {boss.name} 레이드 시작! =====")
    print(f"{player.name} HP: {player.hp}, {boss.name} HP: {boss.hp}")

    while player.hp > 0 and boss.hp > 0:
        # 한 글자씩 입력하는 보스 페이즈
        boss_attack_phase_singlechar(boss, player, base_time_limit=2.0)

        # 페이즈 체크
        boss_phase_check(boss)

        # 상태 출력
        print(f"\n[{player.name} HP: {player.hp} / {boss.name} HP: {boss.hp}]")
        time.sleep(1)

    # 승패 결정
    if boss.hp <= 0 and player.hp > 0:
        print(f"\n★ {boss.name}을(를) 물리쳤다! ★")
    elif player.hp <= 0 and boss.hp > 0:
        print(f"\n★ {player.name}이(가) 쓰러졌다... ★")
    else:
        print("\n★ 양쪽 모두 쓰러졌다... ★")

def main():
    # 플레이어와 보스 생성
    player = Player(name="용사", hp=200, attack=50)
    boss = Boss(name="어둠의 드래곤", hp=500, phase=1)

    # 레이드 시작
    boss_raid(player, boss)

if __name__ == "__main__":
    main()