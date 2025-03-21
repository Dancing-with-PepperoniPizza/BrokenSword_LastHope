import sys
import time
import random
import select

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False

# 데이터 참조 (보스 정보, etc.)
from data import BOSS_DATA, CRITICAL_HIT_CHANCE

BOSS_KEYS = ["Q", "W", "E", "R", "A", "S", "D", "F"]

class Player:
    def __init__(self, name="용사", hp=200, level=0):
        self.name = name
        self.hp = hp
        self.level = level
        self.gold = 0

    def get_attack_damage(self, boss_name):
        boss_info = BOSS_DATA[boss_name]
        min_dmg, max_dmg = boss_info["damage_range"]

        if self.level < boss_info["min_level"]:
            return 1
        
        damage = random.randint(min_dmg, max_dmg)
        if random.random() < CRITICAL_HIT_CHANCE:
            damage = int(damage * 1.5)
            print("💥 크리티컬 히트! 💥")
        return damage

class Boss:
    def __init__(self, name, max_hp, phase=1):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.phase = phase

    def update_phase(self):
        """잔여 체력 비율에 따라 페이즈 결정"""
        ratio = (self.hp / self.max_hp) * 100
        if ratio >= 60:
            self.phase = 1
        elif ratio >= 31:
            self.phase = 2
        else:
            self.phase = 3

def boss_attack_phase(boss: Boss, player: Player, base_time_limit=2.0):
    """
    보스가 보스.phase에 따라 1~3개의 키를 요구.
    올바른 키를 모두 입력하면 보스에게 데미지 부여,
    틀리거나 시간 초과 시 플레이어가 피해를 입음.
    """
    # 보스 페이즈에 따라 요구 키 개수 결정
    num_keys = boss.phase
    pattern = random.sample(BOSS_KEYS, num_keys)

    print(f"\n[보스 패턴] {pattern} → {base_time_limit}초 안에 입력!\n")
    start_time = time.time()

    for idx, required_key in enumerate(pattern, start=1):
        typed_char = None
        remain = base_time_limit - (time.time() - start_time)
        if remain <= 0:
            break

        print("[====================] 남은 시간: 0.00s")
        print(f"{idx}/{len(pattern)} 번째 키: ( {required_key} )")

        while True:
            remain = base_time_limit - (time.time() - start_time)
            if remain <= 0:
                break

            fraction = remain / base_time_limit
            bar_len = 20
            fill_len = int(fraction * bar_len)
            gauge_str = "[" + "=" * fill_len + "-" * (bar_len - fill_len) + "]"

            sys.stdout.write("\033[2F")
            sys.stdout.write(f"\r{gauge_str} 남은 시간: {remain:.2f}s\n")
            prompt_str = f"{idx}/{len(pattern)} 번째 키: ( {required_key} ) → {typed_char or ''}"
            sys.stdout.write(f"\r{prompt_str}\n")
            sys.stdout.flush()

            if WINDOWS:
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getch().decode("utf-8").upper()
                    if ch in ["\n", "\r"]:
                        continue
                    else:
                        typed_char = ch
                        break
            else:
                import select
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    ch = sys.stdin.read(1).upper()
                    if ch in ["\n", "\r"]:
                        continue
                    else:
                        typed_char = ch
                        break

        sys.stdout.write("\033[2F")
        if remain <= 0 or typed_char != required_key:
            print(f"\n★ 실패! {boss.name}의 공격!")
            dmg = random.randint(10, 30)
            player.hp -= dmg
            return

        print(f"\n★ {idx}번째 키 '{typed_char}' 성공!")

    # 모든 키 입력 성공 시 데미지 계산
    damage = player.get_attack_damage(boss.name)
    boss.hp -= damage
    boss.update_phase()  # 체력 감소 후 페이즈 갱신
    print(f"\n★★★ {boss.name}에게 {damage}의 피해를 주었다! (페이즈 {boss.phase}) ★★★")

def boss_raid(player: Player):
    """
    보스를 선택하고 전투.
    보스를 처치하면 gold_min~gold_max 골드 획득.
    """
    print("\n===== 던전 선택 =====")
    print(f"현재 강화 단계: {player.level}강 | 보유 골드: {player.gold}G\n")

    boss_names = list(BOSS_DATA.keys())
    for idx, bname in enumerate(boss_names, start=1):
        min_lv = BOSS_DATA[bname]["min_level"]
        recommended = "<<<" if player.level >= min_lv else ""
        print(f"{idx}. {bname} (적정 강화 {min_lv}강) {recommended}")
    print("0. 돌아가기")

    choice = input("도전할 보스를 선택하세요 (번호 입력): ")
    if not choice.isdigit():
        print("잘못된 입력입니다!")
        return
    choice = int(choice)
    if choice == 0 or choice > len(boss_names):
        print("메인 메뉴로 돌아갑니다.")
        return

    bname = boss_names[choice - 1]
    info = BOSS_DATA[bname]

    # max_hp, phase를 보스별로 설정 (예: offset)
    offset = choice - 1
    max_hp = 300 + offset * 100
    initial_phase = 1  # 시작은 1페이즈 (HP 감소 시 update_phase로 전환)

    current_boss = Boss(name=bname, max_hp=max_hp, phase=initial_phase)
    print(f"\n===== {bname} 레이드 시작! (HP: {max_hp}) =====")

    # 전투 루프
    while player.hp > 0 and current_boss.hp > 0:
        boss_attack_phase(current_boss, player, base_time_limit=2.0)
        print(f"\n[{player.name} HP: {player.hp} / {current_boss.name} HP: {current_boss.hp} (페이즈 {current_boss.phase})]")
        time.sleep(1)

    # 전투 결과
    if current_boss.hp <= 0:
        print(f"\n★ {bname}을(를) 물리쳤다! ★")
        earned = random.randint(info["gold_min"], info["gold_max"])
        player.gold += earned
        print(f"💰 {earned}G를 획득했습니다! (보유 골드: {player.gold}G)")
    else:
        print(f"\n★ {player.name}이(가) 쓰러졌다... ★")

def main():
    player = Player(name="용사", hp=200, level=0)
    boss_raid(player)

if __name__ == "__main__":
    main()