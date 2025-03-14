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


# Example usage
if __name__ == "__main__":
    # Send OTP Example
    phone_number = "+1234567890"
    send_result = send_otp(phone_number)

    if send_result["success"]:
        print("OTP Sent Successfully!")
        otp_id = send_result["otp_id"]
        print(f"OTP ID: {otp_id}")

        # In real usage, you would get the OTP code from user input
        otp_code = input("Enter OTP code: ")

        # Verify OTP Example
        verify_result = verify_otp(otp_id, otp_code)
        if verify_result["success"]:
            print("OTP Verification Successful!")
        else:
            print(f"Verification Failed: {verify_result['message']}")
    else:
        print(f"Failed to send OTP: {send_result['message']}")
