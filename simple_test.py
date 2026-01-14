#!/usr/bin/env python3
import requests
import json

try:
    response = requests.post(
        "http://localhost:7000/api/menu/generate",
        json={"week_start_date": "2026-01-12"},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
