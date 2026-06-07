"""
===============================================================================
RENTAL MANAGEMENT SYSTEM - DATABASE CONNECTION & CRUD OPERATIONS
===============================================================================
This module handles all database operations using mysql-connector-python
Provides connection management, CRUD operations, and error handling
===============================================================================
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path

# Database Configuration - Load from config file or use defaults
DEFAULT_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql@123',  # Set during setup
    'database': 'rental_management_system',
    'port': 3306
}

def load_db_config():
    """Load database configuration from config file"""
    # Try multiple possible locations for the config file
    possible_paths = [
        Path(__file__).parent.parent / '.db_config.json',  # rental_system/.db_config.json
        Path(__file__).parent / '.db_config.json',         # src/.db_config.json  
        Path.cwd() / '.db_config.json',                    # current working directory
    ]
    
    for config_file in possible_paths:
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    saved_config = json.load(f)
                    # Merge with defaults
                    config = DEFAULT_DB_CONFIG.copy()
                    config.update(saved_config)
                    return config
            except Exception as e:
                print(f"Warning: Could not load config file at {config_file}: {e}")
    
    return DEFAULT_DB_CONFIG.copy()

DB_CONFIG = load_db_config()


class DatabaseConnection:
    """Manages database connection and basic operations"""
    
    def __init__(self, config: Dict = None):
        """Initialize database connection"""
        self.config = config or DB_CONFIG
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✓ Database connection successful")
            return True
        except Error as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database disconnected")
    
    def commit(self):
        """Commit changes"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Rollback changes"""
        if self.connection:
            self.connection.rollback()
    
    def execute_query(self, query: str, params: Tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Query execution error: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[Dict]:
        """Fetch all records"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Fetch error: {e}")
            return []
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Dict]:
        """Fetch single record"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Fetch error: {e}")
            return None


