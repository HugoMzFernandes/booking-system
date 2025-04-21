# Therapist Booking System

A microservices-based booking system for therapists, designed to run on AWS Lambda.

## Architecture

The system is split into two main services:

1. **Booking API Service**
   - FastAPI-based REST API
   - Handles booking creation and validation
   - Stores booking data in PostgreSQL
   - Pushes booking events to SQS queue

2. **Notification Service**
   - AWS Lambda consumer
   - Processes booking events from SQS
   - Sends notifications (email/SMS)

## Project Structure

```
booking-system/
├── api/                    # Booking API service
│   ├── src/               # Source code
│   ├── tests/             # Unit tests
│   └── requirements.txt   # Dependencies
├── consumer/              # Notification service
│   ├── src/              # Source code
│   ├── tests/            # Unit tests
│   └── requirements.txt  # Dependencies
└── infrastructure/        # Infrastructure as Code
    └── template.yaml     # AWS SAM template
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd api
pip install -r requirements.txt
cd ../consumer
pip install -r requirements.txt
```

3. Set up PostgreSQL:
```bash
# Create database and tables
psql -U postgres -f api/src/infrastructure/schema.sql
```

4. Run tests:
```bash
# API tests
cd api
pytest

# Consumer tests
cd ../consumer
pytest
```

5. Run the API locally:
```bash
cd api
uvicorn src.main:app --reload
```

## API Endpoints

- `POST /bookings` - Create a new booking
- `GET /bookings/{booking_id}` - Get booking details
- `GET /health` - Health check endpoint

## Possible Improvements

1. **Authentication & Authorization**
   - Implement JWT authentication
   - Role-based access control
   - API key management

2. **Scalability**
   - Add caching layer (Redis)
   - Implement database sharding
   - Add load balancing

3. **Monitoring & Observability**
   - Add CloudWatch metrics
   - Implement distributed tracing
   - Set up error tracking

4. **Features**
   - Therapist availability management
   - Recurring bookings
   - Cancellation handling
   - Payment integration

5. **Testing**
   - Add integration tests
   - Add load tests
   - Add end-to-end tests

## Deployment

The system is designed to be deployed using AWS SAM. The `template.yaml` file contains the infrastructure configuration.

```bash
# Build and deploy
sam build
sam deploy --guided
```

## Development

- Follow PEP 8 style guide
- Write tests for all new features
- Use type hints
- Document all public functions and classes 