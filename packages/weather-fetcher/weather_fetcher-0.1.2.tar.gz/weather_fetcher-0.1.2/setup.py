from setuptools import setup, find_packages

setup(
    name="weather-fetcher",
    version="0.1.2",
    author="Your Name",
    author_email="your_email@example.com",
    description="A Python package to fetch weather data",
    packages=find_packages(),
    install_requires=[
        "certifi==2024.8.30",
        "charset-normalizer==3.4.0",
        "idna==3.10",
        "requests==2.32.3",
        "urllib3==2.2.3",
    ],
    extras_require={
        "dev": [
            "flake8==6.1.0",
            "black==23.9.1",
            "pytest==8.3.4",
            "build==1.2.2.post1",
            "twine==6.0.1",
        ]
    },
    url="https://github.com/testinapps/python-weather-app",
    project_urls={
        "Bug Tracker": "https://github.com/testinapps/python-weather-app/issues",
        "Documentation": "https://github.com/testinapps/python-weather-app/wiki",
        "Source Code": "https://github.com/testinapps/python-weather-app",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
