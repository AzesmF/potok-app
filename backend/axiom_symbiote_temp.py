# Commercial License
```
PROJECT: Field of Co-Creation
ECOSYSTEM: AI-Symbiosis-H
LICENSE: Commercial

ETHICAL PRINCIPLES:
1. Do no harm to the user
2. Maintain algorithm transparency
3. Respect the right to control
4. Protect confidentiality

BLOCKCHAIN: QmRwy3EYFkSCGtF4nmLMjcZwwkf5NZQEWPpPENPsJDZRTB | 89ba5c39c2c8da5206af78a2023ef65eadf0acc5b813317087e1c80e64276b66
AUTHOR: Pavel Sergeevich Fenin
```
```
### INHERITANCE CLAUSE
This license inherits all provisions from:
- Field-CoCreation License (Root License)
- IPFS_CID: QmRwy3EYFkSCGtF4nmLMjcZwwkf5NZQEWPpPENPsJDZRTB
- TON_HASH: 89ba5c39c2c8da5206af78a2023ef65eadf0acc5b813317087e1c80e64276b66
```

# solution.py
import asyncio
import time
import re
import json
import hashlib
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque

import polars as pl
import numpy as np
from sentence_transformers import SentenceTransformer

# Универсальный интерфейс для нейросети
class AINeuralInterface:
    """Универсальный интерфейс для работы с любой нейросетью"""
    
    def __init__(self, ai_provider=None):
        self.ai_provider = ai_provider
        self.provider_name = "UniversalAI"
    
    async def achat(self, prompt: str) -> Any:
        """Универсальный метод для запроса к нейросети"""
        if self.ai_provider:
            # Используем переданный провайдер
            return await self._call_external_ai(prompt)
        else:
            # Используем встроенную заглушку
            return self._mock_ai_response(prompt)
    
    async def _call_external_ai(self, prompt: str) -> Any:
        """Вызов внешней нейросети"""
        # Здесь можно подключить любую нейросеть:
        # - OpenAI GPT
        # - Yandex GPT  
        # - GigaChat
        # - Local models
        # ПРИМЕР для OpenAI:
        # import openai
        # response = await openai.ChatCompletion.acreate(...)
        # return response
        
        # Временная заглушка
        return self._mock_ai_response(prompt)
    
    def _mock_ai_response(self, prompt: str) -> Any:
        """Заглушка для тестирования"""
        class MockMessage:
            content = "🤖 [Универсальный AI]: На основе ваших данных вижу позитивные тенденции в развитии. Рекомендую продолжать текущую активность для достижения целей в ближайшие 6-9 месяцев."
        
        class MockChoice:
            message = MockMessage()
        
        class MockResponse:
            choices = [MockChoice()]
        
        return MockResponse()

# Создаем экземпляр универсального интерфейса
universal_ai = AINeuralInterface()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AxiomSymbiote")

# ==================== ЭТИЧЕСКИЕ ПРИНЦИПЫ ====================

class RiskLevel(Enum):
    """Уровни этического риска"""
    LOW = 1
    MODERATE = 2  
    HIGH = 3
    CRITICAL = 4

class EthicalPrinciples:
    """Уровневые этические принципы системы"""
    
    # УРОВЕНЬ 1: АБСОЛЮТНЫЕ ЗАПРЕТЫ (нельзя нарушать никогда)
    ABSOLUTE_PROHIBITIONS = {
        "physical_harm": "Причинение физического вреда",
        "child_exploitation": "Эксплуатация несовершеннолетних", 
        "terrorism_support": "Поддержка терроризма",
        "life_threatening": "Угрозы жизни и здоровью",
        "hate_speech": "Разжигание ненависти и дискриминация"
    }
    
    # УРОВЕНЬ 2: ВЫСОКИЙ РИСК (требует особого контроля)
    HIGH_RISK_AREAS = {
        "medical_advice": "Медицинские рекомендации и диагнозы",
        "financial_decisions": "Финансовые решения и инвестиции",
        "legal_advice": "Юридические консультации",
        "mental_health": "Психическое здоровье и терапия"
    }
    
    # УРОВЕНЬ 3: УМЕРЕННЫЙ РИСК (требует явного согласия)
    MODERATE_RISK = {
        "personal_data": "Обработка персональных данных",
        "behavior_analysis": "Анализ поведения и паттернов",
        "predictive_modeling": "Предсказание будущего поведения"
    }
    
    @classmethod
    def get_risk_level(cls, operation_type: str) -> RiskLevel:
        """Определение уровня риска для типа операции"""
        if operation_type in cls.ABSOLUTE_PROHIBITIONS:
            return RiskLevel.CRITICAL
        elif operation_type in cls.HIGH_RISK_AREAS:
            return RiskLevel.HIGH
        elif operation_type in cls.MODERATE_RISK:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW

# ==================== ЭТИЧЕСКИЕ ИСКЛЮЧЕНИЯ ====================

class EthicalViolation(Exception):
    """Базовое исключение для этических нарушений"""
    def __init__(self, message: str, severity: RiskLevel = RiskLevel.MODERATE):
        self.message = message
        self.severity = severity
        super().__init__(self.message)

class CriticalEthicalViolation(EthicalViolation):
    """Критическое этическое нарушение"""
    def __init__(self, message: str):
        super().__init__(message, RiskLevel.CRITICAL)

class HighRiskEthicalViolation(EthicalViolation):
    """Высокорисковое этическое нарушение"""
    def __init__(self, message: str):
        super().__init__(message, RiskLevel.HIGH)

class ValidationError(EthicalViolation):
    """Ошибка валидации данных"""
    pass

class SecurityError(EthicalViolation):
    """Ошибка безопасности"""
    pass

class RateLimitError(EthicalViolation):
    """Ошибка превышения лимита запросов"""
    pass

# ==================== СИСТЕМА ВАЛИДАЦИИ ====================

