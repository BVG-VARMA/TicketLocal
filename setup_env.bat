@echo off
echo ===================================================
echo TicketLocal - Setup Environment Configuration
echo ===================================================
if not exist "backend\.env" (
    copy ".env.example" "backend\.env"
    echo [OK] Created backend\.env from .env.example
) else (
    echo [INFO] backend\.env already exists.
)
echo.
echo Ready! You can now start the backend and frontend.
pause
