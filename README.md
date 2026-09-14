# Retail & Wholesale Analytics

End-to-end retail & wholesale analytics case study covering sales, customers, inventory, forecasting, and market basket analysis.

> **Note:** This project uses a synthetic dataset generated with Python for portfolio and analytical demonstration purposes. No proprietary company data or personally identifiable information is used.

---

## Project Overview

This project demonstrates an end-to-end business analytics workflow for a retail and wholesale business.

The project combines data generation, data quality processes, analytical data modeling, business intelligence, time-series forecasting, and market basket analysis to transform transactional data into actionable business insights.

---

## Business Context

The business operates across retail and wholesale channels and manages:

* Customers and shops
* Product categories and suppliers
* Sales transactions
* Inventory
* Operational costs

The analytical objective is to provide management with a consolidated view of commercial performance, customer behavior, inventory conditions, future demand, and product purchasing relationships.

---

## Business Questions

The analysis addresses questions such as:

* How are sales performing over time?
* Which products and categories contribute most to revenue?
* Which customers and geographic areas generate the strongest performance?
* What inventory risks require attention?
* What does the 90-day sales forecast suggest about future demand?
* Which products are frequently purchased together?
* Where can analytical insights support better commercial and supply-chain decisions?

---

## Analytical Workflow

```text
Business Problem
      ↓
Synthetic Data Generation
      ↓
Data Quality & Cleaning
      ↓
Analytical Data Model
      ↓
Power BI Business Intelligence
      ↓
Forecasting
      ↓
Market Basket Analysis
      ↓
Business Insights
```

---

## Dataset

The project uses a synthetic retail and wholesale dataset generated with Python.

The analytical model includes:

* Date dimension
* Product dimension
* Customer dimension
* Sales fact
* Inventory fact
* Cost fact

Additional analytical outputs include:

* 90-day sales forecasting results
* Market basket association rules

Detailed field definitions are available in the [Data Dictionary](docs/data_dictionary.md).

---

## Technology Stack

* Python
* Pandas
* NumPy
* Power BI
* DAX
* Prophet
* mlxtend
* Git
* GitHub

---

## Project Structure

```text
retail-wholesale-analytics/
│
├── data/
│   ├── README.md
│   ├── dim_customer.csv
│   ├── dim_date.csv
│   ├── dim_product.csv
│   ├── fact_cost.csv
│   ├── fact_inventory.csv
│   └── fact_sales.csv
│
├── docs/
│   ├── business_insights.md
│   ├── data_dictionary.md
│   ├── data_model.md
│   └── methodology.md
│
├── outputs/
│   ├── association_rules/
│   │   └── association_rules.csv
│   └── forecast/
│       └── forecast_results.csv
│
├── scripts/
│   ├── data_generation/
│   ├── data_quality/
│   ├── forecasting/
│   └── market_basket/
│
├── .gitignore
└── requirements.txt
```

---

## Data Generation

The dataset is generated programmatically using Python to simulate a realistic retail and wholesale business environment.

The data generation pipeline creates:

* Calendar and Persian calendar attributes
* Product master data
* Customer master data
* Sales transactions
* Inventory records
* Business cost records

Fixed random seeds are used where applicable to improve reproducibility.

The synthetic nature of the dataset makes the project suitable for public portfolio use without exposing proprietary business information.

---

## Data Quality & Cleaning

The project includes a dedicated data-quality stage for preparing the generated data for analysis.

The pipeline includes:

* Data validation
* Cleaning and standardization
* Preparation of analytical datasets
* Generation of downstream analytical outputs

Relevant scripts are located in:

```text
scripts/data_quality/
```

---

## Data Model

The analytical layer follows a star-schema-oriented structure.

### Core Dimensions

* `dim_date`
* `dim_product`
* `dim_customer`

### Fact Tables

* `fact_sales`
* `fact_inventory`
* `fact_cost`

