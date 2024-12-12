from setuptools import setup, find_packages

setup(
    name="aiovm",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aiogram = aiogram_version_manager.main:main",
        ]
    },
    install_requires=[
        "aiogram",
    ],
)
