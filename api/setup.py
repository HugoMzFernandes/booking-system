from setuptools import setup, find_packages

setup(
    name="therapist-booking-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic[email]==2.5.2",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "httpx==0.25.2",
        "boto3==1.29.3",
        "python-dotenv==1.0.0",
        "alembic==1.12.1",
    ],
) 