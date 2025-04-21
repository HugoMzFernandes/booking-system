from setuptools import setup, find_packages

setup(
    name="therapist-booking-consumer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3==1.29.3",
        "python-dotenv==1.0.0",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "moto==4.1.14",
    ],
) 