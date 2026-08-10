from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver # Import WebDriver for type hinting
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # Keep By import if used in functions
import time
import os
from dotenv import load_dotenv
from datetime import datetime

from utility import setup_driver,login,refresh_profile,cleanup

if __name__ == "__main__":

    # Load environment variables
    load_dotenv()
    
    # Get login method from environment
    LOGIN_METHOD = os.getenv("LOGIN_METHOD", "email_password").lower()
    
    # Get credentials based on login method
    if LOGIN_METHOD == "google":
        EMAIL = os.getenv("GOOGLE_EMAIL")
        PASSWORD = None  # Not needed for Google login
    elif LOGIN_METHOD == "email_password":
        EMAIL = os.getenv("NAUKRI_EMAIL")
        PASSWORD = os.getenv("NAUKRI_PASSWORD")
    elif LOGIN_METHOD == "otp":
        PHONE_NUMBER = os.getenv("PHONE_NUMBER")
        EMAIL = None
        PASSWORD = None
    else:
        print(f"❌ Invalid login method: {LOGIN_METHOD}")
        print("✅ Supported methods: google, email_password, otp")
        exit(1)

    # Define resume file path
    RESUME_FILE_PATH = os.getenv("RESUME_FILE_PATH", "./resume.pdf")

    if not os.path.exists(RESUME_FILE_PATH):
        print(f"❌ Error: Resume file not found at: {RESUME_FILE_PATH}")
        print("💡 Upload resume.pdf to the repository root or set RESUME_FILE_PATH in .env")
        exit(1)

    # Check if required environment variables are loaded
    if LOGIN_METHOD == "google" and not EMAIL:
        print("❌ Error: GOOGLE_EMAIL is required for Google login")
        exit(1)
    elif LOGIN_METHOD == "email_password" and not all([EMAIL, PASSWORD]):
        print("❌ Error: NAUKRI_EMAIL and NAUKRI_PASSWORD are required for email/password login")
        exit(1)
    elif LOGIN_METHOD == "otp" and not PHONE_NUMBER:
        print("❌ Error: PHONE_NUMBER is required for OTP login")
        exit(1)
    
    if not RESUME_FILE_PATH:
        print("❌ Error: Resume file path is required")
        exit(1)
    
    print(f"🚀 Starting Naukri automation with {LOGIN_METHOD} login method")
    
    try:
        # Call functions in order
        driver = setup_driver()
        
        # Login with the specified method
        if LOGIN_METHOD == "google":
            login(driver, LOGIN_METHOD, email=EMAIL)
        elif LOGIN_METHOD == "email_password":
            login(driver, LOGIN_METHOD, email=EMAIL, password=PASSWORD)
        elif LOGIN_METHOD == "otp":
            login(driver, LOGIN_METHOD, phone_number=PHONE_NUMBER)
        
        refresh_profile(driver, RESUME_FILE_PATH)
        cleanup(driver)
        
    except Exception as e:
        print(f"❌ Script failed: {e}")
        cleanup(driver) if 'driver' in locals() else None
        exit(1)