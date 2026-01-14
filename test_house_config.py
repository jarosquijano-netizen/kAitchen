#!/usr/bin/env python3
import requests

# Test the house configuration API
try:
    # Test GET endpoint
    response = requests.get('http://localhost:7000/api/house/config')
    print('GET /api/house/config:')
    print('Status:', response.status_code)
    print('Response:', response.json())
    print()
    
    # Test POST endpoint
    test_data = {
        'num_habitaciones': 4,
        'num_banos': 3,
        'mascotas': 'perro'
    }
    
    response = requests.post('http://localhost:7000/api/house/config', json=test_data)
    print('POST /api/house/config:')
    print('Status:', response.status_code)
    print('Response:', response.json())
    
except Exception as e:
    print('Error:', e)
