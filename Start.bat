@echo off
title MyAnimeList & Nekopoi Scrapper by TheKingTermux
cd /d %~dp0

:menu
cls
echo ===================================
echo  MyAnimeList and Nekopoi Scrapper
echo ===================================
echo.
echo 1. Jalankan Scraper
echo 2. Install Requirements
echo 3. Keluar
echo.

set /p choice= Pilih [1-3]: 
if "%choice%"=="1" goto RunCheck
if "%choice%"=="2" goto InstallReq
if "%choice%"=="3" goto exit
goto menu

:RunCheck
:: Cek apakah Python sudah terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python belum terinstall. Mengunduh...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe -OutFile python-installer.exe"
    echo.
    echo Menginstall Python, tunggu sebentar...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe

    echo.
    echo Python sudah siap!
    echo.
    goto InstallReqAndRun
) else (
    goto run
)

:InstallReqAndRun
cls
echo Menginstall library yang dibutuhkan...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Semua library sudah terinstall!
echo.
goto run

:InstallReq
cls
echo Menginstall library yang dibutuhkan...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Semua library sudah terinstall!
echo.
pause
goto menu

:run
cls
python MyAnimeList_and_Nekopoi_Scrapper.py
echo.
echo -------------------------------
echo [Y] Scrape lagi  |  [N] Kembali
echo -------------------------------
set /p ulang= Pilih [Y/N]: 
if /I "%ulang%"=="Y" goto run
if /I "%ulang%"=="N" goto menu
goto menu

:exit
echo Terima kasih sudah menggunakan script ini 💕
timeout /t 2 >nul
exit
