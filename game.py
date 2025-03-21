import random
import time

from boss import Player, boss_raid
from enh import starforce_game, STARFORCE_COST
from shop import Shop

class Game:
    def __init__(self):
        """게임 초기 설정"""
        # Player에 level=0
        self.player = Player(name="용사", hp=200, level=0)
        # 더 이상 self.weapon_level를 별도로 두지 않음
        self.gold = 0  # 굳이 분리 관리하지 않아도 되지만, 기존 코드를 살림

    def main_menu(self):
        while True:
            print("\n=== ⚔️ 게임 메뉴 ===")
            print("1️⃣ 보스 레이드 (골드 획득)")
            print("2️⃣ 무기 상점 (강화권 구매)")
            print("3️⃣ 무기 강화 (골드 사용)")
            print("4️⃣ 현재 상태 확인")
            print("0️⃣ 게임 종료")

            choice = input("\n💡 선택하세요: ")
            if choice == "1":
                self.do_boss_raid()
            elif choice == "2":
                self.weapon_shop()
            elif choice == "3":
                self.enhance_weapon()
            elif choice == "4":
                self.show_status()
            elif choice == "0":
                print("\n🎮 게임을 종료합니다!")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 다시 선택하세요.")

    def do_boss_raid(self):
        """
        보스 레이드 실행
        boss_raid(player) 호출 -> 보스 선택/전투 -> 골드 획득
        """
        print("\n⚔️ 보스 레이드를 시작합니다!")
        # boss.py의 boss_raid(player) 실행
        boss_raid(self.player)
        # 전투 결과로 player.gold가 변동될 수 있으므로, self.gold 동기화
        self.gold = self.player.gold

    def weapon_shop(self):
        """무기 상점 실행"""
        print("\n🛒 무기 상점에 입장합니다!")
        # 상점에 현재 보유 골드를 전달
        shop = Shop(self.gold)
        shop.buy_weapon()
        # 상점 사용 후 남은 골드
        self.gold = shop.player_gold
        # 상점에서 구매한 무기 단계와 비교 -> player.level 갱신
        self.player.level = max(self.player.level, shop.current_weapon)

    def enhance_weapon(self):
        """무기 강화 실행 (인디케이터)"""
        # player.level로 강화 비용 계산
        cost = STARFORCE_COST.get(self.player.level, 10000)
        print(f"\n🔧 현재 {self.player.level}강 → {self.player.level+1}강 시도")
        print(f"{cost}G가 소모됩니다. (보유 골드: {self.gold}G)")

        if self.gold < cost:
            print("❌ 골드가 부족하여 강화할 수 없습니다!")
            return

        confirm = input("강화 시도를 진행하시겠습니까? (Y/N): ").lower()
        if confirm != 'y':
            print("강화 시도를 취소합니다.")
            return

        self.gold -= cost
        print(f"{cost}G를 지불하고 강화 시도를 진행합니다! (남은 골드: {self.gold})")

        # 인디케이터 방식 강화
        result = starforce_game(self.player.level)
        if result == "success":
            self.player.level += 1
            print(f"✅ {self.player.level}강으로 강화 성공! (남은 골드: {self.gold}G)")
        elif result == "downgrade":
            if self.player.level >= 1:
                print(f"🔽 단계 하락! {self.player.level}강 → {self.player.level - 1}강")
                self.player.level -= 1
            else:
                print("0강 이하로 하락은 불가, 현재 0강 유지.")
        elif result == "destroy":
            print("💥 무기가 파괴되었습니다! 초기화됩니다. 💥")
            self.player.level = 0
        else:  # fail
            print(f"강화 실패... 현재 {self.player.level}강 유지.")

        # player.gold와 self.gold 동기화
        self.player.gold = self.gold

    def show_status(self):
        """플레이어 및 무기 상태 확인"""
        # player.gold와 self.gold 동기화
        self.player.gold = self.gold

        print("\n=== 📜 현재 상태 ===")
        print(f"💰 보유 골드: {self.gold}G")
        print(f"🗡️ 무기 강화 단계: {self.player.level}강")
        print(f"❤️ 플레이어 체력: {self.player.hp}HP")

if __name__ == "__main__":
    game = Game()
    game.main_menu()