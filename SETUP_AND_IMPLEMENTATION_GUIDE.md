# 🚀 SETUP & IMPLEMENTATION GUIDE
## Complete Step-by-Step Instructions for Building the Analytics System

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [File-by-File Implementation](#file-by-file-implementation)
5. [Testing Guide](#testing-guide)
6. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Software Requirements
- **Windows 10/11** (or macOS/Linux with minor path adjustments)
- **Python 3.10+** (Miniconda or Anaconda recommended)
- **MySQL 8.0+** (with MySQL Workbench)
- **VS Code** (or any text editor)
- **Web Browser** (Chrome, Firefox, Edge)

### Knowledge Requirements
- Basic Python programming
- HTML/CSS/JavaScript basics
- SQL basics (CREATE, INSERT, SELECT)
- Flask framework familiarity (helpful but not required)

---

## 2. Environment Setup

### Step 2.1: Install Python (Miniconda)

1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html
2. Run installer, select "Add to PATH"
3. Open Command Prompt or PowerShell
4. Verify installation:
   ```bash
   python --version
   # Should show: Python 3.10.x or higher
   ```

### Step 2.2: Create Project Environment

```bash
# Create conda environment
conda create -n analytics_env python=3.10 -y

# Activate environment
conda activate analytics_env

# Verify activation (prompt should show (analytics_env))
```

### Step 2.3: Install MySQL

1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Select "Custom" installation
3. Install:
   - MySQL Server 8.0
   - MySQL Workbench 8.0
4. During setup:
   - Set root password: `Santosh@2005` (or note your own password)
   - Configure as development machine
   - Start MySQL Server

### Step 2.4: Verify MySQL

1. Open MySQL Workbench
2. Create connection:
   - Name: `Local Dev`
   - Host: `localhost`
   - Port: `3306`
   - Username: `root`
   - Password: `Santosh@2005`
3. Click "Test Connection" → Should succeed

---

## 3. Database Setup

###Step 3.1: Create Project Folder

```bash
# Create project directory
mkdir "d:\Analytics Project"
cd "d:\Analytics Project"

# Create subfolders
mkdir database
mkdir static\css
mkdir templates
mkdir uploads
```

### Step 3.2: Create Database Schema

**File: `database/schema.sql`**

```sql
-- ==========================================================
-- Marketing ROI & Footfall Analytics System
-- Database Schema
-- ==========================================================

CREATE DATABASE IF NOT EXISTS analytics_project;
USE analytics_project;

-- Drop existing tables (for clean creation)
DROP TABLE IF EXISTS stock_entries;
DROP TABLE IF EXISTS monthly_stock_summary;
DROP TABLE IF EXISTS marketing_spend;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- 1. Users table (authentication)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Products master table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL,
    price_per_unit DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Stock movement entries (individual transactions)
CREATE TABLE stock_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_date DATE NOT NULL,
    product_id INT NOT NULL,
    entry_type ENUM('OPENING', 'RECEIVED', 'SOLD') NOT NULL,
    qty DECIMAL(12,2) NOT NULL,
    price_per_unit DECIMAL(12,2) DEFAULT 0,
    total_value DECIMAL(15,2) DEFAULT 0,
    note VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_entry_date (entry_date),
    INDEX idx_product (product_id),
    INDEX idx_type (entry_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Monthly stock summary (historical data)
CREATE TABLE monthly_stock_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month_name VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    product_id INT NOT NULL,
    opening_qty DECIMAL(12,2) DEFAULT 0,
    opening_value DECIMAL(15,2) DEFAULT 0,
    received_qty DECIMAL(12,2) DEFAULT 0,
    received_value DECIMAL(15,2) DEFAULT 0,
    sold_qty DECIMAL(12,2) DEFAULT 0,
    sold_value DECIMAL(15,2) DEFAULT 0,
    closing_qty DECIMAL(12,2) DEFAULT 0,
    closing_value DECIMAL(15,2) DEFAULT 0,
    remarks VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_monthly (month_name, year, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Marketing spend data (daily)
CREATE TABLE marketing_spend (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spend_date DATE NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_type VARCHAR(20) NOT NULL,
    digital_spend DECIMAL(12,2) DEFAULT 0,
    print_spend DECIMAL(12,2) DEFAULT 0,
    outdoor_spend DECIMAL(12,2) DEFAULT 0,
    total_spend DECIMAL(12,2) DEFAULT 0,
    customer_walk_ins INT DEFAULT 0,
    sales_amount DECIMAL(15,2) DEFAULT 0,
    INDEX idx_spend_date (spend_date),
    INDEX idx_month (month_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Verify tables created
SHOW TABLES;
SELECT 'Database analytics_project created successfully!' AS status;
```

### Step 3.3: Execute Schema

1. Open MySQL Workbench
2. Connect to `Local Dev` connection
3. Open schema.sql file (File → Open SQL Script)
4. Click ⚡ Execute button
5. Verify output: Should see "Database analytics_project created successfully!"
6. Verify tables: In left sidebar, expand "analytics_project" → "Tables" → Should see 5 tables

---

## 4. File-by-File Implementation

### Step 4.1: Configuration File

**File: `config.py`**

```python
"""
Database configuration for MySQL connection
"""

class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    
    # MySQL Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Santosh@2005'  # Change if you used different password
    MYSQL_DATABASE = 'analytics_project'
    MYSQL_PORT = 3306
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf', 'docx'}
```

**Save as:** `d:\Analytics Project\config.py`

### Step 4.2: Dependencies File

**File: `requirements.txt`**

```txt
Flask==3.0.0
mysql-connector-python==8.2.0
Werkzeug==3.0.1
pandas==2.1.4
numpy==1.26.2
openpyxl==3.1.2
PyPDF2==3.0.1
python-docx==1.1.0
scikit-learn==1.3.2
```

**Save as:** `d:\Analytics Project\requirements.txt`

**Install dependencies:**
```bash
cd "d:\Analytics Project"
pip install -r requirements.txt
```

**Wait for installation** (2-3 minutes). Verify:
```bash
pip list | findstr Flask
# Should show: Flask 3.0.0
```

### Step 4.3: Data Import Script

**File: `import_data.py`**

```python
"""
Import CSV data into the MySQL database.
Run this AFTER creating the database via schema.sql.
Usage:  python import_data.py
"""

import csv
import os
import calendar
from datetime import datetime, date
import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config

MONTH_MAP = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}


def get_connection():
    """Get MySQL database connection."""
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )


def safe_float(val):
    """Safely convert value to float."""
    try:
        return float(val.strip()) if val and val.strip() else 0
    except (ValueError, AttributeError):
        return 0


def safe_int(val):
    """Safely convert value to integer."""
    try:
        return int(float(val.strip())) if val and val.strip() else 0
    except (ValueError, AttributeError):
        return 0


def create_admin_user(cursor):
    """Create default admin user."""
    password_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
        ('admin', password_hash)
    )
    print("[OK] Admin user created  (username: admin  |  password: admin123)")


def import_products(cursor, stock_file):
    """Extract unique products from stock CSV and insert into products table."""
    products = {}
    with open(stock_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = row.get('Item', '').strip()
            unit = row.get('Unit', '').strip().lower()
            if item and unit and item not in products:
                products[item] = unit

    for name, unit in products.items():
        cursor.execute(
            "INSERT IGNORE INTO products (name, unit) VALUES (%s, %s)",
            (name, unit)
        )

    cursor.execute("SELECT id, name FROM products")
    product_map = {row[1]: row[0] for row in cursor.fetchall()}
    print(f"[OK] {len(product_map)} products imported: {', '.join(product_map.keys())}")
    return product_map


def import_monthly_stock(cursor, stock_file, product_map):
    """Import monthly stock summary from CSV."""
    count = 0
    with open(stock_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = row.get('Month', '').strip()
            item = row.get('Item', '').strip()
            if not month or not item or item not in product_map:
                continue

            product_id = product_map[item]
            cursor.execute("""
                INSERT INTO monthly_stock_summary
                (month_name, year, product_id, opening_qty, opening_value,
                 received_qty, received_value, sold_qty, sold_value,
                 closing_qty, closing_value, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    opening_qty   = VALUES(opening_qty),
                    opening_value = VALUES(opening_value),
                    received_qty  = VALUES(received_qty),
                    received_value= VALUES(received_value),
                    sold_qty      = VALUES(sold_qty),
                    sold_value    = VALUES(sold_value),
                    closing_qty   = VALUES(closing_qty),
                    closing_value = VALUES(closing_value),
                    remarks       = VALUES(remarks)
            """, (
                month, 2025, product_id,
                safe_float(row.get('Opening_Qty')),
                safe_float(row.get('Opening_Value')),
                safe_float(row.get('Received_Qty')),
                safe_float(row.get('Received_Value')),
                safe_float(row.get('Sold_Qty')),
                safe_float(row.get('Sold_Value')),
                safe_float(row.get('Closing_Qty')),
                safe_float(row.get('Closing_Value')),
                row.get('Remarks', '').strip()
            ))
            count += 1
    print(f"[OK] Imported {count} monthly stock summary rows")


def import_stock_entries(cursor, stock_file, product_map):
    """Create individual stock entries from monthly data."""
    count = 0
    with open(stock_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = row.get('Month', '').strip()
            item = row.get('Item', '').strip()
            if not month or not item or item not in product_map:
                continue

            product_id = product_map[item]
            month_num = MONTH_MAP.get(month, 1)
            
            opening_qty = safe_float(row.get('Opening_Qty'))
            opening_val = safe_float(row.get('Opening_Value'))
            received_qty = safe_float(row.get('Received_Qty'))
            received_val = safe_float(row.get('Received_Value'))
            sold_qty = safe_float(row.get('Sold_Qty'))
            sold_val = safe_float(row.get('Sold_Value'))

            # Create opening entry (1st of month)
            if opening_qty > 0:
                entry_date = date(2025, month_num, 1)
                price = opening_val / opening_qty if opening_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'OPENING', %s, %s, %s, %s)
                """, (entry_date, product_id, opening_qty, price, opening_val, f'{month} opening'))
                count += 1

            # Create received entry (15th of month)
            if received_qty > 0:
                entry_date = date(2025, month_num, 15)
                price = received_val / received_qty if received_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'RECEIVED', %s, %s, %s, %s)
                """, (entry_date, product_id, received_qty, price, received_val, f'{month} received'))
                count += 1

            # Create sold entry (last day of month)
            if sold_qty > 0:
                last_day = calendar.monthrange(2025, month_num)[1]
                entry_date = date(2025, month_num, last_day)
                price = sold_val / sold_qty if sold_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'SOLD', %s, %s, %s, %s)
                """, (entry_date, product_id, sold_qty, price, sold_val, f'{month} sales'))
                count += 1

    print(f"[OK] Imported {count} stock entries")


def import_marketing_spend(cursor, marketing_file):
    """Import marketing spend data from CSV."""
    count = 0
    with open(marketing_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('Date', '').strip()
            if not date_str:
                continue

            try:
                spend_date = datetime.strptime(date_str, '%d-%m-%Y').date()
            except ValueError:
                continue

            cursor.execute("""
                INSERT INTO marketing_spend
                (spend_date, month_name, day_type, digital_spend, print_spend,
                 outdoor_spend, total_spend, customer_walk_ins, sales_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                spend_date,
                row.get('Month', '').strip(),
                row.get('Day_Type', 'Weekday').strip(),
                safe_float(row.get('Digital_Spend')),
                safe_float(row.get('Print_Spend')),
                safe_float(row.get('Outdoor_Spend')),
                safe_float(row.get('Total_Spend')),
                safe_int(row.get('Customer_Walk_Ins')),
                safe_float(row.get('Sales_Amount'))
            ))
            count += 1
    print(f"[OK] Imported {count} marketing spend rows")


if __name__ == '__main__':
    STOCK_FILE = 'dataset_stock_and_sales_2025.csv'
    MARKETING_FILE = 'month_wise_spend_data.csv'

    # Verify CSV files exist
    if not os.path.exists(STOCK_FILE):
        print(f"ERROR: {STOCK_FILE} not found!")
        print("Please ensure the CSV file is in the project root directory.")
        exit(1)
    if not os.path.exists(MARKETING_FILE):
        print(f"ERROR: {MARKETING_FILE} not found!")
        print("Please ensure the CSV file is in the project root directory.")
        exit(1)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("\n=== Starting data import ===\n")
        
        create_admin_user(cursor)
        product_map = import_products(cursor, STOCK_FILE)
        import_monthly_stock(cursor, STOCK_FILE, product_map)
        import_stock_entries(cursor, STOCK_FILE, product_map)
        import_marketing_spend(cursor, MARKETING_FILE)

        conn.commit()
        print("\n✅ Data import completed successfully!")
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during import: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
```

**Save as:** `d:\Analytics Project\import_data.py`

### Step 4.4: Prepare Sample CSV Files

You need two CSV files in the project root:

1. **dataset_stock_and_sales_2025.csv** - Contains columns:
   - Month, Item, Unit, Opening_Qty, Opening_Value, Received_Qty, Received_Value, Sold_Qty, Sold_Value, Closing_Qty, Closing_Value, Remarks

2. **month_wise_spend_data.csv** - Contains columns:
   - Date, Month, Day_Type, Digital_Spend, Print_Spend, Outdoor_Spend, Total_Spend, Customer_Walk_Ins, Sales_Amount

**Place both files in:** `d:\Analytics Project\`

### Step 4.5: Run Data Import

```bash
cd "d:\Analytics Project"
python import_data.py
```

**Expected Output:**
```
=== Starting data import ===

[OK] Admin user created  (username: admin  |  password: admin123)
[OK] 6 products imported: Glass, Plywood, Hardwares, Beeding, Laminates, Doors
[OK] Imported 90 monthly stock summary rows
[OK] Imported 180 stock entries
[OK] Imported 90 marketing spend rows

✅ Data import completed successfully!

You can now login with:
  Username: admin
  Password: admin123
```

### Step 4.6: Verify Data in MySQL

```sql
-- In MySQL Workbench
USE analytics_project;

SELECT COUNT(*) FROM products;        -- Should be 6
SELECT COUNT(*) FROM users;           -- Should be 1
SELECT COUNT(*) FROM monthly_stock_summary;  -- Should be ~90
SELECT COUNT(*) FROM stock_entries;   -- Should be ~180
SELECT COUNT(*) FROM marketing_spend; -- Should be ~90

-- View sample data
SELECT * FROM products LIMIT 5;
SELECT * FROM users;
```

---

## 5. Flask Application & Templates

Due to length constraints, the complete Flask app.py code (~1100 lines) is provided in the **COMPLETE_PROJECT_DOCUMENTATION.md** file.

### Key Files to Create:

1. **app.py** (~1100 lines) - Main Flask application
2. **templates/base.html** - Base template with CDN links
3. **templates/login.html** - Login page
4. **templates/admin.html** (~320 lines) - Dashboard
5. **templates/stock_log.html** (~260 lines) - Stock movement log
6. **templates/monthly_history.html** (~450 lines) - Charts page
7. **templates/upload.html** (~130 lines) - File upload
8. **templates/predictions.html** (~240 lines) - ML predictions
9. **static/css/style.css** (~500 lines) - Custom CSS

**Refer to COMPLETE_PROJECT_DOCUMENTATION.md for full code of each file.**

---

## 6. Testing Guide

### Step 6.1: Start Flask Server

```bash
cd "d:\Analytics Project"
conda activate analytics_env
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
   Press CTRL+C to quit
```

### Step 6.2: Test Login

1. Open browser: http://localhost:5000
2. Should redirect to http://localhost:5000/login
3. Enter credentials:
   - Username: **admin**
   - Password: **admin123**
4. Click "Sign In"
5. Should redirect to dashboard

### Step 6.3: Test Dashboard

- [ ] See "Welcome, admin!" header
- [ ] Stock overview table shows 6 products
- [ ] Product list on right shows all products
- [ ] Add new product form present
- [ ] 3 action buttons visible (Stock Log, Upload Data, Predictions)

### Step 6.4: Test Stock Log

1. Click "Stock Log" button
2. Should show stock movements table
3. Test filters:
   - Select specific product → table updates
   - Select specific month → table updates
   - Click "Reset Filters" → all data shown
4. Test bulk delete:
   - Check "Select All" → all rows selected
   - Click "Delete Selected" → confirmation dialogs
   - Cancel confirmation

### Step 6.5: Test Monthly History

1. Click "Monthly History" from navbar
2. Select a month from dropdown
3. Click "View"
4. Should see 5 charts:
   - Sales Bar Chart (horizontal bars)
   - Sold Quantity Doughnut (pie chart)
   - Stock Flow Grouped Bar (4 colors)
   - Marketing Channel Pie (3 slices)
   - Month-on-Month Trend Line
5. Verify all charts have data labels
6. Check Key Insights panel

### Step 6.6: Test File Upload

1. Click "Upload Data"
2. Stock Data form:
   - Select dataset_stock_and_sales_2025.csv
   - Enter year: 2025
   - Click "Upload"
   - Should show success message
3. Test with Excel (.xlsx) file if available

### Step 6.7: Test Predictions

1. Click "Predictions"
2. Should see current month and next month banners
3. Enter budget:
   - Digital: 5000
   - Print: 3000
   - Outdoor: 2000
4. Click "Predict Sales"
5. Should see:
   - 4 stat cards (Budget, Sales, Walk-Ins, ROI)
   - Budget allocation pie chart
   - Predicted vs Historical bar chart
   - Stock recommendations table
   - Smart recommendations

### Step 6.8: Test Database Cleanup

1. Go to Dashboard → Tab 2 (Stock Log & Entries)
2. Scroll to bottom → Danger Zone
3. Click "Delete All Database Data"
4. Complete 3-step confirmation
5. Database cleared
6. Restore: `python import_data.py`

---

## 7. Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip uninstall mysql-connector
pip install mysql-connector-python==8.2.0
```

### Issue: "Access denied for user 'root'@'localhost'"
**Solution:** Update `config.py` with correct MySQL password

### Issue: Flask app not starting
**Solution:**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F
```

### Issue: Charts not showing data labels
**Solution:** Verify Chart.js DataLabels plugin loaded AFTER Chart.js in base.html

### Issue: Import data script fails
**Solution:**
- Verify CSV files in project root
- Check CSV column names match exactly (case-sensitive)
- Ensure MySQL server running

---

## 8. Next Steps

After successful setup:

1. **Customize:** Modify gradients, colors in style.css
2. **Add Features:** Implement user roles, export reports to PDF
3. **Deploy:** Use Gunicorn + Nginx for production
4. **Backup:** Regular MySQL backups (mysqldump)
5. **Monitor:** Add logging with Flask logging module

---

## 📝 Summary Checklist

- [ ] Python 3.10+ installed
- [ ] MySQL 8.0+ installed and running
- [ ] Project folder created: `d:\Analytics Project\`
- [ ] Database schema executed (5 tables created)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] CSV files placed in project root
- [ ] Data import successful (`python import_data.py`)
- [ ] Flask app runs without errors (`python app.py`)
- [ ] Login works (admin/admin123)
- [ ] Dashboard shows data
- [ ] Charts render with data labels
- [ ] File upload works
- [ ] Predictions generate forecasts
- [ ] Database cleanup and restore tested

**If all checkboxes checked: ✅ Project setup complete!**

---

## 📞 Support

If you encounter issues:

1. Check **TROUBLESHOOTING.md** (if created)
2. Review **DATABASE_CLEANUP_GUIDE.md** for data restoration
3. Read **MASTER_AI_PROMPT.md** for feature specifications
4. Verify Python packages: `pip list`
5. Check MySQL status: Open MySQL Workbench → Test Connection

**Good luck building your Analytics System! 🚀**
