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
                safe_float(row.get('Opening_Qty', '')),
                safe_float(row.get('Opening_Value', '')),
                safe_float(row.get('Received_Qty', '')),
                safe_float(row.get('Received_Value', '')),
                safe_float(row.get('Sold_Qty', '')),
                safe_float(row.get('Sold_Value', '')),
                safe_float(row.get('Closing_Qty', '')),
                safe_float(row.get('Closing_Value', '')),
                row.get('Remarks', '').strip() or None
            ))
            count += 1
    print(f"[OK] {count} monthly stock summary records imported")


def import_stock_entries(cursor, stock_file, product_map):
    count = 0
    with open(stock_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = row.get('Month', '').strip()
            item = row.get('Item', '').strip()
            if not month or not item or item not in product_map or month not in MONTH_MAP:
                continue

            product_id = product_map[item]
            month_num = MONTH_MAP[month]
            year = 2025
            last_day = calendar.monthrange(year, month_num)[1]

            opening_qty = safe_float(row.get('Opening_Qty', ''))
            opening_val = safe_float(row.get('Opening_Value', ''))
            received_qty = safe_float(row.get('Received_Qty', ''))
            received_val = safe_float(row.get('Received_Value', ''))
            sold_qty = safe_float(row.get('Sold_Qty', ''))
            sold_val = safe_float(row.get('Sold_Value', ''))

            entries = []

            if opening_qty > 0:
                ppu = round(opening_val / opening_qty, 2)
                entries.append((
                    date(year, month_num, 1), product_id, 'OPENING',
                    opening_qty, ppu, opening_val, f'{month} opening stock'
                ))

            if received_qty > 0:
                ppu = round(received_val / received_qty, 2)
                entries.append((
                    date(year, month_num, 15), product_id, 'RECEIVED',
                    received_qty, ppu, received_val, f'{month} received stock'
                ))

            if sold_qty > 0:
                ppu = round(sold_val / sold_qty, 2)
                entries.append((
                    date(year, month_num, last_day), product_id, 'SOLD',
                    sold_qty, ppu, sold_val, f'{month} sales'
                ))

            for entry in entries:
                cursor.execute("""
                    INSERT INTO stock_entries
                    (entry_date, product_id, entry_type, qty, price_per_unit, total_value, note)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, entry)
                count += 1

    print(f"[OK] {count} stock movement entries created")


def import_marketing_spend(cursor, spend_file):
    count = 0
    with open(spend_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('Date', '').strip()
            month = row.get('Month', '').strip()
            if not date_str or not month:
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
                month,
                row.get('Day_Type', '').strip(),
                safe_float(row.get('Digital_Spend', '')),
                safe_float(row.get('Print_Spend', '')),
                safe_float(row.get('Outdoor_Spend', '')),
                safe_float(row.get('Total_Spend', '')),
                safe_int(row.get('Customer_Walk_Ins', '')),
                safe_float(row.get('Sales_Amount', ''))
            ))
            count += 1
    print(f"[OK] {count} marketing spend records imported")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stock_file = os.path.join(base_dir, 'dataset_stock_and_sales_2025.csv')
    spend_file = os.path.join(base_dir, 'month_wise_spend_data.csv')

    for fpath in [stock_file, spend_file]:
        if not os.path.exists(fpath):
            print(f"[ERROR] File not found: {fpath}")
            return

    print("=" * 55)
    print("  Analytics Project — Data Import")
    print("=" * 55)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        create_admin_user(cursor)
        conn.commit()

        product_map = import_products(cursor, stock_file)
        conn.commit()

        import_monthly_stock(cursor, stock_file, product_map)
        conn.commit()

        import_stock_entries(cursor, stock_file, product_map)
        conn.commit()

        import_marketing_spend(cursor, spend_file)
        conn.commit()

        print("=" * 55)
        print("  All data imported successfully!")
        print("=" * 55)

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
