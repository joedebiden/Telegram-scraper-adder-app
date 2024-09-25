@echo off
title Telegram-Telebox - by Baudelaire
chcp 65001 >nul


mode con: cols=175 lines=45

rem Activer les codes ANSI
setlocal EnableDelayedExpansion
set "ESC="


set "colors[1]=%ESC%[38;2;128;0;128m"  rem Violet
set "colors[2]=%ESC%[38;2;102;0;153m"
set "colors[3]=%ESC%[38;2;76;0;179m"
set "colors[4]=%ESC%[38;2;51;0;204m"
set "colors[5]=%ESC%[38;2;25;0;230m"
set "colors[6]=%ESC%[38;2;0;0;255m"   rem Bleu

:banner
echo.
echo.
rem Afficher chaque ligne avec une couleur différente du dégradé
echo !colors[1]!       ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗   ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗
echo !colors[2]!       ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝
echo !colors[3]!          ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║█████╗██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝ 
echo !colors[4]!          ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║╚════╝██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗ 
echo !colors[5]!          ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║      ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
echo !colors[6]!          ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
echo.

rem Réinitialiser les couleurs
echo %ESC%[0m

pause

:: Start script
echo Starting setup process...

:: Vérifier et installer wget
call :install_wget

:: Vérifier et installer Python
call :install_python

:: Installer pip et les modules nécessaires
python -m ensurepip --default-pip
python -m pip install --upgrade pip

:: Créer et activer l'environnement virtuel
echo Creating virtual environment...
python -m venv .venv

:: Activer l'environnement virtuel
call .venv\Scripts\activate

:: Installer les dépendances
echo Installing requirements...
pip install -r requirements.txt

:: Exécuter le setup pour configurer le compte Telegram
echo Starting setup.exe to configure Telegram account...
setup.exe

:: Vérifier si le setup s'est bien terminé
IF %ERRORLEVEL% NEQ 0 (
    echo Setup.exe failed or was interrupted.
    exit /b
)

:menu
cls
echo.
echo Please choose an option:
echo 1 - Start scraper.exe
echo 2 - Start adder.exe
echo 3 - Start messagesender.exe
echo 4 - Exit
set /p choice="Enter your choice: "

IF "%choice%"=="1" (
    echo Starting scraper.exe...
    scraper.exe
    goto menu
) ELSE IF "%choice%"=="2" (
    echo Starting adder.exe...
    adder.exe
    goto menu
) ELSE IF "%choice%"=="3" (
    echo Starting messagesender.exe...
    messagesender.exe
    goto menu
) ELSE IF "%choice%"=="4" (
    echo Exiting...
    goto end
) ELSE (
    echo Invalid choice, please try again.
    pause
    goto menu
)

:end
echo Hope all is doing well. Please reach me if there are any problems on my Discord: Baudelaire
exit

:: Subroutine pour l'installation de wget
:install_wget
where wget >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo wget is not installed. Installing wget...

    :: Télécharger wget via PowerShell
    powershell -Command "Invoke-WebRequest -Uri https://eternallybored.org/misc/wget/current/wget.exe -OutFile wget.exe"

    :: Vérifier si wget a été installé correctement
    where wget >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo wget installation failed. Exiting...
        exit /b
    ) ELSE (
        echo wget installed successfully.
    )
)
exit /b

:: Subroutine pour l'installation de Python
:install_python
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...

    :: Télécharger l'installateur de Python via wget
    wget -O python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

    :: Exécuter l'installateur en mode silencieux
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Vérifier si Python a été installé correctement
    where python >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Python installation failed. Exiting...
        exit /b
    ) ELSE (
        echo Python installed successfully.
        python --version
    )
)
exit /b
