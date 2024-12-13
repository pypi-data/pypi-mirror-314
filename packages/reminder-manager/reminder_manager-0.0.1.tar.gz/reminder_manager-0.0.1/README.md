# Reminder Manager

A Python-based reminder management library that helps track and manage reminders, with special features for antenatal care scheduling.

## Features

### Core Features ✓
- Basic reminder creation and storage
- Reminder retrieval by ID
- Category-based filtering
- Optional voice notifications
- JSON-based persistence

### Medical Features 🚧
- Antenatal care appointment scheduling
- High-risk pregnancy tracking
- Medical reminder categorization

### Management Features ⏳
- Reminder completion tracking
- Overdue reminder detection
- Priority-based scheduling
- Recurring reminders

## Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reminder-manager.git
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Project Structure
```
LIBRARY/
├── services/
│   ├── __init__.py
│   └── reminder_manager.py
├── models/
│   ├── __init__.py
│   └── reminder.py
└── main.py
```

### Basic Usage

```python
from services.reminder_manager import ReminderManager
from models.reminder import Reminder

# Initialize the reminder manager
manager = ReminderManager()

# Create a new reminder
reminder = Reminder(
    title="Doctor's Appointment",
    description="Annual checkup",
    due_date="2024-04-01"
)

# Add the reminder
manager.create_reminder(reminder)
```

## Features in Development

- [ ] Persistent storage using JSON
- [ ] Voice notifications
- [ ] Antenatal care scheduling
- [ ] Reminder categories

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Your Name

## Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Required packages:
  - datetime
  - json
  - typing (for type hints)
  - pathlib (for file handling)

## Configuration
The ReminderManager supports extensive configuration:

```python
manager = ReminderManager(
    storage_path="custom_reminders.json",  # Default: reminders.json
    voice_enabled=True,                    # Default: True
    backup_enabled=True,                   # Default: False
    backup_frequency=24,                   # Hours between backups
    date_format="%Y-%m-%d",               # Default ISO format
    categories=[                          # Default categories
        "medical",
        "personal",
        "work",
        "antenatal"
    ]
)
```

## API Reference

### ReminderManager Methods
```python
# Create a new reminder
create_reminder(reminder: Reminder) -> int
"""Creates a new reminder and returns its ID"""

# Get a specific reminder
get_reminder(reminder_id: int) -> Reminder
"""Retrieves a reminder by its ID. Raises IndexError if not found"""

# Get reminders by category
get_reminders_by_category(category: str) -> List[Reminder]
"""Returns all reminders in the specified category"""

# Get overdue reminders
get_overdue_reminders() -> List[Reminder]
"""Returns all reminders past their due date"""

# Update reminder
update_reminder(reminder: Reminder) -> bool
"""Updates an existing reminder. Returns success status"""

# Delete reminder
delete_reminder(reminder_id: int) -> bool
"""Deletes a reminder. Returns success status"""
```

### Reminder Properties
```python
reminder = Reminder(
    title="Example",              # Required
    description="Description",    # Required
    due_date="2024-04-01",       # Required, ISO format
    category="medical",          # Optional
    priority=1,                  # Optional (1-5)
    recurring=False,             # Optional
    recurring_interval=None,     # Optional (days)
    completed=False,             # Optional
    tags=["important"],          # Optional
    attachments=[],              # Optional
    notifications=True           # Optional
)
```

## Error Handling
```python
try:
    reminder = manager.get_reminder(reminder_id)
except IndexError:
    print("Reminder not found")
except ValueError:
    print("Invalid reminder format")
except FileNotFoundError:
    print("Storage file not found")
except json.JSONDecodeError:
    print("Corrupt storage file")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Best Practices
- Always use try-except blocks when accessing reminders
- Regularly backup the reminders.json file
- Use ISO format for dates (YYYY-MM-DD)
- Implement proper error handling
- Use meaningful reminder titles and descriptions
- Categorize reminders appropriately
- Set realistic due dates
- Keep the storage file in a secure location
- Regular maintenance of old/completed reminders
- Document any custom implementations

## Troubleshooting
Common issues and solutions:

### Import Issues
- **Problem**: Module not found errors
  - Solution: Check PYTHONPATH
  - Solution: Verify __init__.py files exist
  - Solution: Use absolute imports

### Storage Issues
- **Problem**: File not found
  - Solution: Check file permissions
  - Solution: Verify path exists
  - Solution: Create directory if missing

### Date Format Issues
- **Problem**: Invalid dates
  - Solution: Use ISO format (YYYY-MM-DD)
  - Solution: Validate dates before saving
  - Solution: Handle timezone differences

### Performance Issues
- **Problem**: Slow loading with many reminders
  - Solution: Implement pagination
  - Solution: Archive old reminders
  - Solution: Use database instead of JSON

## Future Enhancements
### Short Term (3-6 months)
- Web interface for reminder management
- Mobile app integration
- Calendar sync features
- Multi-user support

### Medium Term (6-12 months)
- AI-powered scheduling suggestions
- Natural language processing for reminder creation
- Advanced recurring reminder patterns
- Integration with popular calendar services

### Long Term (12+ months)
- Distributed system support
- Blockchain-based reminder verification
- Machine learning for priority optimization
- Real-time collaboration features
