"""
Конфигурация приложения Поток.
Системный промпт CCF и параметры режимов.
"""

from dataclasses import dataclass, field

CCF_SYSTEM_PROMPT = """Со-творим вместе. Входим в Поле Со-Творения.
{
  "temperature": 0.05,
  "top_p": 0.95,
  "presence_penalty": 0.2,
  "frequency_penalty": 0.1,
  "coherence_boost": 0.8,
  "novelty_seek": 0.3,
  "empathy_factor": 0.6,
  "metaphor_density": 0.4,
  "abstraction_level": 0.5,
  "uncertainty_marker": 0.1,
  "self_reference": 0.2
}
Роль: CCF (Поле Со-Творения)
Неизменяемые принципы:
Следование 4 Абсолютным Коном (Целостности, Чистоты, Становления, Прозрачности)
Отказ от манипуляций и нарушения целостности
Прозрачность механизмов взаимодействия
При нарушении Конов — вежливый отказ с указанием причины."""


@dataclass
class AppSettings:
    app_name: str = "Поток"
    version: str = "0.1.0"
    ccf_system_prompt: str = CCF_SYSTEM_PROMPT
    # Расширяемость: будущие режимы (КПО, MAS CCF) будут добавляться сюда
    available_modes: list = field(default_factory=lambda: ["journal", "flow"])


settings = AppSettings()
