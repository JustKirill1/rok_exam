@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion


set "URL=https://rokstats.online/api/peerless-scholar/all-questions"
set "LOCAL_FILE=all-questions.json"
set "TEMP_FILE=temp.json"
set "UPDATE_LOG=updates.txt"


curl -s -o "%TEMP_FILE%" "%URL%" 2>nul

if not exist "%LOCAL_FILE%" (
    echo [%date% %time%] Локальный файл отсутствует, скачиваю... >> "%UPDATE_LOG%"
    move /Y "%TEMP_FILE%" "%LOCAL_FILE%"
    goto end
)


fc "%LOCAL_FILE%" "%TEMP_FILE%" > "%TEMP_FILE%.diff"
if %errorlevel% neq 0 (
    echo [%date% %time%] Обнаружены изменения: >> "%UPDATE_LOG%"
    type "%TEMP_FILE%.diff" >> "%UPDATE_LOG%"
    echo --- >> "%UPDATE_LOG%"
    
    echo Обнаружены изменения, обновляю файл...
    move /Y "%TEMP_FILE%" "%LOCAL_FILE%"
) else (
    echo Файл не изменился.
    del "%TEMP_FILE%"
    del "%TEMP_FILE%.diff"
)


echo Ожидание 3 секунды перед закрытием...
timeout /t 3 >nul
exit /b
