"""
===============================================================================
RENTAL MANAGEMENT SYSTEM - TKINTER GUI APPLICATION
===============================================================================
Improved desktop application with sidebar navigation and modern design
Built using tkinter with proper layouts and user experience
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import RentalManagementSystem

# Color Scheme
COLORS = {
    'primary': '#2c3e50',      # Dark blue-gray
    'sidebar': '#34495e',      # Darker blue-gray
    'accent': '#3498db',       # Bright blue
    'accent_light': '#5dade2', # Light blue
    'success': '#27ae60',       # Green
    'danger': '#e74c3c',        # Red
    'warning': '#f39c12',       # Orange
    'bg_light': '#ecf0f1',      # Light gray
    'text': '#2c3e50',          # Dark text
    'text_light': '#ffffff',    # White text
}


class RentalManagementGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Rental Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['primary'])
        
        # Initialize database
        self.system = RentalManagementSystem()
        
        # Current screen reference
        self.current_frame = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI layout"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar()
        
        # Content area
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show home screen initially
        self.show_home()
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = tk.Frame(self.root, bg=COLORS['sidebar'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        sidebar.pack_propagate(False)
        
        # Header
        header = tk.Frame(sidebar, bg=COLORS['accent'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏢 Rental System", font=("Arial", 16, "bold"),
                        bg=COLORS['accent'], fg=COLORS['text_light'])
        title.pack(pady=15)
        
        subtitle = tk.Label(header, text="Management Platform", font=("Arial", 9),
                           bg=COLORS['accent'], fg=COLORS['text_light'])
        subtitle.pack()
        
        # Separator
        sep1 = tk.Frame(sidebar, bg=COLORS['accent'], height=2)
        sep1.pack(fill=tk.X)
        
        # Navigation sections
        sections = [
            ("LANDLORDS & TENANTS", [
                ("Add Landlord", self.show_add_landlord),
                ("View Landlords", self.show_view_landlords),
                ("Add Tenant", self.show_add_tenant),
                ("View Tenants", self.show_view_tenants),
                ("Search Tenant", self.show_search_tenant),
            ]),
            ("PROPERTIES & ROOMS", [
                ("Add Building", self.show_add_building),
                ("View Buildings", self.show_view_buildings),
                ("Add Room", self.show_add_room),
                ("View Rooms", self.show_view_rooms),
            ]),
            ("RENTALS", [
                ("Create Agreement", self.show_create_agreement),
                ("View Agreements", self.show_view_agreements),
                ("Active Rentals", self.show_active_rentals),
            ]),
            ("TRANSACTIONS", [
                ("Record Payment", self.show_record_transaction),
                ("View Transactions", self.show_view_transactions),
                ("Filter by Status", self.show_filter_transactions),
            ]),
        ]
        
        for section_title, options in sections:
            # Section header
            sec_frame = tk.Frame(sidebar, bg=COLORS['sidebar'])
            sec_frame.pack(fill=tk.X, padx=10, pady=10)
            
            sec_label = tk.Label(sec_frame, text=section_title, font=("Arial", 9, "bold"),
                               bg=COLORS['sidebar'], fg=COLORS['accent'])
            sec_label.pack(anchor=tk.W)
            
            # Options
            for option_text, callback in options:
                btn = tk.Button(sec_frame, text=option_text, command=callback,
                              bg=COLORS['sidebar'], fg=COLORS['text_light'],
                              font=("Arial", 9), relief=tk.FLAT,
                              padx=10, pady=8, anchor=tk.W)
                btn.pack(fill=tk.X, pady=3)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS['accent']))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS['sidebar']))
        
        # Separator
        sep2 = tk.Frame(sidebar, bg=COLORS['accent'], height=2)
        sep2.pack(fill=tk.X, pady=10)
        
        # Footer buttons
        footer_frame = tk.Frame(sidebar, bg=COLORS['sidebar'])
        footer_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        
        home_btn = tk.Button(footer_frame, text="🏠 HOME", command=self.show_home,
                           bg=COLORS['accent'], fg=COLORS['text_light'],
                           font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
        home_btn.pack(fill=tk.X, pady=5)
        
        exit_btn = tk.Button(footer_frame, text="❌ EXIT", command=self.root.quit,
                           bg=COLORS['danger'], fg=COLORS['text_light'],
                           font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
        exit_btn.pack(fill=tk.X)
    
    def clear_content(self):
        """Clear content frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def create_header(self, title: str):
        """Create page header"""
        self.clear_content()
        
        self.current_frame = tk.Frame(self.content_frame, bg=COLORS['bg_light'])
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        header = tk.Frame(self.current_frame, bg=COLORS['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=title, font=("Arial", 20, "bold"),
                              bg=COLORS['primary'], fg=COLORS['text_light'])
        title_label.pack(pady=12)
        
        return self.current_frame
    
    # ========================================================================
    # HOME SCREEN
    # ========================================================================
    
    def show_home(self):
        """Show home screen"""
        frame = self.create_header("Welcome to Rental Management System")
        
        content = tk.Frame(frame, bg=COLORS['bg_light'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        welcome_text = tk.Label(content, text="Hello! Welcome to Your Rental Management Platform",
                               font=("Arial", 24, "bold"), fg=COLORS['primary'],
                               bg=COLORS['bg_light'])
        welcome_text.pack(pady=20)
        
        desc = tk.Label(content, text="Manage landlords, tenants, buildings, rooms, and rental agreements efficiently",
                       font=("Arial", 12), fg=COLORS['text'], bg=COLORS['bg_light'])
        desc.pack(pady=10)
        
        # Quick stats
        stats_frame = tk.Frame(content, bg=COLORS['bg_light'])
        stats_frame.pack(pady=30)
        
        landlords = len(self.system.get_all_landlords())
        tenants = len(self.system.get_all_tenants())
        buildings = len(self.system.get_all_buildings())
        rooms = len(self.system.get_all_rooms())
        
        stats = [
            ("Landlords", landlords),
            ("Tenants", tenants),
            ("Buildings", buildings),
            ("Rooms", rooms),
        ]
        
        for stat_name, stat_value in stats:
            stat_box = tk.Frame(stats_frame, bg=COLORS['accent'], relief=tk.RAISED, bd=2)
            stat_box.grid(row=0, column=stats.index((stat_name, stat_value)), padx=10, pady=10)
            
            stat_frame_inner = tk.Frame(stat_box, bg=COLORS['accent'])
            stat_frame_inner.pack(padx=20, pady=15)
            
            value_label = tk.Label(stat_frame_inner, text=str(stat_value), 
                                  font=("Arial", 28, "bold"), fg=COLORS['text_light'],
                                  bg=COLORS['accent'])
            value_label.pack()
            
            name_label = tk.Label(stat_frame_inner, text=stat_name, 
                                 font=("Arial", 10), fg=COLORS['text_light'],
                                 bg=COLORS['accent'])
            name_label.pack()
    
    # ========================================================================
    # LANDLORD OPERATIONS
    # ========================================================================
    
    def show_add_landlord(self):
        """Add landlord form"""
        frame = self.create_header("Add New Landlord")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Address:", "address"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        def submit():
            data = {k: v.get() for k, v in entries.items()}
            if all(data.values()):
                if self.system.add_landlord(**data):
                    messagebox.showinfo("Success", "Landlord added successfully!")
                    self.show_view_landlords()
                else:
                    messagebox.showerror("Error", "Failed to add landlord")
            else:
                messagebox.showwarning("Warning", "Please fill all fields")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(btn_frame, text="⟳ Clear", command=lambda: [e.delete(0, tk.END) for e in entries.values()],
                            bg=COLORS['warning'], fg=COLORS['text_light'],
                            font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_landlords(self):
        """View all landlords"""
        frame = self.create_header("View All Landlords")
        
        # Create treeview
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "First Name", "Last Name", "Email", "Phone", "Address")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=150, anchor=tk.W)
            tree.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data
        landlords = self.system.get_all_landlords()
        for landlord in landlords:
            values = (landlord['landlord_id'], landlord['first_name'], landlord['last_name'],
                     landlord['email'], landlord['phone'], landlord['address'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Landlords: {len(landlords)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    # ========================================================================
    # TENANT OPERATIONS
    # ========================================================================
    
    def show_add_tenant(self):
        """Add tenant form"""
        frame = self.create_header("Add New Tenant")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("ID Proof:", "id_proof"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        def submit():
            data = {k: v.get() for k, v in entries.items()}
            if all(data.values()):
                if self.system.add_tenant(**data):
                    messagebox.showinfo("Success", "Tenant added successfully!")
                    for entry in entries.values():
                        entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Failed to add tenant (Email or ID might be duplicate)")
            else:
                messagebox.showwarning("Warning", "Please fill all fields")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(btn_frame, text="⟳ Clear", command=lambda: [e.delete(0, tk.END) for e in entries.values()],
                            bg=COLORS['warning'], fg=COLORS['text_light'],
                            font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_tenants(self):
        """View all tenants"""
        frame = self.create_header("View All Tenants")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "First Name", "Last Name", "Email", "Phone", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=150, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tenants = self.system.get_all_tenants()
        for tenant in tenants:
            values = (tenant['tenant_id'], tenant['first_name'], tenant['last_name'],
                     tenant['email'], tenant['phone'], tenant['status'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Tenants: {len(tenants)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    def show_search_tenant(self):
        """Search tenant by name"""
        frame = self.create_header("Search Tenant")
        
        search_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        label = tk.Label(search_frame, text="Enter Name or Email:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        search_entry = tk.Entry(search_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
        search_entry.pack(fill=tk.X, pady=5)
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "First Name", "Last Name", "Email", "Phone", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=15, show='tree headings')
        
        for col in columns:
            tree.column(col, width=150, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def search():
            search_term = search_entry.get()
            if search_term:
                tenants = self.system.search_tenant_by_name(search_term)
                tree.delete(*tree.get_children())
                for tenant in tenants:
                    values = (tenant['tenant_id'], tenant['first_name'], tenant['last_name'],
                             tenant['email'], tenant['phone'], tenant['status'])
                    tree.insert("", tk.END, values=values)
            else:
                messagebox.showwarning("Warning", "Please enter a search term")
        
        btn_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=5)
        
        search_btn = tk.Button(btn_frame, text="🔍 Search", command=search,
                             bg=COLORS['accent'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        search_btn.pack()
    
    # ========================================================================
    # BUILDING OPERATIONS
    # ========================================================================
    
    def show_add_building(self):
        """Add building form"""
        frame = self.create_header("Add New Building")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Landlord dropdown
        label = tk.Label(form_frame, text="Select Landlord:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        landlords = self.system.get_all_landlords()
        landlord_options = [f"{l['landlord_id']} - {l['first_name']} {l['last_name']}" for l in landlords]
        
        landlord_var = tk.StringVar()
        landlord_combo = ttk.Combobox(form_frame, textvariable=landlord_var, 
                                     values=landlord_options, state='readonly', width=37)
        landlord_combo.pack(fill=tk.X, pady=5)
        
        fields = [
            ("Building Name:", "building_name"),
            ("Location:", "location"),
            ("Year Built:", "year_built"),
            ("Total Floors:", "total_floors"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        def submit():
            if not landlord_var.get():
                messagebox.showwarning("Warning", "Please select a landlord")
                return
            
            landlord_id = int(landlord_var.get().split(" - ")[0])
            data = {k: v.get() for k, v in entries.items()}
            
            try:
                data['year_built'] = int(data['year_built'])
                data['total_floors'] = int(data['total_floors'])
                
                if self.system.add_building(landlord_id, **data):
                    messagebox.showinfo("Success", "Building added successfully!")
                    self.show_view_buildings()
                else:
                    messagebox.showerror("Error", "Failed to add building")
            except ValueError:
                messagebox.showerror("Error", "Year and floors must be numbers")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_buildings(self):
        """View all buildings"""
        frame = self.create_header("View All Buildings")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Landlord", "Building Name", "Location", "Year", "Floors")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=120, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        buildings = self.system.get_all_buildings()
        for building in buildings:
            values = (building['building_id'], building['landlord_name'], building['building_name'],
                     building['location'], building['year_built'], building['total_floors'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Buildings: {len(buildings)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    # ========================================================================
    # ROOM OPERATIONS
    # ========================================================================
    
    def show_add_room(self):
        """Add room form"""
        frame = self.create_header("Add New Room")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Building dropdown
        label = tk.Label(form_frame, text="Select Building:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        buildings = self.system.get_all_buildings()
        building_options = [f"{b['building_id']} - {b['building_name']}" for b in buildings]
        
        building_var = tk.StringVar()
        building_combo = ttk.Combobox(form_frame, textvariable=building_var,
                                     values=building_options, state='readonly', width=37)
        building_combo.pack(fill=tk.X, pady=5)
        
        fields = [
            ("Room Number:", "room_number"),
            ("Room Type (Studio/1BHK/2BHK/3BHK):", "room_type"),
            ("Area (Sq Ft):", "area_sqft"),
            ("Monthly Rent:", "monthly_rent"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        def submit():
            if not building_var.get():
                messagebox.showwarning("Warning", "Please select a building")
                return
            
            building_id = int(building_var.get().split(" - ")[0])
            data = {k: v.get() for k, v in entries.items()}
            
            try:
                data['area_sqft'] = float(data['area_sqft'])
                data['monthly_rent'] = float(data['monthly_rent'])
                
                if self.system.add_room(building_id, **data):
                    messagebox.showinfo("Success", "Room added successfully!")
                    for entry in entries.values():
                        entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Failed to add room")
            except ValueError:
                messagebox.showerror("Error", "Area and Rent must be numbers")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_rooms(self):
        """View all rooms"""
        frame = self.create_header("View All Rooms")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Building", "Room #", "Type", "Area Sq/Ft", "Rent", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=130, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        rooms = self.system.get_all_rooms()
        for room in rooms:
            values = (room['room_id'], room['building_name'], room['room_number'],
                     room['room_type'], room['area_sqft'], room['monthly_rent'], room['status'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Rooms: {len(rooms)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    # ========================================================================
    # RENTAL AGREEMENT OPERATIONS
    # ========================================================================
    
    def show_create_agreement(self):
        """Create rental agreement form"""
        frame = self.create_header("Create Rental Agreement")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Tenant dropdown
        label = tk.Label(form_frame, text="Select Tenant:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        tenants = self.system.get_active_tenants()
        tenant_options = [f"{t['tenant_id']} - {t['first_name']} {t['last_name']}" for t in tenants]
        
        tenant_var = tk.StringVar()
        tenant_combo = ttk.Combobox(form_frame, textvariable=tenant_var,
                                   values=tenant_options, state='readonly', width=37)
        tenant_combo.pack(fill=tk.X, pady=5)
        
        # Room dropdown
        label = tk.Label(form_frame, text="Select Available Room:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        available_rooms = self.system.get_available_rooms()
        room_options = [f"{r['room_id']} - {r['building_name']} - {r['room_number']}" for r in available_rooms]
        
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(form_frame, textvariable=room_var,
                                 values=room_options, state='readonly', width=37)
        room_combo.pack(fill=tk.X, pady=5)
        
        fields = [
            ("Start Date (YYYY-MM-DD):", "start_date"),
            ("End Date (YYYY-MM-DD):", "end_date"),
            ("Monthly Rent:", "monthly_rent"),
            ("Deposit Amount:", "deposit_amount"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        def submit():
            if not tenant_var.get() or not room_var.get():
                messagebox.showwarning("Warning", "Please select tenant and room")
                return
            
            tenant_id = int(tenant_var.get().split(" - ")[0])
            room_id = int(room_var.get().split(" - ")[0])
            
            try:
                data = {k: v.get() for k, v in entries.items()}
                data['monthly_rent'] = float(data['monthly_rent'])
                data['deposit_amount'] = float(data['deposit_amount'])
                
                if self.system.create_rental_agreement(tenant_id, room_id, **data):
                    messagebox.showinfo("Success", "Rental agreement created successfully!")
                    self.show_view_agreements()
                else:
                    messagebox.showerror("Error", "Failed to create agreement")
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_agreements(self):
        """View all rental agreements"""
        frame = self.create_header("View All Rental Agreements")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Tenant", "Building", "Room", "Rent", "Start", "End", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=110, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        agreements = self.system.get_all_rental_agreements()
        for agreement in agreements:
            values = (agreement['agreement_id'], agreement['tenant_name'],
                     agreement['building_name'], agreement['room_number'],
                     agreement['monthly_rent'], agreement['start_date'],
                     agreement['end_date'], agreement['status'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Agreements: {len(agreements)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    def show_active_rentals(self):
        """Show active rentals view"""
        frame = self.create_header("Active Rentals View")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Tenant", "Building", "Room", "Rent", "Days Remaining", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=120, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        active_rentals = self.system.get_active_rentals_view()
        for rental in active_rentals:
            values = (rental['agreement_id'], rental['tenant_name'],
                     rental['building_name'], rental['room_number'],
                     rental['monthly_rent'], rental['days_remaining'], rental['status'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Active Rentals: {len(active_rentals)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    # ========================================================================
    # TRANSACTION OPERATIONS
    # ========================================================================
    
    def show_record_transaction(self):
        """Record transaction form"""
        frame = self.create_header("Record Payment Transaction")
        
        form_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Agreement dropdown
        label = tk.Label(form_frame, text="Select Rental Agreement:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        agreements = self.system.get_active_rental_agreements()
        agreement_options = [f"{a['agreement_id']} - {a['tenant_name']} - {a['room_number']}" for a in agreements]
        
        agreement_var = tk.StringVar()
        agreement_combo = ttk.Combobox(form_frame, textvariable=agreement_var,
                                      values=agreement_options, state='readonly', width=37)
        agreement_combo.pack(fill=tk.X, pady=5)
        
        fields = [
            ("Transaction Type (Rent/Deposit/Refund):", "transaction_type"),
            ("Amount:", "amount"),
            ("Payment Date (YYYY-MM-DD):", "payment_date"),
            ("Payment Method:", "payment_method"),
        ]
        
        entries = {}
        
        for label_text, key in fields:
            label = tk.Label(form_frame, text=label_text, font=("Arial", 11, "bold"),
                           bg=COLORS['bg_light'], fg=COLORS['text'])
            label.pack(anchor=tk.W, pady=5)
            
            entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
            entry.pack(fill=tk.X, pady=5)
            entries[key] = entry
        
        # Status radio
        label = tk.Label(form_frame, text="Status:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        status_var = tk.StringVar(value="Paid")
        radio_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        radio_frame.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        ttk.Radiobutton(radio_frame, text="Paid", variable=status_var, value="Paid").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(radio_frame, text="Pending", variable=status_var, value="Pending").pack(side=tk.LEFT, padx=10)
        
        # Notes
        label = tk.Label(form_frame, text="Notes (Optional):", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        notes_entry = tk.Entry(form_frame, font=("Arial", 10), width=40, relief=tk.GROOVE, bd=2)
        notes_entry.pack(fill=tk.X, pady=5)
        
        def submit():
            if not agreement_var.get():
                messagebox.showwarning("Warning", "Please select an agreement")
                return
            
            agreement_id = int(agreement_var.get().split(" - ")[0])
            
            try:
                data = {k: v.get() for k, v in entries.items()}
                data['amount'] = float(data['amount'])
                
                if self.system.add_transaction(agreement_id, status=status_var.get(), notes=notes_entry.get(), **data):
                    messagebox.showinfo("Success", "Transaction recorded successfully!")
                    for entry in entries.values():
                        entry.delete(0, tk.END)
                    notes_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Failed to record transaction")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
        
        btn_frame = tk.Frame(form_frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="✓ Submit", command=submit,
                             bg=COLORS['success'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        submit_btn.pack(side=tk.LEFT, padx=5)
    
    def show_view_transactions(self):
        """View all transactions"""
        frame = self.create_header("View All Transactions")
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Tenant", "Room", "Type", "Amount", "Date", "Method", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=110, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        transactions = self.system.get_all_transactions()
        for txn in transactions:
            values = (txn['transaction_id'], txn['tenant_name'], txn['room_number'],
                     txn['transaction_type'], txn['amount'], txn['payment_date'],
                     txn['payment_method'], txn['status'])
            tree.insert("", tk.END, values=values)
        
        info_label = tk.Label(frame, text=f"Total Transactions: {len(transactions)}", 
                             font=("Arial", 10), bg=COLORS['accent'],
                             fg=COLORS['text_light'])
        info_label.pack(fill=tk.X, padx=10, pady=5)
    
    def show_filter_transactions(self):
        """Filter transactions by status"""
        frame = self.create_header("Filter Transactions by Status")
        
        filter_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        filter_frame.pack(fill=tk.X, padx=20, pady=20)
        
        label = tk.Label(filter_frame, text="Select Status:", font=("Arial", 11, "bold"),
                       bg=COLORS['bg_light'], fg=COLORS['text'])
        label.pack(anchor=tk.W, pady=5)
        
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(filter_frame, textvariable=status_var,
                                   values=["Paid", "Pending"], state='readonly', width=20)
        status_combo.pack(fill=tk.X, pady=5)
        
        tree_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Tenant", "Room", "Type", "Amount", "Date", "Method", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='tree headings')
        
        for col in columns:
            tree.column(col, width=110, anchor=tk.W)
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        def filter_data():
            status = status_var.get()
            if not status:
                messagebox.showwarning("Warning", "Please select a status")
                return
            
            transactions = self.system.get_transactions_by_status(status)
            tree.delete(*tree.get_children())
            
            for txn in transactions:
                values = (txn['transaction_id'], txn['tenant_name'], txn['room_number'],
                         txn['transaction_type'], txn['amount'], txn['payment_date'],
                         txn['payment_method'], txn['status'])
                tree.insert("", tk.END, values=values)
        
        btn_frame = tk.Frame(frame, bg=COLORS['bg_light'])
        btn_frame.pack(pady=5)
        
        filter_btn = tk.Button(btn_frame, text="🔍 Filter", command=filter_data,
                             bg=COLORS['accent'], fg=COLORS['text_light'],
                             font=("Arial", 11, "bold"), relief=tk.FLAT, padx=20, pady=10)
        filter_btn.pack()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = RentalManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
