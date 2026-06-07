#!/bin/bash
# OR for Windows: .ps1 file

# ============================================================================
# RENTAL MANAGEMENT SYSTEM - SETUP AND RUN GUIDE
# ============================================================================
# Complete steps to set up and run the application
# ============================================================================

echo "=========================================="
echo "RENTAL MANAGEMENT SYSTEM - SETUP"
echo "=========================================="

# Step 1: Check Python installation
echo ""
echo "Step 1: Checking Python installation..."
python --version

if [ $? -ne 0 ]; then
    echo "Error: Python not found. Please install Python 3.8+."
    exit 1
fi

# Step 2: Install required Python packages
echo ""
echo "Step 2: Installing Python packages..."
pip install mysql-connector-python

# Step 3: MySQL setup instructions
echo ""
echo "Step 3: MySQL Database Setup"
echo "---"
echo "Prerequisites:"
echo "  1. MySQL Server installed and running"
echo "  2. MySQL username: root"
echo "  3. Password: (configure in database.py if needed)"
echo ""
echo "Follow these steps:"
echo ""
echo "a) Open MySQL command line or MySQL Workbench"
echo ""
echo "b) Create database:"
echo "   mysql -u root -p < database/schema.sql"
echo ""
echo "c) Insert sample data:"
echo "   mysql -u root -p rental_management_system < database/sample_data.sql"
echo ""
echo "d) Add views, triggers, and procedures:"
echo "   mysql -u root -p rental_management_system < database/views_triggers_sprocs.sql"
echo ""
echo "e) (Optional) Test ACID properties:"
echo "   mysql -u root -p rental_management_system < database/acid_demo.sql"
echo ""

# Step 4: Configure database connection
echo ""
echo "Step 4: Configure Database Connection"
echo "---"
echo "If your MySQL password is different:"
echo "  Edit src/database.py"
echo "  Update: DB_CONFIG['password'] = 'your_password'"
echo ""

# Step 5: Run the application
echo ""
echo "Step 5: Running the Application"
echo "---"
echo "Execute: python src/gui.py"
echo ""

echo "=========================================="
echo "Setup complete! Application ready to run."
echo "=========================================="
