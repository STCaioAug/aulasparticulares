import os
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_sms(to_phone_number, message_body):
    """
    Send an SMS message using Twilio
    
    Args:
        to_phone_number (str): The recipient's phone number in E.164 format
        message_body (str): The message content to send
        
    Returns:
        dict: Response from Twilio API including message SID if successful
    """
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send the message
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        
        return {"success": True, "message_sid": message.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}