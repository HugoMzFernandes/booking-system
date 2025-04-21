import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import json
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import NotificationService, lambda_handler

@pytest.fixture
def mock_sqs():
    with patch('boto3.client') as mock_client:
        mock_sqs = MagicMock()
        mock_client.return_value = mock_sqs
        yield mock_sqs

@pytest.fixture
def notification_service(mock_sqs):
    return NotificationService()

def test_send_notification(notification_service):
    message = {
        "booking_id": 1,
        "therapist_id": 1,
        "client_email": "test@example.com",
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "event_type": "booking_created"
    }
    
    # This should not raise any exceptions
    notification_service.send_notification(message)

def test_process_message(notification_service):
    message = {
        "booking_id": 1,
        "therapist_id": 1,
        "client_email": "test@example.com",
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "event_type": "booking_created"
    }
    
    # This should not raise any exceptions
    notification_service.process_message(message)

def test_start_listening(notification_service, mock_sqs):
    # Mock SQS response
    mock_sqs.receive_message.return_value = {
        "Messages": [
            {
                "MessageId": "1",
                "ReceiptHandle": "receipt-1",
                "Body": json.dumps({
                    "booking_id": 1,
                    "therapist_id": 1,
                    "client_email": "test@example.com",
                    "start_time": datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "event_type": "booking_created"
                })
            }
        ]
    }
    
    # Start the service and let it process one message
    notification_service.start()
    
    # Verify that the message was processed
    mock_sqs.receive_message.assert_called_once()
    mock_sqs.delete_message.assert_called_once()

def test_lambda_handler():
    # Create a mock event
    event = {
        "Records": [
            {
                "messageId": "1",
                "body": json.dumps({
                    "booking_id": 1,
                    "therapist_id": 1,
                    "client_email": "test@example.com",
                    "start_time": datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "event_type": "booking_created"
                })
            }
        ]
    }
    
    # Mock the NotificationService
    with patch('src.main.NotificationService') as mock_service:
        mock_instance = mock_service.return_value
        response = lambda_handler(event, None)
        
        assert response["statusCode"] == 200
        assert "Messages processed successfully" in response["body"]
        mock_instance.process_message.assert_called_once()

def test_lambda_handler_error():
    # Create a mock event with invalid JSON
    event = {
        "Records": [
            {
                "messageId": "1",
                "body": "invalid json"
            }
        ]
    }
    
    response = lambda_handler(event, None)
    assert response["statusCode"] == 500
    assert "Error processing messages" in response["body"] 