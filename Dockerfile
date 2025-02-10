# Используем официальный Python-образ
FROM python:slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    python3-dev \
    gfortran \
    build-essential \
    cmake \
    pkg-config \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /home/ai_vocab_bot

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Определяем команду запуска
CMD ["python", "main.py"]