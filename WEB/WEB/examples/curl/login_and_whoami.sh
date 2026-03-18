set -e

BASE="${BASE:-http://localhost:8000}"

echo "NOTE: auth_service is a separate service in this scaffold."
echo "This script calls gateway whoami with a placeholder token if you wire it."
echo
curl -sS "$BASE/health" | python -m json.tool