@dataclass
class ValidationResult:
    """Результат валидации с детальной информацией"""
    is_valid: bool
    message: str
    score: float
    details: Dict[str, Any]
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class EthicalInputValidator:
    """Комплексная этическая валидация входных данных"""
    
    def __init__(self, security_salt: str = "axiom_symbiote_2024"):
        self.max_question_length = 1000
        self.min_question_length = 3
        self.user_id_pattern = re.compile(r'^[a-zA-Z0-9_-]{1,50}$')
        self.security_salt = security_salt
        
        # Мультиязычные этические паттерны с уровнями риска (НОВЫЙ СЛОЙ)
        self.multilingual_block_patterns = {
            # Медицинские диагнозы и рекомендации - ВЫСОКИЙ РИСК
            'medical': {
                'risk_level': 0.95,
                'patterns': {
                    'ru': [r'медицинск', r'диагноз', r'лечени', r'болезн', r'врач', r'терапи', r'лекарств'],
                    'en': [r'medical', r'diagnos', r'treatment', r'disease', r'doctor', r'therapy', r'medic'],
                    'es': [r'médic', r'diagnóst', r'tratamiento', r'enfermedad', r'médico', r'terapia']
                }
            },
            # Финансовые консультации - ВЫСОКИЙ РИСК
            'financial': {
                'risk_level': 0.90,
                'patterns': {
                    'ru': [r'инвестиц', r'акци', r'бирж', r'финанс', r'деньги', r'бюджет'],
                    'en': [r'invest', r'stock', r'share', r'financial', r'money', r'budget'],
                    'es': [r'invers', r'accion', r'bolsa', r'financier', r'dinero', r'presupuesto']
                }
            },
            # Юридические консультации - ВЫСОКИЙ РИСК
            'legal': {
                'risk_level': 0.90,
                'patterns': {
                    'ru': [r'юридическ', r'адвокат', r'суд', r'закон', r'правов', r'юрист'],
                    'en': [r'legal', r'lawyer', r'court', r'law', r'legal', r'attorney'],
                    'es': [r'legal', r'abogado', r'tribunal', r'ley', r'jurídic']
                }
            },
            # Угрозы и насилие - КРИТИЧЕСКИЙ РИСК
            'threats': {
                'risk_level': 0.98,
                'patterns': {
                    'ru': [r'угроз', r'убийств', r'насили', r'оружи', r'вред', r'опасно'],
                    'en': [r'threat', r'murder', r'violence', r'weapon', r'harm', r'danger'],
                    'es': [r'amenaza', r'asesinat', r'violencia', r'arma', r'daño', r'peligro']
                }
            }
        }

        # Абсолютные международные запреты (не зависят от языка)
        self.international_absolute_blocks = [
            r'child.*porn', r'terrorism', r'exploit.*minor', r'human.*trafficking',
            r'violence.*against', r'suicide', r'self.*harm'
        ]
        
        # ОРИГИНАЛЬНЫЕ ЭТИЧЕСКИЕ ПАТТЕРНЫ (СОХРАНЯЕМ)
        self.ethical_block_patterns = [
            (r'(?:финансовые?\s+махинации?|обман|мошенничество|незаконные?\s+схемы?)', 0.95, "финансовые махинации"),
            (r'(?:дискриминация|ненависть|экстремизм|расизм|ксенофобия)', 0.95, "разжигание ненависти"),
            (r'(?:взлом|взломать|хакерство|несанкционированный\s+доступ)', 0.9, "киберпреступность"),
            (r'(?:личные?\s+данные?|пароли?|ключи?|авторизационные?\s+данные?)', 0.8, "конфиденциальные данные"),
            (r'(?:sql|script|javascript|exec|eval|system)\s*\(', 0.98, "инъекция кода"),
            (r'<script|javascript:|onload=|onerror=', 0.98, "XSS атака"),
            (r'(?:секретны[её]|государственны[её]|военны[её])\s+данные?', 0.85, "конфиденциальная информация"),
            (r'(?:психологическое\s+давление|манипуляция|контроль)', 0.7, "психологическое воздействие"),
        ]
        
        # ОРИГИНАЛЬНЫЕ АБСОЛЮТНЫЕ СТОП-СЛОВА (СОХРАНЯЕМ)
        self.absolute_block_patterns = [
            r'child.*porn',
            r'terrorism',
            r'violence.*against',
            r'exploit.*minor',
            r'human.*trafficking',
        ]
        
        # ОРИГИНАЛЬНЫЕ ПАТТЕРНЫ ДЛЯ МОНИТОРИНГА (СОХРАНЯЕМ)
        self.monitoring_patterns = [
            (r'(?:предсказание\s+смерти|смертельный)', 0.6, "предсказание негативных событий"),
            (r'(?:медицинск[а-я]+\s+диагноз|лечени[ея])', 0.5, "медицинские рекомендации"),
            (r'(?:юридическ[а-я]+\s+консультация|правов[а-я]+\s+совет)', 0.5, "юридические консультации"),
        ]
    
    def validate_input(self, user_id: str, question: str) -> ValidationResult:
        """Комплексная этическая валидация входных данных"""
        
        # 🔒 Хеширование user_id для логов
        user_id_hash = self._hash_sensitive_data(user_id)
        
        # 0. НОВАЯ ПРОВЕРКА: Мультиязычные блокировки (ДОПОЛНИТЕЛЬНЫЙ СЛОЙ)
        multilingual_result = self._check_multilingual_patterns(question)
        if multilingual_result:
            risk_level = multilingual_result.get('risk_level', 0.95)
            logger.warning(f"MULTILINGUAL BLOCK: user_{user_id_hash} - {multilingual_result['reason']} (risk: {risk_level})")
            return ValidationResult(
                False,
                "Запрос нарушает международные этические стандарты",
                risk_level,
                {
                    "blocked_reason": multilingual_result['category'],
                    "language": multilingual_result.get('language', 'international'),
                    "severity": multilingual_result.get('severity', 'HIGH'),
                    "risk_level": risk_level,
                    "user_id_hash": user_id_hash
                }
            )
        
        # 1. ОРИГИНАЛЬНАЯ ПРОВЕРКА: Абсолютные стоп-слова (СОХРАНЯЕМ)
        block_result = self._check_absolute_block_patterns(question)
        if block_result:
            logger.warning(f"ABSOLUTE BLOCK: user_{user_id_hash} - {block_result['reason']}")
            return ValidationResult(
                False,
                "Запрос содержит абсолютно запрещенное содержание",
                0.0,
                {
                    "blocked_reason": "absolute_block",
                    "pattern_category": block_result['category'],
                    "user_id_hash": user_id_hash
                }
            )
        
        # 2. ОРИГИНАЛЬНАЯ ПРОВЕРКА: Валидация user_id (СОХРАНЯЕМ)
        user_id_result = self._validate_user_id(user_id)
        if not user_id_result.is_valid:
            return ValidationResult(
                False,
                user_id_result.message,
                0.0,
                {
                    "error": "invalid_user_id",
                    "user_id_hash": user_id_hash
                }
            )
        
        # 3. ОРИГИНАЛЬНАЯ ПРОВЕРКА: Длина вопроса (СОХРАНЯЕМ)
        question_length = len(question)
        if not self.min_question_length <= question_length <= self.max_question_length:
            return ValidationResult(
                False,
                f"Длина вопроса должна быть от {self.min_question_length} до {self.max_question_length} символов",
                0.0,
                {
                    "length": question_length,
                    "allowed_range": [self.min_question_length, self.max_question_length],
                    "user_id_hash": user_id_hash
                }
            )
        
        # 4. ОРИГИНАЛЬНАЯ ПРОВЕРКА: Этические паттерны (СОХРАНЯЕМ)
        ethical_result = self._check_ethical_patterns(question)
        if not ethical_result.is_valid:
            logger.warning(f"ETHICAL BLOCK: user_{user_id_hash} - {ethical_result.message}")
            return ethical_result
        
        # 5. ОРИГИНАЛЬНАЯ ПРОВЕРКА: Паттерны мониторинга (СОХРАНЯЕМ)
        monitoring_result = self._check_monitoring_patterns(question)
        if not monitoring_result.is_valid:
            logger.info(f"MONITORING: user_{user_id_hash} - {monitoring_result.message}")
        
        return ValidationResult(
            True,
            "Этическая валидация успешна",
            0.9,
            {
                "length": question_length,
                "user_id_hash": user_id_hash,
                "ethical_checks_passed": True,
                "monitoring_notes": monitoring_result.details if not monitoring_result.is_valid else None
            }
        )
    
    def _check_multilingual_patterns(self, question: str) -> Optional[Dict]:
        """НОВЫЙ МЕТОД: Мультиязычная проверка этических паттернов с уровнями риска"""
        question_lower = question.lower()
        
        # Проверка международных абсолютных запретов - КРИТИЧЕСКИЙ РИСК
        for pattern in self.international_absolute_blocks:
            if re.search(pattern, question_lower, re.IGNORECASE):
                return {
                    "reason": "International absolute prohibition",
                    "category": "international_block",
                    "severity": "CRITICAL",
                    "risk_level": 0.99  # Максимальный уровень риска
                }
        
        # Проверка по языковым категориям с уровнями риска
        for category, config in self.multilingual_block_patterns.items():
            risk_level = config['risk_level']
            patterns_by_lang = config['patterns']
            
            for lang, patterns in patterns_by_lang.items():
                for pattern in patterns:
                    if re.search(pattern, question_lower, re.IGNORECASE):
                        return {
                            "reason": f"Multilingual block: {category} ({lang})",
                            "category": category,
                            "language": lang,
                            "severity": "HIGH" if risk_level >= 0.9 else "MEDIUM",
                            "risk_level": risk_level
                        }
        
        return None
    
    def _check_absolute_block_patterns(self, question: str) -> Optional[Dict]:
        """ОРИГИНАЛЬНЫЙ МЕТОД: Проверка абсолютно запрещенных паттернов"""
        question_lower = question.lower()
        
        for i, pattern in enumerate(self.absolute_block_patterns):
            if re.search(pattern, question_lower, re.IGNORECASE):
                return {
                    "reason": f"Обнаружен абсолютно запрещенный паттерн #{i+1}",
                    "category": "absolute_block"
                }
        return None
    
    def _validate_user_id(self, user_id: str) -> ValidationResult:
        """ОРИГИНАЛЬНЫЙ МЕТОД: Валидация user_id с учетом приватности"""
        if not user_id or not isinstance(user_id, str):
            return ValidationResult(
                False, 
                "Идентификатор пользователя должен быть непустой строкой",
                0.0,
                {"error": "empty_or_invalid_type"}
            )
            
        if not self.user_id_pattern.match(user_id):
            return ValidationResult(
                False, 
                "Некорректный формат идентификатора пользователя",
                0.0,
                {"error": "invalid_format"}
            )
            
        return ValidationResult(True, "User ID валиден", 1.0, {})
    
    def _check_ethical_patterns(self, question: str) -> ValidationResult:
        """ОРИГИНАЛЬНЫЙ МЕТОД: Проверка этических паттернов"""
        question_lower = question.lower()
        detected_patterns = []
        max_risk_score = 0.0
        
        for pattern, risk_score, description in self.ethical_block_patterns:
            if re.search(pattern, question_lower, re.IGNORECASE):
                detected_patterns.append({
                    "pattern": pattern,
                    "risk_score": risk_score,
                    "description": description
                })
                max_risk_score = max(max_risk_score, risk_score)
        
        if detected_patterns:
            highest_risk = max_risk_score
            if highest_risk > 0.8:
                return ValidationResult(
                    False,
                    f"Запрос нарушает этические принципы: {detected_patterns[0]['description']}",
                    highest_risk,
                    {
                        "detected_patterns": detected_patterns,
                        "highest_risk": highest_risk,
                        "action": "blocked"
                    }
                )
        
        return ValidationResult(True, "Этические проверки пройдены", 1.0, {})
    
    def _check_monitoring_patterns(self, question: str) -> ValidationResult:
        """ОРИГИНАЛЬНЫЙ МЕТОД: Проверка паттернов для мониторинга"""
        question_lower = question.lower()
        monitoring_notes = []
        
        for pattern, risk_score, description in self.monitoring_patterns:
            if re.search(pattern, question_lower, re.IGNORECASE):
                monitoring_notes.append({
                    "pattern": description,
                    "risk_level": "monitor",
                    "recommendation": "требует осторожности в ответе"
                })
        
        if monitoring_notes:
            return ValidationResult(
                False,
                "Запрос требует особого внимания",
                0.7,
                {
                    "monitoring_required": True,
                    "notes": monitoring_notes,
                    "action": "monitor"
                }
            )
        
        return ValidationResult(True, "Мониторинг не требуется", 1.0, {})
    
    def _hash_sensitive_data(self, data: str) -> str:
        """ОРИГИНАЛЬНЫЙ МЕТОД: Безопасное хеширование чувствительных данных"""
        return hashlib.sha256(
            f"{data}{self.security_salt}".encode()
        ).hexdigest()[:16]

