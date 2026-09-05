#!/usr/bin/env python3
"""
Генератор Агрегированного SBOM (Software Bill of Materials) в формате CycloneDX 1.4.
Стандарт PUR-L3: Единый аудит состава всего monorepo (Backend + Frontend).
"""
import json
import hashlib
import datetime
import os
import re

def parse_requirements(file_path: str) -> list:
    components = []
    if not os.path.exists(file_path):
        return components
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^([a-zA-Z0-9_-]+)==([0-9.]+)', line)
            if match:
                name, version = match.groups()
                components.append({"type": "library", "name": name, "version": version, "purl": f"pkg:pypi/{name}@{version}"})
    return components

def parse_pubspec(file_path: str) -> list:
    components = []
    if not os.path.exists(file_path):
        return components
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Простой парсинг секции dependencies в pubspec.yaml
    deps_match = re.search(r'dependencies:\s*\n((?:\s+[a-zA-Z0-9_-]+:.*\n)+)', content)
    if deps_match:
        deps_block = deps_match.group(1)
        for line in deps_block.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Формат: package_name: ^1.0.0 или package_name:
            match = re.match(r'^([a-zA-Z0-9_-]+):\s*(?:\^\s*)?([0-9.]+)?', line)
            if match:
                name = match.group(1)
                version = match.group(2) or "unknown"
                components.append({"type": "library", "name": name, "version": version, "purl": f"pkg:pub/{name}@{version}"})
    return components

def generate_aggregate_sbom():
    backend_comps = parse_requirements("backend/requirements.txt")
    frontend_comps = parse_pubspec("frontend/pubspec.yaml")
    
    all_components = backend_comps + frontend_comps
    
    # Генерируем уникальный серийный номер
    comp_str = json.dumps(all_components, sort_keys=True)
    serial_number = f"urn:uuid:{hashlib.md5(comp_str.encode()).hexdigest()}"
    
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": serial_number,
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "tools": [{"vendor": "Kon-Matrix", "name": "generate-sbom.py", "version": "2.0.0"}],
            "component": {
                "type": "application",
                "name": "potok-app-monorepo",
                "version": "0.3.0",
                "description": "Агрегированный SBOM пилотного проекта KON-MATRIX"
            }
        },
        "components": all_components
    }
    
    os.makedirs("sbom", exist_ok=True)
    output_file = "sbom/aggregate.cyclonedx.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sbom, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Агрегированный SBOM сгенерирован: {output_file}")
    print(f"📦 Всего компонентов: {len(all_components)} (Backend: {len(backend_comps)}, Frontend: {len(frontend_comps)})")

if __name__ == "__main__":
    generate_aggregate_sbom()
