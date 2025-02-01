# Telebox application 

Telebox (Telegram toolbox app) is an free application for managing Telegram accounts, scraping groups, and adding members, with a user-friendly graphical interface. This project uses `customtkinter` for the user interface and `telethon` for interaction with the Telegram API.

## Features

- **Telegram account management**: Add, modify, delete, and display Telegram accounts.
- **Group scraping**: Retrieve members of a Telegram group and save them in a CSV file.
- **Add members**: Add users to a Telegram group from a CSV file.
- **Proxy management**: Add, modify, delete, and display proxies (coming soon).
- **Message sending**: Send messages to users or groups (coming soon).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/joedebiden/Telebox-app.git
    cd Telebox-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate 
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Launch the main application:
    ```sh
    cd telebox 
    python main.py
    {or} 
    python telebox\main.py
    ```

2. Use the graphical interface to manage your Telegram accounts, scrape groups, and add members.

3. If you struggle by using the app, feel free to check how to use it on my website : [TeleboxWebsite](https://telegram-toolbox.online/software/how-to-use)


## Modification

To modify the application, you can edit the files in the `features` and `gui` directories. Here are some starting points:

- **Add Features**: Add new features in the `features` directory and create corresponding user interfaces in the `gui` directory.
- **Modify the User Interface**: Modify the files in the `gui` directory to change the appearance and behavior of the application.
- **Tests**: Add or modify tests in the `tests` directory to ensure your changes work correctly.

## Acknowledgements and Credits

A big thank you to everyone who contributed to this project. This project uses the following libraries:

- [Telethon](https://github.com/LonamiWebs/Telethon) for interaction with the Telegram API.
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for the user interface.

Thanks also to the open-source community for their support and contributions.

---
This app is free and will be free, don't buy for stupid clone.

© 2025 Evan. This project is licensed under the GNU General Public License v3.0.