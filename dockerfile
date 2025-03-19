# 1. 베이스 이미지 선택
FROM python:3.12-bullseye

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 스크립트 복사 (enh.py, boss.py 등)
COPY enh.py ./
COPY boss.py ./

# 4. CMD/ENTRYPOINT 생략 or 쉘만 실행
# 아무것도 자동 실행하지 않으려면 아래 줄을 아예 적지 않거나, 최소한으로:
# CMD ["/bin/bash"]
# 또는 아무것도 넣지 않아도 됨