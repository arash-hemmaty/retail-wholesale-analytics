import pandas as pd
import numpy as np
import random

# تنظیم seed برای بازتولیدپذیری
np.random.seed(42)
random.seed(42)

# ---------- خواندن تقویم ----------
dim_date = pd.read_csv("../data/dim_date.csv", encoding="utf-8-sig")

# فقط تا امروز (۱۴۰۵/۰۵/۲۲)
today = "1405/05/22"
dim_date = dim_date[dim_date["ShamsiDate"] <= today].copy()

# ---------- استخراج ماه‌های یکتا (سال و ماه شمسی) ----------
months = dim_date[["ShamsiYear", "ShamsiMonth"]].drop_duplicates().sort_values(["ShamsiYear", "ShamsiMonth"])

# برای هر ماه، اولین روز ماه را به‌عنوان نماینده DateKey می‌گیریم
month_date_keys = []
for _, month_row in months.iterrows():
    year = month_row["ShamsiYear"]
    month = month_row["ShamsiMonth"]
    # پیدا کردن ردیف با ShamsiDay == 1
    first_day_row = dim_date[(dim_date["ShamsiYear"] == year) & (dim_date["ShamsiMonth"] == month) & (dim_date["ShamsiDay"] == 1)]
    if len(first_day_row) > 0:
        date_key = first_day_row.iloc[0]["DateKey"]
    else:
        # اگر روز ۱ نبود، اولین روز موجود در آن ماه
        first_day_row = dim_date[(dim_date["ShamsiYear"] == year) & (dim_date["ShamsiMonth"] == month)]
        date_key = first_day_row.iloc[0]["DateKey"]
    month_date_keys.append((year, month, date_key))

# ---------- تعریف انواع هزینه و مقادیر پایه ----------
cost_types = {
    "اجاره": 150_000_000,           # ماهانه ۱۵۰ میلیون تومان
    "حقوق و دستمزد": 200_000_000,    # ماهانه ۲۰۰ میلیون تومان
    "بازاریابی و تبلیغات": 30_000_000,
    "قبوض (آب، برق، گاز، تلفن)": 15_000_000,
    "استهلاک و تعمیرات": 20_000_000,
    "حمل و نقل": 25_000_000,
    "سایر": 10_000_000
}

# ضرایب فصلی برای بازاریابی (در ماه‌های منتهی به عید و تابستان بالاتر)
marketing_season_factor = {
    1: 1.5,   # فروردین (بعد از عید)
    2: 1.2,
    3: 1.0,
    4: 1.3,   # تابستان
    5: 1.5,
    6: 1.4,
    7: 1.1,
    8: 1.0,
    9: 1.0,
    10: 1.2,
    11: 1.3,
    12: 2.0   # اسفند (قبل از عید)
}

rows = []
cost_id = 1

for year, month, date_key in month_date_keys:
    for cost_type, base_amount in cost_types.items():
        # اعمال تغییرات تصادفی برای واقعی‌تر شدن
        if cost_type == "اجاره":
            # اجاره معمولاً ثابت است
            amount = base_amount
        elif cost_type == "حقوق و دستمزد":
            # حقوق ممکن است سالانه کمی افزایش یابد
            year_factor = 1.0 + (year - 1403) * 0.1  # ۱۰٪ افزایش سالانه
            amount = int(base_amount * year_factor * random.uniform(0.9, 1.1))
        elif cost_type == "بازاریابی و تبلیغات":
            seasonal = marketing_season_factor.get(month, 1.0)
            amount = int(base_amount * seasonal * random.uniform(0.8, 1.2))
        else:
            # سایر هزینه‌ها نوسان معمولی دارند
            amount = int(base_amount * random.uniform(0.85, 1.15))
        
        # گرد کردن به نزدیک‌ترین هزار تومان
        amount = (amount // 1000) * 1000
        
        rows.append({
            "CostID": cost_id,
            "DateKey": date_key,
            "CostType": cost_type,
            "Amount": amount,
            "Description": f"{cost_type} - {year}/{month:02d}"
        })
        cost_id += 1

# ---------- ساخت DataFrame و ذخیره ----------
df_cost = pd.DataFrame(rows)
df_cost.to_csv("../data/fact_cost.csv", index=False, encoding="utf-8-sig")

print(f"تعداد رکوردهای هزینه: {len(df_cost)}")
print(df_cost.head())