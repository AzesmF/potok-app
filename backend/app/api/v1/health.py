"""
Health Check и Audit API (Стандарт TRA-L3)
"""

import logging

from fastapi import APIRouter

from app.services.worm_logger import get_worm_logger

logger = logging.getLogger("potok.health")
router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Проверка состояния системы (L3 Standard)"""
    worm_logger = get_worm_logger()
    is_chain_valid = worm_logger.verify_chain()

    return {
        "status": "healthy",
        "components": {
            "database": "ok",
            "quantum_memory": "ok",
            "worm_logger": "ok" if is_chain_valid else "compromised",
        },
        "kon_matrix_compliance": {"TRA-L3": "PASS" if is_chain_valid else "FAIL"},
    }


@router.get("/api/v1/audit-log")
async def get_audit_log(limit: int = 50):
    """Экспорт последних записей аудита (L3 Standard)"""
    worm_logger = get_worm_logger()
    logs = worm_logger.get_recent_logs(limit=limit)

    return {"total": len(logs), "chain_valid": worm_logger.verify_chain(), "logs": logs}

import os
import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse, FileResponse

@router.get("/passport")
async def get_kon_matrix_passport():
    """
    TRA-L3: Экспорт Паспорта зрелости Kon-Matrix в реальном времени.
    """
    # Путь относительно корня проекта (предполагаем запуск из корня или настраиваем абсолютный)
    # Для надежности используем относительный путь от текущего файла
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
    bundle_path = os.path.join(project_root, "audit-bundle.json")
    
    if not os.path.exists(bundle_path):
        raise HTTPException(
            status_code=404, 
            detail="Audit bundle not found. Please run tools/export-audit-bundle.py first."
        )
    
    with open(bundle_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return JSONResponse(content=data)

@router.get("/sbom")
async def get_sbom_file():
    """
    TRA-L3: Экспорт агрегированного SBOM (CycloneDX) для аудита цепочки поставок.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
    
    # Приоритет: агрегированный SBOM, затем бэкенд-специфичный
    sbom_path = os.path.join(project_root, "sbom", "aggregate.cyclonedx.json")
    if not os.path.exists(sbom_path):
        sbom_path = os.path.join(project_root, "sbom", "backend.cyclonedx.json")
        
    if not os.path.exists(sbom_path):
        raise HTTPException(
            status_code=404, 
            detail="SBOM not found. Please run tools/generate-sbom.py first."
        )
    
    return FileResponse(
        sbom_path, 
        media_type="application/json", 
        filename="sbom.cyclonedx.json"
    )