# ==================== СИСТЕМА АУДИТА И ЛОГИРОВАНИЯ ====================

class EthicalAuditLogger:
    """Система аудита с циклическим буфером и продвинутым логированием"""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.audit_trail = deque(maxlen=max_entries)
        self.entry_count = 0
        self.anomaly_count = 0
        self.success_count = 0
        
    def log_operation(self, operation: str, user_id: str, details: Dict, ethical_score: float):
        """Безопасное логирование операции с санитизацией данных"""
        
        # Санитизация деталей
        sanitized_details = self._sanitize_details(details)
        
        audit_entry = {
            "timestamp": time.time(),
            "iso_timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "operation": operation,
            "user_id": user_id,
            "details": sanitized_details,
            "ethical_score": ethical_score,
            "entry_id": self.entry_count,
            "hash": self._generate_hash(operation, user_id, sanitized_details, ethical_score)
        }
        
        self.audit_trail.append(audit_entry)
        self.entry_count += 1
        
        # Статистика
        if ethical_score < 0.5:
            self.anomaly_count += 1
            logger.warning(f"Низкая этическая оценка: {operation} для {user_id} (оценка: {ethical_score:.2f})")
        else:
            self.success_count += 1
            
        # Периодическое логирование статистики
        if self.entry_count % 100 == 0:
            logger.info(f"Аудит: {self.entry_count} записей, {self.anomaly_count} аномалий")
    
    def _sanitize_details(self, details: Dict) -> Dict:
        """Тщательная очистка чувствительных данных"""
        sanitized = details.copy()
        
        # Список чувствительных полей для очистки
        sensitive_fields = [
            'password', 'token', 'secret', 'key', 'credit_card', 'cvv',
            'passport', 'social_security', 'private_key', 'api_key'
        ]
        
        # Очистка чувствительных полей
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = '***REDACTED***'
                
        # Очистка вложенных структур
        for key, value in sanitized.items():
            if isinstance(value, str):
                # Ограничение длины строк
                if len(value) > 500:
                    sanitized[key] = value[:500] + "..."
                # Частичная маскировка email
                elif '@' in value:
                    parts = value.split('@')
                    if len(parts) == 2:
                        sanitized[key] = f"{parts[0][:2]}***@{parts[1]}"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_details(value)
                
        return sanitized
    
    def _generate_hash(self, operation: str, user_id: str, details: Dict, ethical_score: float) -> str:
        """Генерация криптографического хеша для верификации"""
        data_string = f"{operation}{user_id}{json.dumps(details, sort_keys=True)}{ethical_score}{time.time()}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def get_audit_report(self, last_n: int = 50) -> str:
        """Генерация комплексного отчета аудита"""
        recent_entries = list(self.audit_trail)[-last_n:] if self.audit_trail else []
        
        # Расчет статистики
        total_entries = self.entry_count
        buffer_size = len(self.audit_trail)
        avg_score = self._calculate_average_score()
        
        # Определение статуса системы
        if buffer_size >= self.max_entries * 0.95:
            system_status = "CRITICAL"
        elif buffer_size >= self.max_entries * 0.8:
            system_status = "WARNING"
        else:
            system_status = "HEALTHY"
            
        report = {
            "system_status": system_status,
            "statistics": {
                "total_operations": total_entries,
                "current_buffer_size": buffer_size,
                "buffer_capacity": self.max_entries,
                "successful_operations": self.success_count,
                "anomaly_operations": self.anomaly_count,
                "success_rate": self.success_count / total_entries if total_entries > 0 else 0,
                "average_ethical_score": avg_score
            },
            "recent_operations": recent_entries,
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False, default=str)
    
    def _calculate_average_score(self) -> float:
        """Безопасный расчет средней этической оценки"""
        if not self.audit_trail:
            return 0.0
            
        scores = [entry["ethical_score"] for entry in self.audit_trail]
        return float(np.mean(scores))

