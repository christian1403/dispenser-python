#!/usr/bin/env python3
"""
Example client script to demonstrate API usage
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
BASE_URL = "http://localhost:5000"
API_KEY = os.getenv("API_KEY", "dev_api_key_12345")

# Headers with API key
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}


def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_api_status():
    """Test the API status endpoint"""
    print("📊 Testing API status...")
    response = requests.get(f"{BASE_URL}/api/v1/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_create_example():
    """Test creating an example"""
    print("➕ Testing example creation...")
    data = {
        "name": "Test Example",
        "value": "This is a test value",
        "description": "This is a test example created by the client script"
    }
    response = requests.post(f"{BASE_URL}/api/v1/example", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()["data"]["id"]
    return None


def test_get_examples():
    """Test getting all examples"""
    print("📋 Testing get all examples...")
    response = requests.get(f"{BASE_URL}/api/v1/example", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_get_example_by_id(example_id):
    """Test getting example by ID"""
    if not example_id:
        print("⚠️  Skipping get by ID test - no example ID available")
        return
        
    print(f"🔍 Testing get example by ID: {example_id}")
    response = requests.get(f"{BASE_URL}/api/v1/example/{example_id}", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_update_example(example_id):
    """Test updating an example"""
    if not example_id:
        print("⚠️  Skipping update test - no example ID available")
        return
        
    print(f"✏️  Testing update example: {example_id}")
    data = {
        "name": "Updated Test Example",
        "value": "This value has been updated",
        "description": "This example was updated by the client script"
    }
    response = requests.put(f"{BASE_URL}/api/v1/example/{example_id}", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_delete_example(example_id):
    """Test deleting an example"""
    if not example_id:
        print("⚠️  Skipping delete test - no example ID available")
        return
        
    print(f"🗑️  Testing delete example: {example_id}")
    response = requests.delete(f"{BASE_URL}/api/v1/example/{example_id}", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_unauthorized_access():
    """Test access without API key"""
    print("🚫 Testing unauthorized access...")
    response = requests.get(f"{BASE_URL}/api/v1/example")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def main():
    """Run all API tests"""
    print("🧪 Flask API Client Test Script")
    print("=" * 50)
    
    try:
        # Test public endpoints
        test_health_check()
        test_api_status()
        
        # Test unauthorized access
        test_unauthorized_access()
        
        # Test CRUD operations with proper authentication
        example_id = test_create_example()
        print()
        
        test_get_examples()
        test_get_example_by_id(example_id)
        test_update_example(example_id)
        test_delete_example(example_id)
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
