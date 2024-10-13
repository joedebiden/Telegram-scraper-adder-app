@echo off
title (setup) Telegram-Telebox - by Baudelaire
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

:: Create License File
echo Please enter your license key:
set /p license_key=

:: Enregistrer la clé de licence dans un fichier license.txt
echo %license_key% > license.key

echo License key saved successfully!

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



:: Subroutine pour l'installation de Python
:install_python
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...

    :: Télécharger l'installateur de Python via Curl
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

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
