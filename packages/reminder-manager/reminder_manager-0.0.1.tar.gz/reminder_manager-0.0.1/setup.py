from setuptools import setup, find_packages
import codecs
import os

rootPath = os.path.abspath(os.path.dirname(__file__))

readMePath = os.path.join(rootPath, "README.md")

with codecs.open(readMePath, encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A reminder management system'

# Setting up
setup(
    name="reminder_manager",
    version=VERSION,
    author="Iga Martin",
    author_email="<your-actual-email@example.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/yourusername/reminder_manager',
    install_requires=[
        'portalocker',    # For file locking
        'pytest',         # For testing
        'googlemaps',     # For Google Maps integration
        'requests',       # For weather service
        'pyttsx3',        # For text-to-speech
        'playsound',      # For playing notification sounds
        'schedule',       # For scheduling notifications
        'scipy',          # For creating notification sound
        'pydub',          # For audio file conversion
        'numpy',          # Required by scipy
    ],  # Removed unittest-mock as it's part of standard library
    license='MIT',
    keywords=['python', 'reminder', 'pregnancy', 'healthcare', 'hospital'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6.0"
)