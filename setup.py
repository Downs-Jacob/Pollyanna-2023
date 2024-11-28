import os
from setuptools import setup

APP = ['main.py']

# Dynamically collect all files in 'images' and 'songs' directories
def collect_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

DATA_FILES = [
    ('images', collect_files('images')),
    ('songs', collect_files('songs')),
]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL', 'pygame'],  # Include external dependencies
    'includes': ['kidList', 'roundedButton', 'adultList'],  # Include custom modules
    'iconfile': 'icon.icns',  # Optional: Add an app icon if available
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['Pillow', 'pygame'],  # Ensure dependencies are installed
)
