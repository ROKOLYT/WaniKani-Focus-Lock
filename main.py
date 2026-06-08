import os
import asyncio
import sys
from dotenv import load_dotenv
from src.api import WaniKaniAPI
from src.browser import (
    launch_browser_context,
    navigate_to_dashboard,
    enter_fullscreen
)
from src.keyboard_manager import suppress_hotkeys
from src.goals import GoalTracker
from src.ui import get_unlock_banner_script, get_progress_banner_script
from src.config import (
    WANIKANI_DASHBOARD,
    API_POLL_INTERVAL,
    RETRY_DELAY,
    REVIEW_GOAL
)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

async def wait_for_api_connection(max_retries: int = 20) -> None:
    for attempt in range(max_retries):
        try:
            WaniKaniAPI().fetch_summary()
            print(f"✓ API connected")
            return
        except Exception as e:
            if attempt == 0:
                print(f"Waiting for API connection... (retrying every {RETRY_DELAY}s)")
            await asyncio.sleep(RETRY_DELAY)
    
    raise RuntimeError("Failed to connect to WaniKani API after multiple retries")


async def wait_for_browser_navigation(page, max_retries: int = 20) -> None:
    for attempt in range(max_retries):
        try:
            await navigate_to_dashboard(page, WANIKANI_DASHBOARD)
            print("✓ Browser navigation successful")
            return
        except Exception:
            await asyncio.sleep(RETRY_DELAY)
    
    raise RuntimeError("Failed to navigate browser to dashboard")


async def setup_progress_banner(context, page) -> None:
    ui_script = get_progress_banner_script()
    await context.add_init_script(ui_script)
    await page.evaluate(ui_script)
    print("✓ Progress banner displayed")


async def update_progress_banner(
    page,
    lessons_done: int,
    reviews_done: int,
    lesson_goal_met: bool,
    review_goal_met: bool,
    lesson_goal: int,
    review_goal: int = REVIEW_GOAL
) -> None:
    data = {
        "lessons_done": lessons_done,
        "reviews_done": reviews_done,
        "lesson_goal": lesson_goal,
        "review_goal": review_goal,
        "lesson_goal_met": lesson_goal_met,
        "review_goal_met": review_goal_met
    }
    await page.evaluate(
        "(data) => { if (window.updateWkProgress) window.updateWkProgress(data); }",
        data
    )


async def monitor_progress(page, goal_tracker: GoalTracker) -> bool:
    wanikani_api = WaniKaniAPI()
    while not page.is_closed():
        await asyncio.sleep(API_POLL_INTERVAL)
        
        try:
            wanikani_api.fetch_summary()
            current_lessons = wanikani_api.count_todays_lessons()
            current_reviews = wanikani_api.get_reviews()

            lessons_done, reviews_done, lesson_goal_met, review_goal_met = (
                goal_tracker.update_progress(current_reviews, current_lessons)
            )
            await update_progress_banner(
                page,
                lessons_done,
                reviews_done,
                lesson_goal_met,
                review_goal_met,
                goal_tracker.lesson_goal,
                goal_tracker.review_goal
            )
            print(f"Progress: Lessons Done: {lessons_done}, Reviews Done: {reviews_done}")
            
            if lesson_goal_met and review_goal_met:
                print("✓ Goals met!")
                return True
        except Exception as e:
            print(f"Error checking progress: {e}")
            pass
    
    return False


async def show_unlock_banner(context, page) -> asyncio.Event:
    close_event = asyncio.Event()
    
    async def trigger_unlock():
        close_event.set()
    
    await context.expose_function("triggerUnlock", trigger_unlock)
    
    ui_script = get_unlock_banner_script()
    await context.add_init_script(ui_script)
    await page.evaluate(ui_script)
    
    print("✓ Unlock banner displayed")
    
    return close_event


async def main():
    if not API_TOKEN:
        print("Error: API token not found. Please set the API_TOKEN in the config.")
        sys.exit(1)
        
    # Suppress keyboard shortcuts
    suppress_hotkeys()
    print("✓ Keyboard shortcuts suppressed")
    
    # wait for API connection
    await wait_for_api_connection()
    
    # Fetch initial data
    wanikani_api = WaniKaniAPI()
    wanikani_api.fetch_summary()
    initial_lessons = wanikani_api.get_lessons()
    initial_reviews = wanikani_api.get_reviews()
    lessons_batch_size = wanikani_api.get_lessons_batch_size()
    
    review_goal = min(len(initial_reviews), REVIEW_GOAL)
    lesson_goal = min(len(initial_lessons), lessons_batch_size)
    
    completed_lessons = wanikani_api.count_todays_lessons()
    
    print(f"Initial lessons: {initial_lessons}, Initial reviews: {len(initial_reviews)}")
    
    # Launch browser
    context, page, p = await launch_browser_context()
    print("✓ Browser launched")
    
    try:
        # Navigate to dashboard
        await wait_for_browser_navigation(page)
        
        # Enter fullscreen
        await enter_fullscreen(page)
        print("✓ Fullscreen enabled")

        # Monitor progress
        goal_tracker = GoalTracker(initial_reviews, lesson_goal=lesson_goal, review_goal=review_goal, completed_lessons=completed_lessons)
        await setup_progress_banner(context, page)

        lessons_done, reviews_done, lesson_goal_met, review_goal_met = (
            goal_tracker.update_progress(initial_reviews, completed_lessons)
        )
        await update_progress_banner(
            page,
            lessons_done,
            reviews_done,
            lesson_goal_met,
            review_goal_met,
            goal_tracker.lesson_goal,
            goal_tracker.review_goal
        )
        goals_met = await monitor_progress(page, goal_tracker)
        
        # Show unlock banner if goals were met
        if goals_met and not page.is_closed():
            close_event = await show_unlock_banner(context, page)
            await close_event.wait()
        
        # Cleanup
        if not page.is_closed():
            await context.close()
            print("✓ Browser closed")
            
        await p.stop()
        print("✓ Playwright stopped")
    
    except Exception as e:
        print(f"Error: {e}")
        if not page.is_closed():
            await context.close()
        await p.stop()
        raise

if __name__ == "__main__":
    asyncio.run(main())
