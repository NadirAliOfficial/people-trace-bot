# import json
# import requests


# async def send_whatsapp_otp(wa_number, otp):
#     url = "https://graph.facebook.com/v18.0/173790305822177/messages"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer EAANkvcPwc9QBOwyaFQEPZAbUOaPI0ZBkfvGQu5l4aHhEAOSe5svSa16YNZAVQ1bPYNFO1YZCyWTPnj07jFDvLOCpz2DZBMeUbZCyvZBJfLDYHrfRreXZCYxNUVIl1UlqBzV6KbO255m0jdF4jwKo0llFAL9BUrGqvGp1MAeY38YhD2fTKZBb78UExd5kD2kZAW7FRIJhx0tvPYza7H5GAwhZBcm6d6wwzUZD"
#     }

#     data = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": wa_number,
#         "type": "template",
#         "template": {
#             "name": "otp",
#             "language": {"code": "en"},
#             "components": [
#                 {
#                     "type": "body",
#                     "parameters": [
#                         {
#                             "type": "text",
#                             "text": otp
#                         }
#                     ]
#                 },
#                 {
#                     "type": "button",
#                     "sub_type": "url",
#                     "index": "0",
#                     "parameters": [
#                         {
#                             "type": "text",
#                             "text": otp
#                         }
#                     ]
#                 }
#             ]
#         }
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     return response.json()

import requests
import json

# Constants
BASE_URL = "https://api.fazpass.com"
SEND_OTP_AUTH_HEADER = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjo5ODY4fQ.wMV0iaP9cxMJPuvwU0BuYzO9u9pJz-UTcC0fr1idZXc"
GATEWAY_KEY = "f6bb7523-3210-46fa-8b2d-13c88a6eabbf"
MERCHANT_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjo5ODY4fQ.wMV0iaP9cxMJPuvwU0BuYzO9u9pJz-UTcC0fr1idZXc"  # Replace with your actual merchant key


# HV0aN6D5VmdnM2Kt
async def send_otp(phone_number):
    """
    Send OTP to the specified phone number
    Returns dictionary with success status and response data
    """
    data = {
        "phone": phone_number,
        "gateway_key": GATEWAY_KEY,
    }

    headers = {
        "Authorization": SEND_OTP_AUTH_HEADER,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/otp/request",
            data=json.dumps(data),
            headers=headers,
        )

        result = response.json()

        if result.get("status") == True:
            return {
                "success": True,
                "otp_id": result.get("data", {}).get("id"),
                "message": "OTP sent successfully!",
                "full_response": result,
            }
        else:
            return {
                "success": False,
                "message": result.get("message", "Failed to send OTP"),
                "full_response": result,
            }

    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request error: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "message": "Invalid JSON response from server"}


async def verify_otp(otp_id, otp_code):
    """
    Verify OTP with provided OTP ID and code
    Returns dictionary with verification status
    """
    data = {"otp_id": otp_id, "otp": otp_code}

    headers = {
        "Authorization": f"Bearer {MERCHANT_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/otp/verify",
            data=json.dumps(data),
            headers=headers,
        )

        result = response.json()

        if result.get("status") == True:
            return {
                "success": True,
                "message": "OTP verified successfully!",
                "full_response": result,
            }
        else:
            return {
                "success": False,
                "message": result.get("message", "OTP verification failed"),
                "full_response": result,
            }

    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request error: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "message": "Invalid JSON response from server"}
