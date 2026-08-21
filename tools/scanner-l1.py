#!/usr/bin/env python3
"""
KON-MATRIX L1 Scanner
Проверка базового уровня зрелости (Целостность и Чистота)
"""

import os
import sys
from pathlib import Path

def check_required_files():
    """Проверяет наличие обязательных файлов"""
    required = [
        "README.md",
        "LICENSE",
        "docs/adr/0001-use-flutter-and-fastapi.md"
    ]
    
    missing = []
    for file in required:
        if not Path(file).exists():
            missing.append(file)
    
    return missing

def check_directory_structure():
    """Проверяет базовую структуру репозитория"""
    required_dirs = [
        "backend",
        "backend/app",
        "docs",
        "docs/adr",
        "tools"
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).is_dir():
            missing.append(dir_path)
    
    return missing

def main():
    print("=" * 60)
    print("KON-MATRIX L1 Scanner - Проверка целостности")
    print("=" * 60)
    
    errors = []
    
    # Проверка обязательных файлов
    print("\n[1/2] Проверка обязательных файлов...")
    missing_files = check_required_files()
    if missing_files:
        errors.append(f"Отсутствуют файлы: {', '.join(missing_files)}")
        print(f"❌ Отсутствуют: {', '.join(missing_files)}")
    else:
        print("✅ Все обязательные файлы присутствуют")
    
    # Проверка структуры директорий
    print("\n[2/2] Проверка структуры репозитория...")
    missing_dirs = check_directory_structure()
    if missing_dirs:
        errors.append(f"Отсутствуют директории: {', '.join(missing_dirs)}")
        print(f"❌ Отсутствуют: {', '.join(missing_dirs)}")
    else:
        print("✅ Структура репозитория корректна")
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if errors:
        print("❌ ПРОВЕРКА НЕ ПРОЙДЕНА")
        for error in errors:
            print(f"  - {error}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ ПРОВЕРКА ПРОЙДЕНА УСПЕШНО (L1)")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
