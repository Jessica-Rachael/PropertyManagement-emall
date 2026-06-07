-- ============================================================================
-- RENTAL MANAGEMENT SYSTEM - DATABASE SCHEMA (MySQL)
-- ============================================================================
-- Database: rental_management_system
-- Created: April 2026
-- Purpose: Manage landlords, buildings, rooms, tenants, rental agreements, 
--          and transactions
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS rental_management_system;
USE rental_management_system;

-- ============================================================================
-- TABLE 1: LANDLORD
-- ============================================================================
DROP TABLE IF EXISTS transaction_log;
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS rental_agreement;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS tenant;
DROP TABLE IF EXISTS landlord;

CREATE TABLE landlord (
    landlord_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_date DATE NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 2: BUILDING
-- ============================================================================
CREATE TABLE building (
    building_id INT PRIMARY KEY AUTO_INCREMENT,
    landlord_id INT NOT NULL,
    building_name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    year_built INT NOT NULL,
    total_floors INT NOT NULL,
    created_date DATE NOT NULL,
    FOREIGN KEY (landlord_id) REFERENCES landlord(landlord_id) ON DELETE CASCADE,
    INDEX idx_landlord (landlord_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 3: ROOM
-- ============================================================================
CREATE TABLE room (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    building_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    room_type ENUM('Studio', '1BHK', '2BHK', '3BHK') NOT NULL,
    area_sqft DECIMAL(8,2) NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    status ENUM('Available', 'Occupied') NOT NULL DEFAULT 'Available',
    created_date DATE NOT NULL,
    FOREIGN KEY (building_id) REFERENCES building(building_id) ON DELETE CASCADE,
    INDEX idx_building (building_id),
    UNIQUE KEY unique_room (building_id, room_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 4: TENANT
-- ============================================================================
CREATE TABLE tenant (
    tenant_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    id_proof VARCHAR(50) NOT NULL UNIQUE,
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active',
    registration_date DATE NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 5: RENTAL_AGREEMENT
-- ============================================================================
CREATE TABLE rental_agreement (
    agreement_id INT PRIMARY KEY AUTO_INCREMENT,
    tenant_id INT NOT NULL,
    room_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    deposit_amount DECIMAL(10,2) NOT NULL,
    status ENUM('Active', 'Expired') NOT NULL DEFAULT 'Active',
    created_date DATE NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE CASCADE,
    INDEX idx_tenant (tenant_id),
    INDEX idx_room (room_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 6: TRANSACTION
-- ============================================================================
CREATE TABLE transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    agreement_id INT NOT NULL,
    transaction_type ENUM('Rent', 'Deposit', 'Refund') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status ENUM('Paid', 'Pending') NOT NULL DEFAULT 'Pending',
    notes VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agreement_id) REFERENCES rental_agreement(agreement_id) ON DELETE CASCADE,
    INDEX idx_agreement (agreement_id),
    INDEX idx_status (status),
    INDEX idx_payment_date (payment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE 7: TRANSACTION_LOG (For Trigger)
-- ============================================================================
CREATE TABLE transaction_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_reason VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX idx_landlord_email ON landlord(email);
CREATE INDEX idx_tenant_email ON tenant(email);
CREATE INDEX idx_tenant_status ON tenant(status);
CREATE INDEX idx_building_location ON building(location);
CREATE INDEX idx_room_status ON room(status);
CREATE INDEX idx_agreement_dates ON rental_agreement(start_date, end_date);
CREATE INDEX idx_transaction_method ON transaction(payment_method);

-- ============================================================================
-- End of Schema
-- ============================================================================
