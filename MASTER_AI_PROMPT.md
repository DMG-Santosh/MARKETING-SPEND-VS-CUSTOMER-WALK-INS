# 🤖 MASTER PROMPT FOR AI MODEL — Hardware & Plywood Analytics System

**Purpose:** This prompt contains complete specifications for an AI model to rebuild the entire project from scratch without errors or modifications.

---

## 🎯 Project Overview

### Business Domain
You are building a **Marketing ROI & Footfall Analytics System** for a **Hardware & Plywood Store**. The store sells 6-9 products (Glass, Plywood, Hardwares, Beeding, Laminates, Doors, Cement, Steel Rods, Paints) and wants to:

1. **Track Inventory:** Monitor stock levels with opening/received/sold/closing quantities
2. **Analyze Sales:** Visualize monthly sales performance with colorful charts
3. **Monitor Marketing ROI:** Correlate marketing spend (Digital/Print/Outdoor) with sales and walk-ins
4. **Predict Future Sales:** Use machine learning to forecast sales based on marketing budget
5. **Manage Data:** Upload CSV/Excel/PDF/Word files to import new month data
6. **Database Management:** Clear database and restore original data easily

### Target Users
- **Admin/Owner:** Full access to dashboard, can add/delete products, view all reports
- **Accountants:** Need financial data, monthly summaries, sales reports
- **Managers:** Monitor stock movements, predictions, recommendations

---

## 💻 Technology Stack (EXACT VERSIONS)

### Backend
- **Python:** 3.10.19 (Miniconda environment recommended)
- **Flask:** 3.0.0
- **MySQL:** 8.0+ (mysql-connector-python 8.2.0)
- **Werkzeug:** 3.0.1 (password hashing)

### Data Processing
- **pandas:** 2.1.4 (CSV/Excel manipulation)
- **numpy:** 1.26.2 (numerical operations)
- **openpyxl:** 3.1.2 (Excel file reading)
- **PyPDF2:** 3.0.1 (PDF parsing)
- **python-docx:** 1.1.0 (Word document parsing)

### Machine Learning
- **scikit-learn:** 1.3.2 (LinearRegression for predictions)

### Frontend (CDN)
- **Bootstrap:** 5.3.2 (CSS framework)
- **Bootstrap Icons:** 1.11.3 (icon library)
- **Chart.js:** 4.4.1 (interactive charts)
- **Chart.js DataLabels:** 2.2.0 (value labels on charts)
- **Google Fonts:** Inter (typography)

### Database
- **DBMS:** MySQL 8.0+
- **Database Name:** analytics_project
- **Tables:** users, products, stock_entries, monthly_stock_summary, marketing_spend
- **Connection:** Host=localhost, User=root, Password=Santosh@2005, Port=3306

---

## 📊 Database Schema Design

### Design Philosophy
- **Normalization:** Products in separate table, referenced by FK
- **Flexibility:** Support multiple units (sft, nos, pcs, kg, litre, rft, box, custom)
- **Auditability:** Timestamps on all tables
- **Data Integrity:** CASCADE deletes, unique constraints
- **Performance:** Indexes on date and product columns

### Table Structure

#### 1. users (Authentication)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- werkzeug.security hash
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Default User:** username='admin', password='admin123' (hash: werkzeug.security.generate_password_hash)

#### 2. products (Master Data)
```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,     -- e.g., "Glass", "Plywood"
    unit VARCHAR(20) NOT NULL,              -- e.g., "sft", "nos", "kg"
    price_per_unit DECIMAL(12,2) DEFAULT 0, -- selling price
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Sample Products:** Glass (sft), Plywood (sft), Hardwares (nos), Beeding (rft), Laminates (sft), Doors (nos)

#### 3. stock_entries (Granular Transactions)
```sql
CREATE TABLE stock_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_date DATE NOT NULL,               -- transaction date
    product_id INT NOT NULL,                -- FK to products
    entry_type ENUM('OPENING', 'RECEIVED', 'SOLD') NOT NULL,
    qty DECIMAL(12,2) NOT NULL,            -- quantity (can be fractional)
    price_per_unit DECIMAL(12,2) DEFAULT 0,
    total_value DECIMAL(15,2) DEFAULT 0,
    note VARCHAR(255) DEFAULT NULL,         -- optional description
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_entry_date (entry_date),
    INDEX idx_product (product_id),
    INDEX idx_type (entry_type)
);
```
**Purpose:** Track every stock movement for audit trail and filtering

#### 4. monthly_stock_summary (Aggregated Monthly Data)
```sql
CREATE TABLE monthly_stock_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month_name VARCHAR(20) NOT NULL,        -- "January", "February", etc.
    year INT NOT NULL,                      -- 2025, 2026, etc.
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
);
```
**Purpose:** Historical month-wise summaries for charts and analysis

#### 5. marketing_spend (Daily Marketing Data)
```sql
CREATE TABLE marketing_spend (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spend_date DATE NOT NULL,               -- daily date
    month_name VARCHAR(20) NOT NULL,        -- for grouping
    day_type VARCHAR(20) NOT NULL,          -- "Weekday" or "Weekend"
    digital_spend DECIMAL(12,2) DEFAULT 0,  -- Google Ads, Facebook, etc.
    print_spend DECIMAL(12,2) DEFAULT 0,    -- Newspapers, flyers
    outdoor_spend DECIMAL(12,2) DEFAULT 0,  -- Banners, billboards
    total_spend DECIMAL(12,2) DEFAULT 0,    -- sum of above 3
    customer_walk_ins INT DEFAULT 0,        -- footfall count
    sales_amount DECIMAL(15,2) DEFAULT 0,   -- total sales for the day
    INDEX idx_spend_date (spend_date),
    INDEX idx_month (month_name)
);
```
**Purpose:** Correlate marketing budget with footfall and sales for ML predictions

### Database Relationships
```
users (standalone for auth)

