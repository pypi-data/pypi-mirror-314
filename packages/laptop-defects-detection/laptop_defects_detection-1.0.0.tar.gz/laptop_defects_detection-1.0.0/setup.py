from setuptools import setup, find_packages

setup(
    name='laptop-defects-detection',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'streamlit',
        'ultralytics',
        'pandas',
        'Pillow',
    ],
)
