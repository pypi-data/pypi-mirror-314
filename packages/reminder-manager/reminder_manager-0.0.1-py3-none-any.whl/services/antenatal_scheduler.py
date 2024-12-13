from typing import List, NamedTuple
from models.enums import WeatherType
from datetime import datetime, timedelta

class AntenatalAppointment(NamedTuple):
    visit_type: str
    description: str
    date: datetime
    clothing_recommendation: str = ""

class AntenatalScheduler:
    def __init__(self, weather_service=None):
        self.weather_service = weather_service
        self._clothing_recommendations = {
            WeatherType.HOT: {
                "first_trimester": "Wear loose, breathable cotton clothes. Light colors recommended.",
                "second_trimester": "Choose maternity dresses in light fabrics. Consider sun protection.",
                "third_trimester": "Loose maxi dresses, breathable maternity wear, and comfortable sandals."
            },
            WeatherType.COLD: {
                "first_trimester": "Layer with warm, stretchy clothes. Don't forget a scarf.",
                "second_trimester": "Maternity sweaters and warm leggings. Consider a maternity coat.",
                "third_trimester": "Warm maternity wear with good insulation. Slip-resistant boots."
            },
            WeatherType.RAINY: {
                "first_trimester": "Waterproof jacket and non-slip shoes.",
                "second_trimester": "Maternity raincoat and waterproof boots.",
                "third_trimester": "Full coverage rainwear and secure footwear."
            },
            WeatherType.MODERATE: {
                "first_trimester": "Comfortable, layered clothing.",
                "second_trimester": "Adaptable maternity wear that can be layered.",
                "third_trimester": "Loose-fitting, comfortable maternity clothes with good support."
            }
        }

    def _get_trimester(self, week: int) -> str:
        """Determine trimester based on pregnancy week"""
        if week <= 12:
            return "first_trimester"
        elif week <= 27:
            return "second_trimester"
        else:
            return "third_trimester"

    def _get_clothing_recommendation(self, week: int, date: datetime, location: str = None) -> str:
        """Get clothing recommendation based on weather and pregnancy stage"""
        trimester = self._get_trimester(week)
        
        if self.weather_service and location:
            weather = self.weather_service.get_weather(location, date)
        else:
            weather = WeatherType.MODERATE
            
        return self._clothing_recommendations[weather][trimester]

    def generate_schedule(self, due_date: datetime, location: str = None) -> List['AntenatalAppointment']:
        """Generate antenatal appointment schedule with clothing recommendations"""
        pregnancy_start = due_date - timedelta(days=280)
        current_week = (datetime.now() - pregnancy_start).days // 7

        schedule = []
        appointments = [
            (8, "First Trimester Screening", "Initial checkup and blood tests"),
            (12, "Dating Scan", "Ultrasound to confirm due date"),
            (20, "Anomaly Scan", "Detailed ultrasound examination"),
            (28, "Glucose Test", "Check for gestational diabetes"),
            (32, "Growth Scan", "Check baby's growth and position"),
            (36, "Final Position Check", "Confirm baby's position"),
            (38, "Pre-birth Check", "Final preparations for birth"),
            (40, "Due Date Check", "Monitor for labor signs")
        ]

        for week, visit_type, description in appointments:
            if week >= current_week:
                appointment_date = pregnancy_start + timedelta(weeks=week)
                if appointment_date < due_date:
                    clothing_rec = self._get_clothing_recommendation(week, appointment_date, location)
                    schedule.append(AntenatalAppointment(
                        visit_type=visit_type,
                        description=description,
                        date=appointment_date,
                        clothing_recommendation=clothing_rec
                    ))

        return schedule