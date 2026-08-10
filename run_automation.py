#!/usr/bin/env python3
"""
Enhanced Naukri Automation Runner
This script provides better error handling and user guidance.
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if environment variables are properly configured."""
    print("🔍 Checking environment configuration...")
    
    # Load environment variables
    load_dotenv()
    
    login_method = os.getenv("LOGIN_METHOD")
    if not login_method:
        print("❌ LOGIN_METHOD not set!")
        print("💡 Run: python setup_env.py to configure")
        return False
    
    print(f"✅ Login method: {login_method}")
    
    if login_method == "google":
        email = os.getenv("GOOGLE_EMAIL")
        if not email:
            print("❌ GOOGLE_EMAIL not set!")
            return False
        print(f"✅ Google email: {email}")
        
    elif login_method == "email_password":
        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASSWORD")
        if not email or not password:
            print("❌ NAUKRI_EMAIL or NAUKRI_PASSWORD not set!")
            return False
        print(f"✅ Naukri email: {email}")
        print("✅ Password: [SET]")
        
    elif login_method == "otp":
        phone = os.getenv("PHONE_NUMBER")
        if not phone:
            print("❌ PHONE_NUMBER not set!")
            return False
        print(f"✅ Phone number: {phone}")
    
    return True

def main():
    """Main function to run the automation."""
    print("🚀 Naukri Automation Runner")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment not properly configured!")
        print("💡 Please run: python setup_env.py")
        sys.exit(1)
    
    print("\n✅ Environment check passed!")
    
    # Check if resume file exists
    resume_path = os.getenv("RESUME_FILE_PATH", "./resume.pdf")
    if not os.path.exists(resume_path):
        print(f"⚠️ Resume file not found at: {resume_path}")
        print("💡 Upload resume.pdf to the repository root or set RESUME_FILE_PATH in .env")
        
        # Ask for alternative path
        alt_path = input("📄 Enter path to your resume file (or press Enter to skip): ").strip()
        if alt_path and os.path.exists(alt_path):
            print(f"✅ Using resume: {alt_path}")
            os.environ["RESUME_FILE_PATH"] = alt_path
        else:
            print("⚠️ Continuing without resume upload...")
    
    # Run the main automation
    try:
        print("\n🚀 Starting Naukri automation...")
        from main import main as run_main
        run_main()
    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped by user")
    except Exception as e:
        print(f"\n❌ Automation failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify your login credentials")
        print("3. Try a different login method")
        print("4. Check if Naukri.com is accessible")
        sys.exit(1)

def update_resume_path(new_path):
    """Update resume path in main.py."""
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Replace the hardcoded path
        old_path = "/Users/mac/Documents/Job Material/Prakhar_PM_resume.pdf"
        content = content.replace(old_path, new_path)
        
        with open('main.py', 'w') as f:
            f.write(content)
        
        print(f"✅ Updated resume path to: {new_path}")
    except Exception as e:
        print(f"⚠️ Could not update resume path: {e}")

if __name__ == "__main__":
    main()

