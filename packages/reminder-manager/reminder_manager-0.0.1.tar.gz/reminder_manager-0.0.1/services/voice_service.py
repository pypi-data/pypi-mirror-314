from playsound import playsound
import pyttsx3
import logging

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            # Test the engine
            voices = self.engine.getProperty('voices')
            if voices:
                # Set the first available voice
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            # Test speak
            self.engine.say("Voice service initialized")
            self.engine.runAndWait()
            logger.info("Voice service successfully initialized")
        except Exception as e:
            logger.error(f"Failed to initialize voice service: {str(e)}")
            self.engine = None

    def play_reminder(self, reminder):
        """Play a voice notification for the given reminder"""
        if not self.engine:
            logger.error("Voice service not properly initialized")
            return False
            
        try:
            # Construct message
            message = f"Reminder: {reminder.title}. {reminder.description}"
            
            # Convert text to speech
            self.engine.say(message)
            self.engine.runAndWait()
            
            # Play notification sound
            try:
                self.play_sound()
            except Exception as e:
                logger.warning(f"Could not play notification sound: {str(e)}")
            
            return True
        except Exception as e:
            logger.error(f"Error playing voice reminder: {str(e)}")
            return False

    def play_sound(self):
        """Play notification sound"""
        try:
            import winsound
            winsound.Beep(440, 500)  # frequency=440Hz, duration=500ms
            return True
        except Exception as e:
            logger.warning(f"Could not play notification sound: {str(e)}")
            return False