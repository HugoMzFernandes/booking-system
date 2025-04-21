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
│   └── setup.py          # Package configuration
├── consumer/              # Notification service
│   ├── src/              # Source code
│   ├── tests/            # Unit tests
│   └── setup.py         # Package configuration
└── infrastructure/        # Infrastructure as Code
    └── template.yaml     # AWS SAM template
```

## Environment Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- AWS Account (for SQS)
- Git

### Database Setup

1. Create a PostgreSQL database:
```bash
createdb therapist_booking
```

2. Apply the database schema:
```bash
psql -U postgres -d therapist_booking -f api/src/infrastructure/schema.sql
```

### Environment Variables

1. Create `.env` files in both `api/` and `consumer/` directories with the following content:

For `api/.env`:
```
# Database configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/therapist_booking

# AWS configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your_account_id/booking-queue
```

For `consumer/.env`:
```
# AWS configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your_account_id/booking-queue
```

Replace the placeholder values with your actual credentials.

## Setup Instructions

1. Clone the repository:
```bash
git clone <https://github.com/HugoMzFernandes/booking-system.git>
cd booking-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd api
pip install -e .
cd ../consumer
pip install -e .
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

## Swagger Documentation

Once the API is running, you can access the Swagger documentation at:
```
http://localhost:8000/docs
```

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