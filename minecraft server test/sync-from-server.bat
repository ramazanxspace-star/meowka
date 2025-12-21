@echo off
echo Синхронизация изменений с тестового сервера...

echo Копирование изменений обратно на тестовый сервер...
robocopy . "C:\Users\1R\Documents\minecraft server test" /E /XD .git logs world world_nether world_the_end cache libraries versions

if %ERRORLEVEL% LEQ 1 (
    echo Успешно! Изменения синхронизированы с тестовым сервером.
    echo Не забудьте перезапустить сервер для применения изменений.
) else (
    echo ОШИБКА: Синхронизация не удалась!
    pause
    exit /b 1
)

pause
