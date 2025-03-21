# 10강을 찍으려다 검이 부서져 세계를 구하지 못할 위기에 처했지만 포기하지 않고 다시 대장간으로 갔습니다

![Project Banner](https://raw.githubusercontent.com/Dancing-with-PepperoniPizza/BrokenSword_LastHope/main/images/main_banner.png)

## 프로젝트 개요
**"10강을 찍으려다 검이 부서져 세계를 구하지 못할 위기에 처했지만 포기하지 않고 다시 대장간으로 갔습니다"**는  
무기를 **강화**하고, **보스를 처치**하며, 궁극적으로 세계를 구하는 것을 목표로 한 **텍스트 기반 RPG 게임**입니다.

플레이어는 **강화 실패**와 **재도전**을 통해 게임의 핵심 메시지인 **"포기하지 않는 도전"**을 체험할 수 있습니다.

---

## 주요 기능

### 1. 🔨 강화 시스템 (`enh.py`)
![Enhancement System](https://raw.githubusercontent.com/Dancing-with-PepperoniPizza/BrokenSword_LastHope/main/images/enhsys_main.png)

- 최대 10강까지 무기를 강화 가능  
- **인디케이터(게이지)**를 실시간으로 움직이며, 엔터(Enter)로 정지  
- **강화 실패 시** 단계 하락 또는 무기 파괴 확률

---

### 2. 🐉 보스 전투 (`boss.py`)
![Boss Battle](https://raw.githubusercontent.com/Dancing-with-PepperoniPizza/BrokenSword_LastHope/main/images/boss_main.png)

- **보스 선택**: 보스별 `HP`, `페이즈(1~3)`가 존재  
- **페이즈**에 따라 입력해야 할 키(`Q, W, E, R, A, S, D, F`) 개수가 달라짐  
- 제한 시간 내 키 입력 성공 → 보스에게 데미지  
- **보스 처치 시** 골드 획득 (보스마다 `gold_min ~ gold_max`)

---

### 3. 🛒 상점 (`Shop.py`)
![Shop System](https://raw.githubusercontent.com/Dancing-with-PepperoniPizza/BrokenSword_LastHope/main/images/shop_main.png)

- **무기 강화권** 구매 (특정 강화 단계의 무기 즉시 획득)  
- **추가 아이템**(안전 스크롤, 성공 확률 부스트, 단계 보호권 등) 구매  
- 골드 부족 시 구매 불가

---

### 4. 📊 데이터 중앙화 (`data.py`)
- **보스 정보**(`BOSS_DATA`), **강화 확률**(`STARFORCE_TABLE`), **상점 목록**(무기·아이템) 등  
- 한 곳에서 모든 밸런스/수치 관리 가능

---

### 5. 📖 스토리텔링
- 강화 실패와 재도전을 중심으로 몰입감 있는 서사  
- **보스 레이드** 진행 → 골드 획득 → **강화 비용** 지불 → **강화 도전**  
- 최종 목표: 10강 달성 & 보스 제압

---

## 프로젝트 구조