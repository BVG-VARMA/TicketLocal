#!/usr/bin/env bash
echo "==================================================="
echo "TicketLocal - Setup Environment Configuration"
echo "==================================================="
if [ ! -f "backend/.env" ]; then
    cp .env.example backend/.env
    echo "[OK] Created backend/.env from .env.example"
else
    echo "[INFO] backend/.env already exists."
fi
echo ""
echo "Ready! You can now start the backend and frontend."
