from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"

SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SALES_ROWS = 5000
MAX_PRODUCTS = 50
MAX_CUSTOMERS = 100


# ---------------------------------------------------------
# Load source data
# ---------------------------------------------------------

date = pd.read_csv(DATA_DIR / "dim_date.csv")
product = pd.read_csv(DATA_DIR / "dim_product.csv")
customer = pd.read_csv(DATA_DIR / "dim_customer.csv")
sales = pd.read_csv(DATA_DIR / "fact_sales.csv")
inventory = pd.read_csv(DATA_DIR / "fact_inventory.csv")
cost = pd.read_csv(DATA_DIR / "fact_cost.csv")


# ---------------------------------------------------------
# Select a representative sales sample
# ---------------------------------------------------------

sales_sample = (
    sales
    .sort_values("DateKey")
    .head(SALES_ROWS)
    .copy()
)


# ---------------------------------------------------------
# Preserve referential integrity
# ---------------------------------------------------------

product_keys = (
    sales_sample["ProductKey"]
    .drop_duplicates()
    .head(MAX_PRODUCTS)
    .tolist()
)

customer_keys = (
    sales_sample["CustomerKey"]
    .drop_duplicates()
    .head(MAX_CUSTOMERS)
    .tolist()
)

sales_sample = sales_sample[
    sales_sample["ProductKey"].isin(product_keys)
    & sales_sample["CustomerKey"].isin(customer_keys)
].copy()


# ---------------------------------------------------------
# Related dimensions
# ---------------------------------------------------------

product_sample = product[
    product["ProductKey"].isin(
        sales_sample["ProductKey"].unique()
    )
].copy()

customer_sample = customer[
    customer["CustomerKey"].isin(
        sales_sample["CustomerKey"].unique()
    )
].copy()

date_keys = sales_sample["DateKey"].unique()

date_sample = date[
    date["DateKey"].isin(date_keys)
].copy()


# ---------------------------------------------------------
# Related inventory data
# ---------------------------------------------------------

inventory_sample = inventory[
    inventory["ProductKey"].isin(
        sales_sample["ProductKey"].unique()
    )
    & inventory["DateKey"].isin(date_keys)
].copy()


# ---------------------------------------------------------
# Related cost data
# ---------------------------------------------------------

cost_sample = cost[
    cost["DateKey"].isin(date_keys)
].copy()


# ---------------------------------------------------------
# Save sample datasets
# ---------------------------------------------------------

datasets = {
    "dim_date.csv": date_sample,
    "dim_product.csv": product_sample,
    "dim_customer.csv": customer_sample,
    "fact_sales.csv": sales_sample,
    "fact_inventory.csv": inventory_sample,
    "fact_cost.csv": cost_sample,
}


for filename, dataframe in datasets.items():
    output_path = SAMPLE_DIR / filename
    dataframe.to_csv(output_path, index=False)
    print(f"Created: {output_path.relative_to(ROOT)}")
    print(f"Rows: {len(dataframe):,}")


print("\nSample dataset creation completed successfully.")