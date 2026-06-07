-- ============================================================================
-- SAMPLE DATA FOR RENTAL MANAGEMENT SYSTEM
-- ============================================================================
-- This file contains 3-5 sample records for each table
-- Run this AFTER creating the schema
-- ============================================================================

USE rental_management_system;

-- ============================================================================
-- SAMPLE LANDLORD DATA (5 records)
-- ============================================================================
INSERT INTO landlord (landlord_id, first_name, last_name, email, phone, address, created_date) VALUES
(1, 'Rajesh', 'Kumar', 'rajesh.kumar@email.com', '9876543210', '123 MG Road, Delhi', '2025-01-15'),
(2, 'Priya', 'Singh', 'priya.singh@email.com', '9876543211', '456 Brigade Road, Bangalore', '2025-01-20'),
(3, 'Amit', 'Patel', 'amit.patel@email.com', '9876543212', '789 Marine Drive, Mumbai', '2025-02-01'),
(4, 'Sneha', 'Desai', 'sneha.desai@email.com', '9876543213', '321 Connaught Place, Delhi', '2025-02-10'),
(5, 'Vikram', 'Sharma', 'vikram.sharma@email.com', '9876543214', '654 Koramangala, Bangalore', '2025-02-15');

-- ============================================================================
-- SAMPLE BUILDING DATA (5 records)
-- ============================================================================
INSERT INTO building (building_id, landlord_id, building_name, location, year_built, total_floors, created_date) VALUES
(1, 1, 'Skyview Apartments', 'Delhi - Sector 12', 2015, 10, '2025-01-16'),
(2, 2, 'Green Valley Complex', 'Bangalore - Whitefield', 2018, 15, '2025-01-21'),
(3, 3, 'Oceanfront Residency', 'Mumbai - Bandra', 2020, 20, '2025-02-02'),
(4, 4, 'Central Park Towers', 'Delhi - CP', 2019, 12, '2025-02-11'),
(5, 5, 'Tech Park Residences', 'Bangalore - Indiranagar', 2017, 8, '2025-02-16');

-- ============================================================================
-- SAMPLE ROOM DATA (5+ records across different buildings)
-- ============================================================================
INSERT INTO room (room_id, building_id, room_number, room_type, area_sqft, monthly_rent, status, created_date) VALUES
(1, 1, '101', 'Studio', 450.50, 15000, 'Available', '2025-01-16'),
(2, 1, '102', '1BHK', 650.75, 22000, 'Occupied', '2025-01-16'),
(3, 1, '201', '2BHK', 950.00, 35000, 'Available', '2025-01-16'),
(4, 2, 'A101', '1BHK', 700.25, 25000, 'Occupied', '2025-01-21'),
(5, 2, 'A102', '2BHK', 1100.50, 40000, 'Available', '2025-01-21'),
(6, 3, 'B501', '3BHK', 1500.75, 65000, 'Occupied', '2025-02-02'),
(7, 3, 'B502', '2BHK', 1050.00, 45000, 'Available', '2025-02-02'),
(8, 4, 'CP01', '1BHK', 750.50, 28000, 'Occupied', '2025-02-11'),
(9, 5, 'TP01', '2BHK', 950.75, 38000, 'Available', '2025-02-16');

-- ============================================================================
-- SAMPLE TENANT DATA (5+ records)
-- ============================================================================
INSERT INTO tenant (tenant_id, first_name, last_name, email, phone, id_proof, status, registration_date) VALUES
(1, 'Arun', 'Verma', 'arun.verma@email.com', '9012345678', 'ID001234', 'Active', '2025-01-20'),
(2, 'Neha', 'Gupta', 'neha.gupta@email.com', '9012345679', 'ID001235', 'Active', '2025-01-25'),
(3, 'Sanjay', 'Rao', 'sanjay.rao@email.com', '9012345680', 'ID001236', 'Active', '2025-02-05'),
(4, 'Pooja', 'Nair', 'pooja.nair@email.com', '9012345681', 'ID001237', 'Active', '2025-02-10'),
(5, 'Rohit', 'Iyer', 'rohit.iyer@email.com', '9012345682', 'ID001238', 'Inactive', '2024-12-15');

-- ============================================================================
-- SAMPLE RENTAL_AGREEMENT DATA (5+ records)
-- ============================================================================
INSERT INTO rental_agreement (agreement_id, tenant_id, room_id, start_date, end_date, monthly_rent, deposit_amount, status, created_date) VALUES
(1, 1, 2, '2025-01-25', '2026-01-24', 22000, 66000, 'Active', '2025-01-20'),
(2, 2, 4, '2025-02-01', '2026-01-31', 25000, 75000, 'Active', '2025-01-25'),
(3, 3, 6, '2025-02-10', '2026-02-09', 65000, 195000, 'Active', '2025-02-05'),
(4, 4, 8, '2025-02-15', '2026-02-14', 28000, 84000, 'Active', '2025-02-10'),
(5, 5, 3, '2024-10-01', '2025-09-30', 35000, 105000, 'Expired', '2024-09-25');

-- ============================================================================
-- SAMPLE TRANSACTION DATA (5+ records)
-- ============================================================================
INSERT INTO transaction (transaction_id, agreement_id, transaction_type, amount, payment_date, payment_method, status, notes) VALUES
(1, 1, 'Deposit', 66000, '2025-01-25', 'Bank Transfer', 'Paid', 'Initial deposit received'),
(2, 1, 'Rent', 22000, '2025-02-01', 'Online', 'Paid', 'February 2025 rent'),
(3, 2, 'Deposit', 75000, '2025-02-01', 'Cheque', 'Paid', 'Initial deposit received'),
(4, 2, 'Rent', 25000, '2025-03-01', 'Online', 'Pending', 'March 2025 rent - Due'),
(5, 3, 'Deposit', 195000, '2025-02-10', 'Bank Transfer', 'Paid', 'Initial deposit received'),
(6, 3, 'Rent', 65000, '2025-03-01', 'Cheque', 'Paid', 'February 2025 rent'),
(7, 4, 'Deposit', 84000, '2025-02-15', 'Online', 'Paid', 'Initial deposit received'),
(8, 5, 'Refund', 105000, '2025-10-15', 'Bank Transfer', 'Paid', 'Deposit refunded after expiry');

-- ============================================================================
-- Verify Data Insertion
-- ============================================================================
SELECT 'Landlords' AS table_name, COUNT(*) AS record_count FROM landlord
UNION ALL
SELECT 'Buildings', COUNT(*) FROM building
UNION ALL
SELECT 'Rooms', COUNT(*) FROM room
UNION ALL
SELECT 'Tenants', COUNT(*) FROM tenant
UNION ALL
SELECT 'Rental Agreements', COUNT(*) FROM rental_agreement
UNION ALL
SELECT 'Transactions', COUNT(*) FROM transaction;

-- ============================================================================
-- End of Sample Data
-- ============================================================================
