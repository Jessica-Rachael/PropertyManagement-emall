-- ============================================================================
-- ACID PROPERTIES DEMONSTRATION
-- ============================================================================
-- This file demonstrates ACID properties using simple, real-world scenarios
-- from the Rental Management System
-- ============================================================================

USE rental_management_system;

-- ============================================================================
-- 1. ATOMICITY DEMO
-- ===========================================================================
-- Atomicity: A transaction is all-or-nothing. 
-- If any part fails, the entire transaction is rolled back.
-- ============================================================================

-- SCENARIO: Transfer deposit from one agreement to another for a tenant moving rooms
-- If transfer fails halfway, both should remain unchanged

SET autocommit = 0;

START TRANSACTION;

-- Deduct deposit from old agreement
UPDATE rental_agreement 
SET deposit_amount = deposit_amount - 50000 
WHERE agreement_id = 1;

-- Insert refund transaction for old agreement
INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
VALUES (1, 'Refund', 50000, CURDATE(), 'Bank Transfer', 'Pending', 'Deposit transfer initiated');

-- Add deposit to new agreement
UPDATE rental_agreement 
SET deposit_amount = deposit_amount + 50000 
WHERE agreement_id = 5;

-- Insert deposit received transaction for new agreement
INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
VALUES (5, 'Deposit', 50000, CURDATE(), 'Bank Transfer', 'Received', 'Deposit transferred');

-- All or nothing - commit or rollback together
-- To test rollback, uncomment ROLLBACK below
COMMIT;
-- ROLLBACK;  -- Uncommit this to rollback entire transaction

SELECT 'ATOMICITY DEMO - After Transaction' AS test_type;
SELECT agreement_id, tenant_id, deposit_amount FROM rental_agreement WHERE agreement_id IN (1, 5);
SELECT transaction_id, transaction_type, amount, status FROM transaction WHERE agreement_id IN (1, 5) ORDER BY transaction_id DESC LIMIT 2;

SET autocommit = 1;

-- ============================================================================
-- 2. CONSISTENCY DEMO
-- ============================================================================
-- Consistency: Database moves from one valid state to another valid state.
-- Foreign key constraints and validation rules are maintained.
-- ============================================================================

-- SCENARIO: Try to create a rental agreement with a non-existent room
-- This should violate referential integrity and be rejected

SELECT 'CONSISTENCY DEMO - Before Constraint Violation' AS test_type;

-- This will FAIL because room_id 9999 doesn't exist (FK constraint)
-- The database remains in a valid state
INSERT INTO rental_agreement (tenant_id, room_id, start_date, end_date, monthly_rent, deposit_amount, status, created_date)
VALUES (1, 9999, '2025-01-01', '2026-01-01', 25000, 75000, 'Active', CURDATE());
-- Error: FOREIGN KEY constraint failed

-- The table is still valid - no invalid data was inserted
SELECT COUNT(*) AS rental_agreements_count FROM rental_agreement;

-- ============================================================================
-- 3. ISOLATION DEMO
-- ============================================================================
-- Isolation: Concurrent transactions don't interfere with each other.
-- Each transaction sees a consistent view of the data.
-- ============================================================================

-- SCENARIO: Two simultaneous rent payments for different agreements
-- Each transaction is isolated and doesn't affect the other

SELECT 'ISOLATION DEMO - Before Concurrent Transactions' AS test_type;

-- Transaction 1: Record rent payment for Agreement 1
START TRANSACTION;
INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
VALUES (1, 'Rent', 22000, CURDATE(), 'Online', 'Paid', 'March 2025 rent - Online');
COMMIT;

-- Transaction 2: Record rent payment for Agreement 2
-- (In real scenario, this would run simultaneously)
START TRANSACTION;
INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
VALUES (2, 'Rent', 25000, CURDATE(), 'Online', 'Paid', 'March 2025 rent - Online');
COMMIT;

