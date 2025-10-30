"""
Backend API Test Script

This script tests all backend endpoints to ensure they're working correctly.
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = 'http://localhost:5000/api'

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f'{BASE_URL}/health')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful!")
            print(f"Status: {data.get('status')}")
            print(f"Model loaded: {data.get('model_loaded')}")
            print(f"Classes loaded: {data.get('classes_loaded')}")
            print(f"SerpAPI configured: {data.get('serpapi_configured')}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure the backend is running: python app.py")
        return False

def test_get_classes():
    """Test the get classes endpoint"""
    print("\n" + "="*50)
    print("Testing Get Classes Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f'{BASE_URL}/classes')
        
        if response.status_code == 200:
            data = response.json()
            classes = data.get('classes', [])
            print("✅ Get classes successful!")
            print(f"Total classes: {data.get('total')}")
            print(f"Classes: {', '.join(classes)}")
            return True
        else:
            print(f"❌ Get classes failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predict(image_path=None):
    """Test the prediction endpoint"""
    print("\n" + "="*50)
    print("Testing Prediction Endpoint")
    print("="*50)
    
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                data = {'use_serpapi': 'false'}  # Set to 'true' to test SerpAPI
                
                response = requests.post(f'{BASE_URL}/predict', files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Prediction successful!")
                    print(f"Predicted disease: {result.get('prediction')}")
                    print(f"Confidence: {result.get('confidence') * 100:.2f}%")
                    
                    if 'all_predictions' in result:
                        print("\nTop predictions:")
                        for i, pred in enumerate(result['all_predictions'][:3], 1):
                            print(f"  {i}. {pred['disease']}: {pred['confidence']*100:.2f}%")
                    
                    return True
                else:
                    print(f"❌ Prediction failed with status: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    else:
        print("⚠️ No test image provided or image not found")
        print("To test prediction, provide an image path:")
        print("python test_api.py path/to/image.jpg")
        return None

def test_search_recommendations():
    """Test the search recommendations endpoint"""
    print("\n" + "="*50)
    print("Testing Search Recommendations Endpoint")
    print("="*50)
    
    try:
        data = {'disease': 'acne'}
        response = requests.post(f'{BASE_URL}/search-recommendations', json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Search recommendations successful!")
            print(f"Disease: {result.get('disease')}")
            
            if 'recommendations' in result and 'recommendations' in result['recommendations']:
                recs = result['recommendations']['recommendations']
                print(f"Found {len(recs)} recommendations")
            
            return True
        else:
            print(f"❌ Search failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🔬 Backend API Test Suite")
    print("="*60)
    
    results = {
        'Health Check': test_health_check(),
        'Get Classes': test_get_classes(),
        'Search Recommendations': test_search_recommendations(),
    }
    
    # Test prediction if image path is provided
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        results['Prediction'] = test_predict(image_path)
    else:
        results['Prediction'] = test_predict()
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️ SKIPPED"
        
        print(f"{test_name}: {status}")
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    total = len([r for r in results.values() if r is not None])
    
    print("\n" + "="*60)
    print(f"Overall: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == '__main__':
    main()
