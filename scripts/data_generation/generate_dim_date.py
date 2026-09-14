import pandas as pd
import jdatetime
from datetime import date, timedelta

# تعریف بازهٔ شمسی: از ۱ فروردین ۱۴۰۳ تا ۳۰ آبان ۱۴۰۵
start_j = jdatetime.date(1403, 1, 1)
end_j = jdatetime.date(1405, 8, 30)

# تبدیل به میلادی برای پیمایش روزانه
start_g = start_j.togregorian()
end_g = end_j.togregorian()

# لیستی که همهٔ روزها را نگه می‌دارد
rows = []

current = start_g
while current <= end_g:
    # تبدیل تاریخ میلادی به شمسی
    jdate = jdatetime.date.fromgregorian(date=current)

    # تعطیلات رسمی تقریبی (فقط مهم‌ها)
    official_holidays = [
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 13),   # فروردین
        (3, 14), (3, 15),                           # خرداد
        (11, 22),                                   # بهمن
        (12, 29)                                    # اسفند
    ]
    is_official = (jdate.month, jdate.day) in official_holidays

    # جمعه‌ها (weekday = 4) تعطیل‌اند
    is_friday = current.weekday() == 4

    # فصل شمسی: بهار ۱-۳، تابستان ۴-۶، پاییز ۷-۹، زمستان ۱۰-۱۲
    if jdate.month in (1, 2, 3):
        season = "بهار"
    elif jdate.month in (4, 5, 6):
        season = "تابستان"
    elif jdate.month in (7, 8, 9):
        season = "پاییز"
    else:
        season = "زمستان"

    # اضافه کردن ردیف
    rows.append({
        "DateKey": int(jdate.strftime("%Y%m%d")),      # مثل 14030522
        "Date": current,                               # تاریخ میلادی (برای Power BI)
        "ShamsiDate": jdate.strftime("%Y/%m/%d"),      # نمایش شمسی
        "ShamsiYear": jdate.year,
        "ShamsiMonth": jdate.month,
        "ShamsiMonthName": jdate.j_months_fa[jdate.month - 1],
        "ShamsiDay": jdate.day,
        "IsHoliday": is_official or is_friday,
        "Season": season
    })

    # برو به روز بعد
    current += timedelta(days=1)

# ساخت DataFrame و ذخیره
df_date = pd.DataFrame(rows)
df_date.to_csv("../data/dim_date.csv", index=False, encoding="utf-8-sig")

print("تعداد روزها:", len(df_date))
print(df_date.head())