-- Both transactions completed successfully without interference
SELECT 'ISOLATION DEMO - After Concurrent Transactions' AS test_type;
SELECT transaction_id, agreement_id, transaction_type, amount, status 
FROM transaction 
WHERE (agreement_id IN (1, 2) AND transaction_type = 'Rent')
ORDER BY transaction_id DESC LIMIT 2;

-- ============================================================================
-- 4. DURABILITY DEMO
-- ============================================================================
-- Durability: Once a transaction is committed, it persists permanently.
-- Even if the system crashes, the data remains.
-- ============================================================================

-- SCENARIO: After committing a transaction, the data is durable

SELECT 'DURABILITY DEMO - Durable Data After Commit' AS test_type;

-- Add a transaction
INSERT INTO transaction (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
VALUES (3, 'Rent', 65000, CURDATE(), 'Cheque', 'Paid', 'Durable transaction test');

-- Commit ensures durability
COMMIT;

-- Even if system crashes now, this data will exist after restart
SELECT * FROM transaction WHERE notes = 'Durable transaction test';

-- ============================================================================
-- 5. PRACTICAL TRANSACTION EXAMPLES
-- ============================================================================

-- Example 1: Full rental agreement setup with multiple steps (should all succeed or all fail)
DROP PROCEDURE IF EXISTS create_complete_rental;

DELIMITER $$
CREATE PROCEDURE create_complete_rental(
    IN p_tenant_id INT,
    IN p_room_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_monthly_rent DECIMAL(10,2),
    IN p_deposit_amount DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'ERROR: Rental creation failed - transaction rolled back' AS result;
    END;
    
    START TRANSACTION;
    
    -- Step 1: Create rental agreement
    INSERT INTO rental_agreement 
    (tenant_id, room_id, start_date, end_date, monthly_rent, deposit_amount, status, created_date)
    VALUES (p_tenant_id, p_room_id, p_start_date, p_end_date, p_monthly_rent, p_deposit_amount, 'Active', CURDATE());
    
    -- Step 2: Update room status
    UPDATE room SET status = 'Occupied' WHERE room_id = p_room_id;
    
    -- Step 3: Record initial deposit transaction
    INSERT INTO transaction 
    (agreement_id, transaction_type, amount, payment_date, payment_method, status, notes)
    SELECT 
        LAST_INSERT_ID(),
        'Deposit',
        p_deposit_amount,
        CURDATE(),
        'Bank Transfer',
        'Paid',
        'Initial deposit received'
    FROM DUAL;
    
    COMMIT;
    SELECT 'SUCCESS: Rental agreement created completely' AS result;
END$$

DELIMITER ;

-- Test the procedure
-- CALL create_complete_rental(1, 3, '2025-04-01', '2026-03-31', 35000, 105000);

-- ============================================================================
-- 6. TRANSACTION LOG VIEW (Uses the TRIGGER)
-- ============================================================================
SELECT 'TRANSACTION LOG - Showing all updates triggered' AS section;
SELECT * FROM transaction_log LIMIT 5;

-- ============================================================================
-- 7. VIEWS FOR DATA CONSISTENCY
-- ============================================================================
SELECT 'ACTIVE RENTALS VIEW - Consistent Point-In-Time Data' AS section;
SELECT * FROM active_rentals LIMIT 5;

-- ============================================================================
-- SUMMARY OF ACID PROPERTIES TESTED
-- ============================================================================
/*
✓ ATOMICITY:    Deposit transfer - all debt/credit operations succeed or all fail
✓ CONSISTENCY:  FK constraint violation test - database rejects invalid state
✓ ISOLATION:    Concurrent rent payments - transactions don't interfere
✓ DURABILITY:   After COMMIT, data persists permanently
✓ TRIGGERS:     Transaction status changes are logged automatically
✓ VIEWS:        Active rentals show consistent, aggregated data
✓ PROCEDURES:   Complex multi-step operations maintain consistency
*/

-- ============================================================================
-- End of ACID Demo
-- ============================================================================
