@echo off
title Thanos Sealed Secrets CLI

:menu
cls
echo ========================================================================
echo                     THANOS SEALED SECRETS CLI TOOL      
echo ========================================================================
echo.
echo [1] Seal a Secret
echo [2] Decrypt a Secret
echo [3] Decode base64 String
echo [0] Exit
echo.
set /p choice=Enter your choice: 

if "%choice%"=="1" (
    echo.
    .\seal.exe
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    .\decrypt.exe
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    .\decode.exe
    pause
    goto menu
)

if "%choice%"=="0" (
    echo Exiting...
    exit
)

echo Invalid choice.
pause
goto menu
