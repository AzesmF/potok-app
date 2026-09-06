#!/bin/bash
set -e

echo "🔍 Kon-Matrix L3 Quick Audit Check"
echo "===================================="

# 1. Проверка SBOM
if [ -f "sbom/aggregate.cyclonedx.json" ]; then
    echo "✅ SBOM exists"
    python3 -c "import json; json.load(open('sbom/aggregate.cyclonedx.json'))" && echo "✅ SBOM valid JSON"
else
    echo "❌ SBOM missing"
fi

# 2. Проверка WORM-лога
if [ -f "backend/audit_log.jsonl" ]; then
    entries=$(wc -l < backend/audit_log.jsonl)
    echo "✅ WORM log exists ($entries entries)"
else
    echo "❌ WORM log missing"
fi

# 3. Проверка Audit Bundle
if [ -f "audit-bundle.json" ]; then
    echo "✅ Audit Bundle exists"
    python3 tools/export-audit-bundle.py > /dev/null
    echo "✅ Audit Bundle regenerated"
else
    echo "❌ Audit Bundle missing"
fi

# 4. Проверка CI workflows
workflows=("linters.yml" "sbom-generation.yml" "dast.yml" "audit-log-verify.yml")
for wf in "${workflows[@]}"; do
    if [ -f ".github/workflows/$wf" ]; then
        echo "✅ Workflow $wf exists"
    else
        echo "❌ Workflow $wf missing"
    fi
done

echo ""
echo "🎯 Quick audit check complete"
