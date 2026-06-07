"""
===============================================================================
RENTAL MANAGEMENT SYSTEM - QUICK LAUNCHER
===============================================================================
This script checks setup and launches the GUI application
Run this to start the application
===============================================================================
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def check_dependencies():
    """Check if all dependencies are installed"""
    print(f"{Colors.BLUE}Checking dependencies...{Colors.END}\n")
    
    missing = []
    
    # Check mysql-connector-python
    try:
        import mysql.connector
        print(f"{Colors.GREEN}✓ mysql-connector-python installed{Colors.END}")
    except ImportError:
        print(f"{Colors.RED}✗ mysql-connector-python NOT installed{Colors.END}")
        missing.append("mysql-connector-python")
    
    # Check tkinter
    try:
        import tkinter
        print(f"{Colors.GREEN}✓ tkinter available{Colors.END}")
    except ImportError:
        print(f"{Colors.RED}✗ tkinter NOT available{Colors.END}")
        missing.append("tkinter")
    
    if missing:
        print(f"\n{Colors.YELLOW}Missing packages:{Colors.END}")
        for pkg in missing:
            print(f"  - {pkg}")
        
        if "mysql-connector-python" in missing:
            print(f"\n{Colors.CYAN}Install with:{Colors.END}")
            print(f"  pip install mysql-connector-python")
        
        return False
    
    return True


def check_database():
    """Check if database is set up"""
    print(f"\n{Colors.BLUE}Checking database connection...{Colors.END}\n")
    
    try:
        # Import will now load config from .db_config.json if it exists
        from database import RentalManagementSystem
        system = RentalManagementSystem()
        
        # If connection is established, test it
        if not system.db.connection:
            print(f"{Colors.RED}✗ Cannot connect to MySQL{Colors.END}")
            print(f"{Colors.RED}  Database connection failed - check your MySQL credentials{Colors.END}")
            print(f"{Colors.YELLOW}Please run setup first: python setup_database.py{Colors.END}\n")
            return False
        
        # Test database
        try:
            landlords = system.get_all_landlords()
            print(f"{Colors.GREEN}✓ Database connected and verified{Colors.END}")
            print(f"{Colors.GREEN}✓ Found {len(landlords)} landlords in database{Colors.END}\n")
        except Exception as e:
            print(f"{Colors.RED}✗ Could not query database: {e}{Colors.END}")
            print(f"{Colors.YELLOW}Database may not be set up properly{Colors.END}")
            print(f"{Colors.YELLOW}Please run: python setup_database.py{Colors.END}\n")
            return False
        finally:
            system.db.disconnect()
        
        return True
    except ImportError as e:
        print(f"{Colors.RED}✗ Cannot import database module: {e}{Colors.END}")
        print(f"{Colors.YELLOW}Please run: python setup_database.py{Colors.END}\n")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ Database error: {e}{Colors.END}")
        print(f"{Colors.YELLOW}Please run: python setup_database.py{Colors.END}\n")
        return False


def launch_gui():
    """Launch the GUI application"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}Launching Rental Management System...{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    try:
        from gui import RentalManagementGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = RentalManagementGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"{Colors.RED}✗ Error launching GUI: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main launcher"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}RENTAL MANAGEMENT SYSTEM - LAUNCHER{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    # Check dependencies
    if not check_dependencies():
        print(f"\n{Colors.RED}Please install missing packages and try again{Colors.END}\n")
        sys.exit(1)
    
    # Check database
    if not check_database():
        print(f"\n{Colors.RED}Database not set up. Running setup...{Colors.END}")
        print(f"{Colors.YELLOW}Execute this first: python setup_database.py{Colors.END}\n")
        sys.exit(1)
    
    # Launch GUI
    launch_gui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Application closed by user{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
