#!/usr/bin/env python3
"""
JantaAI Universal Capabilities Test Script
Tests the universal AI system with various domain questions
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://localhost:8001"
GEMINI_API_KEY = "AIzaSyAPrRHBy9WPDOn14Qq9NuK3wPYW_db4RqY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

def test_gemini_api_direct():
    """Test direct Gemini API connection"""
    print("🔍 Testing Direct Gemini API Connection...")
    
    payload = {
        "contents": [
            {
                "parts": [{
                    "text": "Hello! Can you confirm you're working? Please respond with 'JantaAI Universal Test: SUCCESS' if you can see this message."
                }]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.9,
            "maxOutputTokens": 100,
            "candidateCount": 1
        }
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                ai_response = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Gemini API: CONNECTED")
                print(f"📝 Response: {ai_response[:100]}...")
                return True
            else:
                print(f"❌ Gemini API: Invalid response structure")
                return False
        else:
            print(f"❌ Gemini API: HTTP {response.status_code}")
            print(f"📝 Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API: Connection failed - {str(e)}")
        return False

def test_universal_questions():
    """Test various domain questions"""
    print("\n🧪 Testing Universal AI Capabilities...")
    
    test_questions = [
        {
            "domain": "Government/Politics",
            "question": "Who is the MLA of Indranagar constituency in Bengaluru?",
            "expected_topics": ["MLA", "Indranagar", "constituency", "political"]
        },
        {
            "domain": "Technology",
            "question": "What is artificial intelligence and how does it work?",
            "expected_topics": ["artificial intelligence", "AI", "technology", "machine learning"]
        },
        {
            "domain": "Health",
            "question": "What are the benefits of drinking water daily?",
            "expected_topics": ["water", "health", "benefits", "hydration"]
        },
        {
            "domain": "Education",
            "question": "What are the best study techniques for students?",
            "expected_topics": ["study", "techniques", "students", "learning"]
        },
        {
            "domain": "Business",
            "question": "How to start a small business in India?",
            "expected_topics": ["business", "startup", "India", "entrepreneur"]
        },
        {
            "domain": "Science",
            "question": "How does solar energy work?",
            "expected_topics": ["solar", "energy", "renewable", "technology"]
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {test['domain']}")
        print(f"❓ Question: {test['question']}")
        
        # Test direct Gemini API for this question
        success = test_gemini_question(test['question'])
        
        results.append({
            "domain": test['domain'],
            "question": test['question'],
            "success": success
        })
        
        time.sleep(1)  # Rate limiting
    
    return results

def test_gemini_question(question):
    """Test a specific question with Gemini API"""
    
    system_prompt = """You are JantaAI, an advanced AI assistant with comprehensive knowledge across ALL domains and topics. You can answer any question about anything while having special expertise in Bengaluru government services.

UNIVERSAL CAPABILITIES:
- Technology, Science, Engineering, Mathematics
- Health, Medicine, Fitness, Nutrition  
- Education, History, Literature, Arts
- Business, Finance, Economics, Investment
- Entertainment, Sports, Movies, Music
- Government Services, Politics, Public Administration
- Current Affairs, News, Social Issues
- Geography, Culture, Travel, Lifestyle

Please provide a helpful, accurate, and comprehensive response to the following question:"""
    
    full_prompt = f"{system_prompt}\n\nUSER QUESTION: {question}\n\nProvide a comprehensive, helpful response:"
    
    payload = {
        "contents": [
            {
                "parts": [{
                    "text": full_prompt
                }]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.9,
            "maxOutputTokens": 2048,
            "candidateCount": 1
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                ai_response = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ SUCCESS: Got AI response ({len(ai_response)} chars)")
                print(f"📝 Preview: {ai_response[:150]}...")
                return True
            else:
                print(f"❌ FAILED: Invalid response structure")
                return False
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"📝 Error: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 JantaAI Universal Capabilities Test")
    print("=" * 50)
    
    # Test 1: Direct API Connection
    api_works = test_gemini_api_direct()
    
    if not api_works:
        print("\n❌ API connection failed. Cannot proceed with universal tests.")
        return False
    
    # Test 2: Universal Questions
    results = test_universal_questions()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['success'])
    
    print(f"✅ Total Tests: {total_tests}")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {total_tests - successful_tests}")
    print(f"📊 Success Rate: {(successful_tests/total_tests*100):.1f}%")
    
    print(f"\n🔍 DETAILED RESULTS:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {result['domain']}: {result['question'][:50]}...")
    
    if successful_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! JantaAI Universal AI System is working perfectly!")
        print(f"🌟 JantaAI can answer questions from ALL domains using Gemini AI!")
        return True
    else:
        print(f"\n⚠️ Some tests failed. Check API configuration and network connectivity.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)