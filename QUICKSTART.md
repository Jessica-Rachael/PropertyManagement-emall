# RENTAL MANAGEMENT SYSTEM QUICK START

## ⚡ 5-Minute Setup

### Step 1: Install Python Package (1 minute)
```bash
pip install mysql-connector-python
```

### Step 2: Database Setup (3 minutes)

**Open MySQL Command Line or MySQL Workbench and run:**

```bash
# Create tables and schema
mysql -u root -p < rental_system\database\schema.sql

# Add sample data
mysql -u root -p rental_management_system < rental_system\database\sample_data.sql

# Add views, triggers, procedures
mysql -u root -p rental_management_system < rental_system\database\views_triggers_sprocs.sql
```

**Or in MySQL Workbench:**
- File → Open SQL Script → schema.sql → Execute
- File → Open SQL Script → sample_data.sql → Execute
- File → Open SQL Script → views_triggers_sprocs.sql → Execute

### Step 3: Run Application (1 minute)

```bash
python rental_system\src\gui.py
```

## ✅ What You Should See

1. **GUI Window Opens** - "Rental Management System"
2. **Sidebar Loads** - Categories: Landlords, Properties, Rentals, Transactions
3. **Dashboard Appears** - Shows stats (5 Landlords, 5 Tenants, 5 Buildings, 9 Rooms)

## 🎯 Try These Features First

### 1. View Sample Data
- Click "View Landlords" → See 5 landlords
- Click "View Tenants" → See 5 tenants
- Click "View Rooms" → See 9 rooms
- Click "Active Rentals" → See current agreements

### 2. Search Feature
- Click "Search Tenant"
- Type "Arun" or "Neha"
- See filtered results

### 3. Add New Data
- Click "Add Tenant"
- Fill form (e.g., John, Doe, john@email.com, 9999999999, ID123)
- Click "Submit"
- Success message!

### 4. Filter Transactions
- Click "Filter Transactions"
- Select "Pending"
- Click "Filter"
- See only pending payments

## 🛠️ Config (Only if MySQL password is set)

Edit `rental_system\src\database.py` line 11:
```python
DB_CONFIG = {
    'password': 'your_mysql_password',  # ← Change here
    ...
}
```

## 📊 Database Files Explained

| File | Purpose |
|------|---------|
| `schema.sql` | Creates 7 tables with relationships |
| `sample_data.sql` | Adds 5+ records per table |
| `views_triggers_sprocs.sql` | Views, Triggers, Procedures |
| `acid_demo.sql` | ACID properties test |

## 🔗 File Structure
```
rental_system/
├── ER_DIAGRAM.txt          ← See entity relationships
├── README.md               ← Full documentation
├── setup.sh                ← Setup guide
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   ├── views_triggers_sprocs.sql
│   └── acid_demo.sql
└── src/
    ├── database.py         ← Backend (DB operations)
    └── gui.py              ← Frontend (Tkinter GUI)
```

## ❌ Troubleshooting

**"Connection refused"**
- Start MySQL: `net start MySQL80` (Windows)
- Or use MySQL UI to start

**"Unknown database"**
- Run `schema.sql` first
- Check database name: `rental_management_system`

**"GUI won't start"**
- Check Python 3.8+: `python --version`
- Verify mysql-connector installed: `pip list | grep mysql`

**"Foreign Key error"**
- Run `sample_data.sql` before `views_triggers_sprocs.sql`
- Ensure schema executed successfully

## 📖 Key Renamed Terms

- Owner → **Landlord**
- Customer → **Tenant**  
- Property → **Building**
- Unit → **Room**
- Lease → **Rental Agreement**
- Payment → **Transaction**

## 🎓 ACID Demo (Advanced)

```bash
mysql -u root -p rental_management_system < rental_system\database\acid_demo.sql
```

Tests atomicity, consistency, isolation, durability

## 💡 Pro Tips

1. **Add landlord first** → Then buildings → Then rooms
2. **Add tenant first** → Then create rental agreement
3. **Check Active Rentals** → Best overview of current business
4. **Search is powerful** → Find tenants by name or email
5. **Filter transactions** → See Paid vs Pending payments

---

**Ready? Run: `python rental_system\src\gui.py`** 🚀
