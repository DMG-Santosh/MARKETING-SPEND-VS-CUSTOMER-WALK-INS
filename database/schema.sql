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