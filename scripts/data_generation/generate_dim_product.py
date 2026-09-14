import pandas as pd
import numpy as np
import random

# تنظیم seed برای تولید قابل تکرار
np.random.seed(42)
random.seed(42)

# ---------- تعریف دسته‌بندی‌ها، نام‌ها، رنگ‌ها و ... ----------
categories = {
    "عروسک": {
        "subcats": ["پارچه‌ای", "پلاستیکی", "فیگور", "پولیشی"],
        "names": ["عروسک خرسی", "عروسک باربی", "عروسک سخنگو", "عروسک پولیشی", "عروسک بامزی"]
    },
    "لگو و ساختنی": {
        "subcats": ["لگو", "بلوک ساختمانی", "پازل سه‌بعدی", "ماکت"],
        "names": ["لگو پلیس", "لگو آتش‌نشانی", "بلوک‌های خانه", "پازل سه‌بعدی برج", "لگو ماشین"]
    },
    "ماشین و رادیویی": {
        "subcats": ["ماشین کنترلی", "ماشین ساده", "هواپیما", "قایق"],
        "names": ["ماشین کنترلی شارژی", "ماشین فلزی", "هواپیمای کنترلی", "قایق اسباب‌بازی", "ماشین سرعتی"]
    },
    "فکری و آموزشی": {
        "subcats": ["پازل", "بازی فکری", "وسایل آموزشی", "کتاب داستان"],
        "names": ["پازل ۱۰۰ تکه", "بازی فکری شطرنج", "چرتکه آموزشی", "کتاب قصه‌های کهن", "پازل نقشه ایران"]
    },
    "بازی در فضای باز": {
        "subcats": ["توپ", "دوچرخه", "اسکوتر", "استخر بادی"],
        "names": ["توپ فوتبال", "دوچرخه کودک", "اسکوتر", "استخر بادی", "توپ بسکتبال"]
    },
    "اکشن فیگور": {
        "subcats": ["شخصیت کارتونی", "ابرقهرمان", "سرباز", "ربات"],
        "names": ["فیگور مرد عنکبوتی", "فیگور بتمن", "سرباز اسباب‌بازی", "ربات جنگجو", "فیگور شرک"]
    },
    "نوزاد و خردسال": {
        "subcats": ["جغجغه", "عروسک پارچه‌ای", "موزیکال", "پازل چوبی"],
        "names": ["جغجغه", "عروسک پارچه‌ای", "موبایل موزیکال", "پازل چوبی", "دندانگیر"]
    },
    "مهمانی و بادکنک": {
        "subcats": ["بادکنک", "کلاه تولد", "فشفشه", "ظروف یکبارمصرف"],
        "names": ["بادکنک رنگی", "کلاه جشن تولد", "فشفشه", "ظروف مهمانی", "کاغذ رنگی"]
    }
}

colors = ["قرمز", "آبی", "سبز", "زرد", "سفید", "مشکی", "صورتی", "بنفش", "نارنجی", "چندرنگ"]
sizes = ["کوچک", "متوسط", "بزرگ", "خانواده"]

brands = ["تویز", "کیدزلند", "فانتزی", "پلی‌تویز", "آسمان", "شادی", "زرافه", "پاندورا", "دنیای اسباب‌بازی", "پیکولو"]

suppliers = [
    {"SupplierID": 1, "SupplierName": "اسباب‌بازی ایران"},
    {"SupplierID": 2, "SupplierName": "تویز لند"},
    {"SupplierID": 3, "SupplierName": "بازی و شادی"},
    {"SupplierID": 4, "SupplierName": "کیان تویز"},
    {"SupplierID": 5, "SupplierName": "پارس اسباب‌بازی"},
    {"SupplierID": 6, "SupplierName": "نوین تویز"},
    {"SupplierID": 7, "SupplierName": "آریا اسباب‌بازی"},
    {"SupplierID": 8, "SupplierName": "ماهان تویز"},
    {"SupplierID": 9, "SupplierName": "پویا تویز"},
    {"SupplierID": 10, "SupplierName": "دنیای شادی"}
]

# ---------- تولید ۲۵۰۰ محصول ----------
rows = []
for i in range(2500):
    # انتخاب دسته‌بندی و زیردسته
    category = random.choice(list(categories.keys()))
    subcat = random.choice(categories[category]["subcats"])
    base_name = random.choice(categories[category]["names"])
    
    # انتخاب رنگ و اندازه
    color = random.choice(colors)
    size = random.choice(sizes)
    product_name = f"{base_name} {color} {size}"
    
    # برند و تأمین‌کننده
    brand = random.choice(brands)
    supplier = random.choice(suppliers)
    
    # قیمت‌ها: خرید و فروش (تومان)
    unit_cost = int(np.random.uniform(30000, 1000000))   # قیمت خرید واقعی‌تر
    markup = round(np.random.uniform(1.4, 2.0), 2)       # ضریب سود منطقی‌تر
    unit_price_base = int(unit_cost * markup)
    
    # حداقل موجودی و زمان تأمین
    min_stock = int(np.random.randint(5, 50))
    lead_time_days = int(np.random.randint(3, 30))
    
    rows.append({
        "ProductKey": i + 1,
        "ProductCode": f"TOY-{i+1:04d}",
        "ProductName": product_name,
        "Category": category,
        "Subcategory": subcat,
        "Color": color,
        "Size": size,
        "Brand": brand,
        "UnitCost": unit_cost,
        "UnitPriceBase": unit_price_base,
        "SupplierID": supplier["SupplierID"],
        "SupplierName": supplier["SupplierName"],
        "MinStock": min_stock,
        "LeadTimeDays": lead_time_days
    })

# ساخت DataFrame و ذخیره
df_product = pd.DataFrame(rows)
df_product.to_csv("../data/dim_product.csv", index=False, encoding="utf-8-sig")

print("تعداد محصولات:", len(df_product))
print(df_product.head())