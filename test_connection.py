#!/usr/bin/env python
"""Test database connection"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("TESTING DATABASE CONNECTION")
print("=" * 60)

# Import and test
try:
    from database import RentalManagementSystem, DB_CONFIG
    
    print(f"\nDB_CONFIG loaded:")
    print(f"  Host: {DB_CONFIG.get('host')}")
    print(f"  User: {DB_CONFIG.get('user')}")
    print(f"  Password: {'*' * len(DB_CONFIG.get('password', ''))}")
    print(f"  Database: {DB_CONFIG.get('database')}")
    
    print(f"\nConnecting to MySQL...")
    system = RentalManagementSystem()
    
    if system.db.connection:
        print("✓ Connection successful!")
        
        # Try to fetch data
        print("\nFetching landlords...")
        landlords = system.get_all_landlords()
        print(f"✓ Found {len(landlords)} landlords")
        
        system.db.disconnect()
        print("\n✓ All tests passed!")
    else:
        print("✗ Connection failed!")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
