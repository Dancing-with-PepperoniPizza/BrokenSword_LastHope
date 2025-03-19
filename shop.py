import sys
import time

class Shop:
    def __init__(self, player_gold):
        self.player_gold = player_gold
        self.weapon_levels = {3: 100, 5: 300, 7: 700}  # 강화 단계: 가격(골드)
        self.current_weapon = 0  # 현재 무기 강화 단계

    def display_shop(self):
        """상점 UI 출력"""
        print("\n=== 🛒 무기 상점 ===")
        print(f"💰 현재 골드: {self.player_gold}G")
        print("\n🛠️ 구매 가능한 무기:")
        for level, price in self.weapon_levels.items():
            print(f"  🔹 {level}강 무기 - {price}G (구매하려면 {level} 입력)")
        print("  ❌ 0. 종료 (상점 나가기)")

    def buy_weapon(self):
        """무기 구매 기능"""
        while True:
            self.display_shop()
            choice = input("\n🛍️ 구매할 무기의 강화 단계를 입력하세요 (0: 종료): ")
            
            if choice == "0":
                print("❌ 상점에서 나갑니다.\n")
                break
            
            try:
                choice = int(choice)
                if choice in self.weapon_levels:
                    if self.player_gold >= self.weapon_levels[choice]:
                        self.player_gold -= self.weapon_levels[choice]
                        self.current_weapon = choice
                        print(f"✅ {choice}강 무기를 구매했습니다! (현재 무기 강화 단계: {self.current_weapon}강)")
                    else:
                        print("❌ 골드가 부족합니다! 보스를 처치하여 골드를 획득하세요!")
                else:
                    print("⚠️ 잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("⚠️ 숫자를 입력하세요.")

            time.sleep(1)

if __name__ == "__main__":
    player_gold = 0  # 시작 골드 없음
    shop = Shop(player_gold)
    shop.buy_weapon()
    print(f"🏆 최종 무기 강화 단계: {shop.current_weapon}강, 남은 골드: {shop.player_gold}G")