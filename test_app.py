#!/usr/bin/env python3
from app import app

# Test the Flask app routes
with app.test_client() as client:
    # Test main routes
    routes_to_test = ['/', '/strategic', '/tactical', '/analytical']
    
    for route in routes_to_test:
        try:
            response = client.get(route)
            print(f"Route {route}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.data.decode()[:200]}")
        except Exception as e:
            print(f"Route {route}: Exception - {e}")
    
    # Test API routes
    api_routes = ['/api/strategic/overview', '/api/strategic/borough-crimes', '/api/strategic/crime-categories']
    
    print("\nAPI Routes:")
    for route in api_routes:
        try:
            response = client.get(route)
            print(f"Route {route}: Status {response.status_code}")
            if response.status_code == 200:
                print(f"  Data: {response.get_json()}")
        except Exception as e:
            print(f"Route {route}: Exception - {e}")