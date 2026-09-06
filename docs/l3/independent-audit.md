# Independent Security Audit Guide

**Статус:** Draft  
**Проект:** potok-app  
**Конформность:** PUR-L3 (Независимый аудит безопасности)

---

## 1. Цель аудита

Документ описывает процедуру независимого аудита безопасности пилотного проекта "Поток" для верификации соответствия стандартам Kon-Matrix L3.

**Аудитор:** Внешняя независимая сторона (security researcher, penetration tester)  
**Периодичность:** Рекомендуется ежеквартально или при значимых изменениях архитектуры

---

## 2. Аудитируемые артефакты

### 2.1 Supply Chain Security (PUR-L3)

| Артефакт | Путь | Формат | Назначение |
|----------|------|--------|-----------|
| SBOM (Backend) | `sbom/backend.cyclonedx.json` | CycloneDX 1.4 | Список зависимостей Python |
| SBOM (Aggregate) | `sbom/aggregate.cyclonedx.json` | CycloneDX 1.4 | Список всех зависимостей monorepo |
| Dependabot config | `.github/dependabot.yml` | YAML | Конфигурация мониторинга уязвимостей |
| DAST отчеты | GitHub Artifacts (`zap-report`) | HTML | Результаты сканирования OWASP ZAP |

**Процедура проверки:**
```bash
# 1. Сгенерировать актуальный SBOM
python3 tools/generate-sbom.py

# 2. Проверить валидность формата
python3 -c "import json; json.load(open('sbom/aggregate.cyclonedx.json'))"

# 3. Загрузить SBOM в систему анализа уязвимостей (например, Dependency-Track)
# curl -X POST http://dependency-track:8080/api/v1/bom -H "Content-Type: application/json" -d @sbom/aggregate.cyclonedx.json
```

### 2.2 Audit Trail Integrity (TRA-L3)

| Артефакт | Путь | Формат | Назначение |
|----------|------|--------|-----------|
| WORM-лог | `backend/audit_log.jsonl` | JSONL (append-only) | Неизменяемый журнал событий |
| Audit Bundle | `audit-bundle.json` | JSON | Паспорт зрелости проекта |

**Процедура проверки целостности:**
```bash
# 1. Запустить верификацию цепочки хешей
python3 -c "
import json
import hashlib

with open('backend/audit_log.jsonl', 'r') as f:
    lines = f.readlines()

expected_hash = 'genesis_hash_kon_matrix_2026'
for i, line in enumerate(lines):
    entry = json.loads(line)
    if entry['previous_hash'] != expected_hash:
        print(f'❌ Chain broken at entry {i}')
        exit(1)
    
    payload = {k: v for k, v in entry.items() if k != 'current_hash'}
    payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    expected_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    
    if entry['current_hash'] != expected_hash:
        print(f'❌ Hash mismatch at entry {i}')
        exit(1)

print(f'✅ WORM chain valid: {len(lines)} entries')
"

# 2. Сгенерировать актуальный паспорт зрелости
python3 tools/export-audit-bundle.py

# 3. Проверить через API (если сервер запущен)
curl -s http://localhost:8000/passport | python3 -m json.tool
```

### 2.3 API Security (PUR-L3)

| Endpoint | Метод | Назначение |
|----------|-------|-----------|
| `/health` | GET | Проверка состояния системы |
| `/metrics` | GET | Базовые метрики |
| `/passport` | GET | Экспорт паспорта зрелости |
| `/sbom` | GET | Экспорт SBOM |
| `/api/v1/audit-log` | GET | Экспорт записей аудита |

**Процедура DAST-сканирования:**
```bash
# 1. Запустить backend
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# 2. Запустить OWASP ZAP (локально)
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:8000

# 3. Или использовать GitHub Actions workflow
# .github/workflows/dast.yml автоматически запускает ZAP при каждом push
```

---

## 3. Критерии соответствия

### 3.1 PUR-L3 (Чистота)

