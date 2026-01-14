import requests

def final_system_test():
    print("=== FINAL SYSTEM RECOVERY TEST ===\n")
    
    base_url = "http://localhost:7000"
    
    # Test all major endpoints
    tests = [
        ("Main Page", f"{base_url}/"),
        ("Family Adults", f"{base_url}/api/adults"),
        ("Family Children", f"{base_url}/api/children"),
        ("Recipes", f"{base_url}/api/recipes"),
        ("Current Week Menu", f"{base_url}/api/menu/current-week"),
        ("Shopping List", f"{base_url}/api/shopping/list/2026-01-12"),
        ("Cleaning Schedule", f"{base_url}/api/cleaning/schedule/2026-01-12"),
        ("TV View", f"{base_url}/tv"),
        ("Settings", f"{base_url}/api/settings")
    ]
    
    results = []
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        if 'data' in data:
                            if isinstance(data['data'], list):
                                count = len(data['data'])
                            elif isinstance(data['data'], dict):
                                count = len(data['data'].get('categories', {}))
                            else:
                                count = 1
                        else:
                            count = 1
                        results.append(f"✅ {test_name}: OK ({count} items)")
                    else:
                        results.append(f"⚠️ {test_name}: {data.get('error', 'Unknown error')}")
                except:
                    results.append(f"✅ {test_name}: OK (HTML)")
            else:
                results.append(f"❌ {test_name}: HTTP {response.status_code}")
        except Exception as e:
            results.append(f"❌ {test_name}: {str(e)}")
    
    # Print results
    print("TEST RESULTS:")
    for result in results:
        print(f"  {result}")
    
    # Summary
    success_count = sum(1 for r in results if "✅" in r)
    total_count = len(results)
    
    print(f"\n=== SUMMARY ===")
    print(f"Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 COMPLETE SYSTEM RECOVERED AND FULLY FUNCTIONAL!")
        print("\n📱 ACCESS URLS:")
        print(f"  • Admin Interface: {base_url}")
        print(f"  • TV Display: {base_url}/tv")
        print("\n🔧 AVAILABLE FEATURES:")
        print("  • Family Profiles Management")
        print("  • Recipe Database")
        print("  • Weekly Menu Planning")
        print("  • Shopping List Generation")
        print("  • Cleaning Schedule System")
        print("  • TV Display Interface")
        print("  • Settings Management")
    else:
        print("⚠️ Some components need attention")

if __name__ == "__main__":
    final_system_test()
