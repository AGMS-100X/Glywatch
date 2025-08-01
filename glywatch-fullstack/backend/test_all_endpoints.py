#!/usr/bin/env python3
"""
Comprehensive test script for all GlyWatch API endpoints
Tests both Nightscout integration and Supabase database operations
"""

import requests
import json
import time
from typing import Dict, List

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_patient_id = "test_patient_123"
        self.results = []
    
    def test_endpoint(self, method: str, endpoint: str, description: str, expected_status: int = 200) -> Dict:
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        print(f"🔍 Testing: {description}")
        print(f"   URL: {method} {url}")
        
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, timeout=30)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported method: {method}"
                }
            
            response_time = round((time.time() - start_time) * 1000, 2)
            
            result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "success": response.status_code == expected_status,
                "response_size": len(response.content),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if response.status_code == expected_status:
                try:
                    result["data"] = response.json()
                    print(f"   ✅ Success ({response_time}ms)")
                except json.JSONDecodeError:
                    result["data"] = response.text
                    print(f"   ✅ Success ({response_time}ms) - Non-JSON response")
            else:
                result["error"] = f"Expected {expected_status}, got {response.status_code}"
                print(f"   ❌ Failed - Status {response.status_code}")
            
            self.results.append(result)
            return result
            
        except requests.exceptions.ConnectionError:
            error_msg = "Connection refused - Is the server running?"
            print(f"   ❌ Failed - {error_msg}")
            result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "success": False,
                "error": error_msg,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.results.append(result)
            return result
            
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"   ❌ Failed - {error_msg}")
            result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "success": False,
                "error": error_msg,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.results.append(result)
            return result
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive API Tests")
        print("=" * 60)
        print()
        
        # Test connection endpoints
        print("🔌 Testing Connection Endpoints")
        print("-" * 40)
        self.test_endpoint("GET", "/health", "Health Check")
        self.test_endpoint("GET", "/cgm/test-connection", "Nightscout Connection Test")
        self.test_endpoint("GET", "/cgm/test-db-connection", "Supabase Connection Test")
        self.test_endpoint("GET", "/cgm/test-all-connections", "All Connections Test")
        print()
        
        # Test glucose endpoints
        print("🩸 Testing Glucose Endpoints")
        print("-" * 35)
        self.test_endpoint("GET", f"/cgm/latest/{self.test_patient_id}", "Latest Glucose from Nightscout")
        self.test_endpoint("GET", f"/cgm/latest-db/{self.test_patient_id}", "Latest Glucose from Database")
        self.test_endpoint("GET", f"/cgm/history/{self.test_patient_id}?hours=24", "Glucose History from Nightscout")
        self.test_endpoint("GET", f"/cgm/history-db/{self.test_patient_id}?hours=24", "Glucose History from Database")
        print()
        
        # Test device status endpoints
        print("📱 Testing Device Status Endpoints")
        print("-" * 40)
        self.test_endpoint("GET", f"/cgm/device-status/{self.test_patient_id}", "Device Status from Nightscout")
        self.test_endpoint("GET", "/cgm/device-status", "General Device Status")
        print()
        
        # Test treatments endpoints
        print("💊 Testing Treatments Endpoints")
        print("-" * 35)
        self.test_endpoint("GET", f"/cgm/treatments/{self.test_patient_id}?hours=24", "Treatments from Nightscout")
        print()
        
        # Test other endpoints
        print("📊 Testing Other Endpoints")
        print("-" * 30)
        self.test_endpoint("GET", "/cgm/readings", "General Glucose Readings")
        self.test_endpoint("GET", "/cgm/current", "Current Reading")
        self.test_endpoint("GET", "/cgm/history?days=7", "General History")
        self.test_endpoint("POST", "/cgm/calibrate", "Sensor Calibration")
        print()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("📋 Test Summary")
        print("=" * 60)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.get("success", False))
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ Failed Tests:")
            for result in self.results:
                if not result.get("success", False):
                    print(f"   • {result['description']}: {result.get('error', 'Unknown error')}")
            print()
        
        # Performance summary
        response_times = [r.get("response_time_ms", 0) for r in self.results if r.get("success", False)]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print("⚡ Performance Summary:")
            print(f"   Average Response Time: {avg_response_time:.2f}ms")
            print(f"   Fastest Response: {min_response_time:.2f}ms")
            print(f"   Slowest Response: {max_response_time:.2f}ms")
            print()
        
        print("🎯 Recommendations:")
        if failed_tests == 0:
            print("   ✅ All tests passed! Your API is working perfectly.")
        elif failed_tests < total_tests * 0.3:
            print("   ⚠️  Most tests passed. Check failed endpoints for configuration issues.")
        else:
            print("   ❌ Many tests failed. Check your configuration and server status.")
        
        if avg_response_time > 5000:
            print("   ⚠️  Response times are slow. Consider optimizing your setup.")
        
        print()
        print("📚 Next Steps:")
        print("   1. Check the detailed results above for any issues")
        print("   2. Verify your Nightscout and Supabase configurations")
        print("   3. Test with real patient data")
        print("   4. Monitor the API in production")
    
    def save_results(self, filename: str = "api_test_results.json"):
        """Save test results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    "test_run": {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "base_url": self.base_url,
                        "total_tests": len(self.results),
                        "successful_tests": sum(1 for r in self.results if r.get("success", False))
                    },
                    "results": self.results
                }, f, indent=2)
            print(f"💾 Results saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

def main():
    """Main function"""
    import sys
    
    # Parse command line arguments
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print("🌙 GlyWatch API Comprehensive Test Suite")
    print("=" * 60)
    print(f"Target API: {base_url}")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
        else:
            print("⚠️  Server responded but health check failed")
    except:
        print("❌ Server is not running or not accessible")
        print("   Please start your server with: python main.py")
        print("   Then run this test script again")
        return
    
    print()
    
    # Run tests
    tester = APITester(base_url)
    tester.run_all_tests()
    
    # Save results
    tester.save_results()

if __name__ == "__main__":
    main() 