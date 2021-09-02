@echo off
set ENV_FILE="%~dp0set_env_vars.local.cmd"
call %ENV_FILE%
if exist %ENV_FILE% (
    :: call %ENV_FILE% :: call will async in if..else block.
    wsl bash -c "export DJANGO_SETTINGS_MODULE=%DJANGO_SETTINGS_MODULE% && export DJANGO_DB_USER=%DJANGO_DB_USER% && export DJANGO_DB_PASS=%DJANGO_DB_PASS% && export DJANGO_SECRET=%DJANGO_SECRET% && export DJANGO_DB_NAME=%DJANGO_DB_NAME% && export DJANGO_DB_TYPE=%DJANGO_DB_TYPE% && export DJANGO_DB_PORT=%DJANGO_DB_PORT% && export MYSQL_PROBLEM_TYPE_HOST=%MYSQL_PROBLEM_TYPE_HOST% && export MYSQL_PROBLEM_TYPE_USER=%MYSQL_PROBLEM_TYPE_USER% && export MYSQL_PROBLEM_TYPE_USER_PASSWORD=%MYSQL_PROBLEM_TYPE_USER_PASSWORD% && python3.7 $(pwd)/manage.py %*"
) else (
    echo copy set_env_vars.cmd to set_env_vars.local.cmd end edit environment variables
)