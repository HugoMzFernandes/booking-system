import json
import os
import boto3
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class NotificationService:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.queue_url = os.getenv('SQS_QUEUE_URL')

    def send_notification(self, message: Dict[str, Any]) -> None:
        """
        Send a notification based on the message type.
        In a real implementation, this would send actual emails/SMS.
        
        Args:
            message: Dictionary containing the notification details
        """
        # This is a mock implementation
        # In a real system, you would integrate with an email service (e.g., SES)
        # or SMS service (e.g., SNS)
        print(f"Sending notification for booking {message['booking_id']}")
        print(f"To: {message['client_email']}")
        print(f"Event: {message['event_type']}")

    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a message from the SQS queue.
        
        Args:
            message: Dictionary containing the message data
        """
        try:
            self.send_notification(message)
        except Exception as e:
            # In a production environment, you would want to log this error
            # and possibly retry the operation or move the message to a DLQ
            print(f"Failed to process message: {str(e)}")

    def start(self) -> None:
        """
        Start listening for messages from the SQS queue.
        """
        while True:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20
                )

                if 'Messages' in response:
                    for message in response['Messages']:
                        try:
                            message_body = json.loads(message['Body'])
                            self.process_message(message_body)
                            
                            # Delete the message from the queue
                            self.sqs.delete_message(
                                QueueUrl=self.queue_url,
                                ReceiptHandle=message['ReceiptHandle']
                            )
                        except Exception as e:
                            print(f"Error processing message: {str(e)}")
                            
            except Exception as e:
                print(f"Error receiving messages: {str(e)}")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event
        context: Lambda context
        
    Returns:
        Dict containing the response
    """
    try:
        # Process each record from the event
        for record in event['Records']:
            message_body = json.loads(record['body'])
            notification_service = NotificationService()
            notification_service.process_message(message_body)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Messages processed successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing messages: {str(e)}')
        }

if __name__ == "__main__":
    # For local development
    notification_service = NotificationService()
    notification_service.start() 