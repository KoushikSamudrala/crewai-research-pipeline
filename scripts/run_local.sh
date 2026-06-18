#!/usr/bin/env bash
set -e

echo "Starting FastAPI backend on :8000 ..."
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting Streamlit frontend on :8501 ..."
streamlit run frontend/app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "========================================="
echo "  Backend  →  http://localhost:8000"
echo "  API Docs →  http://localhost:8000/docs"
echo "  Frontend →  http://localhost:8501"
echo "========================================="
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
