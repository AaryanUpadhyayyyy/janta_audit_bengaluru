import requests
import json

def test_imagekit_endpoint():
    try:
        print("🧪 Testing ImageKit authentication endpoint...")
        response = requests.get("http://localhost:8000/api/imagekit-auth")
        
        if response.status_code == 200:
            print("✅ ImageKit endpoint is working!")
            auth_data = response.json()
            print("📋 Authentication data received:")
            print(json.dumps(auth_data, indent=2))
            
            # Check if required fields are present
            required_fields = ['signature', 'expire', 'token']
            missing_fields = [field for field in required_fields if field not in auth_data]
            
            if missing_fields:
                print(f"⚠️  Missing fields: {missing_fields}")
            else:
                print("✅ All required authentication fields are present!")
                
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on port 8000.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_imagekit_endpoint()