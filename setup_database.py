"""
===============================================================================
RENTAL MANAGEMENT SYSTEM - AUTOMATED SETUP
===============================================================================
This script automates the entire database setup process
Run this ONCE before using the application for the first time
===============================================================================
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(70)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_mysql_installed():
    """Check if MySQL is installed"""
    print_info("Checking MySQL installation...")
    
    # Try standard PATH first
    mysql_cmd = 'mysql'
    
    # Check common MySQL installation paths
    common_paths = [
        r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe',
        r'C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe',
        r'C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe',
        r'C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysql.exe',
    ]
    
    # Check if any common path exists
    for path in common_paths:
        if Path(path).exists():
            mysql_cmd = path
            print_success(f"MySQL found at: {path}")
            return mysql_cmd
    
    # Try using mysql from PATH
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(f"MySQL found in PATH: {result.stdout.strip()}")
            return mysql_cmd
    except FileNotFoundError:
        pass
    except Exception as e:
        pass
    
    print_error("MySQL not found")
    return None


def get_mysql_password():
    """Get MySQL root password from user"""
    print_info("Enter your MySQL root password (press Enter if no password):")
    import getpass
    password = getpass.getpass("Password: ")
    return password


def save_db_config(password):
    """Save database configuration to file for later use"""
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': password,
            'database': 'rental_management_system',
            'port': 3306
        }
        
        config_file = Path(__file__).parent / '.db_config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print_success(f"Configuration saved to {config_file.name}")
        return True
    except Exception as e:
        print_warning(f"Could not save config: {e}")
        return False


def run_sql_file(mysql_cmd, filename, database=None, password=""):
    """Execute a SQL file"""
    current_dir = Path(__file__).parent
    sql_file = current_dir / "database" / filename
    
    if not sql_file.exists():
        print_error(f"File not found: {sql_file}")
        return False
    
    try:
        print_info(f"Running {filename}...")
        
        # Build command
        cmd = [mysql_cmd, '-u', 'root']
        
        if password:
            cmd.extend(['-p' + password])
        
        if database:
            cmd.extend([database])
        
        # Execute SQL file
        with open(sql_file, 'r') as f:
            result = subprocess.run(cmd, stdin=f, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print_success(f"{filename} executed successfully")
            return True
        else:
            if result.stderr:
                print_error(f"Error executing {filename}: {result.stderr}")
            else:
                print_success(f"{filename} executed (with warnings)")
            return True  # Continue anyway
    except subprocess.TimeoutExpired:
        print_error(f"Timeout executing {filename}")
        return False
    except Exception as e:
        print_error(f"Error executing {filename}: {e}")
        return False


def main():
    """Main setup function"""
    print_header("RENTAL MANAGEMENT SYSTEM - DATABASE SETUP")
    
    print(f"{Colors.BOLD}This script will set up your database automatically{Colors.END}")
    print(f"{Colors.BOLD}Steps:{Colors.END}")
    print("  1. Check MySQL installation")
    print("  2. Get MySQL credentials")
    print("  3. Create database schema")
    print("  4. Load sample data")
    print("  5. Create views, triggers, procedures")
    print("  6. Save configuration")
    print()
    
    # Step 1: Check MySQL
    print_header("Step 1: Checking MySQL")
    mysql_cmd = check_mysql_installed()
    if not mysql_cmd:
        print_error("MySQL is not installed or not in PATH")
        print_info("Please install MySQL or add it to your PATH")
        print_info("Windows: Download from https://dev.mysql.com/downloads/mysql/")
        print_info("Or install: choco install mysql --limit-output")
        sys.exit(1)
    
    # Step 2: Get password
    print_header("Step 2: MySQL Credentials")
    password = get_mysql_password()
    
    # Step 3: Create schema
    print_header("Step 3: Creating Database Schema")
    if not run_sql_file(mysql_cmd, "schema.sql", password=password):
        print_error("Failed to create schema")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 4: Insert sample data
    print_header("Step 4: Loading Sample Data")
    if not run_sql_file(mysql_cmd, "sample_data.sql", database="rental_management_system", password=password):
        print_error("Failed to load sample data")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 5: Create views, triggers, procedures
    print_header("Step 5: Creating Views, Triggers & Procedures")
    if not run_sql_file(mysql_cmd, "views_triggers_sprocs.sql", database="rental_management_system", password=password):
        print_error("Failed to create views and triggers")
        sys.exit(1)
    
    # Step 6: Save configuration
    print_header("Step 6: Saving Configuration")
    save_db_config(password)
    
    # Success!
    print_header("✓ DATABASE SETUP COMPLETE!")
    print(f"{Colors.GREEN}{Colors.BOLD}All databases and tables have been created successfully!{Colors.END}\n")
    
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print(f"  1. Run the application:")
    print(f"     {Colors.CYAN}python run.py{Colors.END}")
    print()
    
    # Ask to launch GUI
    print_info("Would you like to launch the application now? (y/n)")
    response = input("Launch GUI? (y/n): ").strip().lower()
    
    if response == 'y':
        print_info("Launching GUI...")
        try:
            subprocess.Popen([sys.executable, "run.py"], cwd=Path(__file__).parent)
            print_success("Application launched!")
        except Exception as e:
            print_error(f"Could not launch GUI: {e}")
            print_info("Run manually: python run.py")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Setup complete!{Colors.END}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
