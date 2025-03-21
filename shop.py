import sys
import time
from data import WEAPON_SHOP, ITEM_SHOP

class Shop:
    def __init__(self, player_gold):
        self.player_gold = player_gold
        self.current_weapon = 0  # 현재 무기 강화 단계
        self.inventory = []

    def shop_main_menu(self):
        """상점 메인 메뉴"""
        while True:
            print("\n=== 🛒 무기 상점 ===")
            print(f"💰 현재 골드: {self.player_gold}G\n")
            print("🛠️  1. 무기 강화권")
            print("🎁 2. 추가 아이템")
            print("❌ 0. 종료")

            choice = input("\n번호를 입력하세요: ").strip()
            if choice == "0":
                print("❌ 상점에서 나갑니다.\n")
                break
            elif choice == "1":
                self.shop_weapon_menu()
            elif choice == "2":
                self.shop_item_menu()
            else:
                print("⚠️ 잘못된 입력입니다.")
                time.sleep(1)

    def shop_weapon_menu(self):
        """무기 강화권 메뉴"""
        while True:
            print("\n🛠️ 무기 강화권")
            for i, w in enumerate(WEAPON_SHOP, start=1):
                print(f"  {i}. {w['name']} - {w['price']}G")
            print("  0. 뒤로가기")

            choice = input("\n무기 번호를 입력하세요: ").strip()
            if choice == "0":
                print("🔙 무기 메뉴에서 나갑니다.\n")
                break

            if not choice.isdigit():
                print("⚠️ 숫자를 입력하세요.")
                time.sleep(1)
                continue

            idx = int(choice)
            if 1 <= idx <= len(WEAPON_SHOP):
                item = WEAPON_SHOP[idx - 1]
                self.buy_weapon_item(item)
            else:
                print("⚠️ 잘못된 번호입니다.")
                time.sleep(1)

    def shop_item_menu(self):
        """추가 아이템 메뉴"""
        while True:
            print("\n🎁 추가 아이템")
            for i, it in enumerate(ITEM_SHOP, start=1):
                print(f"  {i}. {it['name']} - {it['price']}G")
            print("  0. 뒤로가기")

            choice = input("\n아이템 번호를 입력하세요: ").strip()
            if choice == "0":
                print("🔙 아이템 메뉴에서 나갑니다.\n")
                break

            if not choice.isdigit():
                print("⚠️ 숫자를 입력하세요.")
                time.sleep(1)
                continue

            idx = int(choice)
            if 1 <= idx <= len(ITEM_SHOP):
                item = ITEM_SHOP[idx - 1]
                self.buy_item(item)
            else:
                print("⚠️ 잘못된 번호입니다.")
                time.sleep(1)

    def buy_weapon_item(self, wdata):
        """무기 강화권 구매 처리"""
        cost = wdata["price"]
        if self.player_gold < cost:
            print("❌ 골드가 부족합니다! 보스를 처치하여 골드를 획득하세요!")
            return

        self.player_gold -= cost
        new_level = wdata.get("level", 0)
        self.current_weapon = max(self.current_weapon, new_level)
        print(f"✅ {wdata['name']}를 구매했습니다! (현재 무기 {self.current_weapon}강)")
        time.sleep(1)

    def buy_item(self, idata):
        """추가 아이템 구매 처리"""
        cost = idata["price"]
        if self.player_gold < cost:
            print("❌ 골드가 부족합니다! 보스를 처치하여 골드를 획득하세요!")
            return

        self.player_gold -= cost
        self.inventory.append(idata.get("itemKey", "unknown"))
        print(f"✅ {idata['name']}을(를) 구매했습니다! (인벤토리에 추가됨)")
        time.sleep(1)

    def buy_weapon(self):
        """
        기존 코드 호환:
        상점 메인 메뉴로 진입
        """
        self.shop_main_menu()

if __name__ == "__main__":
    # 테스트
    from data import WEAPON_SHOP, ITEM_SHOP

    player_gold = 0
    shop = Shop(player_gold)
    shop.buy_weapon()
    print(f"🏆 최종 무기 강화 단계: {shop.current_weapon}강, 남은 골드: {shop.player_gold}G")
    print("인벤토리:", shop.inventory)