import os
from twilio.rest import Client
from random import randint

# Load Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory storage for TAC codes (replace with a database in production)
tac_store = {}


def generate_tac():
    """Generate a 6-digit Time-based Authentication Code (TAC)."""
    return str(randint(100000, 999999))


def send_sms(phone_number, tac):
    """
    Send an SMS with the TAC to the provided phone number.

    Args:
        phone_number (str): The recipient's phone number (e.g., "+1234567890").
        tac (str): The 6-digit TAC to send.

    Returns:
        bool: True if the SMS was sent successfully, False otherwise.
    """
    try:
        message = client.messages.create(
            body=f"Your verification code is: {tac}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
        # Store the TAC in memory for verification
        tac_store[phone_number] = tac
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def verify_tac(phone_number, user_tac):
    """
    Verify the TAC entered by the user.

    Args:
        phone_number (str): The recipient's phone number.
        user_tac (str): The TAC entered by the user.

    Returns:
        bool: True if the TAC matches, False otherwise.
    """
    stored_tac = tac_store.get(phone_number)
    if stored_tac and stored_tac == user_tac:
        # Clear the TAC after successful verification
        del tac_store[phone_number]
        return True
    return False
