import json
import boto3
import os
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

class SQSClient:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.queue_url = os.getenv('SQS_QUEUE_URL')

    def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a message to the SQS queue.
        
        Args:
            message: Dictionary containing the message data
            
        Returns:
            Dict containing the response from SQS
        """
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message)
            )
            return response
        except Exception as e:
            # In a production environment, you would want to log this error
            # and possibly retry the operation
            raise Exception(f"Failed to send message to SQS: {str(e)}") 