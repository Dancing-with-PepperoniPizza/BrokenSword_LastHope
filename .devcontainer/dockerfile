# 🐍 Python 3.12 (Debian 기반) 이미지 사용
FROM python:3.12-bullseye

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치 (터미널 입출력 관련)
RUN pip install --no-cache-dir pynput

# 컨테이너 실행 시 main.py 실행
CMD ["python", "main.py"]