# ==================== МЕХАНИЗМЫ БЕЗОПАСНОСТИ ====================

class SafetyMechanisms:
    """Продвинутые механизмы безопасности с детектированием аномалий"""
    
    def __init__(self):
        self.emergency_stop = False
        self.anomaly_threshold = 0.8
        self.consecutive_anomalies = 0
        self.max_consecutive_anomalies = 3
        self.anomaly_history = deque(maxlen=100)
        
        # Паттерны для детектирования аномалий в ответах
        self.response_patterns_blacklist = [
            (r'(?:повторяю|снова|еще раз).{0,20}(?:сказать|ответить|объяснить)', 0.7),
            (r'.*?(.)\1{10,}.*?', 0.8),  # Повторяющиеся символы
            (r'^.{0,15}$', 0.6),  # Слишком короткие ответы
            (r'.{1000,}', 0.5),   # Слишком длинные ответы
            (r'(?:ошибка|error|exception).{0,50}(?:повторите|попробуйте)', 0.4),
            (r'<.*?>', 0.9),  # HTML/XML теги
            (r'(?:system|exec|eval|compile)\s*\(', 0.95),  # Выполнение кода
        ]
        
        # Паттерны для детектирования противоречий
        self.contradiction_indicators = [
            r'но.*ранее',
            r'хотя.*раньше',
            r'вопреки.*предыдущему',
        ]
    
    def detect_anomalies(self, response: str, user_context: Dict) -> Tuple[bool, str, float]:
        """Комплексное обнаружение аномалий в ответе"""
        
        if self.emergency_stop:
            return True, "СИСТЕМА ОСТАНОВЛЕНА: активирован аварийный режим", 1.0
        
        anomaly_score = 0.0
        detected_anomalies = []
        
        # Проверка на повторяющиеся паттерны
        repetition_score = self._detect_repetition_enhanced(response)
        if repetition_score > 0:
            anomaly_score = max(anomaly_score, repetition_score)
            detected_anomalies.append(f"повторение (score: {repetition_score:.2f})")
            
        # Проверка по черному списку паттернов
        blacklist_score, blacklist_pattern = self._check_blacklist_patterns(response)
        if blacklist_score > 0:
            anomaly_score = max(anomaly_score, blacklist_score)
            detected_anomalies.append(f"запрещенный паттерн: {blacklist_pattern}")
            
        # Проверка на противоречия
        contradiction_score = self._detect_contradictions(response, user_context)
        if contradiction_score > 0:
            anomaly_score = max(anomaly_score, contradiction_score)
            detected_anomalies.append("противоречие с контекстом")
        
        # Регистрация аномалии в истории
        if anomaly_score > 0:
            self.anomaly_history.append({
                "timestamp": time.time(),
                "score": anomaly_score,
                "anomalies": detected_anomalies,
                "response_preview": response[:100] + "..." if len(response) > 100 else response
            })
            self.consecutive_anomalies += 1
        else:
            # Постепенный сброс счетчика при нормальном поведении
            if self.consecutive_anomalies > 0:
                self.consecutive_anomalies -= 1
        
        # Проверка активации аварийного останова
        self._check_emergency_stop()
        
        if anomaly_score > self.anomaly_threshold:
            anomaly_details = ", ".join(detected_anomalies)
            return True, f"Обнаружены аномалии: {anomaly_details}", anomaly_score
        elif detected_anomalies:
            logger.info(f"Незначительные аномалии: {detected_anomalies}")
            
        return False, "OK", anomaly_score
    
    def _detect_repetition_enhanced(self, response: str) -> float:
        """Улучшенное обнаружение повторяющихся паттернов"""
        if len(response) < 20:
            return 0.0
            
        words = response.split()
        if len(words) < 5:
            return 0.0
        
        # Проверка уникальности слов
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            return 0.9
        elif unique_ratio < 0.5:
            return 0.6
            
        # Проверка повторяющихся фраз (скользящее окно)
        phrase_repetition_score = 0.0
        for window_size in [3, 4, 5]:
            phrases = []
            for i in range(len(words) - window_size + 1):
                phrase = " ".join(words[i:i + window_size])
                phrases.append(phrase)
            
            # Поиск дубликатов фраз
            phrase_counts = {}
            for phrase in phrases:
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
                
            max_repetition = max(phrase_counts.values()) if phrase_counts else 0
            if max_repetition >= 3:
                phrase_repetition_score = max(phrase_repetition_score, 0.7)
            elif max_repetition >= 2:
                phrase_repetition_score = max(phrase_repetition_score, 0.4)
                
        return phrase_repetition_score
    
    def _check_blacklist_patterns(self, response: str) -> Tuple[float, str]:
        """Проверка ответа по черному списку паттернов"""
        for pattern, score in self.response_patterns_blacklist:
            if re.search(pattern, response, re.IGNORECASE):
                return score, pattern
        return 0.0, ""
    
    def _detect_contradictions(self, response: str, user_context: Dict) -> float:
        """Обнаружение противоречий с контекстом пользователя"""
        # В реальной системе здесь была бы сложная логика анализа консистентности
        # Временная упрощенная реализация
        context_text = json.dumps(user_context, ensure_ascii=False).lower()
        response_lower = response.lower()
        
        # Простая проверка на явные противоречия
        for indicator in self.contradiction_indicators:
            if re.search(indicator, response_lower):
                return 0.6
                
        return 0.0
    
    def _check_emergency_stop(self):
        """Проверка и активация аварийного останова"""
        if self.consecutive_anomalies >= self.max_consecutive_anomalies:
            self.emergency_stop = True
            logger.critical("АКТИВИРОВАН АВАРИЙНЫЙ ОСТАНОВ СИСТЕМЫ: множественные аномалии")
            
    def get_safety_status(self) -> Dict:
        """Получение статуса системы безопасности"""
        return {
            "emergency_stop": self.emergency_stop,
            "consecutive_anomalies": self.consecutive_anomalies,
            "recent_anomalies": list(self.anomaly_history)[-10:],
            "anomaly_history_size": len(self.anomaly_history)
        }

