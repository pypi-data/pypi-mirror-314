# Import required libraries
import json         # JSON data handling
import os          # File system operations
from typing import Dict, Optional, List  # Type hints
from datetime import datetime
from models.reminder import Reminder
import portalocker  # File locking mechanism
import logging      # Logging functionality

# Set up logger for this module
logger = logging.getLogger(__name__)

class JsonStorage:
    """
    Handles persistent storage of reminders in JSON format with file locking
    Provides CRUD operations for reminder data
    """
    def __init__(self, filename: str):
        """
        Initialize storage with specified file path
        Args:
            filename: Path to JSON storage file
        """
        self.filename = filename
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist with proper initial structure"""
        if not os.path.exists(self.filename):
            initial_data = {
                "reminders": {},
                "next_id": 1
            }
            self._save_data(initial_data)
        else:
            try:
                with open(self.filename, 'r') as f:
                    portalocker.lock(f, portalocker.LOCK_SH)
                    data = json.load(f)
                    portalocker.unlock(f)
                    # Ensure the file has the correct structure
                    if not isinstance(data, dict) or "reminders" not in data or "next_id" not in data:
                        self._save_data({"reminders": {}, "next_id": 1})
            except json.JSONDecodeError:
                self._save_data({"reminders": {}, "next_id": 1})

    def _load_data(self) -> Dict:
        """Load data from storage with proper error handling"""
        try:
            with open(self.filename, 'r') as f:
                portalocker.lock(f, portalocker.LOCK_SH)
                data = json.load(f)
                portalocker.unlock(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Failed to load data: {str(e)}")
            return {"reminders": {}, "next_id": 1}

    def _save_data(self, data: Dict) -> None:
        """Save data with proper locking and error handling"""
        try:
            with open(self.filename, 'w') as f:
                portalocker.lock(f, portalocker.LOCK_EX)
                json.dump(data, f, indent=2)
                f.flush()  # Ensure data is written to disk
                os.fsync(f.fileno())  # Force write to disk
                portalocker.unlock(f)
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")
            raise

    def save_reminder(self, reminder: Reminder) -> int:
        """Save reminder with proper locking for concurrent access"""
        with open(self.filename, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            try:
                data = json.load(f)
                
                # Assign new ID if needed
                if reminder.id is None:
                    reminder.id = data["next_id"]
                    data["next_id"] += 1

                # Save reminder
                data["reminders"][str(reminder.id)] = reminder.to_dict()
                
                # Write back to file
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
                
                return reminder.id
            finally:
                portalocker.unlock(f)

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """
        Get a reminder by ID
        Args:
            reminder_id: ID of reminder to retrieve
        Returns:
            Reminder object if found, None if not found
        """
        data = self._load_data()
        reminder_data = data["reminders"].get(str(reminder_id))
        return Reminder.from_dict(reminder_data) if reminder_data else None

    def get_all_reminders(self) -> List[Reminder]:
        """Get all reminders with proper locking"""
        with open(self.filename, 'r') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            try:
                data = json.load(f)
                return [Reminder.from_dict(r) for r in data["reminders"].values()]
            finally:
                portalocker.unlock(f)

    def update_reminder(self, reminder_id: int, reminder: Reminder) -> bool:
        """Update reminder with proper locking"""
        with open(self.filename, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            try:
                data = json.load(f)
                str_id = str(reminder_id)
                
                if str_id not in data["reminders"]:
                    return False
                
                data["reminders"][str_id] = reminder.to_dict()
                
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
                
                return True
            finally:
                portalocker.unlock(f)

    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete reminder with proper locking"""
        with open(self.filename, 'r+') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            try:
                data = json.load(f)
                str_id = str(reminder_id)
                
                if str_id not in data["reminders"]:
                    return False
                
                del data["reminders"][str_id]
                
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
                
                return True
            finally:
                portalocker.unlock(f)