class RentalManagementSystem:
    """Main system for CRUD operations"""
    
    def __init__(self, db_config: Dict = None):
        """Initialize system with database connection"""
        self.db = DatabaseConnection(db_config)
        self.db.connect()
    
    # ========================================================================
    # LANDLORD OPERATIONS
    # ========================================================================
    
    def add_landlord(self, first_name: str, last_name: str, email: str, 
                     phone: str, address: str) -> bool:
        """Add new landlord"""
        if not email or not phone:
            print("✗ Email and phone are required")
            return False
        
        query = """
        INSERT INTO landlord (first_name, last_name, email, phone, address, created_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, phone, address, datetime.now().date())
        return self.db.execute_query(query, params)
    
    def get_all_landlords(self) -> List[Dict]:
        """Get all landlords"""
        query = "SELECT * FROM landlord ORDER BY landlord_id DESC"
        return self.db.fetch_all(query)
    
    def get_landlord(self, landlord_id: int) -> Optional[Dict]:
        """Get specific landlord"""
        query = "SELECT * FROM landlord WHERE landlord_id = %s"
        return self.db.fetch_one(query, (landlord_id,))
    
    def update_landlord(self, landlord_id: int, first_name: str, last_name: str,
                       email: str, phone: str, address: str) -> bool:
        """Update landlord details"""
        query = """
        UPDATE landlord 
        SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s
        WHERE landlord_id = %s
        """
        return self.db.execute_query(query, (first_name, last_name, email, phone, address, landlord_id))
    
    # ========================================================================
    # BUILDING OPERATIONS
    # ========================================================================
    
    def add_building(self, landlord_id: int, building_name: str, location: str,
                    year_built: int, total_floors: int) -> bool:
        """Add new building"""
        query = """
        INSERT INTO building (landlord_id, building_name, location, year_built, total_floors, created_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (landlord_id, building_name, location, year_built, total_floors, datetime.now().date()))
    
    def get_all_buildings(self) -> List[Dict]:
        """Get all buildings with landlord names"""
        query = """
        SELECT b.*, CONCAT(l.first_name, ' ', l.last_name) AS landlord_name
        FROM building b
        JOIN landlord l ON b.landlord_id = l.landlord_id
        ORDER BY b.building_id DESC
        """
        return self.db.fetch_all(query)
    
    def get_buildings_by_landlord(self, landlord_id: int) -> List[Dict]:
        """Get buildings for specific landlord"""
        query = """
        SELECT * FROM building WHERE landlord_id = %s ORDER BY building_id DESC
        """
        return self.db.fetch_all(query, (landlord_id,))
    
    # ========================================================================
    # ROOM OPERATIONS
    # ========================================================================
    
    def add_room(self, building_id: int, room_number: str, room_type: str,
                area_sqft: float, monthly_rent: float) -> bool:
        """Add new room"""
        query = """
        INSERT INTO room (building_id, room_number, room_type, area_sqft, monthly_rent, status, created_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (building_id, room_number, room_type, area_sqft, monthly_rent, 'Available', datetime.now().date()))
    
    def get_all_rooms(self) -> List[Dict]:
        """Get all rooms with building details"""
        query = """
        SELECT r.*, b.building_name
        FROM room r
        JOIN building b ON r.building_id = b.building_id
        ORDER BY r.room_id DESC
        """
        return self.db.fetch_all(query)
    
    def get_rooms_by_building(self, building_id: int) -> List[Dict]:
        """Get rooms in specific building"""
        query = """
        SELECT * FROM room WHERE building_id = %s ORDER BY room_number ASC
        """
        return self.db.fetch_all(query, (building_id,))
    
    def get_available_rooms(self) -> List[Dict]:
        """Get all available rooms"""
        query = """
        SELECT r.*, b.building_name
        FROM room r
        JOIN building b ON r.building_id = b.building_id
        WHERE r.status = 'Available'
        ORDER BY r.room_id DESC
        """
        return self.db.fetch_all(query)
    
    # ========================================================================
    # TENANT OPERATIONS
    # ========================================================================
    
    def add_tenant(self, first_name: str, last_name: str, email: str,
                   phone: str, id_proof: str) -> bool:
        """Add new tenant"""
        query = """
        INSERT INTO tenant (first_name, last_name, email, phone, id_proof, status, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (first_name, last_name, email, phone, id_proof, 'Active', datetime.now().date()))
    
    def get_all_tenants(self) -> List[Dict]:
        """Get all tenants"""
        query = "SELECT * FROM tenant ORDER BY tenant_id DESC"
        return self.db.fetch_all(query)
    
    def search_tenant_by_name(self, name: str) -> List[Dict]:
        """Search tenants by name"""
        search_term = f"%{name}%"
        query = """
        SELECT * FROM tenant 
        WHERE CONCAT(first_name, ' ', last_name) LIKE %s OR email LIKE %s
        ORDER BY tenant_id DESC
        """
        return self.db.fetch_all(query, (search_term, search_term))
    
    def get_active_tenants(self) -> List[Dict]:
        """Get all active tenants"""
        query = "SELECT * FROM tenant WHERE status = 'Active' ORDER BY tenant_id DESC"
        return self.db.fetch_all(query)
    
    # ========================================================================
    # RENTAL AGREEMENT OPERATIONS
    # ========================================================================
    
    def create_rental_agreement(self, tenant_id: int, room_id: int, 
                               start_date: str, end_date: str, monthly_rent: float,
                               deposit_amount: float) -> bool:
        """Create new rental agreement"""
        query = """
        INSERT INTO rental_agreement (tenant_id, room_id, start_date, end_date, monthly_rent, deposit_amount, status, created_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            result = self.db.execute_query(query, (tenant_id, room_id, start_date, end_date, monthly_rent, deposit_amount, 'Active', datetime.now().date()))
            
            # Update room status to Occupied
            if result:
                update_query = "UPDATE room SET status = 'Occupied' WHERE room_id = %s"
                self.db.execute_query(update_query, (room_id,))
            
            return result
        except Exception as e:
            print(f"✗ Error creating rental agreement: {e}")
            return False
    
    def get_all_rental_agreements(self) -> List[Dict]:
        """Get all rental agreements"""
        query = """
        SELECT ra.*, CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
               r.room_number, b.building_name
        FROM rental_agreement ra
        JOIN tenant t ON ra.tenant_id = t.tenant_id
        JOIN room r ON ra.room_id = r.room_id
        JOIN building b ON r.building_id = b.building_id
        ORDER BY ra.agreement_id DESC
        """
        return self.db.fetch_all(query)
    
    def get_active_rental_agreements(self) -> List[Dict]:
        """Get active rental agreements"""
        query = """
        SELECT ra.*, CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
               r.room_number, b.building_name
        FROM rental_agreement ra
        JOIN tenant t ON ra.tenant_id = t.tenant_id
        JOIN room r ON ra.room_id = r.room_id
        JOIN building b ON r.building_id = b.building_id
        WHERE ra.status = 'Active'
        ORDER BY ra.end_date ASC
        """
        return self.db.fetch_all(query)
    
    # ========================================================================
    # TRANSACTION OPERATIONS
    # ========================================================================
    
    def add_transaction(self, agreement_id: int, transaction_type: str, amount: float,
                       payment_date: str, payment_method: str, status: str, notes: str = "") -> bool:
        """Record new transaction"""
        query = """
        INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes))
    
    def get_all_transactions(self) -> List[Dict]:
        """Get all transactions"""
        query = """
        SELECT t.*, CONCAT(tn.first_name, ' ', tn.last_name) AS tenant_name, r.room_number
        FROM transaction t
        JOIN rental_agreement ra ON t.agreement_id = ra.agreement_id
        JOIN tenant tn ON ra.tenant_id = tn.tenant_id
        JOIN room r ON ra.room_id = r.room_id
        ORDER BY t.transaction_id DESC
        """
        return self.db.fetch_all(query)
    
    def get_transactions_by_status(self, status: str) -> List[Dict]:
        """Get transactions by status (Paid/Pending)"""
        query = """
        SELECT t.*, CONCAT(tn.first_name, ' ', tn.last_name) AS tenant_name, r.room_number
        FROM transaction t
        JOIN rental_agreement ra ON t.agreement_id = ra.agreement_id
        JOIN tenant tn ON ra.tenant_id = tn.tenant_id
        JOIN room r ON ra.room_id = r.room_id
        WHERE t.status = %s
        ORDER BY t.transaction_id DESC
        """
        return self.db.fetch_all(query, (status,))
    
    def update_transaction_status(self, transaction_id: int, status: str) -> bool:
        """Update transaction status"""
        query = "UPDATE transaction SET status = %s WHERE transaction_id = %s"
        return self.db.execute_query(query, (status, transaction_id))
    
    # ========================================================================
    # VIEW OPERATIONS
    # ========================================================================
    
    def get_active_rentals_view(self) -> List[Dict]:
        """Get active rentals from view"""
        query = "SELECT * FROM active_rentals"
        return self.db.fetch_all(query)
    
    # ========================================================================
    # STORED PROCEDURE OPERATIONS
    # ========================================================================
    
    def insert_monthly_rent(self) -> bool:
        """Call stored procedure to insert monthly rent"""
        try:
            self.db.cursor.callproc('insert_monthly_rent')
            self.db.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error calling stored procedure: {e}")
            return False
    
    # ========================================================================
    # REPORTS AND STATISTICS
    # ========================================================================
    
    def get_building_statistics(self) -> List[Dict]:
        """Get statistics per building"""
        query = """
        SELECT b.building_id, b.building_name,
               COUNT(DISTINCT r.room_id) AS total_rooms,
               SUM(CASE WHEN r.status = 'Occupied' THEN 1 ELSE 0 END) AS occupied_rooms,
               SUM(CASE WHEN r.status = 'Available' THEN 1 ELSE 0 END) AS available_rooms,
               ROUND(SUM(r.monthly_rent), 2) AS total_monthly_rent
        FROM building b
        LEFT JOIN room r ON b.building_id = r.building_id
        GROUP BY b.building_id, b.building_name
        """
        return self.db.fetch_all(query)
    
    def get_pending_payments(self) -> List[Dict]:
        """Get all pending payments"""
        query = """
        SELECT t.*, CONCAT(tn.first_name, ' ', tn.last_name) AS tenant_name,
               r.room_number, b.building_name
        FROM transaction t
        JOIN rental_agreement ra ON t.agreement_id = ra.agreement_id
        JOIN tenant tn ON ra.tenant_id = tn.tenant_id
        JOIN room r ON ra.room_id = r.room_id
        JOIN building b ON r.building_id = b.building_id
        WHERE t.status = 'Pending'
        ORDER BY t.payment_date ASC
        """
        return self.db.fetch_all(query)
    
    def close(self):
        """Close database connection"""
        self.db.disconnect()


# Test connection on import
if __name__ == "__main__":
    # Test basic connection
    system = RentalManagementSystem()
    landlords = system.get_all_landlords()
    print(f"Found {len(landlords)} landlords")
    system.close()
