from playwright.async_api import async_playwright, BrowserContext, Page
from src.config import USER_DATA_DIR, BROWSER_ARGS
from typing import Any


async def launch_browser_context() -> tuple[BrowserContext, Page, Any]:
    p = await async_playwright().start()
    context = await p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",
        no_viewport=True,
        ignore_default_args=["--enable-automation"],
        args=BROWSER_ARGS
    )
    return context, context.pages[0], p


async def navigate_to_dashboard(page: Page, dashboard_url: str) -> None:
    if page.url == "about:blank" or page.url == "":
        await page.goto(dashboard_url)


async def enter_fullscreen(page: Page) -> None:
    await page.keyboard.press('F11')
