"""
WORM-логгер (Write-Once-Read-Many) с цепочкой хешей.
Реализует стандарт TRA-L3: неизменяемость аудита.
"""
import json
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("potok.worm_logger")

class WORMLogger:
    def __init__(self, log_file: str = "audit_log.jsonl"):
        self.log_file = log_file
        self._last_hash = self._load_last_hash()
        logger.info(f"✅ WORM-логгер инициализирован. Последний хеш: {self._last_hash[:8]}...")

    def _load_last_hash(self) -> str:
        """Загружает хеш последней записи из файла (или возвращает genesis hash)"""
        if not os.path.exists(self.log_file):
            return "genesis_hash_kon_matrix_2026"
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get('current_hash', "genesis_hash_kon_matrix_2026")
        except Exception as e:
            logger.warning(f"Ошибка чтения лога: {e}")
        
        return "genesis_hash_kon_matrix_2026"

    def log(self, operation: str, details: Dict, ethical_score: float = 1.0) -> str:
        """Добавляет неизменяемую запись в лог"""
        timestamp = datetime.utcnow().isoformat()
        
        # Формируем данные для хеширования
        payload = {
            "timestamp": timestamp,
            "operation": operation,
            "details": details,
            "ethical_score": ethical_score,
            "previous_hash": self._last_hash
        }
        
        # Вычисляем текущий хеш (SHA-256)
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        current_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        # Добавляем текущий хеш в запись
        payload["current_hash"] = current_hash
        
        # Записываем в файл (append mode = WORM)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(payload, ensure_ascii=False) + '\n')
        
        self._last_hash = current_hash
        logger.info(f"🔒 WORM-запись добавлена: {operation} (hash: {current_hash[:8]}...)")
        
        return current_hash

    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Получает последние записи лога"""
        if not os.path.exists(self.log_file):
            return []
        
        logs = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except Exception as e:
            logger.error(f"Ошибка чтения лога: {e}")
            
        return logs[-limit:]

    def verify_chain(self) -> bool:
        """Проверяет целостность цепочки хешей"""
        if not os.path.exists(self.log_file):
            return True
            
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            expected_hash = "genesis_hash_kon_matrix_2026"
            for line in lines:
                entry = json.loads(line)
                if entry.get('previous_hash') != expected_hash:
                    logger.error(f"❌ Нарушение целостности цепи! Ожидался: {expected_hash}, получено: {entry.get('previous_hash')}")
                    return False
                
                # Пересчитываем хеш для проверки
                payload_to_check = {
                    "timestamp": entry["timestamp"],
                    "operation": entry["operation"],
                    "details": entry["details"],
                    "ethical_score": entry["ethical_score"],
                    "previous_hash": entry["previous_hash"]
                }
                payload_str = json.dumps(payload_to_check, sort_keys=True, ensure_ascii=False)
                expected_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
                
                if entry.get('current_hash') != expected_hash:
                    logger.error(f"❌ Хеш записи не совпадает!")
                    return False
                    
            logger.info("✅ Целостность WORM-цепи подтверждена")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка проверки цепи: {e}")
            return False

# Singleton
_worm_logger_instance: Optional[WORMLogger] = None

def get_worm_logger() -> WORMLogger:
    global _worm_logger_instance
    if _worm_logger_instance is None:
        _worm_logger_instance = WORMLogger()
    return _worm_logger_instance
