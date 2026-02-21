import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.getcwd())

try:
    from app.services.whatsapp_service import send_match_alert
    import random

    print("--- Starting WhatsApp Test ---")
    # Using one of the numbers from the DB
    test_phone = "+918589958840" 
    test_name = "Test Case - Devika"
    location = "Main Terminal - Gate 4"
    officer_no = f"{random.randint(7000, 9999)}{random.randint(100000, 999999)}"

    print(f"Attempting to send alert to: {test_phone}")
    result = send_match_alert(
        complainant_phone=test_phone,
        missing_name=test_name,
        match_distance=0.2,
        case_id=999,
        location=location,
        officer_no=officer_no
    )

    if result.get("success"):
        print(f"SUCCESS! Message SID: {result.get('sid')}")
    else:
        print(f"FAILED! Error: {result.get('error')}")

except Exception as e:
    print(f"EXCEPTION: {e}")
