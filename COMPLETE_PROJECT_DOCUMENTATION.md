# 📊 Hardware & Plywood Store - Marketing ROI & Analytics System
## Complete Project Documentation

**Version:** 1.0  
**Date:** March 9, 2026  
**Project Type:** Flask Web Application with MySQL Database  
**Purpose:** Analytics system for hardware store to track inventory, sales, marketing ROI, and predict future sales

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Database Schema](#database-schema)
5. [Backend Code](#backend-code)
6. [Frontend Code](#frontend-code)
7. [CSS Styling](#css-styling)
8. [Data Files](#data-files)
9. [Setup Instructions](#setup-instructions)
10. [Features List](#features-list)
11. [Testing Guide](#testing-guide)

---

## 1. Project Overview

### Business Context
A Hardware & Plywood store needs a system to:
- Track product inventory (Glass, Plywood, Hardwares, Beeding, Laminates, Doors, Cement, Steel Rods, Paints)
- Monitor stock movements (opening, received, sold)
- Analyze marketing spend vs sales correlation
- Predict future sales based on marketing budget
- Generate visual reports with charts

### Key Stakeholders
- **Admin/Owner:** Full access to all features
- **Accountants:** Need financial data and reports
- **Managers:** Monitor stock and sales performance

### Core Functionality
1. **Authentication:** Secure login system
2. **Dashboard:** Product management and overview
3. **Stock Log:** Track all inventory movements
4. **Monthly History:** Visual analytics with 5 chart types
5. **Data Upload:** Import CSV/Excel/PDF/Word files
6. **Predictions:** ML-based sales forecasting
7. **Database Management:** Clear and restore data

---

## 2. Technology Stack

### Backend
- **Python 3.10.19** (Miniconda environment: "forsche")
- **Flask 3.0.0** - Web framework
- **MySQL 8.0** - Database (mysql-connector-python 8.2.0)
- **Werkzeug** - Password hashing and security

### Data Processing
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **openpyxl** - Excel file reading
- **PyPDF2** - PDF parsing
- **python-docx** - Word document parsing

### Machine Learning
- **scikit-learn** - LinearRegression model for predictions

### Frontend
- **Bootstrap 5.3.2** - UI framework
- **Bootstrap Icons 1.11.3** - Icon library
- **Chart.js 4.4.1** - Interactive charts
- **Chart.js DataLabels 2.2.0** - Value labels on charts
- **Google Fonts (Inter)** - Typography

### Database Configuration
- **Host:** localhost
- **User:** root
- **Password:** Santosh@2005
- **Database:** analytics_project
- **Port:** 3306

---

## 3. Project Structure

```
d:\Analytics Project\
│
├── app.py                          # Main Flask application (~1100 lines)
├── config.py                       # Database configuration
├── import_data.py                  # CSV data import script
├── generate_test_data.py           # Test data generator
├── requirements.txt                # Python dependencies
├── DATABASE_CLEANUP_GUIDE.md       # Database restoration guide
├── COMPLETE_PROJECT_DOCUMENTATION.md (this file)
│
├── database/
│   └── schema.sql                  # MySQL database schema
│
├── static/
│   └── css/
│       └── style.css               # Custom CSS (~500 lines)
│
├── templates/
│   ├── base.html                   # Base template with nav
│   ├── login.html                  # Login page
│   ├── admin.html                  # Dashboard (~300 lines)
│   ├── stock_log.html              # Stock movement log
│   ├── monthly_history.html        # Charts & insights (~450 lines)
│   ├── upload.html                 # File upload interface
│   └── predictions.html            # ML predictions (~240 lines)
│
├── test_data/
│   ├── stock_may_2026.csv
│   ├── marketing_may_2026.csv
│   ├── stock_june_2026.xlsx
│   ├── marketing_june_2026.docx
│   └── README.md
│
├── dataset_stock_and_sales_2025.csv    # Original stock data
└── month_wise_spend_data.csv           # Original marketing data
```

---

## 4. Database Schema

### Complete SQL Schema

```sql
-- ==========================================================
-- Marketing ROI & Footfall Analytics System
-- Database Schema — Run this in MySQL Workbench
-- ==========================================================

CREATE DATABASE IF NOT EXISTS analytics_project;
USE analytics_project;

-- Drop tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS stock_entries;
DROP TABLE IF EXISTS monthly_stock_summary;
DROP TABLE IF EXISTS marketing_spend;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- ---------------------------------------------------------
-- 1. Users table (authentication)
-- ---------------------------------------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- 2. Products master table
-- ---------------------------------------------------------
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL,
    price_per_unit DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- 3. Stock movement entries (individual transactions)
-- ---------------------------------------------------------
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

-- ---------------------------------------------------------
-- 4. Monthly stock summary (historical CSV data)
-- ---------------------------------------------------------
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

-- ---------------------------------------------------------
-- 5. Marketing spend data (daily)
-- ---------------------------------------------------------
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

-- Verify all tables created
SHOW TABLES;
SELECT 'Database analytics_project created successfully!' AS status;
```

### Database Relationships

```
users (auth data)
  ↓
products
  ↓
  ├── stock_entries (FK: product_id)
  └── monthly_stock_summary (FK: product_id)

marketing_spend (standalone, analyzed with monthly_stock_summary)
```

---

## 5. Backend Code

### 5.1 config.py

```python
"""
Database configuration for MySQL connection
"""

class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Santosh@2005'
    MYSQL_DATABASE = 'analytics_project'
    MYSQL_PORT = 3306
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
```

### 5.2 app.py (Main Application)

Due to the extensive length (~1100 lines), I'll provide the complete structure with key sections. 

**File: app.py**

```python
"""
Marketing ROI & Footfall Analytics System — Flask Application
"""

import calendar
import os
import io
import re
from datetime import date, datetime
from functools import wraps

import mysql.connector
from mysql.connector import pooling
import json
import numpy as np
import pandas as pd
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from config import Config

# ── App setup ────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

MONTH_ORDER = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


# ── Custom Jinja2 filter for number formatting ───────────────
@app.template_filter('numfmt')
def number_format(value, decimals=0):
    try:
        return '{:,.{d}f}'.format(float(value), d=int(decimals))
    except (ValueError, TypeError):
        return value


# ── Database helpers ─────────────────────────────────────────
db_pool = None


def init_pool():
    global db_pool
    db_pool = pooling.MySQLConnectionPool(
        pool_name="app_pool",
        pool_size=5,
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )


def get_db():
    if db_pool is None:
        init_pool()
    return db_pool.get_connection()


# ── Login required decorator ─────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ══════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════

# ── Home / Index ─────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# ── Login ────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


# ── Logout ───────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# ── Dashboard (Admin Panel) ──────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get all products
        cursor.execute("SELECT * FROM products ORDER BY name")
        products = cursor.fetchall()

        # Get stock overview (latest month closing stock for each product)
        cursor.execute("""
            SELECT p.name, p.unit, m.closing_qty, m.closing_value, m.month_name, m.year
            FROM products p
            LEFT JOIN monthly_stock_summary m ON p.id = m.product_id
            WHERE (m.year, FIELD(m.month_name, 'January','February','March','April','May','June',
                                 'July','August','September','October','November','December'))
            IN (
                SELECT year, FIELD(month_name, 'January','February','March','April','May','June',
                                    'July','August','September','October','November','December')
                FROM monthly_stock_summary
                WHERE product_id = p.id
                ORDER BY year DESC, FIELD(month_name, 'January','February','March','April','May','June',
                                           'July','August','September','October','November','December') DESC
                LIMIT 1
            )
            ORDER BY p.name
        """)
        stock_overview = cursor.fetchall()

        # Get available months
        cursor.execute("""
            SELECT DISTINCT month_name, year
            FROM monthly_stock_summary
            ORDER BY year DESC, FIELD(month_name, 'January','February','March','April','May','June',
                                      'July','August','September','October','November','December') DESC
        """)
        available_months = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template('admin.html',
                           products=products,
                           stock_overview=stock_overview,
                           available_months=available_months)


# ── Add product ──────────────────────────────────────────────
@app.route('/add-product', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name', '').strip()
    unit = request.form.get('unit', '').strip().lower()
    custom_unit = request.form.get('custom_unit', '').strip().lower()
    price_per_unit = request.form.get('price_per_unit', '0')

    # If "New" option selected, use custom unit
    if unit == 'new' and custom_unit:
        unit = custom_unit

    if not name or not unit:
        flash('Product name and unit are required.', 'error')
        return redirect(url_for('dashboard'))

    try:
        price = float(price_per_unit)
    except ValueError:
        price = 0.0

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, unit, price_per_unit) VALUES (%s, %s, %s)",
            (name, unit, price)
        )
        conn.commit()
        flash(f'Product "{name}" added successfully!', 'success')
    except mysql.connector.IntegrityError:
        flash(f'Product "{name}" already exists.', 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('dashboard'))


# ── Delete product ───────────────────────────────────────────
@app.route('/delete-product/<int:pid>', methods=['POST'])
@login_required
def delete_product(pid):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (pid,))
        conn.commit()
        flash('Product deleted.', 'success')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))


# ── Clear ALL Database Data (DANGER) ─────────────────────────
@app.route('/clear-database', methods=['POST'])
@login_required
def clear_database():
    """Clear all data from the database (except users). USE WITH EXTREME CAUTION!"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Delete all data from tables (in reverse order of dependencies)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")  # Temporarily disable FK checks
        cursor.execute("TRUNCATE TABLE stock_entries")
        cursor.execute("TRUNCATE TABLE monthly_stock_summary")
        cursor.execute("TRUNCATE TABLE marketing_spend")
        cursor.execute("TRUNCATE TABLE products")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Re-enable FK checks
        conn.commit()
        flash('✅ Database cleared successfully! All data has been deleted (users preserved).', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'❌ Error clearing database: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))


# ── Stock Movement Log ───────────────────────────────────────
@app.route('/stock-log')
@login_required
def stock_log():
    product_filter = request.args.get('product', 'all')
    month_filter = request.args.get('month', 'all')
    year_filter = request.args.get('year', 'all')

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name FROM products ORDER BY name")
        products = cursor.fetchall()
        
        # Get distinct months and years
        cursor.execute("""
            SELECT DISTINCT 
                DATE_FORMAT(entry_date, '%M') AS month_name,
                MONTH(entry_date) AS month_num,
                YEAR(entry_date) AS year
            FROM stock_entries
            ORDER BY year DESC, month_num DESC
        """)
        date_data = cursor.fetchall()
        months = sorted(set(d['month_name'] for d in date_data), key=lambda x: datetime.strptime(x, '%B').month)
        years = sorted(set(d['year'] for d in date_data), reverse=True)

        # Build query with filters
        query = """
            SELECT se.*, p.name AS product_name, p.unit
            FROM stock_entries se
            JOIN products p ON se.product_id = p.id
            WHERE 1=1
        """
        params = []
        
        if product_filter != 'all' and product_filter.isdigit():
            query += " AND se.product_id = %s"
            params.append(int(product_filter))
            
        if month_filter != 'all':
            query += " AND DATE_FORMAT(se.entry_date, '%M') = %s"
            params.append(month_filter)
            
        if year_filter != 'all':
            query += " AND YEAR(se.entry_date) = %s"
            params.append(int(year_filter))
        
        query += " ORDER BY se.entry_date DESC, se.id DESC"
        
        cursor.execute(query, params)
        entries = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('stock_log.html',
                           entries=entries,
                           products=products,
                           product_filter=product_filter,
                           month_filter=month_filter,
                           year_filter=year_filter,
                           months=months,
                           years=years)


# ── Add stock entry ──────────────────────────────────────────
@app.route('/add-stock-entry', methods=['POST'])
@login_required
def add_stock_entry():
    product_id = request.form.get('product_id', '')
    entry_type = request.form.get('entry_type', '')
    qty = request.form.get('qty', '')
    price_per_unit = request.form.get('price_per_unit', '')
    note = request.form.get('note', '').strip()
    entry_date = request.form.get('entry_date', '')

    # Validate
    if not all([product_id, entry_type, qty, price_per_unit, entry_date]):
        flash('All fields are required.', 'error')
        return redirect(url_for('stock_log'))

    if entry_type not in ('OPENING', 'RECEIVED', 'SOLD'):
        flash('Invalid entry type.', 'error')
        return redirect(url_for('stock_log'))

    try:
        qty_val = float(qty)
        price_val = float(price_per_unit)
        total_value = qty_val * price_val
    except ValueError:
        flash('Invalid quantity or price.', 'error')
        return redirect(url_for('stock_log'))

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO stock_entries 
            (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (entry_date, product_id, entry_type, qty_val, price_val, total_value, note))
        conn.commit()
        flash('Stock entry added successfully!', 'success')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('stock_log'))


# ── Delete entry ─────────────────────────────────────────────
@app.route('/delete-entry/<int:eid>', methods=['POST'])
@login_required
def delete_entry(eid):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stock_entries WHERE id = %s", (eid,))
        conn.commit()
        flash('Entry deleted.', 'success')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('stock_log'))


@app.route('/delete-entries-bulk', methods=['POST'])
@login_required
def delete_entries_bulk():
    """Delete multiple stock entries at once."""
    entry_ids = request.form.getlist('entry_ids[]')
    
    if not entry_ids:
        flash('No entries selected.', 'error')
        return redirect(url_for('stock_log'))
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        placeholders = ','.join(['%s'] * len(entry_ids))
        cursor.execute(f"DELETE FROM stock_entries WHERE id IN ({placeholders})", entry_ids)
        conn.commit()
        flash(f'{len(entry_ids)} entries deleted successfully.', 'success')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('stock_log'))


# ── Monthly History ──────────────────────────────────────────
def _latest_summary_month():
    """Helper to get the most recent month from monthly_stock_summary."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT DISTINCT month_name, year
            FROM monthly_stock_summary
            ORDER BY year DESC, FIELD(month_name, 'January','February','March','April','May','June',
                                      'July','August','September','October','November','December') DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        return (row['month_name'], row['year']) if row else (None, None)
    finally:
        cursor.close()
        conn.close()


@app.route('/monthly-history')
@login_required
def monthly_history():
    selected_month = request.args.get('month')
    selected_year = request.args.get('year', type=int)

    # If not provided, get latest month
    if not selected_month or not selected_year:
        selected_month, selected_year = _latest_summary_month()

    if not selected_month or not selected_year:
        flash('No monthly data available yet.', 'error')
        return render_template('monthly_history.html',
                               products=[],
                               chart_data_json='{}',
                               selected_month=None,
                               selected_year=None,
                               insights=None,
                               all_months_sales=None)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get available months for dropdown
        cursor.execute("""
            SELECT DISTINCT month_name, year
            FROM monthly_stock_summary
            ORDER BY year DESC, FIELD(month_name, 'January','February','March','April','May','June',
                                      'July','August','September','October','November','December') DESC
        """)
        available_months = cursor.fetchall()

        # Get products and monthly data for selected month
        cursor.execute("""
            SELECT p.name, p.unit,
                   m.opening_qty, m.opening_value,
                   m.received_qty, m.received_value,
                   m.sold_qty, m.sold_value,
                   m.closing_qty, m.closing_value, m.remarks
            FROM products p
            LEFT JOIN monthly_stock_summary m ON p.id = m.product_id
                                               AND m.month_name = %s
                                               AND m.year = %s
            ORDER BY p.name
        """, (selected_month, selected_year))
        products = cursor.fetchall()

        # Get marketing spend for selected month
        cursor.execute("""
            SELECT day_type, digital_spend, print_spend, outdoor_spend, total_spend,
                   customer_walk_ins, sales_amount
            FROM marketing_spend
            WHERE month_name = %s
            ORDER BY spend_date
        """, (selected_month,))
        marketing_data = cursor.fetchall()

        # Compute Key Insights
        if products:
            top_product = max(products, key=lambda x: float(x['sold_value'] or 0))
            lowest_product = min(products, key=lambda x: float(x['sold_value'] or 0))
            most_qty_sold = max(products, key=lambda x: float(x['sold_qty'] or 0))
            
            insights = {
                'top_product': {'name': top_product['name'], 'value': float(top_product['sold_value'] or 0)},
                'lowest_product': {'name': lowest_product['name'], 'value': float(lowest_product['sold_value'] or 0)},
                'most_qty_sold': {'name': most_qty_sold['name'], 'qty': float(most_qty_sold['sold_qty'] or 0), 'unit': most_qty_sold['unit']}
            }
        else:
            insights = None

        # Get all months sales for comparison
        cursor.execute("""
            SELECT month_name, SUM(sold_value) as total_sales
            FROM monthly_stock_summary
            WHERE year = %s
            GROUP BY month_name
            ORDER BY FIELD(month_name, 'January','February','March','April','May','June',
                          'July','August','September','October','November','December')
        """, (selected_year,))
        all_months_sales = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    # Marketing aggregates
    if marketing_data:
        total_digital = sum(float(d['digital_spend'] or 0) for d in marketing_data)
        total_print = sum(float(d['print_spend'] or 0) for d in marketing_data)
        total_outdoor = sum(float(d['outdoor_spend'] or 0) for d in marketing_data)
        total_walk_ins = sum(int(d['customer_walk_ins'] or 0) for d in marketing_data)
        total_sales = sum(float(d['sales_amount'] or 0) for d in marketing_data)
    else:
        total_digital = total_print = total_outdoor = total_walk_ins = total_sales = 0

    # Prepare data for Chart.js
    chart_data = {
        'products': [p['name'] for p in products],
        'sold_values': [float(p['sold_value'] or 0) for p in products],
        'sold_qtys': [float(p['sold_qty'] or 0) for p in products],
        'opening_qtys': [float(p['opening_qty'] or 0) for p in products],
        'received_qtys': [float(p['received_qty'] or 0) for p in products],
        'closing_qtys': [float(p['closing_qty'] or 0) for p in products],
        'marketing_channels': ['Digital', 'Print', 'Outdoor'],
        'marketing_spends': [total_digital, total_print, total_outdoor],
        'all_months': [m['month_name'] for m in all_months_sales],
        'all_months_sales': [float(m['total_sales'] or 0) for m in all_months_sales],
    }

    chart_data_json = json.dumps(chart_data)

    return render_template('monthly_history.html',
                           products=products,
                           chart_data_json=chart_data_json,
                           selected_month=selected_month,
                           selected_year=selected_year,
                           available_months=available_months,
                           total_digital=total_digital,
                           total_print=total_print,
                           total_outdoor=total_outdoor,
                           total_walk_ins=total_walk_ins,
                           total_sales=total_sales,
                           insights=insights,
                           all_months_sales=all_months_sales)


# ══════════════════════════════════════════════════════════════
#  FILE UPLOAD & DATA IMPORT
# ══════════════════════════════════════════════════════════════

def _allowed_file(filename):
    """Check if file has allowed extension."""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _parse_file_to_df(filepath):
    """Read uploaded file into a pandas DataFrame."""
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'csv':
        return pd.read_csv(filepath)
    elif ext in ('xlsx', 'xls'):
        return pd.read_excel(filepath, engine='openpyxl')
    elif ext == 'pdf':
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        return _text_to_df(text)
    elif ext == 'docx':
        from docx import Document
        doc = Document(filepath)
        # Try to find a table first
        if doc.tables:
            table = doc.tables[0]
            data = [[c.text.strip() for c in row.cells] for row in table.rows]
            if len(data) > 1:
                return pd.DataFrame(data[1:], columns=data[0])
        # Fallback: parse text
        text = '\n'.join(p.text for p in doc.paragraphs)
        return _text_to_df(text)
    return pd.DataFrame()


def _text_to_df(text):
    """Best-effort: parse tabular text (comma/tab separated) into a DataFrame."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return pd.DataFrame()
    # Detect separator
    sep = ',' if ',' in lines[0] else '\t' if '\t' in lines[0] else ','
    return pd.read_csv(io.StringIO('\n'.join(lines)), sep=sep)


def _safe_float(val):
    try:
        return float(str(val).strip().replace(',', '')) if pd.notna(val) else 0.0
    except (ValueError, TypeError):
        return 0.0


def _safe_int(val):
    try:
        return int(float(str(val).strip().replace(',', ''))) if pd.notna(val) else 0
    except (ValueError, TypeError):
        return 0


def _import_stock_df(df, year, cursor):
    """Import stock DataFrame into monthly_stock_summary + products + stock_entries."""
    # Normalise column names
    col_map = {}
    for c in df.columns:
        cl = c.strip().lower().replace(' ', '_')
        if 'month' in cl:
            col_map[c] = 'Month'
        elif 'item' in cl or 'product' in cl:
            col_map[c] = 'Item'
        elif 'unit' in cl:
            col_map[c] = 'Unit'
        elif 'opening' in cl and 'qty' in cl:
            col_map[c] = 'Opening_Qty'
        elif 'opening' in cl and 'val' in cl:
            col_map[c] = 'Opening_Value'
        elif 'received' in cl and 'qty' in cl:
            col_map[c] = 'Received_Qty'
        elif 'received' in cl and 'val' in cl:
            col_map[c] = 'Received_Value'
        elif 'sold' in cl and 'qty' in cl:
            col_map[c] = 'Sold_Qty'
        elif 'sold' in cl and 'val' in cl:
            col_map[c] = 'Sold_Value'
        elif 'closing' in cl and 'qty' in cl:
            col_map[c] = 'Closing_Qty'
        elif 'closing' in cl and 'val' in cl:
            col_map[c] = 'Closing_Value'
        elif 'remark' in cl:
            col_map[c] = 'Remarks'
    df = df.rename(columns=col_map)

    required = ['Month', 'Item']
    if not all(c in df.columns for c in required):
        return 0, 'Missing required columns: Month, Item'

    count = 0
    for _, row in df.iterrows():
        month = str(row.get('Month', '')).strip()
        item = str(row.get('Item', '')).strip()
        unit = str(row.get('Unit', 'nos')).strip().lower()
        if not month or not item:
            continue

        # Ensure product exists
        cursor.execute("INSERT IGNORE INTO products (name, unit) VALUES (%s, %s)", (item, unit))
        cursor.execute("SELECT id FROM products WHERE name = %s", (item,))
        pid = cursor.fetchone()['id']

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
            month, year, pid,
            _safe_float(row.get('Opening_Qty')),
            _safe_float(row.get('Opening_Value')),
            _safe_float(row.get('Received_Qty')),
            _safe_float(row.get('Received_Value')),
            _safe_float(row.get('Sold_Qty')),
            _safe_float(row.get('Sold_Value')),
            _safe_float(row.get('Closing_Qty')),
            _safe_float(row.get('Closing_Value')),
            str(row.get('Remarks', '')).strip()
        ))
        count += 1

    return count, None


def _import_marketing_df(df, cursor):
    """Import marketing DataFrame into marketing_spend."""
    col_map = {}
    for c in df.columns:
        cl = c.strip().lower().replace(' ', '_')
        if cl == 'date':
            col_map[c] = 'Date'
        elif 'month' in cl:
            col_map[c] = 'Month'
        elif 'day' in cl and 'type' in cl:
            col_map[c] = 'Day_Type'
        elif 'digital' in cl:
            col_map[c] = 'Digital_Spend'
        elif 'print' in cl:
            col_map[c] = 'Print_Spend'
        elif 'outdoor' in cl:
            col_map[c] = 'Outdoor_Spend'
        elif 'total' in cl and 'spend' in cl:
            col_map[c] = 'Total_Spend'
        elif 'walk' in cl or 'customer' in cl:
            col_map[c] = 'Customer_Walk_Ins'
        elif 'sales' in cl or 'amount' in cl:
            col_map[c] = 'Sales_Amount'
    df = df.rename(columns=col_map)

    if 'Date' not in df.columns or 'Month' not in df.columns:
        return 0, 'Missing required columns: Date, Month'

    count = 0
    for _, row in df.iterrows():
        date_str = str(row.get('Date', '')).strip()
        month = str(row.get('Month', '')).strip()
        if not date_str or not month:
            continue
        try:
            # Try multiple date formats
            spend_date = None
            for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                try:
                    spend_date = datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue
            if not spend_date:
                continue
        except Exception:
            continue

        digital = _safe_float(row.get('Digital_Spend'))
        print_s = _safe_float(row.get('Print_Spend'))
        outdoor = _safe_float(row.get('Outdoor_Spend'))
        total = _safe_float(row.get('Total_Spend')) or (digital + print_s + outdoor)

        cursor.execute("""
            INSERT INTO marketing_spend
            (spend_date, month_name, day_type, digital_spend, print_spend,
             outdoor_spend, total_spend, customer_walk_ins, sales_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                digital_spend = VALUES(digital_spend),
                print_spend = VALUES(print_spend),
                outdoor_spend = VALUES(outdoor_spend),
                total_spend = VALUES(total_spend),
                customer_walk_ins = VALUES(customer_walk_ins),
                sales_amount = VALUES(sales_amount)
        """, (
            spend_date, month,
            str(row.get('Day_Type', 'Weekday')).strip(),
            digital, print_s, outdoor, total,
            _safe_int(row.get('Customer_Walk_Ins')),
            _safe_float(row.get('Sales_Amount'))
        ))
        count += 1

    return count, None


@app.route('/upload-data', methods=['GET', 'POST'])
@login_required
def upload_data():
    upload_result = None

    if request.method == 'POST':
        data_type = request.form.get('data_type')  # 'stock' or 'marketing'
        year = request.form.get('year', datetime.now().year, type=int)
        file = request.files.get('file')

        if not file or file.filename == '':
            upload_result = {'success': False, 'message': 'No file selected.', 'details': []}
        elif not _allowed_file(file.filename):
            upload_result = {'success': False, 'message': 'Invalid file type. Use CSV, Excel, PDF, or Word.', 'details': []}
        else:
            filename = secure_filename(file.filename)
            if not os.path.exists(Config.UPLOAD_FOLDER):
                os.makedirs(Config.UPLOAD_FOLDER)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                df = _parse_file_to_df(filepath)
                if df.empty:
                    upload_result = {'success': False, 'message': 'File is empty or could not be parsed.', 'details': []}
                else:
                    conn = get_db()
                    cursor = conn.cursor(dictionary=True)
                    try:
                        if data_type == 'stock':
                            count, error = _import_stock_df(df, year, cursor)
                        elif data_type == 'marketing':
                            count, error = _import_marketing_df(df, cursor)
                        else:
                            count, error = 0, 'Unknown data type.'

                        if error:
                            conn.rollback()
                            upload_result = {'success': False, 'message': error, 'details': []}
                        else:
                            conn.commit()
                            upload_result = {
                                'success': True,
                                'message': f'✅ Successfully imported {count} rows of {data_type} data!',
                                'details': [f'File: {filename}', f'Rows processed: {count}']
                            }
                    finally:
                        cursor.close()
                        conn.close()
            except Exception as e:
                upload_result = {'success': False, 'message': f'Error processing file: {str(e)}', 'details': []}
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)

    return render_template('upload.html', upload_result=upload_result)


# ══════════════════════════════════════════════════════════════
#  PREDICTIONS
# ══════════════════════════════════════════════════════════════

def _build_prediction_model():
    """Train a linear regression model from marketing_spend data."""
    from sklearn.linear_model import LinearRegression

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT month_name,
                   SUM(digital_spend) AS digital, SUM(print_spend) AS print_s,
                   SUM(outdoor_spend) AS outdoor, SUM(total_spend) AS total,
                   SUM(customer_walk_ins) AS walkins, SUM(sales_amount) AS sales
            FROM marketing_spend
            GROUP BY month_name
            HAVING COUNT(*) >= 2
            ORDER BY FIELD(month_name,'January','February','March','April',
                           'May','June','July','August','September',
                           'October','November','December')
        """)
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    if len(rows) < 2:
        return None, None, rows

    X = np.array([[float(r['digital']), float(r['print_s']), float(r['outdoor'])] for r in rows])
    y_sales = np.array([float(r['sales']) for r in rows])
    y_walkins = np.array([float(r['walkins']) for r in rows])

    model_sales = LinearRegression()
    model_sales.fit(X, y_sales)

    model_walkins = LinearRegression()
    model_walkins.fit(X, y_walkins)

    return model_sales, model_walkins, rows


@app.route('/predictions', methods=['GET', 'POST'])
@login_required
def predictions():
    prediction = None
    prediction_json = '{}'
    
    # Get current month and next month based on latest data
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get latest month from monthly_stock_summary
        cursor.execute("""
            SELECT month_name, year 
            FROM monthly_stock_summary 
            ORDER BY year DESC, 
                FIELD(month_name,'January','February','March','April','May','June',
                      'July','August','September','October','November','December') DESC
            LIMIT 1
        """)
        latest_month_data = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    
    current_month = latest_month_data['month_name'] if latest_month_data else 'Unknown'
    current_year = latest_month_data['year'] if latest_month_data else datetime.now().year
    
    # Calculate next month
    if current_month != 'Unknown':
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        current_idx = month_names.index(current_month)
        next_idx = (current_idx + 1) % 12
        next_month = month_names[next_idx]
        next_year = current_year + 1 if next_idx == 0 else current_year
    else:
        next_month = 'Unknown'
        next_year = current_year

    if request.method == 'POST':
        digital = float(request.form.get('digital_spend', 0))
        print_s = float(request.form.get('print_spend', 0))
        outdoor = float(request.form.get('outdoor_spend', 0))
        total_budget = digital + print_s + outdoor

        model_sales, model_walkins, hist_rows = _build_prediction_model()

        if model_sales is None:
            flash('Not enough data to make predictions. Upload more marketing data.', 'error')
            return render_template('predictions.html', 
                                   prediction=None, 
                                   prediction_json='{}',
                                   current_month=current_month,
                                   current_year=current_year,
                                   next_month=next_month,
                                   next_year=next_year)

        input_x = np.array([[digital, print_s, outdoor]])
        pred_sales = max(0, float(model_sales.predict(input_x)[0]))
        pred_walkins = max(0, int(round(model_walkins.predict(input_x)[0])))
        roi = round(pred_sales / total_budget, 1) if total_budget > 0 else 0

        # Historical data for charts
        hist_months = [r['month_name'] for r in hist_rows]
        hist_sales = [float(r['sales']) for r in hist_rows]

        # Confidence note
        n = len(hist_rows)
        if n >= 5:
            confidence_note = 'Good amount of historical data — predictions should be fairly reliable.'
        elif n >= 3:
            confidence_note = 'Moderate data available. More months will improve accuracy.'
        else:
            confidence_note = 'Limited data. Upload more months for better predictions.'

        # Stock recommendations
        stock_recs = _get_stock_recommendations()

        # Smart recommendations
        recommendations = []
        avg_digital = np.mean([float(r['digital']) for r in hist_rows])
        avg_print = np.mean([float(r['print_s']) for r in hist_rows])
        avg_outdoor = np.mean([float(r['outdoor']) for r in hist_rows])

        if digital > avg_digital * 1.3:
            recommendations.append({
                'icon': '📱', 'color': '#4facfe',
                'title': 'High Digital Spend',
                'detail': f'Your digital budget (Rs {digital:,.0f}) is significantly above your average (Rs {avg_digital:,.0f}). '
                          'Digital marketing often gives the best ROI for hardware stores through Google Maps and local search ads.'
            })
        elif digital < avg_digital * 0.7:
            recommendations.append({
                'icon': '📱', 'color': '#f5576c',
                'title': 'Consider Increasing Digital Spend',
                'detail': f'Digital spend (Rs {digital:,.0f}) is below average (Rs {avg_digital:,.0f}). '
                          'More digital presence can significantly boost walk-ins.'
            })

        if print_s > avg_print * 1.3:
            recommendations.append({
                'icon': '📰', 'color': '#11998e',
                'title': 'High Print Spend',
                'detail': f'Print budget (Rs {print_s:,.0f}) is above average (Rs {avg_print:,.0f}). '
                          'Local newspaper ads work well for reaching hardware buyers in your area.'
            })

        if outdoor > avg_outdoor * 1.3:
            recommendations.append({
                'icon': '🪧', 'color': '#f7971e',
                'title': 'Good Outdoor Visibility',
                'detail': f'Outdoor spend (Rs {outdoor:,.0f}) is above average. Banners and signage help attract passing customers.'
            })

        if total_budget > 0 and roi > 5:
            recommendations.append({
                'icon': '🏆', 'color': '#11998e',
                'title': 'Excellent Expected ROI',
                'detail': f'Expected ROI of {roi}x means every Rs 1 spent could return Rs {roi} in sales. This is a strong budget allocation.'
            })
        elif total_budget > 0 and roi < 3:
            recommendations.append({
                'icon': '⚠️', 'color': '#f5576c',
                'title': 'Consider Budget Reallocation',
                'detail': f'Expected ROI of {roi}x is moderate. Consider shifting more budget to the channel that historically performs best.'
            })

        # Weekend tip
        recommendations.append({
            'icon': '📅', 'color': '#764ba2',
            'title': 'Focus on Weekends',
            'detail': 'Historical data shows weekends have significantly higher walk-ins and sales. '
                      'Increase marketing intensity on Fridays and Saturdays for better results.'
        })

        prediction = {
            'total_budget': total_budget,
            'predicted_sales': round(pred_sales),
            'predicted_walkins': pred_walkins,
            'roi': roi,
            'data_points': n,
            'confidence_note': confidence_note,
            'stock_recommendations': stock_recs,
            'recommendations': recommendations,
        }

        prediction_json = json.dumps({
            'digital': digital, 'print_val': print_s, 'outdoor': outdoor,
            'predicted_sales': round(pred_sales),
            'hist_months': hist_months,
            'hist_sales': hist_sales,
        })

    return render_template('predictions.html',
                           prediction=prediction,
                           prediction_json=prediction_json,
                           current_month=current_month,
                           current_year=current_year,
                           next_month=next_month,
                           next_year=next_year)


def _get_stock_recommendations():
    """Get stock purchase recommendations based on recent sales trends."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Average sold qty per product across all months
        cursor.execute("""
            SELECT p.name, p.unit,
                   AVG(m.sold_qty) AS avg_sold,
                   (SELECT m2.closing_qty FROM monthly_stock_summary m2
                    WHERE m2.product_id = p.id
                    ORDER BY m2.year DESC,
                             FIELD(m2.month_name, 'January','February','March','April','May','June',
                                   'July','August','September','October','November','December') DESC
                    LIMIT 1) AS current_closing
            FROM products p
            LEFT JOIN monthly_stock_summary m ON p.id = m.product_id
            GROUP BY p.id, p.name, p.unit
            HAVING avg_sold IS NOT NULL
        """)
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    recommendations = []
    for row in rows:
        avg_sold = float(row['avg_sold'] or 0)
        current_closing = float(row['current_closing'] or 0)
        # Recommend purchasing 1.2x avg sold, minus what's already in stock
        recommended = max(0, round(avg_sold * 1.2 - current_closing, 1))
        recommendations.append({
            'product': row['name'],
            'unit': row['unit'],
            'avg_sold': round(avg_sold, 1),
            'current_closing': round(current_closing, 1),
            'recommended_purchase': recommended
        })

    return recommendations


# ── Run app ──────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 5.3 import_data.py

```python
"""
Import CSV data into the MySQL database.
Run this AFTER creating the database via schema.sql in MySQL Workbench.
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
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )


def safe_float(val):
    try:
        return float(val.strip()) if val and val.strip() else 0
    except (ValueError, AttributeError):
        return 0


def safe_int(val):
    try:
        return int(float(val.strip())) if val and val.strip() else 0
    except (ValueError, AttributeError):
        return 0


def create_admin_user(cursor):
    password_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
        ('admin', password_hash)
    )
    print("[OK] Admin user created  (username: admin  |  password: admin123)")


def import_products(cursor, stock_file):
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

            # Create opening entry
            if opening_qty > 0:
                entry_date = date(2025, month_num, 1)
                price = opening_val / opening_qty if opening_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'OPENING', %s, %s, %s, %s)
                """, (entry_date, product_id, opening_qty, price, opening_val, f'{month} opening'))
                count += 1

            # Create received entry
            if received_qty > 0:
                entry_date = date(2025, month_num, 15)
                price = received_val / received_qty if received_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'RECEIVED', %s, %s, %s, %s)
                """, (entry_date, product_id, received_qty, price, received_val, f'{month} received'))
                count += 1

            # Create sold entry
            if sold_qty > 0:
                entry_date = date(2025, month_num, calendar.monthrange(2025, month_num)[1])
                price = sold_val / sold_qty if sold_qty > 0 else 0
                cursor.execute("""
                    INSERT INTO stock_entries 
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, 'SOLD', %s, %s, %s, %s)
                """, (entry_date, product_id, sold_qty, price, sold_val, f'{month} sales'))
                count += 1

    print(f"[OK] Imported {count} stock entries")


def import_marketing_spend(cursor, marketing_file):
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

    if not os.path.exists(STOCK_FILE):
        print(f"ERROR: {STOCK_FILE} not found!")
        exit(1)
    if not os.path.exists(MARKETING_FILE):
        print(f"ERROR: {MARKETING_FILE} not found!")
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

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during import: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
```

### 5.4 requirements.txt

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

---

*[Document continues with Frontend Code section... Due to character limits, this comprehensive documentation would be split into multiple files. Would you like me to continue with the remaining sections in separate files?]*

---

## Summary

This comprehensive documentation includes:
- Complete database schema
- All backend Python code (app.py, config.py, import_data.py)
- Requirements file
- Project structure

**Remaining sections to create:**
- Frontend HTML templates (all 7 files)
- CSS styling code
- Data files structure
- Complete setup instructions
- Testing guide
- Master AI prompt

Would you like me to continue creating the remaining files?
