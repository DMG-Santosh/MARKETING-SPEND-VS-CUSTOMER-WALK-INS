# 📊 Upload Data Feature - Test Files Guide

## 🎯 Data Format Requirements

### **1. Stock & Sales Data**
Upload monthly stock movement data with these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Month` | Text | Month name | May, June |
| `Item` | Text | Product name | Glass, Plywood, Cement |
| `Unit` | Text | Unit of measurement | SFT, NOS, BAG, LTR, TON |
| `Opening_Qty` | Number | Opening stock quantity | 225, 1500 |
| `Opening_Value` | Number | Opening stock value (₹) | 348208, 450000 |
| `Received_Qty` | Number | Received/purchased quantity | 210, 1200 |
| `Received_Value` | Number | Purchase value (₹) | 324994, 360000 |
| `Sold_Qty` | Number | Sold quantity | 160, 800 |
| `Sold_Value` | Number | Sales value (₹) | 247614, 240000 |
| `Closing_Qty` | Number | Closing stock quantity | 210, 900 |
| `Closing_Value` | Number | Closing stock value (₹) | 324993, 210000 |
| `Remarks` | Text | Optional notes | "High demand", "Festival stock" |

**Accepted File Formats:**
- ✅ CSV (.csv)
- ✅ Excel (.xlsx, .xls)
- ✅ PDF (.pdf) - with tabular data
- ✅ Word (.docx) - with table format

---

### **2. Marketing Spend Data**
Upload daily marketing spend and performance data:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Date` | Date | Date in DD-MM-YYYY format | 01-05-2026, 15-06-2026 |
| `Month` | Text | Month name | May, June |
| `Day_Type` | Text | Weekday or Weekend | Weekday, Weekend |
| `Digital_Spend` | Number | Digital marketing spend (₹) | 1500, 2400 |
| `Print_Spend` | Number | Print media spend (₹) | 600, 950 |
| `Outdoor_Spend` | Number | Outdoor advertising spend (₹) | 400, 750 |
| `Total_Spend` | Number | Total marketing spend (₹) | 2500, 4100 |
| `Customer_Walk_Ins` | Integer | Number of customers | 45, 92 |
| `Sales_Amount` | Number | Sales amount (₹) | 54000, 110400 |

**Accepted File Formats:**
- ✅ CSV (.csv)
- ✅ Excel (.xlsx, .xls)
- ✅ PDF (.pdf) - with tabular data
- ✅ Word (.docx) - with table format

---

## 📁 Test Files Included

### CSV Format (Stock Data)
- **File:** `stock_may_2026.csv`
- **Data:** May 2026 stock movement for 8 products
- **Use:** Test basic CSV upload

### CSV Format (Marketing Data)
- **File:** `marketing_may_2026.csv`
- **Data:** May 2026 daily marketing spend (20 days)
- **Use:** Test basic CSV upload

### Excel Format (Stock Data)
- **File:** `stock_june_2026.xlsx`
- **Data:** June 2026 stock movement with 9 products
- **Use:** Test Excel file parsing

### Word Format (Marketing Data)
- **File:** `marketing_june_2026.docx`
- **Data:** June 2026 marketing data (8 days) in table format
- **Use:** Test Word document table extraction

---

## 🚀 How to Test Upload Feature

1. **Start your Flask server:**
   ```bash
   python app.py
   ```

2. **Login to admin dashboard:**
   - Go to http://localhost:5000
   - Login: admin / admin123

3. **Navigate to Upload Data page:**
   - Click "Upload Data" button on dashboard
   - Or go to: http://localhost:5000/upload-data

4. **Test Stock Data Upload:**
   - Select "Stock & Sales Data" section
   - Choose file: `stock_may_2026.csv` or `stock_june_2026.xlsx`
   - Set Year: 2026
   - Click "Upload Stock Data"
   - ✅ Check success message

5. **Test Marketing Data Upload:**
   - Select "Marketing Spend Data" section
   - Choose file: `marketing_may_2026.csv` or `marketing_june_2026.docx`
   - Click "Upload Marketing Data"
   - ✅ Check success message

6. **Verify Data:**
   - Go to "Monthly History" page
   - Select "May" or "June" from dropdown
   - ✅ See charts updated with new data!

---

## 🎨 Format Examples

### CSV Format Example:
```csv
Month,Item,Unit,Opening_Qty,Opening_Value,Received_Qty,Received_Value,Sold_Qty,Sold_Value,Closing_Qty,Closing_Value,Remarks
May,Glass,SFT,240,371520,280,433440,185,286380,335,518580,New supplier added
May,Plywood,SFT,260,218400,250,210000,195,163800,315,264600,Higher demand
```

### Excel Format:
- Same columns as CSV
- Standard Excel workbook (.xlsx)
- First row contains headers

### Word Format:
- Document contains a table
- First row is header row
- Data in subsequent rows

### PDF Format:
- Contains tabular data
- Text should be extractable (not scanned image)
- Columns separated by spaces/tabs or commas

---

## 💡 Tips

1. **Column Names:** The system is flexible with column names. It recognizes variations like:
   - "Opening Qty" = "Opening_Qty" = "opening qty"
   - "Total Spend" = "Total_Spend" = "total_spend"

2. **Date Formats:** Multiple date formats are supported:
   - DD-MM-YYYY (recommended)
   - YYYY-MM-DD
   - DD/MM/YYYY
   - MM/DD/YYYY

3. **Missing Optional Fields:** 
   - `Remarks` is optional for stock data
   - `Total_Spend` is auto-calculated if missing

4. **Year Selection:** For stock data, specify the year (default: 2025)

5. **Error Messages:** If upload fails, check the error message for:
   - Missing required columns
   - Invalid date formats
   - Empty data rows

---

## 🔄 After Upload

Once data is uploaded successfully:
- ✅ New products are automatically added to products table
- ✅ Monthly stock summary is updated
- ✅ Marketing spend data is inserted
- ✅ Prediction model automatically retrains with new data
- ✅ Charts in "Monthly History" show the new month's data
- ✅ Stock recommendations update based on new trends

---

**Happy Testing! 🎉**
