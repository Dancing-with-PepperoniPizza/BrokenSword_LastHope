"""
data.py
게임 전체에서 사용하는 데이터/설정 값들을 모아둔 파일.
"""

import random

#########################
#   보스 관련 설정
#########################
BOSS_DATA = {
    "슬라임 군단": {
        "min_level": 0,
        "damage_range": (10, 20),
        "gold_min": 100,
        "gold_max": 200
    },
    "폭군 미노타우로스": {
        "min_level": 3,
        "damage_range": (20, 30),
        "gold_min": 200,
        "gold_max": 300
    },
    "어둠의 드래곤": {
        "min_level": 5,
        "damage_range": (30, 40),
        "gold_min": 300,
        "gold_max": 400
    },
    "공허의 파수꾼": {
        "min_level": 7,
        "damage_range": (40, 50),
        "gold_min": 400,
        "gold_max": 500
    }
}

CRITICAL_HIT_CHANCE = 0.01  # 1%

#########################
#   강화 관련 설정
#########################
STARFORCE_TABLE = {
    0: {'success': 100, 'downgrade': 0,   'destroy': 0},
    1: {'success': 100, 'downgrade': 0,   'destroy': 0},
    2: {'success': 100, 'downgrade': 0,   'destroy': 0},
    3: {'success': 90,  'downgrade': 10,  'destroy': 0},
    4: {'success': 85,  'downgrade': 15,  'destroy': 0},
    5: {'success': 60,  'downgrade': 35,  'destroy': 5},
    6: {'success': 55,  'downgrade': 37.5,'destroy': 7.5},
    7: {'success': 50,  'downgrade': 40,  'destroy': 10},
    8: {'success': 40,  'downgrade': 52.5,'destroy': 12.5},
    9: {'success': 30,  'downgrade': 55,  'destroy': 15},
}

STARFORCE_COST = {
    0: 0,     
    1: 100,
    2: 150,
    3: 200,
    4: 300,
    5: 500,
    6: 700,
    7: 1000,
    8: 2000,
    9: 5000,
    10: 10000
}

#########################
#   상점 관련 설정
#########################

# 무기 강화권 판매 목록
WEAPON_SHOP = [
    {"name": "3강 무기", "price": 350,  "level": 3},
    {"name": "5강 무기", "price": 875,  "level": 5},
    {"name": "7강 무기", "price": 1750, "level": 7}
]

# 추가 아이템 판매 목록
ITEM_SHOP = [
    {"name": "안전 스크롤",       "price": 1000, "itemKey": "safe_scroll"},
    {"name": "성공 확률 부스트",   "price": 1500, "itemKey": "success_boost"},
    {"name": "단계 보호권",       "price": 2000, "itemKey": "stage_protection"}
]