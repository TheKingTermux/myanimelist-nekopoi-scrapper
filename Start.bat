@echo off
title MyAnimeList & Nekopoi Scrapper Loader by TheKingTermux
cd /d %~dp0
setlocal EnableDelayedExpansion

:MainMenu
cls
echo.
echo                               MyAnimeList and Nekopoi Scrapper Loader
echo                                   Developer : TheKingTermux-Sama
echo.
echo                   _______________________________________________________________
echo                  ^|                                                               ^|
echo                  ^|      [1] Run The Scraper                                      ^|
echo                  ^|      ___________________________________________________      ^|
echo                  ^|                                                               ^|
echo                  ^|      [2] Install / Update Requirements                        ^|
echo                  ^|      ___________________________________________________      ^|
echo                  ^|                                                               ^|
echo                  ^|      [3] Exit                                                 ^|
echo                  ^|_______________________________________________________________^|

echo:
set /p pil= Masukkan Pilihan Anda [1-4] : 

if "%pil%"=="1" goto RunCheck
if "%pil%"=="2" goto InstallReq
if "%pil%"=="3" goto Exit
goto MainMenu

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
    goto SelectLang
)

:SelectLang
cls
echo ============================================
echo      Pilih Bahasa / Choose Language
echo ============================================
echo.
echo [1] Bahasa Indonesia
echo [2] English
echo.
set /p lang= Silakan pilih (1-2): 
if "%lang%"=="1" goto RunIndo
if "%lang%"=="2" goto RunEng
goto SelectLang

:InstallReqAndRun
cls
echo Menginstall library yang dibutuhkan...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Semua library sudah terinstall!
echo.
goto SelectLang

:InstallReq
cls
echo Menginstall library yang dibutuhkan...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Semua library sudah terinstall!
echo.
pause
goto MainMenu

:RunIndo
cls
python MyAnimeList_and_Nekopoi_Scrapper.py
echo.
echo -------------------------------
echo [Y] Scrape lagi  |  [N] Kembali
echo -------------------------------
set /p ulang= Pilih [Y/N]: 
if /I "%ulang%"=="Y" goto RunIndo
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:RunEng
cls
python MyAnimeList_and_Nekopoi_Scrapper_English.py
echo.
echo -------------------------------
echo [Y] Scrape again |  [N] Back
echo -------------------------------
set /p ulang= Choose [Y/N]: 
if /I "%ulang%"=="Y" goto RunEng
if /I "%ulang%"=="N" goto MainMenu
goto MainMenu

:Exit
cls
echo.
echo Terima kasih sudah menggunakan script ini 💕
timeout /t 2 >nul
exit
