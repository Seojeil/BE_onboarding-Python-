# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt를 컨테이너로 복사
COPY requirements.txt .

# 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Django 서버 실행 포트 설정
EXPOSE 8000

# 환경 변수에 따라 다른 커맨드 실행
CMD ["sh", "-c", "if [ '$DJANGO_ENV' = 'production' ]; then gunicorn myproject.wsgi:application --bind 0.0.0.0:8000; else python manage.py runserver 0.0.0.0:8000; fi"]
