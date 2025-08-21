import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class UserManager:
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self.users_data = self._load_users()
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users data from JSON file."""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_users(self) -> None:
        """Save users data to JSON file."""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving users data: {e}")
    
    def register_user(self, user_id: int, name: str) -> None:
        """Register a new user or update existing user info."""
        user_key = str(user_id)
        
        if user_key not in self.users_data:
            self.users_data[user_key] = {
                "name": name,
                "registered_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "test_history": {}
            }
        else:
            # Update last seen and name if changed
            self.users_data[user_key]["last_seen"] = datetime.now().isoformat()
            if self.users_data[user_key]["name"] != name:
                self.users_data[user_key]["name"] = name
        
        self._save_users()
    
    def get_user_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data by user ID."""
        user_key = str(user_id)
        return self.users_data.get(user_key)
    
    def save_test_result(self, user_id: int, subject_id: str, result: Dict[str, Any]) -> None:
        """Save test result for a user."""
        user_key = str(user_id)
        
        if user_key not in self.users_data:
            self.register_user(user_id, "Unknown User")
        
        # Initialize test_history if not exists
        if "test_history" not in self.users_data[user_key]:
            self.users_data[user_key]["test_history"] = {}
        
        if subject_id not in self.users_data[user_key]["test_history"]:
            self.users_data[user_key]["test_history"][subject_id] = []
        
        # Add timestamp to result
        result_with_timestamp = result.copy()
        result_with_timestamp["completed_at"] = datetime.now().isoformat()
        
        # Save the result
        self.users_data[user_key]["test_history"][subject_id].append(result_with_timestamp)
        
        # Update last seen
        self.users_data[user_key]["last_seen"] = datetime.now().isoformat()
        
        self._save_users()
    
    def clear_user_history(self, user_id: int) -> None:
        """Clear all test history for a user."""
        user_key = str(user_id)
        
        if user_key in self.users_data:
            self.users_data[user_key]["test_history"] = {}
            self.users_data[user_key]["last_seen"] = datetime.now().isoformat()
            self._save_users()
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics for a user."""
        user_data = self.get_user_data(user_id)
        
        if not user_data or not user_data.get("test_history"):
            return {"total_tests": 0, "subjects_attempted": 0, "average_score": 0}
        
        total_tests = 0
        total_correct = 0
        total_questions = 0
        subjects_attempted = len([s for s in user_data["test_history"].values() if s])
        
        for subject_results in user_data["test_history"].values():
            for result in subject_results:
                total_tests += 1
                total_correct += result.get("correct", 0)
                total_questions += result.get("total", 0)
        
        average_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        return {
            "total_tests": total_tests,
            "subjects_attempted": subjects_attempted,
            "average_score": average_score,
            "total_correct": total_correct,
            "total_questions": total_questions
        }
    
    def get_all_users_count(self) -> int:
        """Get total number of registered users."""
        return len(self.users_data)
