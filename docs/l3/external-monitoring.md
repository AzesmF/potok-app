# External Monitoring Integration Guide

**Статус:** Implemented  
**Проект:** potok-app  
**Конформность:** TRA-L3 (Наблюдаемость и интеграция с внешними дашбордами)

---

## 1. Обзор

Пилотный проект "Поток" предоставляет endpoint `/metrics` для интеграции с внешними системами мониторинга (Prometheus, Grafana, Datadog, etc.).

**Endpoint:** `GET /metrics`  
**Формат ответа:** JSON  
**Частота опроса:** рекомендуется каждые 15-30 секунд

---

## 2. Структура метрик

```json
{
  "uptime_seconds": 3600.5,
  "journal_entries": 142,
  "worm_log_entries": 89,
  "timestamp": 1725612345.678
}
```

| Метрика | Тип | Описание |
|---------|-----|----------|
| `uptime_seconds` | Gauge | Время работы приложения с момента старта |
| `journal_entries` | Gauge | Количество записей в дневнике |
| `worm_log_entries` | Gauge | Количество записей в WORM-логе аудита |
| `timestamp` | Counter | Unix timestamp последнего обновления |

---

## 3. Интеграция с Prometheus

### 3.1 Конфигурация `prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'potok-app-backend'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['backend:8000']
        labels:
          environment: 'production'
          service: 'potok-backend'
```

### 3.2 Prometheus Exporter (опционально)

Для конвертации JSON-метрик в формат Prometheus можно использовать `prometheus-json-exporter`:

```yaml
# json-exporter-config.yml
modules:
  potok_metrics:
    metrics:
      - name: potok_uptime_seconds
        path: '{ .uptime_seconds }'
        help: 'Application uptime in seconds'
      - name: potok_journal_entries_total
        path: '{ .journal_entries }'
        help: 'Total journal entries'
      - name: potok_worm_log_entries_total
        path: '{ .worm_log_entries }'
        help: 'Total WORM log entries'
```

Запуск:
```bash
docker run -p 7979:7979 \
  -v $(pwd)/json-exporter-config.yml:/config.yml \
  prometheuscommunity/json-exporter --config.file=/config.yml
```

---

## 4. Интеграция с Grafana

### 4.1 Добавление DataSource

1. Открыть Grafana → Configuration → Data Sources
2. Добавить Prometheus с URL: `http://prometheus:9090`
3. Сохранить и протестировать

### 4.2 Пример дашборда

Создать дашборд с следующими панелями:

**Панель 1: Uptime**
```promql
potok_uptime_seconds
```
Тип визуализации: Stat

**Панель 2: Journal Entries Growth**
```promql
increase(potok_journal_entries_total[1h])
```
Тип визуализации: Time series

**Панель 3: WORM Log Activity**
```promql
rate(potok_worm_log_entries_total[5m])
```
Тип визуализации: Time series

### 4.3 JSON модели дашборда

Экспорт дашборда в JSON и сохранение в `monitoring/grafana-dashboards/potok-overview.json` для версионирования.

---

## 5. Интеграция с Datadog

### 5.1 Конфигурация `datadog.yaml`

```yaml
init_config:

instances:
  - openmetrics_endpoint: http://backend:8000/metrics
    namespace: "potok"
    metrics:
      - uptime_seconds
      - journal_entries
      - worm_log_entries
```

### 5.2 Алерты

Настроить алерты в Datadog:
- **Critical:** `potok_uptime_seconds < 60` (приложение перезапустилось)
- **Warning:** `potok_worm_log_entries` не растёт в течение 1 часа (возможная проблема с аудитом)

---

## 6. Docker Compose с мониторингом

Пример `docker-compose.monitoring.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./monitoring/grafana-dashboards:/var/lib/grafana/dashboards
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

Запуск:
```bash
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

---

## 7. Health Checks для мониторинга

Помимо `/metrics`, доступны endpoints для health monitoring:

| Endpoint | Назначение | Ожидаемый статус |
|----------|-----------|------------------|
| `/health` | Общая проверка состояния | 200 OK |
| `/passport` | Паспорт зрелости Kon-Matrix | 200 OK |
| `/sbom` | SBOM для аудита зависимостей | 200 OK |
| `/api/v1/audit-log` | Последние записи WORM-лога | 200 OK |

---

## 8. Рекомендуемые алерты

| Алерт | Условие | Severity |
|-------|---------|----------|
| Приложение недоступно | `/health` не отвечает 30s | Critical |
| WORM-лог не растёт | `worm_log_entries` не меняется 1h | Warning |
| Высокая задержка | `/metrics` отвечает > 5s | Warning |
| Ошибка цепочки хешей | `/passport` показывает `chain_valid: false` | Critical |

---

## 9. Тестирование интеграции

```bash
# 1. Проверить, что endpoint отвечает
curl -s http://localhost:8000/metrics | python3 -m json.tool

# 2. Проверить Prometheus scrape
curl -s http://prometheus:9090/api/v1/targets | python3 -m json.tool

# 3. Проверить Grafana datasource
curl -s http://admin:admin@localhost:3000/api/datasources | python3 -m json.tool
```

---

## 10. Контакты и эскалация

**Ответственный за мониторинг:** [Email]  
**On-call rotation:** [Ссылка на график]  
**Escalation path:** [Контакты]

---

*Документ обновлён: 2026-09-06*  
*Версия: 1.0*