The model uses many-to-one relationships from fact tables to dimensions with single-direction filtering.

See the [Data Model](docs/data_model.md) for detailed relationship information.

---

## Power BI Dashboard

The Power BI report provides an interactive business intelligence layer covering:

* Executive Summary
* Sales Analysis
* Product Performance
* Customer & Geography
* Inventory & Supply Chain
* 90-Day Forecast
* Market Basket Analysis
* Q&A

### Dashboard Preview

*Power BI dashboard screenshots will be added here.*

---

## Sales & Business Performance

The Power BI analytical layer is designed to help management explore:

* Revenue performance over time
* Product and category contribution
* Customer performance
* Geographic distribution
* Sales trends
* Commercial performance indicators

The dashboard enables users to move from high-level business performance to more detailed product, customer, and geographic analysis.

---

## Inventory & Supply Chain Analysis

The project includes inventory analysis designed to support supply-chain decision making.

The analysis considers:

* Inventory levels
* Stock availability
* Product-level inventory conditions
* Quantity ordered
* Minimum stock thresholds
* Supplier lead times

This layer connects commercial demand with inventory and replenishment considerations.

---

## Forecasting

Sales forecasting is performed using **Prophet**.

The forecasting pipeline uses:

* Daily seasonality
* Weekly seasonality
* Yearly seasonality
* 95% prediction intervals
* 90-day forecast horizon

The forecasting model is intended as an analytical forecasting demonstration rather than a production demand-planning system.

Forecast results are available in:

```text
outputs/forecast/
```

Detailed methodology and assumptions are documented in [Methodology](docs/methodology.md).

---

## Market Basket Analysis

Product purchasing relationships are analyzed using the **Apriori algorithm**.

The workflow includes:

1. Transaction construction
2. Transaction encoding
3. Frequent itemset generation
4. Association rule generation
5. Rule evaluation

The generated rules are evaluated using:

* Support
* Confidence
* Lift

The resulting analytical output is available in:

```text
outputs/association_rules/
```

The analysis can help identify products that are frequently purchased together and may support cross-selling, bundling, and merchandising decisions.

---

## Business Insights

The final business insights will be documented after validating the analytical outputs and Power BI results.

The objective is to translate analytical findings into practical recommendations related to:

* Sales performance
* Product strategy
* Customer management
* Inventory planning
* Demand forecasting
* Cross-selling opportunities
* Supply-chain decisions

See:

[Business Insights](docs/business_insights.md)

---

## Limitations

This project is designed as an analytical portfolio case study rather than a production business system.

Key limitations include:

* The dataset is synthetic.
* Forecasting has not yet been evaluated through formal backtesting.
* Custom holiday regressors have not been incorporated into the forecasting model.
* Inventory data covers a selected subset of products.
* The forecasting model should therefore be interpreted as an analytical demonstration rather than an operational demand forecast.

---

## Future Improvements

Potential future enhancements include:

* Forecast backtesting and model evaluation
* Comparison with alternative forecasting models
* Advanced inventory optimization
* Customer segmentation
* Supplier performance analysis
* Automated data pipelines
* SQL-based analytical layer
* dbt-based transformation workflows
* Advanced predictive analytics
* Integration with real-world public datasets

---

## Reproducibility

The project is organized into separate analytical stages:

```text
scripts/
│
├── data_generation/
├── data_quality/
├── forecasting/
└── market_basket/
```

Install the required Python dependencies using:

```bash
pip install -r requirements.txt
```

The project uses fixed random seeds where applicable to improve reproducibility.

---

## Documentation

Additional project documentation:

* [Data Dictionary](docs/data_dictionary.md)
* [Data Model](docs/data_model.md)
* [Methodology](docs/methodology.md)
* [Business Insights](docs/business_insights.md)

---

## Author

**Arash Hemmati Berivanloo**

Data & Business Analytics
Supply Chain Analytics | EV & Lithium Battery Analytics
