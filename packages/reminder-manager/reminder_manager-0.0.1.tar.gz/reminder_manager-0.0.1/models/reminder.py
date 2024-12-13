from datetime import datetime
from models.enums import ReminderType, ReminderStatus
from typing import Dict, Optional

class Reminder:
    def __init__(self, 
                 title: str,
                 description: str,
                 due_date: datetime,
                 reminder_type: ReminderType,
                 status: ReminderStatus,
                 id: Optional[int] = None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.reminder_type = reminder_type
        self.status = status

    def to_dict(self) -> Dict:
        """Convert reminder to dictionary for storage"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'reminder_type': self.reminder_type.value,
            'status': self.status.value
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Reminder':
        """Create reminder from dictionary data"""
        return cls(
            id=data.get('id'),
            title=data['title'],
            description=data['description'],
            due_date=datetime.fromisoformat(data['due_date']),
            reminder_type=ReminderType(data['reminder_type']),
            status=ReminderStatus(data['status'])
        )