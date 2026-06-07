# RENTAL MANAGEMENT SYSTEM - COMPLETE PROJECT

## 🎯 Project Overview

A fully functional desktop application for managing rental properties, built with:
- **Database**: MySQL 8.0 with normalized design (Database: `rental_management_system`)
- **Backend**: Python 3.8+ with mysql-connector-python
- **Frontend**: Tkinter with modern sidebar navigation
- **Status**: ✅ Fully tested and operational

## 📁 Project Structure

```
rental_system/
├── ER_DIAGRAM.txt                    # Entity Relationship Diagram
├── setup.sh                          # Setup and run guide
├── README.md                         # This file
├── database/
│   ├── schema.sql                   # Database tables (CREATE TABLE)
│   ├── sample_data.sql              # Sample records (INSERT)
│   ├── views_triggers_sprocs.sql    # Views, Triggers, Procedures
│   └── acid_demo.sql                # ACID properties demonstration
└── src/
    ├── database.py                  # Backend: DB connection & CRUD
    └── gui.py                       # Frontend: Tkinter GUI
```

## 🔄 Renamed Entities

| Original | Renamed | Purpose |
|----------|---------|---------|
| Owner | Landlord | Property owner |
| Customer | Tenant | Person renting property |
| Property | Building | Physical structure |
| Unit | Room | Individual rental unit |
| Lease | Rental_Agreement | Rental contract |
| Payment | Transaction | Financial record |

## 🗄️ Database Design

### Tables (6 main + 1 logging)
1. **landlord** - Property owners
2. **building** - Buildings/complexes
3. **room** - Individual rooms/units
4. **tenant** - Renters
5. **rental_agreement** - Active contracts
6. **transaction** - Payments/deposits
7. **transaction_log** - Audit trail (for trigger)

### Key Features
- ✓ AUTO_INCREMENT primary keys
- ✓ Foreign key constraints
- ✓ NOT NULL validations
- ✓ ENUM types for categories
- ✓ Proper indexing for performance

## ⚙️ Backend Features

### CRUD Operations
- Add/View Landlords
- Add/View Buildings
- Add/View Rooms
- Add/View Tenants (with search)
- Create Rental Agreements
- Record Transactions

### Advanced Features
- **Parameterized queries** - SQL injection prevention
- **Connection pooling** - Efficient DB access
- **Error handling** - try-except blocks
- **Transaction support** - COMMIT/ROLLBACK

## 🖥️ Frontend Features

### UI Components
1. **Sidebar Navigation** - Organized menu with sections
2. **Forms** - Structured data entry with validation
3. **Tables (Treeview)** - Scrollable data display
4. **Status Messages** - Success/error popups
5. **Home Dashboard** - Quick statistics

### Sections
- Landlords & Tenants (Add, View, Search)
- Properties & Rooms (Add, View Buildings/Rooms)
- Rentals (Create Agreements, View)
- Transactions (Record, View, Filter)

## 📊 Views, Triggers & Stored Procedures

### 1. Active Rentals VIEW
Shows all currently active rental agreements with:
- Tenant details
- Room information
- Days remaining

```sql
SELECT * FROM active_rentals;
```

### 2. Transaction Update TRIGGER
Logs all status changes to transaction_log table:
- Before/after status
- Timestamp
- Change reason

Automatically fires when transaction status updates.

### 3. Monthly Rent STORED PROCEDURE
Inserts pending rent transactions for all active agreements:

```sql
CALL insert_monthly_rent();
```

Perfect for monthly automation.

## 🔒 ACID Properties

### Atomicity
- Deposit transfer between agreements (all-or-nothing)
- Either complete or rollback

### Consistency
- FK constraint violations rejected
- Database remains in valid state

### Isolation
- Concurrent rent payments
- No interference between transactions

### Durability
- After COMMIT, data persists
- Even on system crash

## 📋 Features Implemented

### Core Functions
- [x] Add Landlord
- [x] Add Building
- [x] Add Room
- [x] Add Tenant
- [x] Create Rental Agreement
- [x] Record Payment/Transaction
- [x] View Data (All tables)

### Advanced Features
- [x] Search Tenant by name
- [x] Filter Transactions (Paid/Pending)
- [x] Active Rentals View
- [x] Building Statistics
- [x] Pending Payments Report
- [x] Transaction Logging

### Database Features
- [x] One VIEW (Active Rentals)
- [x] One TRIGGER (Log Transaction Updates)
- [x] One STORED PROCEDURE (Monthly Rent)
- [x] Sample Data (3-5 per table)

## 🚀 COMPLETE SETUP & RUN GUIDE (For New Users on Different PC)

### ✅ Prerequisites Before Starting

Make sure you have these installed on your computer:

