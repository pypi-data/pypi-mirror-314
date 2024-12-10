from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="open-weather-flask",
    version="0.1.0",
    author="Yoad Paket",
    author_email="heyyoad@gmail.com",
    description="A Python Flask API to fetch weather data",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
