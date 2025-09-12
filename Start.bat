@echo off
title MyAnimeList & Nekopoi Scrapper by TheKIngTermux
cd /d %~dp0

:run
cls
python MyAnimeList_and_Nekopoi_Scrapper.py
echo.
echo -------------------------------
echo [Y] Scrape lagi  |  [N] Keluar
echo -------------------------------
set /p ulang= Pilih [Y/N]: 
if /I "%ulang%"=="Y" goto run
if /I "%ulang%"=="N" goto exit

:exit
echo Terima kasih sudah menggunakan script ini 💕
pause
