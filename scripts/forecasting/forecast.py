import pandas as pd
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

# ---------- 1. خواندن داده‌های تمیز ----------
print("Reading clean data...")
fact_sales = pd.read_csv("../data/clean/fact_sales.csv", encoding="utf-8-sig")
dim_date = pd.read_csv("../data/clean/dim_date.csv", encoding="utf-8-sig")

# ---------- 2. ساخت سری زمانی فروش روزانه ----------
# ابتدا فروش روزانه را از fact_sales جمع می‌کنیم
daily_sales = fact_sales.groupby("DateKey")["LineAmount"].sum().reset_index()
daily_sales.columns = ["DateKey", "y"]

# اتصال به dim_date برای گرفتن تاریخ میلادی (ds)
daily_sales = daily_sales.merge(
    dim_date[["DateKey", "Date"]],
    on="DateKey",
    how="left"
)

# تبدیل Date به datetime
daily_sales["ds"] = pd.to_datetime(daily_sales["Date"])
daily_sales = daily_sales[["ds", "y"]].sort_values("ds")
print(f"Daily sales rows: {len(daily_sales)}")

# ---------- 3. آموزش مدل Prophet ----------
model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05,
    interval_width=0.95  # بازه اطمینان ۹۵٪
)
# اضافه کردن تعطیلات شمسی؟ فعلاً از تعطیلات پیش‌فرض Prophet استفاده نمی‌کنیم،
# ولی می‌توانیم جمعه‌ها را به‌صورت تعطیلات هفتگی اضافه کنیم.
# برای سادگی، همان فصلی هفتگی کافی است.

model.fit(daily_sales)
print("Model fitted.")

# ---------- 4. ساخت آینده ۹۰ روز ----------
future = model.make_future_dataframe(periods=90, freq='D')
print(f"Future dataframe length: {len(future)}")

# ---------- 5. پیش‌بینی ----------
forecast = model.predict(future)
print("Forecast generated.")

# ---------- 6. انتخاب فقط ۹۰ روز آینده (بعد از آخرین تاریخ در داده‌ها) ----------
last_date = daily_sales["ds"].max()
future_forecast = forecast[forecast["ds"] > last_date].copy()
print(f"Future forecast rows: {len(future_forecast)}")

# ---------- 7. اتصال به dim_date برای گرفتن DateKey ----------
# تبدیل ds به تاریخ میلادی (فقط قسمت تاریخ)
future_forecast["Date"] = future_forecast["ds"].dt.date
dim_date["Date"] = pd.to_datetime(dim_date["Date"]).dt.date

merged = future_forecast.merge(
    dim_date[["Date", "DateKey", "ShamsiDate"]],
    on="Date",
    how="left"
)

# انتخاب ستون‌های نهایی و ذخیره
output = merged[["DateKey", "ds", "yhat", "yhat_lower", "yhat_upper"]]
output.columns = ["DateKey", "Date", "Forecast", "LowerBound", "UpperBound"]
output.to_csv("../data/clean/forecast_results.csv", index=False, encoding="utf-8-sig")

print("Forecast saved to '../data/clean/forecast_results.csv'")
print(output.head())