products
  ↓ FK
  ├── stock_entries (product_id)
  └── monthly_stock_summary (product_id)

marketing_spend (standalone, joined with monthly_stock_summary for analysis)
```

---

## 🎨 UI/UX Design Requirements

### Design Philosophy
- **Vibrant & Modern:** Gradient backgrounds, smooth animations, glass-morphism effects
- **Professional:** Clean layouts, consistent spacing, professional color scheme
- **Intuitive:** Clear navigation, visual feedback, contextual help
- **Responsive:** Works on desktop (primary target) and tablet

### Color Palette
```css
Primary Gradient:  linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Header Gradient:   linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)
Success Gradient:  linear-gradient(135deg, #11998e 0%, #38ef7d 100%)
Info Gradient:     linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)
Danger Gradient:   linear-gradient(135deg, #fc5c7d 0%, #e74c3c 100%)
Gold Gradient:     linear-gradient(135deg, #f7971e 0%, #ffd200 100%)
Warm Gradient:     linear-gradient(135deg, #f093fb 0%, #f5576c 100%)
```

### Typography
- **Font Family:** 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif
- **Weights:** 400 (normal), 500 (medium), 600 (semi-bold), 700 (bold), 800 (extra-bold)
- **Scale:** Small (0.72rem), Normal (1rem), Large (1.2rem), Headings (1.5-2rem)

### Animation Requirements
- **Page Load:** Fade-in-up animation (0.6s ease)
- **Cards:** Scale-in animation on load, lift on hover (translateY -4px)
- **Buttons:** Shimmer effect on gradient buttons, lift on hover
- **Gradients:** Slow background-position shift (8s infinite) on header
- **Stagger:** Use animation-delay (.1s, .2s, .3s) for sequential reveals

### Component Specifications

#### 1. Login Page
- Full-viewport gradient background (dark purple-blue)
- Centered white card (max-width 440px) with backdrop-filter blur
- Large circular icon (80px) with gradient background
- Input groups with gradient left borders
- Wide gradient button with shimmer effect on hover
- Floating gradient orbs (radial gradients) animated with pulse

#### 2. Admin Dashboard (Navbar)
- Dark gradient header bar with animated background-position
- Welcome message: "Welcome, {username}!"
- Right-aligned buttons: Monthly History, Logout
- Tabbed interface: "Products & Overview" | "Stock Log & Entries"

#### 3. Stock Log Page
- **Triple Filter System:**
  - Product dropdown (All | Product 1 | Product 2...)
  - Month dropdown (All | January | February...)
  - Year dropdown (All | 2025 | 2026...)
  - Reset Filters button
- **Scrollable Table:**
  - Container: max-height 500px, overflow-y auto
  - Sticky header (position: sticky; top: 0)
  - Gradient header (dark purple-blue)
  - Alternating row hover effects
- **Bulk Delete:**
  - Checkbox column (leftmost)
  - "Select All" checkbox in header
  - Counter showing "X entries selected"
  - "Delete Selected" button (red, only visible when > 0 selected)
  - 3-step confirmation JavaScript

#### 4. Monthly History Page
- Month/Year selector dropdown at top (with "View" button)
- **5 Chart Types (Chart.js with DataLabels plugin):**
  1. **Sales Bar Chart:** Horizontal bars showing sold_value by product
  2. **Sold Quantity Doughnut:** Circle chart with sold_qty breakdown
  3. **Stock Flow Grouped Bar:** Opening/Received/Sold/Closing side-by-side bars
  4. **Marketing Channel Pie:** Digital/Print/Outdoor spend distribution
  5. **Month-on-Month Trend Line:** Line chart showing sales across all available months
- **Chart.js Configuration:**
  - Responsive: true, maintainAspectRatio: false
  - Data labels: display always, anchor: 'end', align: 'top', color: '#333', font: {weight: 'bold'}
  - Gradients: Use CanvasGradient for purple/blue/green fills
  - Tooltips: Enabled with callbacks for formatting
- **Key Insights Panel:**
  - Colorful stat cards showing: Top Product, Lowest Product, Most Qty Sold
  - Gradient top border (4px) on each card
  - Icons in gradient circles

#### 5. Upload Data Page
- Two separate forms side-by-side:
  1. **Stock Data Upload:** Accepts CSV/XLSX/PDF/DOCX, require year input
  2. **Marketing Data Upload:** Accepts same formats, auto-detects dates
- Expected columns list displayed below each form
- Result panel showing success/error with details
- File size limit: 16MB (MAX_CONTENT_LENGTH)

#### 6. Predictions Page
- **Info Banner (Top):**
  - Blue badge: "Current Period: May 2026"
  - Green badge: "Predicting For: June 2026"
- **Budget Input Form:**
  - 3 inputs: Digital Spend (Rs), Print Spend (Rs), Outdoor Spend (Rs)
  - Submit button: "Generate Predictions"
- **Prediction Results:**
  - 4 colorful stat cards: Total Budget, Predicted Sales, Walk-Ins, ROI
  - 2 charts: Budget Allocation Pie, Predicted vs Historical Bar
  - Stock recommendations table (recommended qty to purchase)
  - Smart recommendations panel (context-aware tips)
- **Confidence Note:** Display data points count and reliability message

#### 7. Database Cleanup (Danger Zone)
- Location: Bottom of Admin Panel Tab 2
- Red alert box with border-top separator
- Icon: Exclamation triangle
- **Warning Text:**
  - "This will permanently delete ALL data"
  - Bullet list: products, stock entries, monthly summaries, marketing data
  - "This action CANNOT be undone!"
- **3-Step Confirmation:**
  1. JavaScript confirm: "FIRST WARNING..."
  2. JavaScript confirm: "SECOND WARNING..."
  3. JavaScript prompt: Type "DELETE ALL DATA" exactly
- **Backend:** TRUNCATE tables with FOREIGN_KEY_CHECKS disabled/enabled

---

## 🔧 Flask Application Architecture

### Project Structure
```
d:\Analytics Project\
├── app.py                    # Main Flask application
├── config.py                 # Database configuration class
├── import_data.py            # CSV data import script
├── requirements.txt          # Python dependencies
├── database/
│   └── schema.sql            # MySQL database schema
├── static/
│   └── css/
│       └── style.css         # Custom CSS (~500 lines)
├── templates/
│   ├── base.html             # Base template with CDN links
│   ├── login.html            # Login page
│   ├── admin.html            # Dashboard (tabbed)
│   ├── stock_log.html        # Stock movement log
│   ├── monthly_history.html  # Charts & insights
│   ├── upload.html           # File upload interface
│   └── predictions.html      # ML predictions
├── dataset_stock_and_sales_2025.csv  # Original stock data
└── month_wise_spend_data.csv         # Original marketing data
```

### Flask Routes

#### Authentication Routes
1. **GET/POST /login**
   - GET: Render login.html
   - POST: Validate credentials, check password_hash, set session['user_id']
   - Success: redirect to /dashboard
   - Failure: flash('Invalid username or password', 'error')

2. **GET /logout**
   - Clear session
   - flash('Logged out successfully', 'success')
   - Redirect to /login

3. **@login_required Decorator**
   - Check if 'user_id' in session
   - If not: redirect to /login
   - Use @wraps(f) to preserve function metadata

#### Dashboard Routes
4. **GET /dashboard** (login_required)
   - Query: SELECT all products
   - Query: SELECT latest closing stock for each product (complex JOIN with FIELD() for month ordering)
   - Query: SELECT distinct months and years from monthly_stock_summary
   - Render: admin.html with products, stock_overview, available_months

5. **POST /add-product** (login_required)
   - Form fields: name, unit (dropdown or custom), price_per_unit
   - If unit == '__new__': use custom_unit value (lowercase)
   - INSERT IGNORE into products
   - flash success or error
   - Redirect to /dashboard

6. **POST /delete-product/<int:pid>** (login_required)
   - DELETE FROM products WHERE id = pid
   - Cascade deletes stock_entries and monthly_stock_summary (FK constraint)
   - flash('Product deleted', 'success')
   - Redirect to /dashboard

7. **POST /clear-database** (login_required)
   - CRITICAL: Danger zone operation
   - SET FOREIGN_KEY_CHECKS = 0
   - TRUNCATE TABLE stock_entries, monthly_stock_summary, marketing_spend, products
   - SET FOREIGN_KEY_CHECKS = 1
   - flash('✅ Database cleared successfully! All data has been deleted (users preserved).', 'success')
   - Redirect to /dashboard

#### Stock Log Routes
8. **GET /stock-log** (login_required)
   - Query params: product (id or 'all'), month (name or 'all'), year (int or 'all')
   - Query: SELECT all products for dropdown
   - Query: SELECT distinct months and years from stock_entries (DATE_FORMAT)
   - Build WHERE clause dynamically based on filters
   - Query: SELECT se.*, p.name, p.unit FROM stock_entries JOIN products ORDER BY entry_date DESC
   - Render: stock_log.html with entries, products, filter values, months, years

9. **POST /add-stock-entry** (login_required)
   - Form fields: product_id, entry_type (OPENING/RECEIVED/SOLD), qty, price_per_unit, note, entry_date
   - Validate: all fields required, entry_type in enum
   - Calculate: total_value = qty * price_per_unit
   - INSERT into stock_entries
   - flash('Stock entry added successfully!', 'success')
   - Redirect to /stock-log

10. **POST /delete-entry/<int:eid>** (login_required)
    - DELETE FROM stock_entries WHERE id = eid
    - flash('Entry deleted', 'success')
    - Redirect to /stock-log

11. **POST /delete-entries-bulk** (login_required)
    - Form field: entry_ids[] (array)
    - Validate: len(entry_ids) > 0
    - DELETE FROM stock_entries WHERE id IN (?,?,...)
    - flash(f'{len(entry_ids)} entries deleted successfully', 'success')
    - Redirect to /stock-log

#### Monthly History Routes
12. **GET /monthly-history** (login_required)
    - Query params: month (name), year (int)
    - If not provided: get latest month from monthly_stock_summary (ORDER BY year DESC, FIELD(month_name...) DESC LIMIT 1)
    - Query: SELECT available months for dropdown
    - Query: SELECT products with LEFT JOIN monthly_stock_summary for selected month
    - Query: SELECT marketing_spend for selected month
    - Calculate: Sum digital/print/outdoor spends, total walk-ins, total sales
    - Build insights: top product (max sold_value), lowest product (min sold_value), most qty sold
    - Query: SELECT all months sales for current year (for trend chart)
    - Prepare chart_data dict with products, sold_values, sold_qtys, opening/received/closing, marketing channels, months, sales
    - json.dumps(chart_data) → chart_data_json
    - Render: monthly_history.html with products, chart_data_json, insights, available_months

#### File Upload Routes
13. **GET/POST /upload-data** (login_required)
    - GET: Render upload.html
    - POST:
      - Form fields: data_type ('stock' or 'marketing'), year (int), file (FileStorage)
      - Validate: file exists, allowed extension (.csv, .xlsx, .xls, .pdf, .docx)
      - Save: secure_filename, save to UPLOAD_FOLDER
      - Parse: _parse_file_to_df(filepath) → pandas DataFrame
      - Import: _import_stock_df or _import_marketing_df
      - Cleanup: os.remove(filepath)
      - flash success or error
    - Render: upload.html with upload_result

14. **Helper: _parse_file_to_df(filepath)**
    - CSV: pd.read_csv()
    - Excel: pd.read_excel(engine='openpyxl')
    - PDF: PyPDF2.PdfReader, extract_text, parse to DataFrame
    - Word: python-docx, check tables first, fallback to paragraphs
    - Return: pandas DataFrame or empty DataFrame

15. **Helper: _import_stock_df(df, year, cursor)**
    - Normalize column names (lowercase, replace spaces with _)
    - Map columns to: Month, Item, Unit, Opening_Qty, Opening_Value, Received_Qty, Received_Value, Sold_Qty, Sold_Value, Closing_Qty, Closing_Value, Remarks
    - For each row:
      - INSERT IGNORE INTO products (name, unit)
      - SELECT id FROM products WHERE name = item
      - INSERT INTO monthly_stock_summary ... ON DUPLICATE KEY UPDATE ...
    - Return: (count, error)

16. **Helper: _import_marketing_df(df, cursor)**
    - Normalize columns: Date, Month, Day_Type, Digital_Spend, Print_Spend, Outdoor_Spend, Total_Spend, Customer_Walk_Ins, Sales_Amount
    - For each row:
      - Parse date (try multiple formats: '%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y')
      - Calculate total_spend if not provided
      - INSERT INTO marketing_spend ... ON DUPLICATE KEY UPDATE ...
    - Return: (count, error)

#### Prediction Routes
17. **GET/POST /predictions** (login_required)
    - GET:
      - Query: SELECT latest month from monthly_stock_summary (month_name, year)
      - Calculate: next_month (handle year rollover)
      - Render: predictions.html with current_month, current_year, next_month, next_year
    - POST:
      - Form fields: digital_spend, print_spend, outdoor_spend (floats)
      - Calculate: total_budget = digital + print + outdoor
      - Train model: _build_prediction_model() → (model_sales, model_walkins, hist_rows)
      - Predict: input_x = [[digital, print, outdoor]], pred_sales = model_sales.predict(input_x), pred_walkins = model_walkins.predict(input_x)
      - Calculate: roi = pred_sales / total_budget (if > 0)
      - Get recommendations: _get_stock_recommendations()
      - Build smart_recommendations: Compare budget vs historical avg, add tips
      - Prepare prediction dict and prediction_json (for charts)
      - Render: predictions.html with prediction, prediction_json, current/next month

18. **Helper: _build_prediction_model()**
    - Query: SELECT month_name, SUM(digital/print/outdoor) AS digital/print_s/outdoor, SUM(customer_walk_ins), SUM(sales_amount) FROM marketing_spend GROUP BY month_name HAVING COUNT(*) >= 2
    - Build X: np.array([[digital, print, outdoor], ...])
    - Build y_sales: np.array([sales, ...])
    - Build y_walkins: np.array([walkins, ...])
    - Train: LinearRegression().fit(X, y)
    - Return: (model_sales, model_walkins, hist_rows)

19. **Helper: _get_stock_recommendations()**
    - Query: SELECT p.name, p.unit, AVG(m.sold_qty) AS avg_sold, (latest closing_qty) FROM products JOIN monthly_stock_summary GROUP BY product
    - For each product:
      - recommended_purchase = max(0, avg_sold * 1.2 - current_closing)
    - Return: list of dicts (product, unit, avg_sold, current_closing, recommended_purchase)

### Flask Configuration

#### config.py
```python
class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Santosh@2005'
    MYSQL_DATABASE = 'analytics_project'
    MYSQL_PORT = 3306
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

#### Database Connection Pooling
```python
from mysql.connector import pooling

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
```

#### Custom Jinja2 Filter
```python
@app.template_filter('numfmt')
def number_format(value, decimals=0):
    """Format number with thousand separators and decimal places."""
    try:
        return '{:,.{d}f}'.format(float(value), d=int(decimals))
    except (ValueError, TypeError):
        return value
```
Usage in templates: `{{ value|numfmt }}` or `{{ value|numfmt(2) }}`

---

## 📝 Data Import Script (import_data.py)

### Purpose
Import original CSV files into MySQL database for initial setup.

### Workflow
1. **Create Admin User:** Generate password hash for 'admin'/'admin123'
2. **Import Products:** Extract unique products from stock CSV
3. **Import Monthly Stock Summary:** Load aggregated monthly data
4. **Import Stock Entries:** Create individual transactions (1st, 15th, last day of month)
5. **Import Marketing Spend:** Load daily marketing data

### Key Functions

#### 1. create_admin_user(cursor)
```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash('admin123')
cursor.execute(
    "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
    ('admin', password_hash)
)
```

#### 2. import_products(cursor, stock_file)
```python
products = {}  # {name: unit}
with open(stock_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        item = row['Item'].strip()
        unit = row['Unit'].strip().lower()
        if item and unit:
            products[item] = unit

for name, unit in products.items():
    cursor.execute("INSERT IGNORE INTO products (name, unit) VALUES (%s, %s)", (name, unit))

# Return product_map: {name: id}
cursor.execute("SELECT id, name FROM products")
return {row[1]: row[0] for row in cursor.fetchall()}
```

#### 3. import_monthly_stock(cursor, stock_file, product_map)
```python
with open(stock_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        month = row['Month'].strip()
        item = row['Item'].strip()
        product_id = product_map[item]
        
        cursor.execute("""
            INSERT INTO monthly_stock_summary
            (month_name, year, product_id, opening_qty, opening_value, ...)
            VALUES (%s, %s, %s, %s, %s, ...)
            ON DUPLICATE KEY UPDATE opening_qty = VALUES(opening_qty), ...
        """, (month, 2025, product_id, safe_float(row['Opening_Qty']), ...))
```

#### 4. import_stock_entries(cursor, stock_file, product_map)
Create 3 entries per month per product:
- **OPENING:** Date = 1st of month, qty = Opening_Qty, price = Opening_Value / Opening_Qty
- **RECEIVED:** Date = 15th of month, qty = Received_Qty, price = Received_Value / Received_Qty
- **SOLD:** Date = last day of month, qty = Sold_Qty, price = Sold_Value / Sold_Qty

#### 5. import_marketing_spend(cursor, marketing_file)
```python
with open(marketing_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_str = row['Date'].strip()
        spend_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        
        cursor.execute("""
            INSERT INTO marketing_spend
            (spend_date, month_name, day_type, digital_spend, ...)
            VALUES (%s, %s, %s, %s, ...)
        """, (spend_date, row['Month'], row['Day_Type'], safe_float(row['Digital_Spend']), ...))
```

### Execution
```bash
python import_data.py
```
Output:
```
=== Starting data import ===

[OK] Admin user created  (username: admin  |  password: admin123)
[OK] 6 products imported: Glass, Plywood, Hardwares, Beeding, Laminates, Doors
[OK] Imported 90 monthly stock summary rows
[OK] Imported 180 stock entries
[OK] Imported 90 marketing spend rows

✅ Data import completed successfully!
```

---

## 🎨 Frontend Templates

### base.html (Master Template)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Analytics Project{% endblock %}</title>
    
    <!-- Bootstrap 5.3.2 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons 1.11.3 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    
    <!-- Google Fonts: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    <div class="container mt-3" style="position:relative;z-index:1000">
        {% for category, message in messages %}
        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show" role="alert">
            <i class="bi bi-{{ 'exclamation-triangle' if category == 'error' else 'check-circle' }} me-1"></i>
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    {% endwith %}
    
    <!-- Content Block -->
    {% block content %}{% endblock %}
    
    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Template Guidelines

1. **Extend base.html:** All templates use `{% extends "base.html" %}`
2. **Block title:** Set page-specific title
3. **Block content:** Main page content
4. **Block scripts:** Page-specific JavaScript (Chart.js, custom JS)

---

## 📈 Chart.js Implementation

### Global Configuration
```javascript
// Disable default data labels globally (we use plugin)
Chart.defaults.plugins.datalabels = { display: false };
```

### Chart 1: Sales Bar Chart (Horizontal)
```javascript
const ctx1 = document.getElementById('salesChart').getContext('2d');
const grad1 = ctx1.createLinearGradient(0, 0, 400, 0);
grad1.addColorStop(0, '#667eea');
grad1.addColorStop(1, '#764ba2');

new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: chartData.products,
        datasets: [{
            label: 'Sales (Rs)',
            data: chartData.sold_values,
            backgroundColor: grad1,
            borderRadius: 8
        }]
    },
    options: {
        indexAxis: 'y',  // horizontal bars
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                display: true,
                anchor: 'end',
                align: 'right',
                color: '#333',
                font: { weight: 'bold', size: 11 },
                formatter: (value) => 'Rs ' + value.toLocaleString()
            },
            legend: { display: false },
            tooltip: { enabled: true }
        },
        scales: {
            x: { beginAtZero: true, grid: { display: false } }
        }
    }
});
```

### Chart 2: Sold Quantity Doughnut
```javascript
new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: chartData.products,
        datasets: [{
            data: chartData.sold_qtys,
            backgroundColor: ['#667eea', '#4facfe', '#11998e', '#f7971e', '#fc5c7d', '#764ba2'],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                display: true,
                color: '#fff',
                font: { weight: 'bold', size: 12 },
                formatter: (value, ctx) => {
                    const label = ctx.chart.data.labels[ctx.dataIndex];
                    return label + '\n' + value.toFixed(1);
                }
            },
            legend: { position: 'bottom' }
        }
    }
});
```

### Chart 3: Stock Flow Grouped Bar
```javascript
new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: chartData.products,
        datasets: [
            {
                label: 'Opening',
                data: chartData.opening_qtys,
                backgroundColor: '#667eea'
            },
            {
                label: 'Received',
                data: chartData.received_qtys,
                backgroundColor: '#4facfe'
            },
            {
                label: 'Sold',
                data: chartData.sold_qtys,
                backgroundColor: '#fc5c7d'
            },
            {
                label: 'Closing',
                data: chartData.closing_qtys,
                backgroundColor: '#11998e'
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                display: true,
                anchor: 'end',
                align: 'top',
                color: '#333',
                font: { weight: 'bold', size: 10 },
                formatter: (value) => value.toFixed(1)
            }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

### Chart 4: Marketing Channel Pie
```javascript
new Chart(ctx4, {
    type: 'pie',
    data: {
        labels: chartData.marketing_channels,  // ['Digital', 'Print', 'Outdoor']
        datasets: [{
            data: chartData.marketing_spends,
            backgroundColor: ['#4facfe', '#fc5c7d', '#f7971e']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                display: true,
                color: '#fff',
                font: { weight: 'bold', size: 12 },
                formatter: (value) => 'Rs ' + value.toLocaleString()
            }
        }
    }
});
```

### Chart 5: Month-on-Month Trend Line
```javascript
new Chart(ctx5, {
    type: 'line',
    data: {
        labels: chartData.all_months,
        datasets: [{
            label: 'Sales Trend (Rs)',
            data: chartData.all_months_sales,
            borderColor: '#11998e',
            backgroundColor: 'rgba(17, 153, 142, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 6,
            pointBackgroundColor: '#11998e'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                display: true,
                anchor: 'end',
                align: 'top',
                color: '#333',
                font: { weight: 'bold', size: 11 },
                formatter: (value) => 'Rs ' + value.toLocaleString()
            }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
```

---

## 🧪 Testing & Verification

### Phase 1: Environment Setup
1. Install Python 3.10+ (Miniconda recommended)
2. Create conda environment: `conda create -n analytics_env python=3.10`
3. Activate: `conda activate analytics_env`
4. Install dependencies: `pip install -r requirements.txt`
5. Install MySQL 8.0+ (MySQL Workbench recommended)

### Phase 2: Database Setup
1. Open MySQL Workbench
2. Create connection: localhost, root, password: Santosh@2005
3. Execute schema.sql in SQL editor
4. Verify: `SHOW TABLES;` should show 5 tables

### Phase 3: Data Import
1. Place CSV files in project root:
   - dataset_stock_and_sales_2025.csv
   - month_wise_spend_data.csv
2. Run: `python import_data.py`
3. Verify output: ✅ Data import completed successfully!
4. Check database:
   - `SELECT COUNT(*) FROM products;` → 6 rows
   - `SELECT COUNT(*) FROM monthly_stock_summary;` → 90 rows (6 products × 15 months)
   - `SELECT COUNT(*) FROM stock_entries;` → 180+ rows
   - `SELECT COUNT(*) FROM marketing_spend;` → 90+ rows
   - `SELECT * FROM users;` → 1 row (admin)

### Phase 4: Flask Application
1. Run: `python app.py`
2. **Expected output:**
   ```
    * Serving Flask app 'app'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
   ```
3. Open browser: http://localhost:5000
4. Should redirect to /login

### Phase 5: Feature Testing

#### 5.1 Login System
- [ ] Navigate to http://localhost:5000/login
- [ ] See gradient login card with store icon
- [ ] Enter invalid credentials → flash error "Invalid username or password"
- [ ] Enter valid credentials (admin / admin123) → redirect to /dashboard
- [ ] See welcome message "Welcome, admin!"

#### 5.2 Dashboard
- [ ] See tabbed interface with 2 tabs
- [ ] Tab 1: Products & Overview
  - [ ] Stock overview table shows 6 products
  - [ ] Each product has opening/received/sold/closing/value/price
  - [ ] "In Stock" badge shows green (in stock) or red (out of stock)
- [ ] Add new product form:
  - [ ] Enter product name, select unit, enter price
  - [ ] Click "+ Add" → product added to list
  - [ ] Try adding duplicate product → flash error "Product already exists"
- [ ] Delete product:
  - [ ] Click "Delete" button on any product → confirm dialog
  - [ ] Confirm → product deleted, cascade removes related data
- [ ] Action buttons:
  - [ ] Click "Stock Log" → navigate to /stock-log
  - [ ] Click "Upload Data" → navigate to /upload-data
  - [ ] Click "Predictions" → navigate to /predictions

#### 5.3 Stock Log
- [ ] See table with all stock entries
- [ ] Table has scrollable container (max-height 500px)
- [ ] Header is sticky when scrolling
- [ ] Filter system:
  - [ ] Product dropdown shows "All" + all products
  - [ ] Month dropdown shows "All" + all months from data
  - [ ] Year dropdown shows "All" + all years
  - [ ] Select filters → click apply → table updates
  - [ ] Click "Reset Filters" → clear all filters
- [ ] Bulk delete:
  - [ ] Check "Select All" → all checkboxes checked, counter shows "X entries selected"
  - [ ] Uncheck "Select All" → all unchecked
  - [ ] Check individual entries → counter updates
  - [ ] Click "Delete Selected" → 3-step confirmation
  - [ ] Confirm all 3 steps → entries deleted
  - [ ] Flash: "X entries deleted successfully"
- [ ] Add new entry:
  - [ ] Fill form (product, type, qty, price, date, note)
  - [ ] Click "Add Entry" → entry added to table
  - [ ] Flash: "Stock entry added successfully!"

#### 5.4 Monthly History
- [ ] Month/Year selector at top
- [ ] Select month → click "View" → charts update
- [ ] **5 Charts visible:**
  1. Sales Bar Chart (horizontal bars, gradient purple-blue)
  2. Sold Quantity Doughnut (colorful segments, white labels)
  3. Stock Flow Grouped Bar (4 colors: opening/received/sold/closing)
  4. Marketing Channel Pie (3 slices: digital/print/outdoor)
  5. Month-on-Month Trend Line (green line with area fill)
- [ ] **All charts have data labels** (values on bars/segments/points)
- [ ] Key Insights panel shows:
  - Top product by sales value
  - Lowest product by sales value
  - Most quantity sold
- [ ] Marketing summary cards show totals

#### 5.5 Upload Data
- [ ] See 2 forms (Stock Data | Marketing Data)
- [ ] Stock form:
  - [ ] Select CSV file → upload → success
  - [ ] Try Excel file → success
  - [ ] Try PDF (if formatted) → success or parse error
  - [ ] Try Word (if table) → success or parse error
- [ ] Marketing form:
  - [ ] Upload CSV → success
- [ ] Result panel shows:
  - Success: green alert with row count
  - Error: red alert with error message

#### 5.6 Predictions
- [ ] See info banner at top:
  - Blue badge: "Current Period: {month} {year}"
  - Green badge: "Predicting For: {next_month} {next_year}"
- [ ] Budget input form:
  - Enter digital spend: 5000
  - Enter print spend: 3000
  - Enter outdoor spend: 2000
  - Click "Generate Predictions"
- [ ] Prediction results:
  - [ ] 4 stat cards: Budget (10000), Sales, Walk-Ins, ROI
  - [ ] Budget allocation pie chart (3 slices with labels)
  - [ ] Predicted vs Historical bar chart (comparison)
  - [ ] Stock recommendations table (buy qty for each product)
  - [ ] Smart recommendations panel (colored cards with tips)
- [ ] Confidence note displayed based on data points

#### 5.7 Database Cleanup
- [ ] Navigate to Dashboard → Tab 2 (Stock Log & Entries)
- [ ] Scroll to bottom → see "Danger Zone" section
- [ ] Red alert box with warnings
- [ ] Click "Delete All Database Data" button
- [ ] **3-Step Confirmation:**
  1. First confirm dialog → Click OK
  2. Second confirm dialog → Click OK
  3. Prompt: Type "DELETE ALL DATA" exactly → Submit
- [ ] Database cleared → flash: "✅ Database cleared successfully!"
- [ ] Verify: All products, stock entries, summaries deleted
- [ ] Verify: Users table still has admin (preserved)
- [ ] Restore data: `python import_data.py`

### Phase 6: Error Handling
- [ ] Try accessing /dashboard without login → redirect to /login
- [ ] Enter very large decimal values → accepted (DECIMAL(12,2))
- [ ] Upload invalid file (e.g., .txt) → error: "Invalid file type"
- [ ] Upload empty file → error: "File is empty or could not be parsed"
- [ ] Delete product with stock entries → cascade deletes all related data
- [ ] SQL injection attempts → parameterized queries prevent

### Phase 7: UI/UX Validation
- [ ] All pages have gradient backgrounds
- [ ] Cards have hover effects (lift up, shadow increases)
- [ ] Buttons have shimmer effect on hover
- [ ] Animations play on page load (fade-in-up, stagger delays)
- [ ] Forms have focus states (gradient borders)
- [ ] Flash messages auto-dismiss on close button click
- [ ] Tables have sticky headers
- [ ] Responsive layout (works on 1920x1080, 1366x768)

---

## 🚨 Common Pitfalls & Solutions

### Issue 1: Import Error - Module 'mysql.connector' not found
**Solution:** Install correct package: `pip install mysql-connector-python`

### Issue 2: Chart.js data labels not showing
**Solution:** Ensure Chart.js DataLabels plugin loaded AFTER Chart.js:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
```

### Issue 3: Database connection error "Access denied"
**Solution:** Check config.py credentials match MySQL user
```python
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Santosh@2005'  # Change to your actual password
```

### Issue 4: Empty database after schema.sql
**Solution:** Run `python import_data.py` to populate with initial data

### Issue 5: Jinja2 syntax error in JavaScript
**Solution:** Use `url_for()` outside of JavaScript strings:
```javascript
// WRONG
onclick="window.location.href='{{ url_for('stock_log') }}'"

// CORRECT
const stockLogUrl = '{{ url_for("stock_log") }}';
button.onclick = () => { window.location.href = stockLogUrl; };
```

### Issue 6: Predictions showing "Not enough data"
**Solution:** Ensure at least 2 months of marketing_spend data exists

### Issue 7: File upload fails silently
**Solution:** Check UPLOAD_FOLDER exists, create if not:
```python
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)
```

### Issue 8: Bulk delete not working
**Solution:** Ensure JavaScript sends entry_ids[] as array:
```javascript
form.innerHTML = selectedCheckboxes.map(cb => 
    `<input type="hidden" name="entry_ids[]" value="${cb.value}">`
).join('');
```

---

## 📋 Requirements.txt

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

## 🎓 Implementation Order

### Step 1: Database Setup (30 minutes)
1. Install MySQL 8.0+
2. Create database: analytics_project
3. Execute schema.sql (creates 5 tables)
4. Verify tables created: `SHOW TABLES;`

### Step 2: Project Structure (15 minutes)
1. Create folder: `d:\Analytics Project\`
2. Create subfolders: database/, static/css/, templates/
3. Create files: config.py, requirements.txt
4. Install dependencies: `pip install -r requirements.txt`

### Step 3: Configuration (10 minutes)
1. Write config.py with database credentials
2. Test MySQL connection in Python REPL

### Step 4: Data Import Script (45 minutes)
1. Write import_data.py with 5 functions
2. Place CSV files in project root
3. Run script: `python import_data.py`
4. Verify data in database

### Step 5: Flask Application Core (1 hour)
1. Create app.py skeleton
2. Implement database connection pooling
3. Add login_required decorator
4. Implement login/logout routes
5. Test login at http://localhost:5000/login

### Step 6: Templates Base (30 minutes)
1. Create base.html with CDN links
2. Create login.html extending base
3. Test login page renders

### Step 7: Dashboard (1.5 hours)
1. Implement /dashboard route
2. Create admin.html with tabbed interface
3. Implement add_product, delete_product routes
4. Test product management

### Step 8: Stock Log (2 hours)
1. Implement /stock-log route with filters
2. Create stock_log.html with scrollable table
3. Implement add_stock_entry route
4. Add bulk delete feature (checkbox + JS)
5. Test filtering and deletion

### Step 9: Monthly History (2.5 hours)
1. Implement /monthly-history route
2. Create monthly_history.html
3. Add 5 Chart.js charts with DataLabels
4. Implement insights calculation
5. Test month selector and charts

### Step 10: File Upload (1.5 hours)
1. Implement /upload-data route
2. Write _parse_file_to_df helper
3. Write _import_stock_df and _import_marketing_df helpers
4. Create upload.html with 2 forms
5. Test CSV, Excel, PDF, Word uploads

### Step 11: Predictions (2 hours)
1. Implement /predictions route
2. Write _build_prediction_model with LinearRegression
3. Write _get_stock_recommendations
4. Create predictions.html with forms and charts
5. Add smart recommendations logic
6. Add current/next month detection
7. Test predictions with different budgets

### Step 12: Database Cleanup (45 minutes)
1. Implement /clear-database route with TRUNCATE
2. Add Danger Zone section to admin.html
3. Add 3-step JavaScript confirmation
4. Test cleanup and restoration

### Step 13: CSS Styling (2 hours)
1. Create style.css with 500+ lines
2. Define CSS variables (gradients, colors)
3. Add 6 keyframe animations
4. Style all components (cards, tables, buttons, badges)
5. Test hover effects and animations

### Step 14: Testing & Polish (1 hour)
1. Test all routes and features
2. Check error handling
3. Verify responsive design
4. Test database operations
5. Run end-to-end user flow

**Total Implementation Time: ~15-18 hours**

---

## ✅ Success Criteria

Your rebuild is successful if:

1. ✅ Login page has gradient background, white centered card, working auth
2. ✅ Dashboard shows 6 products with stock overview table
3. ✅ Stock log has triple filters (product/month/year) + bulk delete
4. ✅ Monthly history shows 5 charts with data labels
5. ✅ Upload page accepts CSV/Excel/PDF/Word and imports data
6. ✅ Predictions page shows current/next month + ML forecast
7. ✅ Database cleanup button works with 3-step confirmation
8. ✅ All gradients, animations, glass effects render correctly
9. ✅ No Python errors, no JavaScript errors, no SQL errors
10. ✅ `python import_data.py` restores original data cleanly

---

## 📞 Final Notes for AI Model

**IMPORTANT REMINDERS:**

1. **Do NOT modify feature requirements:** Rebuild exactly as specified
2. **Use EXACT versions:** Flask 3.0.0, Bootstrap 5.3.2, Chart.js 4.4.1, etc.
3. **Database credentials:** Root user with password Santosh@2005 (as per original project)
4. **File paths:** Use absolute paths like `d:\Analytics Project\`
5. **Chart.js DataLabels:** Must load plugin AFTER Chart.js core
6. **Jinja2 in JavaScript:** Extract URL generation outside script tags
7. **SQL parameterization:** Always use %s placeholders, never string concatenation
8. **Bulk delete:** Use entry_ids[] array notation in form data
9. **TRUNCATE safety:** Wrap in FOREIGN_KEY_CHECKS = 0/1
10. **Password hashing:** Use werkzeug.security.generate_password_hash

**Test after each phase before moving to next!**

Good luck rebuilding! 🚀
