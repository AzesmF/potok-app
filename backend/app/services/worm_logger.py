"""
WORM-логгер (Write-Once-Read-Many) с цепочкой хешей.
Стандарт TRA-L3: неизменяемость аудита.
"""

import hashlib
import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger("potok.worm_logger")


class WORMLogger:
    def __init__(self, log_file: str | None = None):
        # Умное разрешение пути: всегда сохраняем в backend/audit_log.jsonl,
        # независимо от того, из какой директории запущен скрипт
        if log_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # current_dir = .../potok-app/backend/app/services
            # Идем на 2 уровня вверх до backend/
            backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
            log_file = os.path.join(backend_dir, "audit_log.jsonl")

        self.log_file = log_file
        self._last_hash = self._load_last_hash()
        logger.info(f"✅ WORM-логгер инициализирован. Путь: {self.log_file}")
        logger.info(f"   Последний хеш: {self._last_hash[:8]}...")

    def _load_last_hash(self) -> str:
        if not os.path.exists(self.log_file):
            return "genesis_hash_kon_matrix_2026"

        try:
            with open(self.log_file, encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get("current_hash", "genesis_hash_kon_matrix_2026")
        except Exception as e:
            logger.warning(f"Ошибка чтения лога: {e}")

        return "genesis_hash_kon_matrix_2026"

    def log(self, operation: str, details: dict, ethical_score: float = 1.0) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()

        payload = {
            "timestamp": timestamp,
            "operation": operation,
            "details": details,
            "ethical_score": ethical_score,
            "previous_hash": self._last_hash,
        }

        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        current_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        payload["current_hash"] = current_hash

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

        self._last_hash = current_hash
        logger.info(f"🔒 WORM-запись добавлена: {operation} (hash: {current_hash[:8]}...)")
        return current_hash

    def get_recent_logs(self, limit: int = 50) -> list[dict]:
        if not os.path.exists(self.log_file):
            return []

        logs = []
        try:
            with open(self.log_file, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except Exception as e:
            logger.error(f"Ошибка чтения лога: {e}")

        return logs[-limit:]

    def verify_chain(self) -> bool:
        if not os.path.exists(self.log_file):
            return True

        try:
            with open(self.log_file, encoding="utf-8") as f:
                lines = f.readlines()

            expected_hash = "genesis_hash_kon_matrix_2026"
            for line in lines:
                entry = json.loads(line)
                if entry.get("previous_hash") != expected_hash:
                    logger.error("❌ Нарушение целостности цепи!")
                    return False

                payload_to_check = {
                    "timestamp": entry["timestamp"],
                    "operation": entry["operation"],
                    "details": entry["details"],
                    "ethical_score": entry["ethical_score"],
                    "previous_hash": entry["previous_hash"],
                }
                payload_str = json.dumps(payload_to_check, sort_keys=True, ensure_ascii=False)
                expected_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

                if entry.get("current_hash") != expected_hash:
                    logger.error("❌ Хеш записи не совпадает!")
                    return False

            return True
        except Exception as e:
            logger.error(f"Ошибка проверки цепи: {e}")
            return False


_worm_logger_instance: WORMLogger | None = None


def get_worm_logger() -> WORMLogger:
    global _worm_logger_instance
    if _worm_logger_instance is None:
        _worm_logger_instance = WORMLogger()
    return _worm_logger_instance
