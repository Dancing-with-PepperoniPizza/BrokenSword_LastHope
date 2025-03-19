import random
import time
from boss import Player, Boss, boss_raid
from enh import starforce_game
from shop import Shop  # 🔥 상점 추가

class Game:
    def __init__(self):
        """게임 초기 설정"""
        self.player = Player(name="용사", hp=200, attack=50)
        self.boss = Boss(name="어둠의 드래곤", hp=500, phase=1)
        self.gold = 0  # 초반 골드 없음
        self.weapon_level = 0  # 무기 초기 강화 단계 0강

    def main_menu(self):
        """게임 메인 메뉴"""
        while True:
            print("\n=== ⚔️ 게임 메뉴 ===")
            print("1️⃣ 보스 레이드 (골드 획득)")
            print("2️⃣ 무기 상점 (강화권 구매)")
            print("3️⃣ 무기 강화 (골드 사용)")
            print("4️⃣ 현재 상태 확인")
            print("0️⃣ 게임 종료")

            choice = input("\n💡 선택하세요: ")

            if choice == "1":
                self.boss_raid()
            elif choice == "2":
                self.weapon_shop()  # 🔥 상점 추가
            elif choice == "3":
                self.enhance_weapon()
            elif choice == "4":
                self.show_status()
            elif choice == "0":
                print("\n🎮 게임을 종료합니다!")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 다시 선택하세요.")

    def boss_raid(self):
        """보스 레이드 실행 → 골드 획득"""
        print("\n⚔️ 보스 레이드를 시작합니다!")
        boss_raid(self.player, self.boss)

        # 보스가 패배했을 경우, 랜덤 골드 지급 및 새로운 보스 생성
        if self.boss.hp <= 0:
            earned_gold = random.randint(100, 300)  # 🔥 골드 지급
            self.gold += earned_gold
            print(f"🏆 {earned_gold}G를 획득했습니다! (총 보유 골드: {self.gold}G)")
            self.boss = Boss(name="어둠의 드래곤", hp=500, phase=1)  # 새로운 보스 생성

    def weapon_shop(self):
        """무기 상점 실행"""
        print("\n🛒 무기 상점에 입장합니다!")
        shop = Shop(self.gold)  # 현재 보유 골드 반영
        shop.buy_weapon()
        self.gold = shop.player_gold  # 🔥 남은 골드 업데이트
        self.weapon_level = max(self.weapon_level, shop.current_weapon)  # 무기 강화 단계 반영

    def enhance_weapon(self):
        """무기 강화 실행 → 골드 사용"""
        cost = (self.weapon_level + 1) * 50  # 강화 비용 = (강화 단계 + 1) × 50G
        if self.gold >= cost:
            print(f"\n🔧 강화 비용: {cost}G (보유 골드: {self.gold}G)")
            success = starforce_game(self.weapon_level)
            if success:
                self.weapon_level += 1
                self.gold -= cost
                print(f"✅ {self.weapon_level}강으로 강화 성공! (남은 골드: {self.gold}G)")
            else:
                print(f"❌ 강화 실패... 현재 {self.weapon_level}강 유지.")
        else:
            print("❌ 골드가 부족하여 강화할 수 없습니다!")

    def show_status(self):
        """플레이어 및 무기 상태 확인"""
        print("\n=== 📜 현재 상태 ===")
        print(f"💰 보유 골드: {self.gold}G")
        print(f"🗡️ 무기 강화 단계: {self.weapon_level}강")
        print(f"❤️ 플레이어 체력: {self.player.hp}HP")
        print(f"🐉 {self.boss.name} 체력: {self.boss.hp}HP (페이즈 {self.boss.phase})")

if __name__ == "__main__":
    game = Game()
    game.main_menu()