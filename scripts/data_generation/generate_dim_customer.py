import pandas as pd
import numpy as np
import random

# تنظیم seed برای بازتولیدپذیری
np.random.seed(42)
random.seed(42)

# ---------- خواندن تقویم برای گرفتن تاریخ‌های شمسی معتبر ----------
dates_df = pd.read_csv("../data/dim_date.csv", encoding="utf-8-sig")
valid_dates = dates_df["ShamsiDate"].tolist()

# ---------- دیکشنری شهرها و استان‌ها (تهران + مراکز استان‌ها) ----------
cities_provinces = {
    "تهران": "تهران",
    "مشهد": "خراسان رضوی",
    "اصفهان": "اصفهان",
    "کرج": "البرز",
    "شیراز": "فارس",
    "تبریز": "آذربایجان شرقی",
    "قم": "قم",
    "اهواز": "خوزستان",
    "رشت": "گیلان",
    "کرمان": "کرمان",
    "ارومیه": "آذربایجان غربی",
    "یزد": "یزد",
    "زاهدان": "سیستان و بلوچستان",
    "همدان": "همدان",
    "کرمانشاه": "کرمانشاه",
    "بندرعباس": "هرمزگان",
    "اراک": "مرکزی",
    "ساری": "مازندران",
    "گرگان": "گلستان",
    "بوشهر": "بوشهر",
    "قزوین": "قزوین",
    "خرم‌آباد": "لرستان",
    "سنندج": "کردستان",
    "ایلام": "ایلام",
    "بیرجند": "خراسان جنوبی",
    "بجنورد": "خراسان شمالی",
    "اردبیل": "اردبیل",
    "زنجان": "زنجان",
    "شهرکرد": "چهارمحال و بختیاری",
    "سمنان": "سمنان",
    "یاسوج": "کهگیلویه و بویراحمد",
    "قشم": "هرمزگان",
    "کیش": "هرمزگان"
}

# ---------- انواع مشتری و لیست نام‌های ساختگی ----------
customer_types = ["عمده‌فروش", "خرده‌فروش", "خاص"]

shop_names_prefix = ["بازار", "فروشگاه", "مرکز", "پخش", "تویز", "بچه‌ها", "شادی", "فانتزی", "کلبه", "دنیای"]
shop_names_suffix = ["اسباب‌بازی", "کودک", "تویز", "بازی", "سرگرمی", "پخش اسباب‌بازی"]

owners_first_names = ["علی", "محمد", "حسین", "رضا", "مهدی", "امیر", "سعید", "مجید", "حمید", "ناصر", "اکبر", "فرشاد", "مصطفی", "جواد", "بهرام"]
owners_last_names = ["احمدی", "محمدی", "رضایی", "حسینی", "کریمی", "موسوی", "جعفری", "صادقی", "نوری", "قاسمی", "هاشمی", "عباسی", "میرزایی", "رحیمی", "شریفی"]

# ---------- تولید ۶۰۰ مشتری ----------
rows = []
for i in range(600):
    city = random.choice(list(cities_provinces.keys()))
    province = cities_provinces[city]
    shop_name = f"{random.choice(shop_names_prefix)} {random.choice(shop_names_suffix)} {city}"
    owner = f"{random.choice(owners_first_names)} {random.choice(owners_last_names)}"
    join_date = random.choice(valid_dates[:700])  # از حدود ۲ سال اول (تاریخ‌های معتبر)
    customer_type = random.choice(customer_types)
    credit_limit = int(np.random.uniform(10_000_000, 500_000_000))  # اعتبار بین ۱۰ میلیون تا ۵۰۰ میلیون تومان
    
    rows.append({
        "CustomerKey": i + 1,
        "CustomerCode": f"CUST-{i+1:04d}",
        "ShopName": shop_name,
        "OwnerName": owner,
        "City": city,
        "Province": province,
        "CustomerType": customer_type,
        "JoinDate": join_date,
        "CreditLimit": credit_limit
    })

# ---------- ساخت DataFrame و ذخیره ----------
df_customer = pd.DataFrame(rows)
df_customer.to_csv("../data/dim_customer.csv", index=False, encoding="utf-8-sig")

print("تعداد مشتریان:", len(df_customer))
print(df_customer.head())