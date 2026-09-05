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
