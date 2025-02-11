@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion


set "URL=https://rokstats.online/api/peerless-scholar/all-questions"
set "LOCAL_FILE=all-questions.json"
set "TEMP_FILE=temp.json"


curl -s -o "%TEMP_FILE%" "%URL%" 2>nul


if not exist "%LOCAL_FILE%" (
    echo Локальный файл отсутствует, скачиваю...
    move /Y "%TEMP_FILE%" "%LOCAL_FILE%"
    goto end
)


fc /b "%LOCAL_FILE%" "%TEMP_FILE%" >nul
if %errorlevel% neq 0 (
    echo Обнаружены изменения, обновляю файл...
    move /Y "%TEMP_FILE%" "%LOCAL_FILE%"
) else (
    echo Файл не изменился.
    del "%TEMP_FILE%"
)

:end
echo Ожидание 3 секунды перед закрытием...
timeout /t 3 >nul
exit /b