1. **Python** (version 3.8 or higher)
   - Download from: https://www.python.org/downloads/
   - During installation, **CHECK the box "Add Python to PATH"**

2. **MySQL Server** (version 5.7 or 8.0)
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Remember your MySQL root password!
   - Note down where MySQL is installed (usually: `C:\Program Files\MySQL\MySQL Server 8.0`)

3. **A code editor** (VS Code recommended)
   - Download from: https://code.visualstudio.com/

---

### 📋 STEP 1: Download & Extract Project

1. Copy the entire `rental_system` folder to your computer
2. Remember the full path (e.g., `D:\projects\rental_system` or `C:\Users\YourName\rental_system`)

---

### 📦 STEP 2: Install Required Python Package (First Time Only)

1. Open **Command Prompt** or **PowerShell**
2. Navigate to your project folder:
   ```bash
   cd D:\path\to\rental_system
   ```
3. Install the required package:
   ```bash
   pip install mysql-connector-python
   ```
   You should see a message like: `Successfully installed mysql-connector-python-X.X.X`

---

### 🗄️ STEP 3: Setup Database (First Time Only)

#### **Method A: Automatic Setup (Recommended - Easiest)**

1. In Command Prompt/PowerShell, make sure you're in the project folder:
   ```bash
   cd D:\path\to\rental_system
   ```

2. Run the automated setup script:
   ```bash
   python setup_database.py
   ```

3. Follow the prompts:
   - **Step 1**: The script will auto-detect MySQL
   - **Step 2**: Enter your MySQL root password (press Enter if no password)
   - **Steps 3-5**: The script automatically creates database, tables, and sample data
   - **Step 6**: Configuration saved automatically

