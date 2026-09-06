# backend/Dockerfile
# Стандарт INT-L3: Reproducible Builds
# Версия: 1.0
# Описание: Воспроизводимая сборка FastAPI backend для potok-app

FROM python:3.10-slim as builder

# Устанавливаем рабочую директорию
WORKDIR /build

# Копируем только requirements для кэширования зависимостей
COPY requirements.txt .

# Устанавливаем зависимости в виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Финальный образ (минимальный размер)
FROM python:3.10-slim

# Метаданные для аудита (OCI labels)
LABEL org.opencontainers.image.title="potok-app-backend"
LABEL org.opencontainers.image.description="Пилотный проект Kon-Matrix L3: дневник с квантовой памятью"
LABEL org.opencontainers.image.version="0.3.0"
LABEL org.opencontainers.image.created="2026-09-06"
LABEL org.opencontainers.image.authors="Pavel (AzemF)"
LABEL org.opencontainers.image.source="https://github.com/AzesmF/potok-app"

# Создаём непривилегированного пользователя (безопасность)
RUN useradd --create-home --shell /bin/bash appuser

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Рабочая директория
WORKDIR /home/appuser/app

# Копируем код приложения
COPY --chown=appuser:appuser app ./app

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Health check (стандарт EVO-L3)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
