import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# ---------- 1. خواندن داده‌های تمیز ----------
print("Reading clean data...")
fact_sales = pd.read_csv("../data/clean/fact_sales.csv", encoding="utf-8-sig")
dim_product = pd.read_csv("../data/clean/dim_product.csv", encoding="utf-8-sig")

# ---------- 2. ساختن لیست تراکنش‌ها (هر فاکتور یک سبد) ----------
print("Building transactions...")
transactions = fact_sales.groupby("InvoiceID")["ProductKey"].apply(list).tolist()
print(f"Number of transactions: {len(transactions)}")

# ---------- 3. تبدیل لیست تراکنش‌ها به ماتریس باینری ----------
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
basket = pd.DataFrame(te_ary, columns=te.columns_)
print(f"Basket matrix shape: {basket.shape}")

# ---------- 4. استخراج آیتم‌های پرتکرار با الگوریتم Apriori ----------
# حداقل پشتیبانی: حداقل 2% فاکتورها باید شامل آن آیتم/آیتم‌ها باشند
min_support = 0.02
frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
print(f"Frequent itemsets found: {len(frequent_itemsets)}")

# ---------- 5. تولید قوانین انجمنی ----------
# معیار اطمینان حداقل: 40% از فاکتورهای حاوی A باید B را هم داشته باشند
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)
print(f"Rules generated: {len(rules)}")

# ---------- 6. مرتب‌سازی و انتخاب قوانین قوی ----------
# بر اساس Lift (بالاتر بهتر) مرتب می‌کنیم
rules = rules.sort_values("lift", ascending=False)

# ---------- 7. تبدیل کد محصولات به نام محصولات ----------
# ابتدا برای هر ProductKey نام فارسی می‌سازیم
product_names = dict(zip(dim_product["ProductKey"], dim_product["ProductName"]))

def map_products(frozenset_items):
    names = [product_names.get(item, str(item)) for item in frozenset_items]
    return ", ".join(names)

rules["antecedents_name"] = rules["antecedents"].apply(map_products)
rules["consequents_name"] = rules["consequents"].apply(map_products)

# ---------- 8. انتخاب ستون‌های نهایی و ذخیره ----------
final_rules = rules[[
    "antecedents_name", "consequents_name",
    "support", "confidence", "lift"
]].copy()
final_rules.columns = ["Antecedent", "Consequent", "Support", "Confidence", "Lift"]
final_rules.to_csv("../data/clean/association_rules.csv", index=False, encoding="utf-8-sig")

print(f"\nTop 5 rules:")
print(final_rules.head())
print(f"\nSaved to '../data/clean/association_rules.csv'")