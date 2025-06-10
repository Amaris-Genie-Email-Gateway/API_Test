@echo off
echo ===============================
echo Checking Local LLM (Ollama) Environment
echo ===============================

:: Check CPU info using PowerShell
echo.
echo --- CPU Info ---
powershell -Command "Get-CimInstance Win32_Processor | Select-Object -Property Name, NumberOfCores, NumberOfLogicalProcessors"

:: Check Memory info using PowerShell
echo.
echo --- Memory Info ---
powershell -Command "Get-CimInstance Win32_OperatingSystem | ForEach-Object { 'Total: ' + [math]::Round($_.TotalVisibleMemorySize / 1MB, 2) + ' GB'; 'Free: ' + [math]::Round($_.FreePhysicalMemory / 1MB, 2) + ' GB' }"

:: Check GPU info using PowerShell
echo.
echo --- GPU Info ---
powershell -Command "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM"

:: Check Python version
echo.
echo --- Python Version ---
python --version 2>NUL || echo Python is not installed or not in PATH

:: Check if virtual environment is active
echo.
echo --- Virtual Environment ---
if defined VIRTUAL_ENV (
    echo Active virtual environment: %VIRTUAL_ENV%
) else (
    echo No virtual environment detected.
)

:: Check if Ollama is installed (in PATH)
echo.
echo --- Ollama Installation ---
where ollama >nul 2>&1 && (
    echo Ollama is installed at:
    where ollama
) || (
    echo Ollama is NOT installed or not in PATH.
)

:: Check if Ollama port is in use (default 11434)
echo.
echo --- Checking if port 11434 is in use ---
netstat -ano | findstr :11434 > nul
if %errorlevel%==0 (
    echo Port 11434 is in use.
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr :11434') do (
        set PID=%%i
        tasklist /FI "PID eq %%i"
    )
) else (
    echo Port 11434 is available.
)

:: List all listening IPv4 ports
@REM echo.
@REM echo --- Active Listening Ports ---
@REM netstat -an | findstr LISTENING | findstr /R "^ *TCP"

echo.
echo ===============================
echo Environment check completed.
pause
