WANIKANI_API_BASE = "https://api.wanikani.com/v2"
WANIKANI_DASHBOARD = "https://www.wanikani.com/dashboard"

# Goals
REVIEW_GOAL = 50

# Browser settings
USER_DATA_DIR = "./wk_profile"
BROWSER_ARGS = [
    '--kiosk',
    '--app=https://www.wanikani.com/dashboard',
    '--disable-infobars',
    '--no-default-browser-check',
    '--window-position=0,0'
]

# Timing
API_POLL_INTERVAL = 2  # seconds
RETRY_DELAY = 1  # seconds

# Keyboard hotkeys to suppress
HOTKEYS_TO_SUPPRESS = [
    'alt+f4',
    'ctrl+w',
    'ctrl+shift+w',
    'ctrl+tab',
    'ctrl+shift+tab',
    'f11'
]
