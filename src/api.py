import os
import datetime
import json
import urllib.request
from config import WANIKANI_API_BASE
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

class WaniKaniAPI:
    def __init__(self, api_token: str = API_TOKEN): # type: ignore
        self.api_token = api_token
        self.summary = None
        
    def fetch_summary(self) -> dict:
        req = urllib.request.Request(
            f"{WANIKANI_API_BASE}/summary",
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
        with urllib.request.urlopen(req) as response:
            self.summary = json.loads(response.read().decode())
        return self.summary
    
    def fetch_user_info(self) -> dict:
        req = urllib.request.Request(
            f"{WANIKANI_API_BASE}/user",
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
        
    def get_lessons_batch_size(self) -> int:
        user_info = self.fetch_user_info()
        return user_info['data']['preferences']['lessons_batch_size']
    
    def get_reviews(self) -> list:
        if self.summary is None:
            self.fetch_summary()
            
        return self.summary['data']['reviews'][0]['subject_ids'] if self.summary['data']['reviews'] else [] # type: ignore
    
    def get_lessons(self) -> list:
        """May be faulty, to be tested, thus not used for now"""
        if self.summary is None:
            self.fetch_summary()
            
        return self.summary['data']['lessons'][0]['subject_ids'] if self.summary['data']['lessons'] else [] # type: ignore
    
    def get_assignments(self):
        today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_iso = today.isoformat().replace("+00:00", "Z")
        
        req = urllib.request.Request(
            f"{WANIKANI_API_BASE}/assignments?updated_after={today_iso}",
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
        
    def count_todays_lessons(self) -> int:
        """Returns count of completed lessons on the current day (resets at midnight UTC)"""
        assignments = self.get_assignments()
        today_prefix = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        lesson_count = 0
        
        for assignment in assignments['data']:
            started_at = assignment['data']['started_at']
            if started_at and started_at.startswith(today_prefix):
                lesson_count += 1
                
        return lesson_count


