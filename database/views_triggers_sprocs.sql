-- ============================================================================
-- VIEWS, TRIGGERS, AND STORED PROCEDURES
-- ============================================================================

USE rental_management_system;

-- ============================================================================
-- VIEW 1: ACTIVE_RENTALS
-- Shows currently active rental agreements with tenant and room details
-- ============================================================================
DROP VIEW IF EXISTS active_rentals;
CREATE OR REPLACE VIEW active_rentals AS
SELECT 
    ra.agreement_id,
    CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
    t.email AS tenant_email,
    t.phone AS tenant_phone,
    b.building_name,
    r.room_number,
    r.room_type,
    ra.monthly_rent,
    ra.start_date,
    ra.end_date,
    ra.deposit_amount,
    ra.status,
    DATEDIFF(ra.end_date, CURDATE()) AS days_remaining
FROM 
    rental_agreement ra
    JOIN tenant t ON ra.tenant_id = t.tenant_id
    JOIN room r ON ra.room_id = r.room_id
    JOIN building b ON r.building_id = b.building_id
WHERE 
    ra.status = 'Active'
    AND ra.start_date <= CURDATE()
    AND ra.end_date >= CURDATE()
ORDER BY 
    ra.end_date ASC;

-- ============================================================================
-- TRIGGER 1: LOG_TRANSACTION_STATUS_UPDATE
-- Logs all updates to transaction status into transaction_log table
-- ============================================================================
DROP TRIGGER IF EXISTS log_transaction_status_update;
DELIMITER $$

CREATE TRIGGER log_transaction_status_update
AFTER UPDATE ON transaction
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO transaction_log (transaction_id, old_status, new_status, change_reason)
        VALUES (NEW.transaction_id, OLD.status, NEW.status, 'Status updated');
    END IF;
END$$

DELIMITER ;

-- ============================================================================
-- STORED PROCEDURE 1: INSERT_MONTHLY_RENT
-- Automatically inserts pending rent transactions for all active agreements
-- Should be executed on the 1st of each month
-- ============================================================================
DROP PROCEDURE IF EXISTS insert_monthly_rent;
DELIMITER $$

CREATE PROCEDURE insert_monthly_rent()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_agreement_id INT;
    DECLARE v_monthly_rent DECIMAL(10,2);
    DECLARE v_current_date DATE;
    
    DECLARE rent_cursor CURSOR FOR
        SELECT ra.agreement_id, ra.monthly_rent
        FROM rental_agreement ra
        WHERE ra.status = 'Active'
        AND ra.start_date <= CURDATE()
        AND ra.end_date >= CURDATE();
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    SET v_current_date = CURDATE();
    
    OPEN rent_cursor;
    
    read_loop: LOOP
        FETCH rent_cursor INTO v_agreement_id, v_monthly_rent;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        INSERT INTO transaction (
            agreement_id,
            transaction_type,
            amount,
            payment_date,
            payment_method,
            status,
            notes
        ) VALUES (
            v_agreement_id,
            'Rent',
            v_monthly_rent,
            v_current_date,
            'Not Specified',
            'Pending',
            CONCAT('Auto-generated rent for ', MONTH(v_current_date), '/', YEAR(v_current_date))
        );
    END LOOP;
    
    CLOSE rent_cursor;
END$$

DELIMITER ;

-- ============================================================================
-- TEST QUERIES FOR VIEWS, TRIGGERS, AND STORED PROCEDURES
-- ============================================================================

-- Test VIEW: SELECT * FROM active_rentals;

-- Test TRIGGER: Update transaction status and check transaction_log
-- UPDATE transaction SET status = 'Paid' WHERE transaction_id = 4;
-- SELECT * FROM transaction_log WHERE transaction_id = 4;

-- Test STORED PROCEDURE: Call the monthly rent insertion procedure
-- CALL insert_monthly_rent();
-- SELECT * FROM transaction WHERE transaction_type = 'Rent' AND status = 'Pending';

-- ============================================================================
-- End of Views, Triggers, and Stored Procedures
-- ============================================================================
