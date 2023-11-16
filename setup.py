from setuptools import setup

APP = ['main.py']  
DATA_FILES = [
    ('images', ['images/santa.png']), 
    ('songs', ['songs/lookLikeChristmas.mp3', 'songs/march.mp3', 'songs/white.mp3'])  
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'PIL', 'pygame'], 
    'includes': ['kidList', 'roundedButton', 'adultList'],  
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
