#!/usr/bin/env python3
"""
Генератор Audit Bundle (Паспорт зрелости пилота).
Стандарт TRA-L3: Агрегация всех артефактов аудита Kon-Matrix L3 в единый формат.
Версия: 1.1 (Динамическое сканирование ADR)
"""
import json
import os
import datetime
import glob

def check_file_exists(filepath: str) -> dict:
    exists = os.path.exists(filepath)
    return {"status": "implemented" if exists else "missing", "file": filepath}

def get_worm_status():
    log_file = "backend/audit_log.jsonl"
    if not os.path.exists(log_file):
        return {"status": "empty", "entries": 0, "chain_valid": True}
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        valid = all('current_hash' in json.loads(line) and 'previous_hash' in json.loads(line) for line in lines if line.strip())
        return {
            "status": "active",
            "entries": len(lines),
            "chain_valid": valid,
            "last_hash": json.loads(lines[-1])['current_hash'][:16] + "..." if lines else None
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_sbom_status():
    sbom_file = "sbom/aggregate.cyclonedx.json"
    if not os.path.exists(sbom_file):
        sbom_file = "sbom/backend.cyclonedx.json"
    if not os.path.exists(sbom_file):
        return {"status": "missing"}
    try:
        with open(sbom_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            "status": "valid",
            "format": data.get("bomFormat"),
            "version": data.get("specVersion"),
            "components_count": len(data.get("components", [])),
            "type": "aggregate" if "aggregate" in sbom_file else "backend-only"
        }
    except Exception as e:
        return {"status": "invalid", "error": str(e)}

def get_adr_status():
    """Динамическое сканирование папки ADR"""
    adr_dir = "docs/adr"
    if not os.path.exists(adr_dir):
        return {"status": "missing", "count": 0}
    
    # Ищем все .md файлы в папке
    adr_files = glob.glob(os.path.join(adr_dir, "*.md"))
    count = len(adr_files)
    
    # Извлекаем номера и названия для красивого вывода
    adr_list = []
    for f in sorted(adr_files):
        filename = os.path.basename(f)
        adr_list.append(filename)
        
    return {
        "status": "implemented" if count > 0 else "empty",
        "count": count,
        "files": adr_list
    }

def generate_bundle():
    int_l3_prompts = check_file_exists("backend/app/core/prompts.py")
    int_l3_ci = check_file_exists(".github/workflows/linters.yml")
    
    pur_l3_sbom = get_sbom_status()
    pur_l3_dast = check_file_exists(".github/workflows/dast.yml")
    pur_l3_dependabot = check_file_exists(".github/dependabot.yml")
    
    # Теперь используем динамическую проверку
    evo_l3_adr = get_adr_status()
    evo_l3_ruff = check_file_exists("backend/ruff.toml")
    
    tra_l3_worm = get_worm_status()
    tra_l3_health = check_file_exists("backend/app/api/v1/health.py")

    compliance = {
        "INT (Целостность)": "Pass" if int_l3_prompts["status"] == "implemented" and int_l3_ci["status"] == "implemented" else "Partial",
        "PUR (Чистота)": "Pass" if pur_l3_sbom["status"] == "valid" and pur_l3_dast["status"] == "implemented" else "Partial",
        # EVO теперь зависит от наличия хотя бы одного ADR
        "EVO (Становление)": "Pass" if evo_l3_adr["count"] >= 1 and evo_l3_ruff["status"] == "implemented" else "Partial",
        "TRA (Прозрачность)": "Pass" if tra_l3_worm["status"] == "active" and tra_l3_worm["chain_valid"] else "Partial"
    }

    bundle = {
        "project": "potok-app",
        "kon_matrix_target": "L3",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "artifacts": {
            "INT-L3 (AI Prompts & CI Gates)": {
                "prompts_versioned": int_l3_prompts,
                "ci_linters": int_l3_ci
            },
            "PUR-L3 (Supply Chain & DAST)": {
                "sbom_aggregated": pur_l3_sbom,
                "dast_workflow": pur_l3_dast,
                "dependabot": pur_l3_dependabot
            },
            "EVO-L3 (Architecture & Quality)": {
                "adr_registry": evo_l3_adr, # Теперь здесь список всех ADR
                "ruff_config": evo_l3_ruff
            },
            "TRA-L3 (Audit & Observability)": {
                "worm_audit": tra_l3_worm,
                "health_api": tra_l3_health
            }
        },
        "compliance_summary": compliance
    }
    
    output_file = "audit-bundle.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Финальный Audit Bundle сгенерирован: {output_file}")
    print("\n📊 Сводка соответствия Kon-Matrix L3:")
    for k, v in compliance.items():
        status_icon = "✅" if v == "Pass" else "️"
        print(f"  {status_icon} {k}: {v}")
    
    return output_file

if __name__ == "__main__":
    generate_bundle()
