import pandas as pd

sales = pd.read_csv("../data/fact_sales.csv", encoding="utf-8-sig")
products = pd.read_csv("../data/dim_product.csv", encoding="utf-8-sig")

print("=== fact_sales ===")
print("تعداد ردیف‌ها:", len(sales))
print("مجموع فروش:", sales["LineAmount"].sum())
print("میانگین LineAmount:", sales["LineAmount"].mean())
print("حداکثر LineAmount:", sales["LineAmount"].max())

print("\n=== dim_product ===")
print("حداقل UnitCost:", products["UnitCost"].min())
print("حداکثر UnitCost:", products["UnitCost"].max())
print("حداقل UnitPriceBase:", products["UnitPriceBase"].min())
print("حداکثر UnitPriceBase:", products["UnitPriceBase"].max())
print("میانگین UnitPriceBase:", products["UnitPriceBase"].mean())