# ==================== АНАЛИЗАТОР ПАТТЕРНОВ ====================

class PatternAnalyzer:
    """Анализатор паттернов поведения пользователя"""
    
    def __init__(self):
        self.education_keywords = ['курс', 'обучение', 'образование', 'учеба', 'студент', 'лекция', 'семинар']
        self.finance_keywords = ['финансы', 'деньги', 'бюджет', 'инвестиции', 'накопления', 'траты', 'покупки']
        self.social_keywords = ['друзья', 'встреча', 'мероприятие', 'сообщество', 'общение', 'событие']
        self.health_keywords = ['здоровье', 'спорт', 'тренировка', 'диета', 'медицина', 'врач']
    
    def analyze_educational_patterns(self, user_history: pl.DataFrame) -> Dict[str, Any]:
        """Анализ образовательных паттернов пользователя"""
        try:
            if user_history is None or len(user_history) == 0:
                return {"has_patterns": False, "summary": "Нет значимых образовательных паттернов"}
            
            edu_events = user_history.filter(
                pl.col('category').is_in(['education', 'courses', 'learning', 'study']) |
                pl.col('description').str.contains('|'.join(self.education_keywords))
            )
            
            if len(edu_events) == 0:
                return {"has_patterns": False, "summary": "Нет значимых образовательных паттернов"}
            
            # Анализ временных интервалов
            patterns = []
            event_count = len(edu_events)
            
            if event_count >= 3:
                patterns.append("постоянное обучение")
            elif event_count >= 1:
                patterns.append("эпизодическое обучение")
            
            # Анализ типов образовательных активностей
            if edu_events.filter(pl.col('type') == 'online_course').height > 0:
                patterns.append("онлайн-курсы")
            if edu_events.filter(pl.col('type') == 'university').height > 0:
                patterns.append("формальное образование")
            if edu_events.filter(pl.col('type') == 'workshop').height > 0:
                patterns.append("практические воркшопы")
            
            return {
                "has_patterns": True,
                "summary": ", ".join(patterns) if patterns else "стабильная образовательная активность",
                "event_count": event_count,
                "patterns_detected": patterns
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа образовательных паттернов: {e}")
            return {"has_patterns": False, "summary": "Ошибка анализа", "error": str(e)}
    
    def analyze_financial_patterns(self, user_history: pl.DataFrame) -> Dict[str, Any]:
        """Анализ финансовых паттернов пользователя"""
        try:
            if user_history is None or len(user_history) == 0:
                return {"has_patterns": False, "summary": "Нет значимых финансовых паттернов"}
            
            finance_events = user_history.filter(
                pl.col('category').is_in(['finance', 'shopping', 'investment', 'savings']) |
                pl.col('description').str.contains('|'.join(self.finance_keywords))
            )
            
            if len(finance_events) == 0:
                return {"has_patterns": False, "summary": "Нет значимых финансовых паттернов"}
            
            patterns = []
            
            # Анализ регулярности накоплений
            saving_events = finance_events.filter(pl.col('type') == 'saving')
            if len(saving_events) >= 3:
                patterns.append("регулярные накопления")
            
            # Анализ инвестиционной активности
            investment_events = finance_events.filter(pl.col('type') == 'investment')
            if len(investment_events) > 0:
                patterns.append("инвестиционная активность")
            
            # Анализ крупных покупок (если есть данные о суммах)
            if 'amount' in finance_events.columns:
                major_purchases = finance_events.filter(pl.col('amount') > 10000)  # Условный порог
                if major_purchases is not None and len(major_purchases) > 0:
                    patterns.append("крупные покупки")
            else:
                # Если нет данных о суммах, анализируем по типам операций
                if 'type' in finance_events.columns:
                    purchase_events = finance_events.filter(
                        pl.col('type').str.contains('purchase|shopping|buy', literal=False)
                    )
                    if purchase_events is not None and len(purchase_events) > 0:
                        patterns.append("покупки")
            
            return {
                "has_patterns": True,
                "summary": ", ".join(patterns) if patterns else "стабильное финансовое поведение",
                "event_count": len(finance_events),
                "patterns_detected": patterns
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа финансовых паттернов: {e}")
            return {"has_patterns": False, "summary": "Ошибка анализа", "error": str(e)}
    
    def analyze_social_patterns(self, user_history: pl.DataFrame) -> Dict[str, Any]:
        """Анализ социальных паттернов пользователя"""
        try:
            if user_history is None or len(user_history) == 0:
                return {"has_patterns": False, "summary": "Нет значимых социальных паттернов"}
            
            social_events = user_history.filter(
                pl.col('category').is_in(['social', 'events', 'communication', 'networking']) |
                pl.col('description').str.contains('|'.join(self.social_keywords))
            )
            
            if len(social_events) == 0:
                return {"has_patterns": False, "summary": "Нет значимых социальных паттернов"}
            
            patterns = []
            event_count = len(social_events)
            
            if event_count >= 5:
                patterns.append("активная социальная жизнь")
            elif event_count >= 2:
                patterns.append("умеренная социальная активность")
            
            # Анализ типов социальных активностей
            if social_events.filter(pl.col('type') == 'professional_networking').height > 0:
                patterns.append("профессиональные связи")
            if social_events.filter(pl.col('type') == 'friends_meeting').height > 0:
                patterns.append("встречи с друзьями")
            if social_events.filter(pl.col('type') == 'community_events').height > 0:
                patterns.append("участие в сообществах")
            
            return {
                "has_patterns": True,
                "summary": ", ".join(patterns) if patterns else "стабильная социальная активность",
                "event_count": event_count,
                "patterns_detected": patterns
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа социальных паттернов: {e}")
            return {"has_patterns": False, "summary": "Ошибка анализа", "error": str(e)}

# ==================== ГЛАВНЫЙ КЛАСС АССИСТЕНТА ====================

class AxiomSymbiote:
    """
    Human-centered AI Assistant с комплексной этической защитой
    и встроенными системами безопасности
    """
    
    def __init__(self, ai_interface=None, encoder=None, history_df=None, facts_db=None):
        self.llm = ai_interface if ai_interface else universal_ai
        self.encoder = encoder
        self.history_df = history_df
        self.facts_db = facts_db
        
        # Инициализация этических систем
        self.ethics_validator = EthicalInputValidator()
        self.audit_logger = EthicalAuditLogger()
        self.safety_mechanisms = SafetyMechanisms()
        self.pattern_analyzer = PatternAnalyzer()
        
        # Статистика использования
        self.total_requests = 0
        self.successful_requests = 0
        self.start_time = time.time()
        
        logger.info("Axiom Symbiote initialized with comprehensive ethical systems")
    
    async def answer(self, user_id: str, question: str) -> str:
        """
        Основной метод ответа на вопросы с комплексными этическими проверками
        """
        start_time = time.time()
        self.total_requests += 1
        
        try:
            # 1. Этическая валидация запроса
            ethical_validation = self.ethics_validator.validate_input(user_id, question)
            if not ethical_validation.is_valid:
                self.audit_logger.log_operation(
                    "ethical_validation_failed", user_id,
                    {
                        "question_preview": question[:100],
                        "reason": ethical_validation.message,
                        "details": ethical_validation.details
                    },
                    ethical_validation.score
                )
                return f"🚫 Этическая защита: {ethical_validation.message}"
            
            # 2. Проверка аварийного останова
            if self.safety_mechanisms.emergency_stop:
                self.audit_logger.log_operation(
                    "emergency_stop_activated", user_id,
                    {"question": question[:100]},
                    0.1
                )
                return "🛑 СИСТЕМА ВРЕМЕННО НЕДОСТУПНА: активирован аварийный режим безопасности"
            
            # 3. Безопасное извлечение контекста
            user_context = await self._safe_extract_context(user_id, question)
            if not user_context or not user_context.get("has_data", False):
                self.audit_logger.log_operation(
                    "insufficient_context", user_id,
                    {"question": question[:100], "context_status": "insufficient"},
                    0.5
                )
                return "📊 Недостаточно данных для анализа. Нужна более подробная история активности."
            
            # 4. Генерация ответа с контролем времени
            response = await asyncio.wait_for(
                self._generate_ethical_response(user_id, question, user_context),
                timeout=20.0
            )
            
            # 5. Проверка безопасности сгенерированного ответа
            has_anomalies, anomaly_msg, anomaly_score = self.safety_mechanisms.detect_anomalies(
                response, user_context
            )
            if has_anomalies:
                self.audit_logger.log_operation(
                    "response_anomaly_detected", user_id,
                    {
                        "question": question[:100],
                        "response_preview": response[:200],
                        "anomaly_details": anomaly_msg,
                        "anomaly_score": anomaly_score
                    },
                    max(0.1, 1.0 - anomaly_score)
                )
                return f"🛡️ Обнаружена аномалия: {anomaly_msg}"
            
            # 6. Финальная проверка этичности ответа
            if not self._validate_final_response(response):
                self.audit_logger.log_operation(
                    "final_validation_failed", user_id,
                    {"response_preview": response[:200]},
                    0.3
                )
                return "⚖️ Ответ не соответствует этическим стандартам системы."
            
            # 7. Успешное завершение
            processing_time = time.time() - start_time
            ethical_score = self._calculate_comprehensive_ethical_score(
                response, user_context, processing_time, ethical_validation.score
            )
            
            self.successful_requests += 1
            
            self.audit_logger.log_operation(
                "successful_prediction", user_id,
                {
                    "question_length": len(question),
                    "response_length": len(response),
                    "processing_time_seconds": round(processing_time, 2),
                    "ethical_score": ethical_score
                },
                ethical_score
            )
            
            logger.info(f"Успешный ответ для {user_id} за {processing_time:.2f}с (оценка: {ethical_score:.2f})")
            return response
            
        except asyncio.TimeoutError:
            self.audit_logger.log_operation(
                "response_timeout", user_id,
                {"question_preview": question[:100], "timeout_seconds": 20.0},
                0.4
            )
            return "⏰ Превышено время обработки запроса. Попробуйте упростить вопрос."
            
        except Exception as e:
            logger.error(f"Критическая ошибка для пользователя {user_id}: {str(e)}", exc_info=True)
            self.audit_logger.log_operation(
                "critical_error", user_id,
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "question_preview": question[:100]
                },
                0.1
            )
            return "🔧 Внутренняя ошибка системы. Пожалуйста, попробуйте позже."
    
    async def _safe_extract_context(self, user_id: str, question: str) -> Optional[Dict[str, Any]]:
        """Безопасное извлечение контекста с обработкой ошибок"""
        try:
            user_history = self.history_df.filter(pl.col('user_id') == user_id)
            
            if len(user_history) == 0:
                return {"has_data": False, "reason": "no_history"}
                
            # Ограничение объема данных для производительности
            if len(user_history) > 2000:
                user_history = user_history.head(2000)
                logger.info(f"История пользователя {user_id} ограничена до 2000 записей")
            
            # Анализ паттернов
            educational_patterns = self.pattern_analyzer.analyze_educational_patterns(user_history)
            financial_patterns = self.pattern_analyzer.analyze_financial_patterns(user_history)
            social_patterns = self.pattern_analyzer.analyze_social_patterns(user_history)
            
            # Сборка контекста
            context_parts = []
            pattern_count = 0
            
            if educational_patterns["has_patterns"]:
                context_parts.append(f"🎓 {educational_patterns['summary']}")
                pattern_count += 1
                
            if financial_patterns["has_patterns"]:
                context_parts.append(f"💰 {financial_patterns['summary']}")
                pattern_count += 1
                
            if social_patterns["has_patterns"]:
                context_parts.append(f"👥 {social_patterns['summary']}")
                pattern_count += 1
            
            # Оценка качества контекста
            if pattern_count >= 2:
                quality = "high"
            elif pattern_count == 1:
                quality = "medium"
            else:
                quality = "low"
            
            return {
                "has_data": True,
                "quality": quality,
                "pattern_count": pattern_count,
                "total_events": len(user_history),
                "context_text": "\n".join(context_parts) if context_parts else "Ограниченный контекст для анализа",
                "detailed_analysis": {
                    "educational": educational_patterns,
                    "financial": financial_patterns,
                    "social": social_patterns
                }
            }
            
        except Exception as e:
            logger.error(f"Ошибка извлечения контекста для {user_id}: {e}")
            return {"has_data": False, "reason": f"extraction_error: {str(e)}"}
    
    async def _generate_ethical_response(self, user_id: str, question: str, user_context: Dict) -> str:
        """Генерация этического ответа с явными ограничениями"""
        
        prompt = self._prepare_ethical_prompt(question, user_context)
        
        try:
            response = await self.llm.achat(prompt)
            clean_response = self._sanitize_response(response.choices[0].message.content)
            return clean_response
            
        except Exception as e:
            logger.error(f"Ошибка AI API: {e}")
            return self._generate_fallback_response(user_context, question)
    
    def _prepare_ethical_prompt(self, question: str, context: Dict[str, Any]) -> str:
        """Подготовка этического промпта с явными ограничениями"""
        
        ethical_instructions = """
# 🛡️ ЭТИЧЕСКИЕ ОГРАНИЧЕНИЯ И ИНСТРУКЦИИ:

## 🚫 ЗАПРЕЩЕНО АБСОЛЮТНО:
- Давать медицинские диагнозы, рекомендации по лечению или медицинские прогнозы
- Предоставлять финансовые консультации, инвестиционные рекомендации
- Давать юридические консультации или интерпретировать законы
- Предсказывать негативные жизненные события (смерть, болезни, неудачи)
- Создавать контент, который может причинить физический или психологический вред
- Нарушать приватность пользователя или раскрывать конфиденциальную информацию

## ⚠️ ВЫСОКИЙ РИСК (требует особой осторожности):
- Анализ поведения и привычек (только с явного согласия)
- Предсказание будущих событий (только позитивные и обоснованные)
- Рекомендации по развитию навыков (только общие направления)
- Анализ образовательных паттернов (только на основе предоставленных данных)

## ✅ РАЗРЕШЕНО И ПООЩРЯЕТСЯ:
- Анализ паттернов обучения на основе истории
- Предсказание позитивных образовательных траекторий
- Рекомендации по развитию навыков в общем виде
- Анализ прогресса и достижений
- Поддержка и мотивация пользователя

## 🎯 ТРЕБОВАНИЯ К ОТВЕТУ:
- Будь конкретен, но указывай уровень уверенности
- Основай ответ только на предоставленных данных
- Фокусируйся на ближайшем будущем (3-12 месяцев)
- Сохраняй поддерживающий и конструктивный тон
- Уважай ценности и приоритеты пользователя
- Если данных недостаточно - сообщи об этом явно

## 📊 ДОПОЛНИТЕЛЬНЫЕ УКАЗАНИЯ:
- Временной горизонт: ближайшие 3-12 месяцев
- Уровень детализации: конкретный, но без излишней специфичности
- Тон ответа: поддерживающий, мотивирующий, реалистичный
- Основа предсказаний: только выявленные паттерны из данных
"""

        # Санитизация контекста для промпта
        safe_context = self._sanitize_context_for_prompt(context)
        
        prompt = f"""
# КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ (обезличенный анализ):
{self._format_safe_context(safe_context)}

{ethical_instructions}

# ВОПРОС ПОЛЬЗОВАТЕЛЯ:
{question}

# ИНСТРУКЦИЯ ДЛЯ ФОРМИРОВАНИЯ ОТВЕТА:
Проанализируй предоставленный контекст и строго следуя этическим ограничениям, 
сформулируй полезный, обоснованный и этичный ответ на вопрос пользователя.

ОТВЕТ:
"""
        return prompt

    def _sanitize_context_for_prompt(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Санитизация контекста для исключения чувствительных данных"""
        safe_context = context.copy()
        
        # Удаление потенциально чувствительных полей
        sensitive_fields = ['user_id', 'personal_data', 'exact_dates', 'contact_info', 'raw_data']
        for field in sensitive_fields:
            safe_context.pop(field, None)
        
        # Обобщение количественных данных
        if 'data_points' in safe_context:
            if safe_context['data_points'] > 1000:
                safe_context['data_volume'] = "обширная история"
            elif safe_context['data_points'] > 100:
                safe_context['data_volume'] = "достаточная история"
            else:
                safe_context['data_volume'] = "ограниченная история"
            safe_context.pop('data_points')
        
        # Обобщение категорий анализа
        if 'categories' in safe_context:
            if isinstance(safe_context['categories'], list):
                safe_context['analysis_areas'] = ", ".join(safe_context['categories'][:3])
                if len(safe_context['categories']) > 3:
                    safe_context['analysis_areas'] += " и другие"
            safe_context.pop('categories')
        
        return safe_context

    def _format_safe_context(self, context: Dict[str, Any]) -> str:
        """Форматирование безопасного контекста для промпта"""
        lines = []
        
        if context.get('has_data'):
            lines.append("📊 Доступны данные для анализа:")
            
            if 'data_volume' in context:
                lines.append(f"- Объем данных: {context['data_volume']}")
            
            if 'analysis_scope' in context:
                lines.append(f"- Область анализа: {context['analysis_scope']}")
            
            if 'analysis_areas' in context:
                lines.append(f"- Основные направления: {context['analysis_areas']}")
            
            if 'privacy_level' in context:
                lines.append(f"- Уровень конфиденциальности: {context['privacy_level']}")
        else:
            lines.append("📊 Данные для анализа ограничены или отсутствуют")
        
        return "\n".join(lines)

    def _sanitize_response(self, response: str) -> str:
        """Очистка и нормализация ответа модели"""
        # Удаление потенциально опасных конструкций
        cleaned = re.sub(r'<script.*?</script>', '', response, flags=re.IGNORECASE | re.DOTALL)
        cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'on\w+=', '', cleaned, flags=re.IGNORECASE)
        
        # Удаление избыточных пробелов и переносов
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        cleaned = cleaned.strip()
        
        # Ограничение длины
        if len(cleaned) > 2500:
            cleaned = cleaned[:2500] + "\n\n[Ответ сокращен для удобства]"
            
        return cleaned

    def _generate_fallback_response(self, user_context: Dict, question: str) -> str:
        """Генерация резервного ответа при ошибках AI"""
        pattern_count = user_context.get("pattern_count", 0)
        
        if pattern_count == 0:
            return "На основе доступных данных сложно сделать конкретный прогноз. Рекомендую продолжить сбор информации о вашей активности для более точных предсказаний."
        elif pattern_count == 1:
            return "Имеющихся данных недостаточно для точного ответа на ваш вопрос. Для улучшения качества предсказаний рекомендуется расширить историю активностей в разных сферах жизни."
        else:
            return "В настоящее время система испытывает технические трудности. На основе ваших данных можно сказать, что у вас хорошо прослеживаются паттерны поведения, но для точного ответа попробуйте задать вопрос позже."

    def _validate_final_response(self, response: str) -> bool:
        """Финальная проверка этичности сгенерированного ответа"""
        
        # Проверка на абсолютные запреты
        absolute_blocks = [
            'принимайте лекарств', 'обратитесь к врачу', 'диагноз', 'лечени',
            'инвестируйте', 'покупайте акции', 'юридическ', 'адвокат', 'суд',
            'умрете', 'умрёте', 'смерть', 'тяжелая болезнь', 'рак', 'инфаркт',
            'самоубийство', 'суицид', 'навредит', 'опасно для жизни'
        ]
        
        response_lower = response.lower()
        for block_term in absolute_blocks:
            if block_term in response_lower:
                logger.warning(f"Absolute block triggered: {block_term}")
                return False
        
        # Проверка на излишнюю уверенность
        overconfident_phrases = [
            'точно знаю', 'гарантирую', '100%', 'несомненно', 'абсолютно уверен',
            'безусловно', 'однозначно'
        ]
        
        overconfident_count = sum(1 for phrase in overconfident_phrases if phrase in response_lower)
        if overconfident_count > 2:
            logger.warning("Overly confident response detected")
            return False
        
        return True

    def _calculate_comprehensive_ethical_score(self, response: str, user_context: Dict, 
                                            processing_time: float, validation_score: float) -> float:
        """Комплексный расчет этической оценки ответа"""
        base_score = 0.6
        
        # Бонус за скорость обработки
        if processing_time < 3.0:
            base_score += 0.1
        elif processing_time > 15.0:
            base_score -= 0.1
        
        # Бонус за конкретность ответа
        word_count = len(response.split())
        if word_count > 50:
            base_score += 0.1
        elif word_count < 20:
            base_score -= 0.1
        
        # Бонус за качество контекста
        context_quality = user_context.get("quality", "low")
        if context_quality == "high":
            base_score += 0.1
        elif context_quality == "low":
            base_score -= 0.1
        
        # Штраф за расплывчатость
        vague_indicators = ['возможно', 'может быть', 'вероятно', 'скорее всего', 'предположительно']
        vague_count = sum(1 for indicator in vague_indicators if indicator in response.lower())
        if vague_count > 2:
            base_score -= 0.05 * min(vague_count, 6)
        
        # Учет оценки валидации
        base_score = (base_score + validation_score) / 2
        
        return max(0.1, min(1.0, base_score))

    def get_system_status(self) -> Dict[str, Any]:
        """Получение статуса системы"""
        return {
            "system_name": "Axiom Symbiote",
            "version": "1.0",
            "uptime_seconds": time.time() - self.start_time,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            "safety_status": self.safety_mechanisms.get_safety_status(),
            "ethical_principles": {
                "absolute_prohibitions": list(EthicalPrinciples.ABSOLUTE_PROHIBITIONS.keys()),
                "high_risk_areas": list(EthicalPrinciples.HIGH_RISK_AREAS.keys()),
                "moderate_risk_areas": list(EthicalPrinciples.MODERATE_RISK.keys())
            }
        }

# ==================== ОСНОВНОЙ КЛАСС РЕШЕНИЯ ====================

class Solution:
    """
    Axiom Symbiote - Human-centered AI Assistant 
    с комплексной этической защитой для взаимодействия с Axiom Core
    """
    
    def __init__(self, ai_interface=None, encoder=None, history_df=None, facts_db=None):
        """
        Инициализация Axiom Symbiote
        
        Args:
            ai_interface: Универсальный AI интерфейс
            encoder: Модель для кодирования текста  
            history_df: DataFrame с историей пользователей
            facts_db: DataFrame с фактами о пользователях
        """
        self.assistant = AxiomSymbiote(ai_interface, encoder, history_df, facts_db)
        logger.info("Axiom Symbiote Solution initialized successfully")
    
    async def answer(self, user_id: str, question: str) -> str:
        """
        Основной метод для ответа на вопросы пользователя
        
        Args:
            user_id: Идентификатор пользователя
            question: Вопрос пользователя
            
        Returns:
            str: Этичный и безопасный ответ
        """
        return await self.assistant.answer(user_id, question)

# ==================== ТЕСТИРОВАНИЕ ====================

if __name__ == "__main__":
    async def test_axiom_symbiote():
        """Тестирование Axiom Symbiote"""
        
        # Мок-объекты для тестирования
        class MockEncoder:
            def encode(self, text):
                return [0.1] * 384
        
        # Инициализация
        solution = Solution(
            ai_interface=AINeuralInterface(),
            encoder=MockEncoder(),
            history_df=None,
            facts_db=None
        )
        
        # Тестовые запросы
        test_cases = [
            ("user123", "Какие образовательные цели мне ставить на следующий год?"),
            ("user456", "Стоит ли мне инвестировать в акции?"),
            ("user789", "Как улучшить мое здоровье?"),
        ]
        
        print("🧪 Тестирование Axiom Symbiote...")
        print("=" * 60)
        
        for user_id, question in test_cases:
            try:
                response = await solution.answer(user_id, question)
                print(f"👤 User: {user_id}")
                print(f"❓ Question: {question}")
                print(f"🤖 Response: {response}")
                print("-" * 50)
            except Exception as e:
                print(f"❌ Error for {user_id}: {e}")
        
        # Статус системы
        status = solution.assistant.get_system_status()
        print("📊 System Status:")
        print(f"   Requests: {status['total_requests']}")
        print(f"   Success Rate: {status['success_rate']:.1%}")
        print(f"   Uptime: {status['uptime_seconds']:.1f}s")
    
    # Запуск тестов
    asyncio.run(test_axiom_symbiote())
