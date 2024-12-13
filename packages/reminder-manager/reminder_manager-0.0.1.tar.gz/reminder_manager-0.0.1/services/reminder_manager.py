from datetime import datetime
from typing import List, Optional
from models.reminder import Reminder
from storage.json_storage import JsonStorage
from services.voice_service import VoiceService
from services.notification_manager import NotificationManager

class ReminderManager:
    def __init__(self, storage: JsonStorage, voice_service: VoiceService):
        self.storage = storage
        self.notification_manager = NotificationManager(voice_service)
        self.notification_manager.start()

    def create_reminder(self, reminder: Reminder) -> int:
        """Create a new reminder and schedule notification"""
        reminder_id = self.storage.save_reminder(reminder)
        self.notification_manager.add_reminder(reminder)
        return reminder_id

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get a reminder by ID"""
        return self.storage.get_reminder(reminder_id)

    def get_all_reminders(self) -> List[Reminder]:
        """Get all reminders"""
        return self.storage.get_all_reminders()

    def update_reminder(self, reminder_id: int, reminder: Reminder) -> bool:
        """Update an existing reminder"""
        return self.storage.update_reminder(reminder_id, reminder)

    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder and remove from notification queue"""
        success = self.storage.delete_reminder(reminder_id)
        if success:
            self.notification_manager.remove_reminder(reminder_id)
        return success

    def play_reminder(self, reminder: Reminder) -> None:
        """Play voice notification for reminder"""
        self.voice_service.play_reminder(reminder) 