@echo off
title (app) Telegram-Telebox - by Baudelaire
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
cls
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



rem Vérifier si l'environnement virtuel existe
if not exist ".venv\Scripts\activate" (
    echo [!] L'environnement virtuel n'existe pas. Veuillez le créer d'abord.
    echo Creating virtual environment...
	python -m venv .venv
	call .venv\Scripts\activate
	pause
    
)

:: Activer l'environnement virtuel
call .venv\Scripts\activate


pause 
echo Starting app...
goto menu

:menu
echo.
echo Please choose an option:
echo 1 - manage account 
echo 2 - manage proxy 
echo 3 - Start scraper
echo 4 - Start adder 
echo 5 - Start message sender
echo 6 - Exit
set /p choice="Enter your choice: "

IF "%choice%"=="1" (
    echo lauching manage account app...
    python account.py 
    goto menu

) ELSE IF "%choice%"=="2" (
    echo launching manage proxy app...
    python auth.py
    goto menu

) ELSE IF "%choice%"=="3" (
    echo starting scraping app...
    python scraper.py
    goto menu

) ELSE IF "%choice%"=="4" (
    rem give the name of members list (with extension) for the adder 
    set /p args="Enter the name of the members list (with extension): " 
    echo starting adder app...
    python adder.py \your_members_list_here\%args%
    rem missing the path of the members list

) ELSE IF "%choice%"=="5" (
    rem give the name of members list (with extension) for the message sender 
    echo starting message sender app...
    python sender.py
    goto menu

) ELSE IF "%choice%"=="6" (
    goto end

) ELSE (
    echo Invalid choice, please try again.
    pause
    goto menu
)

:end
echo Hope all is doing well. Please reach me if there are any problems on my Discord: Baudelaire
exit

