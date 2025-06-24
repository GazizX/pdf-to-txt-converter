FROM python:3.9-slim
WORKDIR /app

# Установка grpcio и других зависимостей
COPY backend/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы (включая сгенерированные *_pb2.py)
COPY backend/python/ .
RUN touch proto/__init__.py

ENV PYTHONPATH="${PYTHONPATH}:/app"
EXPOSE 50051
CMD ["python", "main.py"]