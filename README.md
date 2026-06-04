# WaniKani Focus Lock

Windows-only kiosk launcher for WaniKani. It opens the WaniKani dashboard in full screen upon user login, tracks lessons and reviews via the WaniKani API, and keeps the desktop session locked down until your review and lesson goals are met.

## Requirements

- Windows 10 or Windows 11
- Python 3.9 or higher
- Google Chrome browser installed
- WaniKani API token (Read access only)

## Setup Instructions

1. Clone the repository ```git clone https://github.com/ROKOLYT/WaniKani-Focus-Lock```
2. Create a file named .env in the root directory of the project.
3. Add your WaniKani API token to the .env file
```API_TOKEN=your_wanikani_api_token_here```

4. Right-click setup.bat and select "Run as administrator" to configure the environment.
   - Automatically initializes a localized virtual environment (.venv).
   - Installs required dependencies via pip.
   - Downloads mandatory Playwright browser binaries.
   - Configures the custom Windows user logon shell.
5. Next time you start your PC and log in, the WaniKani Focus Lock will activate immediately.

## Configuration

Settings can be customized inside src/config.py:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| REVIEW_GOAL | 10 | Number of reviews required to trigger the unlock mechanism. |
| API_POLL_INTERVAL | 2 | Time interval (in seconds) between checking current progress. |

The lesson goal dynamically adapts to match your personal lesson batch size specified inside your online WaniKani settings account.

## Uninstall
Run ```uninstall.bat``` as administrator.
This clears the custom Winlogon\Shell entry from your registry.

## Troubleshooting

If the script crashes or your network connection fails during the login phase, you can manually escape the window block:
1. Press Ctrl + Shift + Esc to open the Windows Task Manager.
2. Force close the Browser process to exit the kiosk mode and access your desktop.

## Disclaimer

This project uses the official WaniKani API but is an independent development. It is not officially affiliated with or endorsed by Tofugu LLC.