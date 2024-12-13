# Import the Enum class from Python's built-in enum module
# This provides the base class for creating enumerated types
from enum import Enum

# Define an enumeration for reminder priority levels
# By inheriting from Enum, we create a set of constant values that can't be modified
class ReminderPriority(Enum):
    """Priority levels for reminders"""
    # Each enum member is defined as NAME = "value"
    # The name (e.g., LOW) can be accessed via ReminderPriority.LOW
    # The value (e.g., "low") can be accessed via ReminderPriority.LOW.value
    LOW = "low"        # Represents low priority reminders
    MEDIUM = "medium"  # Represents medium priority reminders
    HIGH = "high"      # Represents high priority reminders

# Define an enumeration for different types of antenatal reminders
class ReminderCategory(Enum):
    """Categories of antenatal reminders"""
    # Each category represents a different type of reminder in the antenatal care system
    # These can be used to categorize and filter reminders
    APPOINTMENT = "appointment"   # For scheduling doctor visits
    MEDICATION = "medication"     # For medication-related reminders
    EXERCISE = "exercise"        # For physical activity reminders
    NUTRITION = "nutrition"      # For diet and nutrition advice
    VACCINATION = "vaccination"   # For vaccine schedules
    GENERAL = "general"          # For general pregnancy-related reminders
    SCREENING = "screening"      # For medical screening tests
    EDUCATION = "education"      # For pregnancy education materials
    CLOTHING = "clothing"        # New category for clothing recommendations

# Define an enumeration for reminder types
class ReminderType(Enum):
    """Types of reminders"""
    MEDICATION = "medication"
    APPOINTMENT = "appointment"

# Define an enumeration for reminder statuses
class ReminderStatus(Enum):
    """Statuses of reminders"""
    PENDING = "pending"
    COMPLETED = "completed"

# Define an enumeration for weather conditions
class WeatherType(Enum):
    """Weather conditions for clothing recommendations"""
    HOT = "hot"
    COLD = "cold"
    RAINY = "rainy"
    MODERATE = "moderate"

# Usage examples:
# priority = ReminderPriority.HIGH
# category = ReminderCategory.APPOINTMENT
# priority.value would return "high"
# category.value would return "appointment"
