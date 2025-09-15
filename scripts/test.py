#!/usr/bin/env python3
"""
Test script for CV_Bot API endpoints
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        return False

def register_test_user():
    """Register a test user"""
    print("Registering test user...")
    user_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print("✅ User registration successful")
            return response.json()
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error registering user: {e}")
        return None

def login_test_user():
    """Login test user"""
    print("Logging in test user...")
    login_data = {
        "username": "test@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
            return response.json()["access_token"]
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error logging in: {e}")
        return None

def create_test_job(token: str):
    """Create a test job"""
    print("Creating test job...")
    job_data = {
        "title": "Senior Python Developer",
        "description": """We are looking for a Senior Python Developer to join our team.

Requirements:
- 5+ years of Python experience
- Experience with FastAPI, Django, or Flask
- Knowledge of PostgreSQL and Redis
- Experience with cloud platforms (AWS, Azure, GCP)
- Strong understanding of software development best practices

Responsibilities:
- Develop and maintain web applications
- Design and implement APIs
- Work with databases and optimize queries
- Collaborate with frontend developers
- Mentor junior developers"""
    }

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/jobs", json=job_data, headers=headers)
        if response.status_code == 200:
            print("✅ Job creation successful")
            return response.json()
        else:
            print(f"❌ Job creation failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error creating job: {e}")
        return None

def test_api_flow():
    """Test the complete API flow"""
    print("Starting API flow test...\n")

    # Test health
    if not test_health():
        return False

    # Register user (may fail if already exists)
    register_test_user()

    # Login user
    token = login_test_user()
    if not token:
        return False

    # Create job
    job = create_test_job(token)
    if not job:
        return False

    print(f"\n✅ API flow test completed successfully!")
    print(f"Job created with ID: {job['id']}")
    print(f"AI-generated requirements: {json.dumps(job.get('requirements', {}), indent=2)}")

    return True

def main():
    """Main test function"""
    print("CV_Bot API Test Suite")
    print("=" * 50)

    success = test_api_flow()

    if success:
        print("\n🎉 All tests passed!")
        print("Your CV_Bot API is working correctly!")
    else:
        print("\n❌ Some tests failed.")
        print("Check the error messages above and ensure:")
        print("1. Backend server is running (python backend/run.py)")
        print("2. Database is running (docker-compose up -d)")
        print("3. Environment variables are configured")
        sys.exit(1)

if __name__ == "__main__":
    main()