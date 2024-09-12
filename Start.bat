::start()
::install python
::install pip
::create .venv file
::activate venv on .venv file
::install requirements
::start setup.exe (create config file for telegram account)
::then when setup process finish
::start scraper.exe
::save members files
::then when process finish
::choose between start adder.exe or messagesender.exe with a csv file
::let the process run
::when process or user terminate the programs exit venv
::send message ("Hope all doing well, please reach me if there any problems on my discord : Bodelaire")
::exit()

@echo off

:: Start script
echo Starting setup process...

:: Check if wget is installed
where wget >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo wget is not installed. Installing wget...

    :: Download wget using PowerShell
    powershell -Command "Invoke-WebRequest -Uri https://eternallybored.org/misc/wget/current/wget.exe -OutFile wget.exe"

    :: Unzip wget
    powershell -Command "Expand-Archive -Path wget.zip -DestinationPath .\wget"

    :: Move wget.exe to a folder in PATH (here we move it to the current directory for simplicity)
    move wget\wget.exe .\

    :: Clean up the zip file
    del wget.zip
    rmdir /S /Q wget

    :: Check if wget was installed correctly
    where wget >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo wget installation failed. Exiting...
        exit /b
    ) ELSE (
        echo wget installed successfully.
    )
)

:: Check if Python is installed
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...

    :: Download Python installer using wget
    wget -O python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

    :: Run the installer silently
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Check if Python was installed correctly
    where python >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Python installation failed. Exiting...
        exit /b
    ) ELSE (
        echo Python installed successfully.
        python --version
    )
)

:: Install pip if not installed
python -m ensurepip --default-pip
python -m pip install --upgrade pip

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv .venv

:: Activate virtual environment
call .venv\Scripts\activate

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt

:: Run setup.exe
echo Starting setup.exe to configure Telegram account...
setup.exe

:: Check if setup.exe finished
IF %ERRORLEVEL% NEQ 0 (
    echo Setup.exe failed or was interrupted.
    exit /b
)

echo Setup complete. Starting scraper.exe...
scraper.exe

:: Save members files process
echo Saving members files...
IF %ERRORLEVEL% NEQ 0 (
    echo Error during scraper.exe execution.
    exit /b
)

:: Choose between adder.exe or messagesender.exe
:choice
echo Please choose:
echo 1 - Start adder.exe with a CSV file
echo 2 - Start messagesender.exe with a CSV file
set /p choice="Enter your choice: "

IF "%choice%"=="1" (
    echo Starting adder.exe...
    adder.exe
) ELSE IF "%choice%"=="2" (
    echo Starting messagesender.exe...
    messagesender.exe
) ELSE (
    echo Invalid choice. Exiting...
    exit /b
)

:: Wait for process termination
echo Waiting for the process to finish...
IF %ERRORLEVEL% NEQ 0 (
    echo Process failed or was interrupted.
    exit /b
)

:: Send final message
echo Hope all doing well, please reach me if there are any problems on my Discord: Bodelaire

:: Exit script
exit
