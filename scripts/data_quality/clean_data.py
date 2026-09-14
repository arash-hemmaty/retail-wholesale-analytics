import pandas as pd
import numpy as np
import os

# ---------- 1. خواندن داده‌های خام ----------
print("Reading raw data...")
dim_date = pd.read_csv("../data/dim_date.csv", encoding="utf-8-sig")
dim_product = pd.read_csv("../data/dim_product.csv", encoding="utf-8-sig")
dim_customer = pd.read_csv("../data/dim_customer.csv", encoding="utf-8-sig")
fact_sales = pd.read_csv("../data/fact_sales.csv", encoding="utf-8-sig")
fact_inventory_raw = pd.read_csv("../data/fact_inventory.csv", encoding="utf-8-sig")
fact_cost = pd.read_csv("../data/fact_cost.csv", encoding="utf-8-sig")

# ---------- 2. تابع گزارش کیفیت ----------
def audit(df, name):
    print(f"\n=== {name} ===")
    print("Shape:", df.shape)
    print("Nulls per column:")
    print(df.isnull().sum())
    print("Duplicated rows:", df.duplicated().sum())
    print("Data types:")
    print(df.dtypes)
    print("First 2 rows:")
    print(df.head(2))

# گزارش اولیه همه جداول
audit(dim_date, "dim_date")
audit(dim_product, "dim_product")
audit(dim_customer, "dim_customer")
audit(fact_sales, "fact_sales")
audit(fact_inventory_raw, "fact_inventory_raw")
audit(fact_cost, "fact_cost")

# ---------- 3. پاکسازی جداول Dimension ----------

# dim_date
dim_date['Date'] = pd.to_datetime(dim_date['Date'])
dim_date['DateKey'] = dim_date['DateKey'].astype(int)
dim_date = dim_date.drop_duplicates(subset='DateKey')

# dim_product
dim_product = dim_product.drop_duplicates(subset='ProductKey')
# حذف محصولات با قیمت غیرمنطقی
dim_product = dim_product[(dim_product['UnitCost'] > 0) & (dim_product['UnitPriceBase'] > 0)]

# dim_customer
dim_customer = dim_customer.drop_duplicates(subset='CustomerKey')

# ---------- 4. پاکسازی Fact Sales ----------
# تبدیل کلیدها به عدد صحیح
for col in ['DateKey', 'CustomerKey', 'ProductKey', 'Quantity', 'UnitPrice', 'DiscountAmount', 'LineAmount']:
    fact_sales[col] = pd.to_numeric(fact_sales[col], errors='coerce')

# حذف ردیف‌های تکراری
fact_sales = fact_sales.drop_duplicates()

# حذف ردیف‌هایی که کلید خارجی نامعتبر دارند
fact_sales = fact_sales[fact_sales['ProductKey'].isin(dim_product['ProductKey'])]
fact_sales = fact_sales[fact_sales['CustomerKey'].isin(dim_customer['CustomerKey'])]
fact_sales = fact_sales[fact_sales['DateKey'].isin(dim_date['DateKey'])]

# حذف مقادیر غیرمنطقی
fact_sales = fact_sales[
    (fact_sales['Quantity'] > 0) &
    (fact_sales['UnitPrice'] >= 0) &
    (fact_sales['DiscountAmount'] >= 0) &
    (fact_sales['LineAmount'] >= 0)
]

# ---------- 5. پاکسازی Fact Cost ----------
fact_cost['DateKey'] = pd.to_numeric(fact_cost['DateKey'], errors='coerce')
fact_cost['Amount'] = pd.to_numeric(fact_cost['Amount'], errors='coerce')
fact_cost = fact_cost.drop_duplicates()
fact_cost = fact_cost[fact_cost['DateKey'].isin(dim_date['DateKey'])]
fact_cost = fact_cost[fact_cost['Amount'] > 0]

# ---------- 6. کاهش حجم Fact Inventory و تمیز کردن ----------
# هدف: رساندن تعداد ردیف‌ها به زیر ۱۰,۰۰۰
# واقعی‌سازی: فقط ۳۰۰ محصول پرفروش (بر اساس تعداد فروش) را ردیابی می‌کنیم و موجودی را ماهانه می‌کنیم.

# محاسبه فروش کل هر محصول
product_sales_qty = fact_sales.groupby('ProductKey')['Quantity'].sum()
top_products = product_sales_qty.nlargest(300).index

# فقط محصولات منتخب
inv_filtered = fact_inventory_raw[fact_inventory_raw['ProductKey'].isin(top_products)].copy()

# تبدیل DateKey به ماه شمسی
inv_filtered = inv_filtered.merge(
    dim_date[['DateKey', 'ShamsiYear', 'ShamsiMonth']],
    on='DateKey',
    how='left'
)

# تجمیع ماهانه: آخرین موجودی ماه و مجموع سفارش‌های ماه
monthly_inv = inv_filtered.groupby(['ShamsiYear', 'ShamsiMonth', 'ProductKey']).agg(
    QuantityOnHand=('QuantityOnHand', 'last'),
    QuantityOrdered=('QuantityOrdered', 'sum')
).reset_index()

# گرفتن DateKey اولین روز هر ماه برای اتصال به تقویم
first_days = dim_date[dim_date['ShamsiDay'] == 1][['ShamsiYear', 'ShamsiMonth', 'DateKey']].drop_duplicates()
monthly_inv = monthly_inv.merge(first_days, on=['ShamsiYear', 'ShamsiMonth'], how='left')

# انتخاب ستون‌های نهایی
monthly_inv = monthly_inv[['DateKey', 'ProductKey', 'QuantityOnHand', 'QuantityOrdered']]
monthly_inv = monthly_inv.dropna(subset=['DateKey'])
monthly_inv['DateKey'] = monthly_inv['DateKey'].astype(int)

# ---------- 7. ذخیره فایل‌های تمیز ----------
os.makedirs("../data/clean", exist_ok=True)

dim_date.to_csv("../data/clean/dim_date.csv", index=False, encoding="utf-8-sig")
dim_product.to_csv("../data/clean/dim_product.csv", index=False, encoding="utf-8-sig")
dim_customer.to_csv("../data/clean/dim_customer.csv", index=False, encoding="utf-8-sig")
fact_sales.to_csv("../data/clean/fact_sales.csv", index=False, encoding="utf-8-sig")
fact_cost.to_csv("../data/clean/fact_cost.csv", index=False, encoding="utf-8-sig")
monthly_inv.to_csv("../data/clean/fact_inventory.csv", index=False, encoding="utf-8-sig")

# ---------- 8. گزارش نهایی ----------
print("\n=== CLEANING COMPLETE ===")
print("dim_date rows:", len(dim_date))
print("dim_product rows:", len(dim_product))
print("dim_customer rows:", len(dim_customer))
print("fact_sales rows:", len(fact_sales))
print("fact_cost rows:", len(fact_cost))
print("fact_inventory rows (cleaned, under 10k expected):", len(monthly_inv))