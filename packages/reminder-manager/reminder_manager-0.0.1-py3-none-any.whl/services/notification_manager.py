from datetime import datetime, timedelta
import schedule
import time
import threading
import logging
from typing import Dict, List
from models.reminder import Reminder
from services.voice_service import VoiceService

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self, voice_service: VoiceService):
        self.voice_service = voice_service
        self.active_reminders: Dict[int, Reminder] = {}
        self._scheduler_thread = None
        self._running = False
        
    def start(self):
        """Start the notification scheduler thread"""
        if self._scheduler_thread is None or not self._scheduler_thread.is_alive():
            self._running = True
            self._scheduler_thread = threading.Thread(target=self._run_scheduler)
            self._scheduler_thread.daemon = True
            self._scheduler_thread.start()
            logger.info("Notification scheduler started")

    def stop(self):
        """Stop the notification scheduler thread"""
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join()
            logger.info("Notification scheduler stopped")

    def add_reminder(self, reminder: Reminder):
        """Add a reminder to be monitored for notifications"""
        self.active_reminders[reminder.id] = reminder
        logger.info(f"Added reminder {reminder.id} to notification queue")

    def remove_reminder(self, reminder_id: int):
        """Remove a reminder from notification monitoring"""
        if reminder_id in self.active_reminders:
            del self.active_reminders[reminder_id]
            logger.info(f"Removed reminder {reminder_id} from notification queue")

    def _run_scheduler(self):
        """Main scheduler loop"""
        while self._running:
            current_time = datetime.now()
            
            # Check for due reminders
            for reminder_id, reminder in list(self.active_reminders.items()):
                if reminder.due_date <= current_time:
                    self._trigger_notification(reminder)
                    self.remove_reminder(reminder_id)
            
            # Sleep for a short interval
            time.sleep(30)  # Check every 30 seconds

    def _trigger_notification(self, reminder: Reminder):
        """Trigger notification for a reminder"""
        try:
            # Play voice notification
            success = self.voice_service.play_reminder(reminder)
            if success:
                logger.info(f"Successfully played notification for reminder {reminder.id}")
            else:
                logger.warning(f"Failed to play notification for reminder {reminder.id}")
        except Exception as e:
            logger.error(f"Error triggering notification: {str(e)}") 