4. When asked "Would you like to launch the application now?", type `n` and press Enter (we'll launch it next)

#### **Method B: Manual Setup (If Automatic Fails)**

If automatic setup fails, follow these steps:

1. Open **MySQL Command Line Client** or **MySQL Workbench**

2. Execute the SQL files in this order:

   **File 1: Create Database & Tables**
   ```sql
   USE mysql;
   SOURCE C:\path\to\rental_system\database\schema.sql;
   ```

   **File 2: Insert Sample Data**
   ```sql
   SOURCE C:\path\to\rental_system\database\sample_data.sql;
   ```

   **File 3: Create Views & Triggers**
   ```sql
   SOURCE C:\path\to\rental_system\database\views_triggers_sprocs.sql;
   ```

3. Verify data was loaded:
   ```sql
   USE rental_management_system;
   SELECT COUNT(*) FROM landlord;
   ```
   You should see: 5 landlords

---

### 🎮 STEP 4: Run the Application

**After database setup is complete**, run the application:

1. Open **Command Prompt** or **PowerShell**
2. Navigate to project folder:
   ```bash
   cd D:\path\to\rental_system
   ```
3. Launch the application:
   ```bash
   python run.py
   ```

4. You should see:
   ```
   ✓ mysql-connector-python installed
   ✓ tkinter available
   ✓ Database connected
   ```

5. The **Rental Management System** GUI window will open

---

### 🔧 TROUBLESHOOTING

#### Problem 1: "MySQL command not found"
- **Solution**: This is handled automatically. The setup script searches common MySQL installation paths.
- If it still fails, specify MySQL path in setup_database.py

#### Problem 2: "Access denied for user 'root'@'localhost'"
- **Solution**: Make sure you entered the correct MySQL password
- If your MySQL has no password, just press Enter when prompted
- Default password is saved to `.db_config.json` (created during setup)

#### Problem 3: "mysql-connector-python not installed"
- **Solution**: Run this in Command Prompt:
  ```bash
  pip install mysql-connector-python
  ```

#### Problem 4: "Module 'tkinter' not found"
- **Solution**: Tkinter comes with Python. If missing:
  - **Windows**: Reinstall Python and check "tcl/tk and IDLE" option
  - **Mac**: `brew install python-tk`
  - **Linux**: `sudo apt-get install python3-tk`

#### Problem 5: "Table 'landlord' already exists"
- **Solution**: Database already set up. Just run `python run.py` to launch
- If you want fresh data, delete database and re-run setup:
  ```sql
  DROP DATABASE rental_management_system;
  ```

---

### ✅ Verification Checklist

After setup, verify everything works:

- [ ] MySQL Server is running
- [ ] `python setup_database.py` completed successfully
- [ ] `python run.py` opens the GUI window
- [ ] You can see the home dashboard with statistics
- [ ] Sidebar menu appears on the left side
- [ ] You can click through different sections

---

### 📂 Project Structure After Setup

```
rental_system/
├── .db_config.json                 ← Config file (auto-created)
├── src/
│   ├── database.py                 ← Backend code (WITH PASSWORD SAVED)
│   └── gui.py                      ← Application interface
├── database/
│   ├── schema.sql                  ← Database tables
│   ├── sample_data.sql             ← Sample records
│   └── views_triggers_sprocs.sql   ← Views & triggers
├── run.py                          ← Application launcher ✅ USE THIS
├── setup_database.py               ← Database setup ✅ USE THIS FIRST
├── test_connection.py              ← Verification script
└── README.md                       ← This file
```

---

### 🎯 Daily Usage

**To run the application every day:**

1. Make sure MySQL Server is running
2. Open Command Prompt/PowerShell
3. Navigate to project folder
4. Run:
   ```bash
   python run.py
   ```
5. The GUI will open with all your saved data

**No need to re-run setup!** Setup is one-time only.

---

### 💾 Database Information

- **Database Name**: `rental_management_system`
- **MySQL User**: `root`
- **MySQL Password**: Saved in `.db_config.json` (created during setup)
- **Host**: `localhost`
- **Port**: `3306`

**Tables Created**:
- landlord (Property owners)
- building (Rental properties)
- room (Individual units)
- tenant (Renters)
- rental_agreement (Lease contracts)
- transaction (Payments)
- transaction_log (Audit trail)

## 📸 Application Screenshots (Conceptual)

### Main Screen
```
┌─────────────────────────────────────────┐
│  🏢 RENTAL MANAGEMENT SYSTEM            │
├────────────┬──────────────────────────┤
│  LANDLORDS │  Welcome to Your          │
│  & TENANTS │  Rental Management        │
│            │  Platform                  │
│ Add...     │                           │
│ View...    │  Landlords: 5             │
│ Search...  │  Tenants: 5               │
│            │  Buildings: 5             │
│ PROPERTIES │  Rooms: 9                 │
│ & ROOMS    │                           │
│            │                           │
│ RENTALS    │                           │
│ & TXNS     │                           │
└────────────┴──────────────────────────┘
```

## 💾 Database Statistics

### Sample Data Provided
- 5 Landlords
- 5 Buildings
- 9 Rooms
- 5 Tenants
- 5 Rental Agreements
- 8 Transactions

### Realistic Scenarios
- Various room types (Studio, 1BHK, 2BHK, 3BHK)
- Mixed transaction statuses (Paid, Pending)
- Active and expired agreements
- Different payment methods

## 🧪 Testing ACID Properties

Run the ACID demo:
```bash
mysql -u root -p rental_management_system < database/acid_demo.sql
```

Tests:
1. **Atomicity** - Deposit transfer (success/rollback)
2. **Consistency** - FK constraint violation
3. **Isolation** - Concurrent transactions
4. **Durability** - Data persistence
5. **Trigger** - Transaction log updates
6. **View** - Active rentals report
7. **Procedure** - Monthly rent generation

## 🔍 Key Design Decisions

### Naming
- Meaningful, landlord-focused terminology
- Consistent across database, backend, GUI
- Clear English labels for user interface

### Database
- Normalized schema (avoiding redundancy)
- Proper indexing for common queries
- Cascading deletes for data integrity
- ENUM types for standardized values

### Backend
- Class-based architecture (RentalManagementSystem)
- Parameterized queries (SQL injection safe)
- Dictionary-based results (ease of access)
- Comprehensive error handling

### Frontend
- Sidebar navigation (improved UX)
- Consistent color scheme
- Responsive layouts with Frames
- Clear field labels and validation
- Success/error messaging

## 📝 Common Operations

### Add a Tenant
1. Click "Add Tenant" in sidebar
2. Fill form fields
3. Click "Submit"
4. Success message appears

### Create Rental Agreement
1. Click "Create Agreement"
2. Select Tenant & Room
3. Enter dates and amounts
4. Click "Submit"
5. Room status changes to "Occupied"

### Record Payment
1. Click "Record Payment"
2. Select Agreement
3. Enter amount & date
4. Select Method
5. Choose Status (Paid/Pending)
6. Click "Submit"
7. Trigger logs the transaction

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in database.py
- Ensure database exists

### FOREIGN KEY Constraint Error
- Don't delete landlord with buildings
- Don't delete building with rooms
- Use existing IDs for foreign keys

### GUI Not Starting
- Verify tkinter installed (usually comes with Python)
- Check Python version is 3.8+
- See console output for errors

## 📚 SQL Reference

### View Active Rentals
```sql
SELECT * FROM active_rentals;
```

### Get Pending Payments
```sql
SELECT * FROM transaction WHERE status = 'Pending';
```

### Build Statistics
```sql
SELECT building_name, COUNT(*) as total_rooms
FROM room r
JOIN building b ON r.building_id = b.building_id
GROUP BY b.building_id;
```

### Call Monthly Rent Procedure
```sql
CALL insert_monthly_rent();
```

## ✨ Future Enhancements

- Export to PDF/Excel
- Email notifications
- Advanced reports
- Mobile app
- Multi-user login
- Payment integrations

## 📄 License & Credits

Educational Project - Loyola University DB Course
Created: April 2026

## 📞 Support

For issues or questions:
1. Check database connection
2. Review error messages in console
3. Verify all SQL files executed
4. Check sample data inserted

---

---

## 🔧 Final Fixes & Improvements (v1.1)

This version includes important fixes to ensure the system works flawlessly on any new PC:

### ✅ Fix 1: MySQL PATH Detection
- **Problem**: MySQL executable not found in system PATH
- **Solution**: `setup_database.py` now auto-detects MySQL in common installation directories:
  - `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`
  - `C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe`
  - `C:\Program Files (x86)\MySQL\*\bin\mysql.exe`
- **Result**: Setup works without manual PATH configuration

### ✅ Fix 2: Password Persistence
- **Problem**: MySQL password forgotten between runs
- **Solution**: 
  - Password automatically saved to `.db_config.json` during setup
  - `src/database.py` loads password from config file
  - Default password hardcoded as fallback
- **Result**: Password remembered across application restarts

### ✅ Fix 3: Idempotent Database Setup
- **Problem**: Re-running setup fails with "table already exists" errors
- **Solution**: SQL files now include `DROP IF EXISTS` statements:
  - `DROP TABLE IF EXISTS transaction_log, transaction, rental_agreement...`
  - `DROP VIEW IF EXISTS active_rentals`
  - `DROP PROCEDURE IF EXISTS insert_monthly_rent`
  - `DROP TRIGGER IF EXISTS log_transaction_status_update`
- **Result**: Can safely re-run setup multiple times

### ✅ Fix 4: Improved Error Handling
- **Backend**: `src/database.py` tries multiple config file locations
- **Frontend**: `run.py` provides clear error messages with solutions
- **Setup**: `setup_database.py` handles password input gracefully
- **Result**: Better debugging when issues occur

### ✅ Fix 5: Config File Management
- **Auto-created**: `.db_config.json` created during setup
- **Multiple locations**: Checked in root, src, and current directory
- **Fallback**: Uses hardcoded password if config not found
- **Result**: Flexible deployment across different PC environments

### ✅ Fix 6: Attribute Name Corrections
- **Problem**: `run.py` was calling `system.system.get_all_landlords()` (double reference)
- **Solution**: Corrected to `system.get_all_landlords()`
- **Result**: Database queries work correctly

### ✅ Fix 7: Comprehensive Testing
- **New file**: `test_connection.py` for quick verification
- **Tests**: Database connection, password authentication, data retrieval
- **Usage**: `python test_connection.py`
- **Result**: Easy troubleshooting during setup

---

## 📊 System Requirements (Verified)

### Minimum Requirements
- **OS**: Windows 7+ / Mac / Linux
- **Python**: 3.8 or higher
- **MySQL**: 5.7 or 8.0
- **RAM**: 2 GB minimum
- **Disk**: 100 MB for full installation

### Recommended Setup
- **OS**: Windows 10/11 / Mac OS 11+ / Ubuntu 20+
- **Python**: 3.9 or higher
- **MySQL**: 8.0
- **RAM**: 4 GB
- **Disk**: 500 MB (with future data growth)

---

## 🎓 Learning Outcomes

This project demonstrates:

1. **Database Design**
   - Entity-Relationship modeling
   - Normalization (3NF)
   - Constraints & Integrity

2. **SQL**
   - DDL (CREATE TABLE, VIEW)
   - DML (INSERT, SELECT, UPDATE)
   - DCL (GRANT privileges)
   - Transactions & ACID

3. **Python**
   - OOP (Classes & Methods)
   - Error handling
   - File I/O
   - Modular design

4. **Desktop GUI**
   - Event-driven programming
   - Layout management
   - Form validation
   - Data binding

5. **DevOps**
   - Environment configuration
   - Deployment automation
   - Troubleshooting

---

## 📞 Support & FAQ

**Q: Can I use this with a password-protected MySQL?**
A: Yes! Enter password during setup. It will be saved to `.db_config.json`

**Q: How do I backup my data?**
A: Use MySQL backup:
```bash
mysqldump -u root -p rental_management_system > backup.sql
```

**Q: Can multiple users run this simultaneously?**
A: Yes, MySQL supports concurrent connections. All users see same data.

**Q: How do I reset to sample data?**
A: Drop and recreate database:
```bash
DROP DATABASE rental_management_system;
```
Then re-run `python setup_database.py`

**Q: Is the data real? Can I use it in production?**
A: No, it's sample data for testing. Create your own records.

---

**Thank you for using the Rental Management System!** 🎉
