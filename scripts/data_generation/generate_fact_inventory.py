import pandas as pd
import numpy as np
import random
from datetime import timedelta

# تنظیم seed برای بازتولیدپذیری
np.random.seed(42)
random.seed(42)

# ---------- خواندن داده‌ها ----------
dim_date = pd.read_csv("../data/dim_date.csv", encoding="utf-8-sig")
dim_product = pd.read_csv("../data/dim_product.csv", encoding="utf-8-sig")
fact_sales = pd.read_csv("../data/fact_sales.csv", encoding="utf-8-sig")

# تبدیل ستون تاریخ میلادی به datetime برای محاسبات هفته
dim_date["Date"] = pd.to_datetime(dim_date["Date"])

# فقط تا امروز (۱۴۰۵/۰۵/۲۲)
today = "1405/05/22"
dim_date = dim_date[dim_date["ShamsiDate"] <= today].copy()

# ---------- محاسبه فروش هفتگی هر محصول ----------
# ابتدا فروش روزانه هر محصول را از fact_sales به‌دست می‌آوریم
sales_daily = fact_sales.groupby(["DateKey", "ProductKey"]).agg(
    total_qty=("Quantity", "sum")
).reset_index()

# تبدیل DateKey به تاریخ میلادی برای گروه‌بندی هفتگی
sales_daily = sales_daily.merge(dim_date[["DateKey", "Date"]], on="DateKey", how="left")

# تعیین هفته‌ی شمسی (با استفاده از شماره هفته از ابتدای سال شمسی)
# برای سادگی، از شماره هفته میلادی استفاده می‌کنیم (چون تاریخ میلادی داریم)
sales_daily["Week"] = sales_daily["Date"].dt.isocalendar().week
sales_daily["Year"] = sales_daily["Date"].dt.isocalendar().year

# گروه‌بندی هفتگی
weekly_sales = sales_daily.groupby(["Year", "Week", "ProductKey"]).agg(
    weekly_qty=("total_qty", "sum")
).reset_index()

# ---------- تولید موجودی هفتگی ----------
# تعریف لیست تاریخ‌های ابتدای هر هفته (دوشنبه یا یکشنبه؟ ما از یکشنبه میلادی استفاده می‌کنیم)
# ابتدا یک ستون WeekStart اضافه می‌کنیم
weekly_sales["WeekStart"] = pd.to_datetime(weekly_sales["Year"].astype(str) + "-W" + weekly_sales["Week"].astype(str) + "-0", format="%Y-W%W-%w")
weekly_sales = weekly_sales.sort_values("WeekStart")

# برای هر محصول، یک سری زمانی هفتگی از اولین هفته تا آخرین هفته می‌سازیم
start_date = dim_date["Date"].min()
end_date = dim_date["Date"].max()
all_weeks = pd.date_range(start=start_date, end=end_date, freq="W-MON")  # هر دوشنبه

# لیست محصولات
products = dim_product["ProductKey"].tolist()

inventory_rows = []

for product_key in products:
    product_row = dim_product[dim_product["ProductKey"] == product_key].iloc[0]
    min_stock = product_row["MinStock"]
    lead_time_days = product_row["LeadTimeDays"]
    
    # محاسبه میانگین فروش هفتگی این محصول (اگر وجود دارد)
    product_weekly_sales = weekly_sales[weekly_sales["ProductKey"] == product_key]
    if len(product_weekly_sales) > 0:
        avg_weekly_sales = product_weekly_sales["weekly_qty"].mean()
    else:
        avg_weekly_sales = 5  # محصولات کم‌فروش هم مقدار کمی فروش دارند
    
    # تعیین موجودی اولیه: حداقل = min_stock + (چند برابر میانگین فروش هفتگی)
    initial_stock = max(min_stock * 2, int(avg_weekly_sales * 4) + min_stock)
    
    current_stock = initial_stock
    in_transit = 0  # سفارش در راه
    days_until_delivery = 0
    
    # حلقه روی هفته‌ها
    for week_start in all_weeks:
        # پیدا کردن فروش این هفته (ممکن است نداشته باشیم)
        week_end = week_start + timedelta(days=6)
        # تبدیل به مقایسه با WeekStart
        sales_this_week = product_weekly_sales[
            (product_weekly_sales["WeekStart"] == week_start)
        ]["weekly_qty"].sum() if not product_weekly_sales.empty else 0
        
        # کاهش موجودی با فروش این هفته
        current_stock -= sales_this_week
        
        # اگر سفارش در راه رسید
        if days_until_delivery > 0:
            days_until_delivery -= 7  # هر هفته ۷ روز می‌گذرد
            if days_until_delivery <= 0:
                current_stock += in_transit
                in_transit = 0
        
        # بررسی نیاز به سفارش
        if current_stock < min_stock:
            # مقدار سفارش = چند برابر میانگین فروش هفتگی + min_stock
            order_qty = int(avg_weekly_sales * 2) + min_stock
            in_transit = order_qty
            days_until_delivery = lead_time_days
            quantity_ordered = order_qty
        else:
            quantity_ordered = 0
        
        # کمی نویز تصادفی برای واقعی‌تر شدن (موجودی نهایی)
        current_stock = max(0, int(current_stock + random.uniform(-5, 5)))
        
        # ثبت رکورد این هفته
        # DateKey متناظر با این هفته (اولین روز هفته)
        # از dim_date بر اساس تاریخ میلادی
        date_row = dim_date[dim_date["Date"] == week_start]
        if len(date_row) > 0:
            date_key = date_row.iloc[0]["DateKey"]
        else:
            # اگر تاریخ دقیق نبود، نزدیک‌ترین دوشنبه
            continue
        
        inventory_rows.append({
            "DateKey": date_key,
            "ProductKey": product_key,
            "QuantityOnHand": current_stock,
            "QuantityOrdered": quantity_ordered
        })

# ---------- ساخت DataFrame و ذخیره ----------
df_inventory = pd.DataFrame(inventory_rows)
df_inventory.to_csv("../data/fact_inventory.csv", index=False, encoding="utf-8-sig")

print(f"تعداد رکوردهای موجودی: {len(df_inventory)}")
print(df_inventory.head())