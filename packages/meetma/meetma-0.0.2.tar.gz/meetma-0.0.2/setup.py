from setuptools import setup, find_packages

setup(
    name='meetma',  # Package name in lowercase
    version='0.0.2',
    packages=find_packages(where='.'),  # Automatically find packages
    install_requires=[
        'PyQt6',
        'beautifulsoup4',
        'googletrans',
        'requests',
        'selenium'
    ],
    entry_points={
        'console_scripts': [
            'meetma=src.main:main',  # Adjust based on your actual structure
        ],
    },
    author='Siyamak Abasnezhad, Mahan Shirsavar',
    author_email='pydevcasts@gmail.com',
    description='The Google Meet bot is a Python application that automates participation in Google Meet meetings. This bot extracts real-time subtitles, translates them, and detects questions to enhance the user experience in online meetings. You can also save the meeting in a file.',
    url='https://github.com/pydevcasts/MeetMa',  
)