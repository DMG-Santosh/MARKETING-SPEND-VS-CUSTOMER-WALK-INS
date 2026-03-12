# 🗑️ Database Cleanup & Restoration Guide

## ⚠️ IMPORTANT: Read Before Deleting Database!

This guide explains how to safely delete all database data and restore it with your original clean dataset.

---

## 📋 **Step-by-Step Process**

### **STEP 1: Use the DELETE DATABASE Button** 🔴

1. **Login** to your admin panel: http://localhost:5000
2. **Go to Dashboard** (main admin page)
3. **Scroll down** to the bottom where you see **"Danger Zone"** section (red border)
4. **Click** the button: **"Delete All Database Data"**
5. **Confirm** the 3 security prompts:
   - First warning: Click **OK**
   - Second warning: Click **OK**
   - Final confirmation: Type exactly `DELETE ALL DATA` and press **OK**

**Result:** All data from these tables will be deleted:
- ✅ Products (empty)
- ✅ Stock entries (empty)
- ✅ Monthly stock summaries (empty)
- ✅ Marketing spend data (empty)
- ✅ Users table is **NOT deleted** (your admin login still works!)

---

### **STEP 2: Restore Original Clean Data** 📦

Now you'll restore your original dataset using the import script.

#### **Option A: Using import_data.py (Recommended)**

1. **Open PowerShell** in your project folder:
   ```powershell
   cd "d:\Analytics Project"
   ```

2. **Make sure your CSV files are ready:**
   - `dataset_stock_and_sales_2025.csv` - Stock/sales data
   - `month_wise_spend_data.csv` - Marketing spend data

3. **Run the import script:**
   ```powershell
   python import_data.py
   ```

4. **Expected Output:**
   ```
   [OK] Admin user created  (username: admin  |  password: admin123)
   [OK] 6 products imported: Glass, Plywood, Hardwares, Beeding, Laminates, Doors
   [OK] Imported 36 monthly stock summary rows
   [OK] Imported 180 stock entries
   [OK] Imported 90 marketing spend rows
   ✅ Data import completed successfully!
   ```

---

#### **Option B: Upload via Web Interface**

If you prefer using the web interface:

1. **Login** to http://localhost:5000
2. **Go to Upload Data** page
3. **Upload Stock Data:**
   - Select file: `dataset_stock_and_sales_2025.csv`
   - Year: `2025`
   - Click **"Upload Stock Data"**
   - Wait for success message

4. **Upload Marketing Data:**
   - Select file: `month_wise_spend_data.csv`
   - Click **"Upload Marketing Data"**
   - Wait for success message

---

### **STEP 3: Verify Data Restoration** ✅

1. **Go to Dashboard** - You should see 6 products listed
2. **Go to Monthly History** - Select "March" or "April" - Charts should display
3. **Go to Stock Log** - You should see stock entries
4. **Go to Predictions** - Should show current month as latest data month

---

## 🔄 **What Gets Deleted & What Stays**

### **DELETED:**
- ❌ All products
- ❌ All stock movement entries
- ❌ Monthly stock summaries (all months)
- ❌ Marketing spend data (all months)
- ❌ Test data (May, June 2026 data you uploaded)

### **PRESERVED:**
- ✅ Users table (admin account stays)
- ✅ Database structure (tables not dropped)
- ✅ Your login credentials

---

## 📁 **File Locations**

### **Original Clean Data Files:**
```
d:\Analytics Project\dataset_stock_and_sales_2025.csv
d:\Analytics Project\month_wise_spend_data.csv
```

### **Test Data Files (will NOT be imported):**
```
d:\Analytics Project\test_data\stock_may_2026.csv
d:\Analytics Project\test_data\marketing_may_2026.csv
d:\Analytics Project\test_data\stock_june_2026.xlsx
d:\Analytics Project\test_data\marketing_june_2026.docx
```

---

## 🚨 **Troubleshooting**

### **Problem 1: "Admin user already exists" error**
**Solution:** This is fine! The admin user was preserved. You can login with `admin` / `admin123`

---

### **Problem 2: Charts not showing after restoration**
**Solution:** 
1. Check that data was imported: Go to Stock Log and verify entries exist
2. Try selecting a different month in Monthly History dropdown
3. Check browser console for JavaScript errors (F12)

---

### **Problem 3: "File not found" when running import_data.py**
**Solution:**
1. Make sure you're in the correct directory:
   ```powershell
   cd "d:\Analytics Project"
   dir  # Should show dataset_stock_and_sales_2025.csv
   ```
2. If files are missing, check your Downloads folder or wherever you originally saved them

---

### **Problem 4: Import script fails with MySQL error**
**Solution:**
1. Check MySQL is running (open MySQL Workbench)
2. Verify database exists: `USE analytics_project;` in MySQL Workbench
3. Check config.py has correct password: `Santosh@2005`

---

## 🎯 **Quick Restoration Checklist**

- [ ] Step 1: Click "Delete All Database Data" button
- [ ] Step 2: Confirm 3 security prompts
- [ ] Step 3: Run `python import_data.py` in PowerShell
- [ ] Step 4: Verify products show in Dashboard
- [ ] Step 5: Check Monthly History has charts
- [ ] Step 6: Test Predictions page shows correct current month
- [ ] Step 7: Stock Log has entries
- [ ] ✅ Done! Clean data restored successfully

---

## 💾 **Backup Tips for Future**

Before testing with new data in future:

1. **Take MySQL Backup:**
   ```sql
   -- In MySQL Workbench:
   -- Server > Data Export > Select analytics_project
   -- Export to Self-Contained File: backup_YYYYMMDD.sql
   -- Click "Start Export"
   ```

2. **Or Export via Command Line:**
   ```powershell
   mysqldump -u root -p analytics_project > backup.sql
   ```

3. **To Restore from Backup:**
   ```powershell
   mysql -u root -p analytics_project < backup.sql
   ```

---

## 📞 **Need Help?**

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all files are in the correct location
3. Make sure Flask server is NOT running when you import data
4. Check MySQL Workbench connection is working

---

**Remember:** The DELETE DATABASE button is a powerful tool. Always make sure you have backups before using it! 🛡️
