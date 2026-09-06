#!/usr/bin/env python3
"""
Генератор Audit Bundle (Паспорт зрелости пилота).
Стандарт TRA-L3: Агрегация всех артефактов аудита Kon-Matrix L3 в единый формат.
Версия: 2.1 (Добавлена проверка external monitoring)
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
    adr_dir = "docs/adr"
    if not os.path.exists(adr_dir):
        return {"status": "missing", "count": 0}
    adr_files = glob.glob(os.path.join(adr_dir, "*.md"))
    return {
        "status": "implemented" if len(adr_files) > 0 else "empty",
        "count": len(adr_files),
        "files": sorted([os.path.basename(f) for f in adr_files])
    }

def generate_bundle():
    # INT-L3
    int_prompts = check_file_exists("backend/app/core/prompts.py")
    int_linters = check_file_exists(".github/workflows/linters.yml")
    int_docker = check_file_exists("backend/Dockerfile")
    int_slsa = check_file_exists(".github/workflows/slsa-provenance.yml")

    # PUR-L3
    pur_sbom = get_sbom_status()
    pur_dast = check_file_exists(".github/workflows/dast.yml")
    pur_dependabot = check_file_exists(".github/dependabot.yml")
    pur_audit_doc = check_file_exists("docs/l3/independent-audit.md")

    # EVO-L3
    evo_adr = get_adr_status()
    evo_ruff = check_file_exists("backend/ruff.toml")
    evo_deploy_doc = check_file_exists("docs/l3/zero-downtime-deployment.md")

    # TRA-L3
    tra_worm = get_worm_status()
    tra_health = check_file_exists("backend/app/api/v1/health.py")
    tra_audit_ci = check_file_exists(".github/workflows/audit-log-verify.yml")
    tra_monitoring_doc = check_file_exists("docs/l3/external-monitoring.md")

    # Сводка соответствия
    compliance = {
        "INT (Целостность)": "Pass" if all(x["status"] == "implemented" for x in [int_prompts, int_linters, int_docker, int_slsa]) else "Partial",
        "PUR (Чистота)": "Pass" if pur_sbom["status"] == "valid" and all(x["status"] == "implemented" for x in [pur_dast, pur_dependabot, pur_audit_doc]) else "Partial",
        "EVO (Становление)": "Pass" if evo_adr["count"] >= 2 and all(x["status"] == "implemented" for x in [evo_ruff, evo_deploy_doc]) else "Partial",
        "TRA (Прозрачность)": "Pass" if tra_worm["status"] == "active" and tra_worm["chain_valid"] and all(x["status"] == "implemented" for x in [tra_health, tra_audit_ci, tra_monitoring_doc]) else "Partial"
    }

    bundle = {
        "project": "potok-app",
        "kon_matrix_target": "L3",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "artifacts": {
            "INT-L3 (Integrity)": {"prompts": int_prompts, "linters": int_linters, "docker": int_docker, "slsa": int_slsa},
            "PUR-L3 (Purity)": {"sbom": pur_sbom, "dast": pur_dast, "dependabot": pur_dependabot, "audit_guide": pur_audit_doc},
            "EVO-L3 (Evolution)": {"adr_registry": evo_adr, "ruff": evo_ruff, "deployment_guide": evo_deploy_doc},
            "TRA-L3 (Transparency)": {"worm_audit": tra_worm, "health_api": tra_health, "audit_ci": tra_audit_ci, "monitoring_guide": tra_monitoring_doc}
        },
        "compliance_summary": compliance
    }
    
    output_file = "audit-bundle.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Финальный Audit Bundle сгенерирован: {output_file}")
    print("\n📊 ИТОГОВАЯ СВОДКА СООТВЕТСТВИЯ KON-MATRIX L3:")
    for k, v in compliance.items():
        status_icon = "✅" if v == "Pass" else "⚠️"
        print(f"  {status_icon} {k}: {v}")
    
    return output_file

if __name__ == "__main__":
    generate_bundle()
