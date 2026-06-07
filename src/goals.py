from typing import Tuple
from src.config import REVIEW_GOAL

"""This GoalTracker has a glitch, probably API related. It doesn't count completed lessons correctly."""
# class GoalTracker:
#     def __init__(self, reviews: list[int], lessons: list[int], lesson_goal: int, review_goal: int = REVIEW_GOAL, completed_lessons: int = 0):
#         self.reviews = set(reviews)
#         self.lessons = set(lessons)
#         self.lesson_goal = lesson_goal
#         self.review_goal = review_goal
#         self.total_lessons_done = completed_lessons
#         self.total_reviews_done = 0

#     def update_progress(self, current_reviews: list[int], current_lessons: list[int]) -> Tuple[int, int, bool, bool]:
#         completed_reviews = self.reviews - set(current_reviews)
#         completed_lessons = self.lessons - set(current_lessons)
        
#         self.reviews -= completed_reviews
#         self.lessons -= completed_lessons
        
#         self.total_reviews_done += len(completed_reviews)
#         self.total_lessons_done += len(completed_lessons)

#         lesson_goal_met = self.total_lessons_done >= self.lesson_goal or current_lessons == 0
#         review_goal_met = self.total_reviews_done >= self.review_goal or current_reviews == 0

#         return self.total_lessons_done, self.total_reviews_done, lesson_goal_met, review_goal_met

"""Because of how we track completed lessons which reset at midnight UTC this will reset lesson progress at midnight UTC,
but no one except me is using this, so it's not a problem. If it becomes a problem I'll fix it"""
class GoalTracker:
    def __init__(self, reviews: list[int], lesson_goal: int, review_goal: int = REVIEW_GOAL, completed_lessons: int = 0):
        self.reviews = set(reviews)
        self.lesson_goal = lesson_goal
        self.review_goal = review_goal
        self.total_lessons_done = completed_lessons
        self.total_reviews_done = 0

    def update_progress(self, current_reviews: list[int], current_lessons: int) -> Tuple[int, int, bool, bool]:
        completed_reviews = self.reviews - set(current_reviews)
        
        self.reviews -= completed_reviews
        
        self.total_reviews_done += len(completed_reviews)
        self.total_lessons_done = current_lessons

        lesson_goal_met = self.total_lessons_done >= self.lesson_goal or current_lessons == 0
        review_goal_met = self.total_reviews_done >= self.review_goal or current_reviews == 0

        return self.total_lessons_done, self.total_reviews_done, lesson_goal_met, review_goal_met