| Требование | Критерий | Статус |
|------------|---------|--------|
| SBOM актуален | Файл сгенерирован < 7 дней назад | ✅ |
| SBOM валиден | CycloneDX 1.4 формат | ✅ |
| Dependabot активен | Workflow запускается еженедельно | ✅ |
| DAST выполнен | ZAP отчет доступен в артефактах | ✅ |
| Нет критических CVE | SBOM не содержит CVE с severity Critical | ✅ |

### 3.2 TRA-L3 (Прозрачность)

| Требование | Критерий | Статус |
|------------|---------|--------|
| WORM-лог существует | Файл `audit_log.jsonl` присутствует | ✅ |
| Цепочка хешей валидна | Все хеши совпадают | ✅ |
| API доступен | Endpoints `/passport`, `/sbom`, `/metrics` отвечают 200 | ✅ |
| Audit Bundle актуален | Файл сгенерирован < 24 часа назад | ✅ |

---

## 4. Инструменты аудитора

### 4.1 Автоматизированные проверки

```bash
# Скрипт быстрой проверки всех артефактов
cat << 'SCRIPT' > tools/quick-audit-check.sh
#!/bin/bash
set -e

echo "🔍 Kon-Matrix L3 Quick Audit Check"
echo "===================================="

# 1. Проверка SBOM
if [ -f "sbom/aggregate.cyclonedx.json" ]; then
    echo "✅ SBOM exists"
    python3 -c "import json; json.load(open('sbom/aggregate.cyclonedx.json'))" && echo "✅ SBOM valid JSON"
else
    echo "❌ SBOM missing"
fi

# 2. Проверка WORM-лога
if [ -f "backend/audit_log.jsonl" ]; then
    entries=$(wc -l < backend/audit_log.jsonl)
    echo "✅ WORM log exists ($entries entries)"
else
    echo "❌ WORM log missing"
fi

# 3. Проверка Audit Bundle
if [ -f "audit-bundle.json" ]; then
    echo "✅ Audit Bundle exists"
    python3 tools/export-audit-bundle.py > /dev/null
    echo "✅ Audit Bundle regenerated"
else
    echo "❌ Audit Bundle missing"
fi

# 4. Проверка CI workflows
workflows=("linters.yml" "sbom-generation.yml" "dast.yml" "audit-log-verify.yml")
for wf in "${workflows[@]}"; do
    if [ -f ".github/workflows/$wf" ]; then
        echo "✅ Workflow $wf exists"
    else
        echo "❌ Workflow $wf missing"
    fi
done

echo ""
echo "🎯 Quick audit check complete"
SCRIPT

chmod +x tools/quick-audit-check.sh

# Запуск
./tools/quick-audit-check.sh
```

### 4.2 Ручная проверка

1. **Открыть паспорт зрелости:**
   ```bash
   curl -s http://localhost:8000/passport | python3 -m json.tool
   ```

2. **Скачать SBOM:**
   ```bash
   curl -s http://localhost:8000/sbom -o sbom-audit.json
   ```

3. **Проверить WORM-лог через API:**
   ```bash
   curl -s http://localhost:8000/api/v1/audit-log | python3 -m json.tool
   ```

---

## 5. Отчетность

После завершения аудита составляется отчет со следующей структурой:

```markdown
# Security Audit Report

**Дата:** YYYY-MM-DD  
**Аудитор:** [Имя/Организация]  
**Проект:** potok-app  
**Версия:** [Git tag или commit hash]

## Executive Summary
[Краткое описание результатов]

## Findings
### Critical
[Список критических уязвимостей]

### High
[Список высоких уязвимостей]

### Medium
[Список средних уязвимостей]

### Low
[Список низких уязвимостей]

## Compliance Status
| Standard | Status | Notes |
|----------|--------|-------|
| PUR-L3 | Pass/Fail | [Детали] |
| TRA-L3 | Pass/Fail | [Детали] |

## Recommendations
[Рекомендации по улучшению]

## Appendix
- SBOM analysis
- WORM chain verification
- DAST scan results
```

---

## 6. Контакты

**Ответственный за аудит:** [Email]  
**Escalation path:** [Контакты]  
**Частота аудита:** Ежеквартально

---

*Документ обновлён: 2026-09-06*  
*Версия: 1.0*
