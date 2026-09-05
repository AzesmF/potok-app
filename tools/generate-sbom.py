#!/usr/bin/env python3
"""
Генератор SBOM (Software Bill of Materials) в формате CycloneDX 1.4.
Реализует стандарт PUR-L3: независимый аудит состава ПО.
"""
import json
import hashlib
import datetime
import os
import re

def parse_requirements(file_path: str) -> list:
    """Парсит requirements.txt и извлекает пакеты и версии"""
    components = []
    if not os.path.exists(file_path):
        return components
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Простой парсинг имени и версии (например, fastapi==0.100.0)
            match = re.match(r'^([a-zA-Z0-9_-]+)==([0-9.]+)', line)
            if match:
                name, version = match.groups()
                components.append({
                    "type": "library",
                    "name": name,
                    "version": version,
                    "purl": f"pkg:pypi/{name}@{version}"
                })
            else:
                # Если версии нет, берем только имя
                name = re.match(r'^([a-zA-Z0-9_-]+)', line)
                if name:
                    components.append({
                        "type": "library",
                        "name": name.group(1),
                        "version": "unknown",
                        "purl": f"pkg:pypi/{name.group(1)}"
                    })
    return components

def generate_sbom():
    """Генерирует CycloneDX 1.4 SBOM для backend"""
    req_file = "backend/requirements.txt"
    components = parse_requirements(req_file)
    
    # Генерируем уникальный серийный номер на основе хеша компонентов
    comp_str = json.dumps(components, sort_keys=True)
    serial_number = f"urn:uuid:{hashlib.md5(comp_str.encode()).hexdigest()}"
    
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": serial_number,
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "Kon-Matrix",
                    "name": "generate-sbom.py",
                    "version": "1.0.0"
                }
            ],
            "component": {
                "type": "application",
                "name": "potok-app-backend",
                "version": "0.2.0",
                "description": "Пилотный проект методологии KON-MATRIX: дневник с квантовой памятью"
            }
        },
        "components": components
    }
    
    # Сохраняем в файл
    output_file = "sbom/backend.cyclonedx.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sbom, f, indent=2, ensure_ascii=False)
        
    print(f"✅ SBOM успешно сгенерирован: {output_file}")
    print(f"📦 Найдено компонентов: {len(components)}")
    return output_file

if __name__ == "__main__":
    generate_sbom()
