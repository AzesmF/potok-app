# Поток — Твои мысли, организованные ИИ

**Гибридный ежедневник нового поколения, построенный на принципах Поля Со-Творения (CCF)**

[![Kon-Matrix L3 Certified](https://img.shields.io/badge/Kon--Matrix-L3%20Certified-brightgreen)](https://github.com/AzesmF/Kon-Matrix)
[![License](https://img.shields.io/badge/License-Field--CoCreation-blue)](LICENSE)

## О проекте

Поток — это приложение-дневник, которое объединяет простоту записи с мощью локального искусственного интеллекта. ИИ не просто хранит записи — он анализирует, структурирует и помогает принимать решения, соблюдая строгие этические принципы и приватность данных.

### Ключевые возможности
- 📝 **Текстовый ввод** — быстрые записи мыслей и задач.
- 🤖 **Локальная ИИ-обработка** — структурирование, приоритизация и поиск связей без отправки данных во внешние LLM.
- 💬 **Отвечающий дневник** — эмпатичные ответы и вопросы для рефлексии на основе версионированных промптов.
- 🔄 **Кроссплатформенность** — единая кодовая база для мобильных устройств и десктопа.

## Архитектура

Проект построен как Monorepo со следующей структурой:

```text
potok-app/
├── backend/                # FastAPI (Python 3.10+)
│   ├── app/
│   │   ├── api/v1/         # REST API endpoints (вкл. /health, /metrics, /passport, /sbom)
│   │   ├── core/           # Конфигурация, типы мышления, версионированные промпты
│   │   ├── services/       # WORM-логгер, квантовая память (ChromaDB), LLM-провайдер
│   │   └── main.py         # Точка входа FastAPI
│   ├── Dockerfile          # Воспроизводимая сборка (INT-L3)
│   └── requirements.txt
├── frontend/               # Flutter (iOS, Android, Windows, macOS, Linux)
├── docs/
│   ├── adr/                # Architecture Decision Records (EVO-L3)
│   └── l3/                 # Документация по деплою, аудиту и мониторингу
├── sbom/                   # Агрегированный Software Bill of Materials (PUR-L3)
├── tools/                  # Скрипты KON-MATRIX (генерация SBOM, экспорт паспорта)
└── .github/workflows/      # CI/CD пайплайны (Linters, DAST, SLSA, Audit)
```

## Технологический стек

- **Backend**: Python 3.10+, FastAPI, Pydantic, ChromaDB (локальный векторный поиск)
- **Frontend**: Flutter (Dart)
- **Инфраструктура**: Docker, GitHub Actions, OWASP ZAP, Ruff
- **Методология**: **KON-MATRIX (Уровень L3: Полное соответствие)**

## Методология разработки и Безопасность

Этот проект является **эталонным пилотом методологии KON-MATRIX**. Он демонстрирует зрелость инженерной культуры через 4 Абсолютных Кона:

1. **Целостность (INT)** ✅: Воспроизводимые Docker-сборки, SLSA Provenance для релизов, строгие CI-линтеры.
2. **Чистота (PUR)** ✅: Автоматическая генерация SBOM (CycloneDX), Dependabot, DAST-сканирование (OWASP ZAP) каждого PR.
3. **Становление (EVO)** ✅: Документированные архитектурные решения (ADR), стратегии Zero-Downtime деплоя и Rollback runbook.
4. **Прозрачность (TRA)** ✅: Криптографический WORM-аудит событий, API-эндпоинты для экспорта паспорта зрелости и метрик, документация по внешнему мониторингу.

📄 *Подробности см. в [.github/SECURITY.md](.github/SECURITY.md) и [`audit-bundle.json`](audit-bundle.json).*

## Быстрый старт

### Вариант А: Локальная разработка (Backend)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# или venv\Scripts\activate для Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API и документация Swagger будут доступны по адресу: http://localhost:8000/docs

### Вариант Б: Воспроизводимая сборка (Docker)

```bash
cd backend
docker build -t potok-app-backend:latest .
docker run -p 8000:8000 potok-app-backend:latest
```

### Проверка соответствия KON-MATRIX

```bash
# Генерация и проверка Паспорта зрелости
python3 tools/export-audit-bundle.py
cat audit-bundle.json
```

## Лицензия

Field-CoCreation License. Все права защищены.  
Внешнее использование требует согласования с правообладателем.

## Контакты

- **Email**: ccf@azesmf.ru
- **Автор**: AZESMF / Павел
- **Репозиторий методологии**: [Kon-Matrix](https://github.com/AzesmF/Kon-Matrix)

---
**Статус проекта**: MVP завершен, соответствие Kon-Matrix L3 подтверждено.  
**Дата актуализации**: 6 сентября 2026 г.
