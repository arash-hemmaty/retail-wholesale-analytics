# Methodology

This document describes the analytical methodology used throughout the Retail & Wholesale Analytics case study.

The project is designed as an end-to-end portfolio analytics workflow, starting from synthetic data generation and ending with business intelligence, forecasting, and market basket analysis.

---

## 1. Synthetic Data Generation

The project uses synthetic data generated programmatically with Python.

The objective was to create a realistic analytical environment representing a retail and wholesale business while avoiding the use of proprietary or personally identifiable information.

The generated dataset includes:

* Calendar and Persian calendar attributes
* Product master data
* Customer master data
* Sales transactions
* Inventory records
* Operational cost records

Random seeds are used where applicable to improve reproducibility.

The data generation scripts are located in:

```text
scripts/data_generation/
```

---

## 2. Data Quality & Cleaning

Generated datasets are processed through a dedicated data-quality stage before being used for downstream analysis.

The data-quality workflow focuses on:

* Structural validation
* Data type consistency
* Missing-value handling
* Standardization
* Preparation of analytical datasets
* Validation of relationships between entities

The relevant scripts are located in:

```text
scripts/data_quality/
```

The cleaned analytical datasets are stored locally under:

```text
data/clean/
```

These generated intermediate datasets are excluded from the public repository.

---

## 3. Analytical Data Model

The project follows a star-schema-oriented analytical model.

### Dimension Tables

* `dim_date`
* `dim_product`
* `dim_customer`

### Fact Tables

* `fact_sales`
* `fact_inventory`
* `fact_cost`

The main relationships are many-to-one from fact tables to dimension tables with single-direction filtering.

This structure supports consistent filtering and aggregation across the Power BI analytical layer.

Detailed relationships are documented in:

[Data Model](data_model.md)

---

## 4. Power BI Business Intelligence

Power BI is used as the primary business intelligence and visualization layer.

The report is structured into several analytical perspectives:

* Executive Summary
* Sales Analysis
* Product Performance
* Customer & Geography
* Inventory & Supply Chain
* 90-Day Forecast
* Market Basket Analysis
* Q&A

The analytical layer uses DAX measures for business calculations and KPI development.

The dashboard is designed to support both high-level management review and deeper analytical exploration.

---

## 5. Sales Analysis

Sales analysis focuses on understanding commercial performance across multiple dimensions.

Key analytical dimensions include:

* Time
* Product
* Category
* Customer
* Geography

The analysis is intended to identify:

* Sales trends
* High-performing products
* Customer contribution
* Category performance
* Geographic patterns

The Power BI model allows users to move from aggregated KPIs to detailed business segments through interactive filtering.

---

## 6. Inventory & Supply Chain Analysis

Inventory analysis connects product demand with inventory availability and replenishment considerations.

The analytical layer includes:

* Quantity on hand
* Quantity ordered
* Minimum stock thresholds
* Supplier lead times
* Product-level inventory conditions

Inventory data covers a selected subset of top-selling products rather than the complete product catalog.

Therefore, inventory-related conclusions should be interpreted within the scope of the available inventory dataset.

---

## 7. Sales Forecasting

Sales forecasting is performed using Facebook Prophet.

The forecasting workflow aggregates historical sales into a daily time series and uses Prophet to generate future demand estimates.

The model configuration includes:

```python
Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05,
    interval_width=0.95
)
```

A 90-day forecasting horizon is generated.

The forecast includes:

* Point forecast
* Lower prediction bound
* Upper prediction bound

The prediction interval is set to 95%.

### Important Limitations

The current forecasting implementation is intended as an analytical demonstration.

Formal time-series backtesting and model comparison have not yet been implemented.

The current model also does not use custom holiday regressors or external explanatory variables.

Therefore, forecast results should not be interpreted as a validated production demand-planning model.

Forecast outputs are stored in:

```text
outputs/forecast/
```

---

## 8. Market Basket Analysis

Market basket analysis is performed using the Apriori algorithm through the `mlxtend` library.

The analytical process consists of:

1. Grouping products by invoice
2. Converting transactions into a binary transaction matrix
3. Generating frequent itemsets
4. Generating association rules
5. Evaluating rules using support, confidence, and lift

The current configuration uses:

```text
Minimum Support: 0.02
Minimum Confidence: 0.40
```

Generated rules are sorted by lift to highlight potentially stronger product associations.

The main evaluation metrics are:

### Support

Measures how frequently an itemset appears across transactions.

### Confidence

Measures how frequently the consequent appears when the antecedent is present.

### Lift

Measures the strength of the association relative to the expected frequency of the consequent.

Rules with higher lift may provide useful signals for:

* Cross-selling
* Product bundling
* Merchandising
* Recommendation strategies

The resulting analytical output is stored in:

```text
outputs/association_rules/
```

---

## 9. Reproducibility

The project is organized into independent analytical stages:

```text
Data Generation
      ↓
Data Quality
      ↓
Analytical Data Model
      ↓
Power BI
      ↓
Forecasting
      ↓
Market Basket Analysis
```

Python dependencies are defined in:

```text
requirements.txt
```

Random seeds are used where applicable to improve reproducibility of the synthetic data generation process.

---

## 10. Analytical Limitations

Several limitations should be considered when interpreting the results.

### Synthetic Dataset

The dataset is artificially generated and does not represent an actual company's operational data.

### Forecast Validation

The forecasting model has not yet undergone formal backtesting or comparison against alternative forecasting approaches.

### Inventory Coverage

Inventory data represents a selected subset of top-selling products rather than the full product catalog.

### External Variables

The forecasting model does not currently incorporate external explanatory variables such as promotions, pricing changes, macroeconomic conditions, or custom holiday effects.

### Business Generalization

Insights generated from the synthetic environment should be interpreted as analytical examples rather than direct recommendations for a real organization.

---

## 11. Future Analytical Development

Potential extensions include:

* Forecast backtesting
* Forecast model comparison
* Customer segmentation
* Advanced inventory optimization
* Supplier performance analysis
* Promotion and pricing analysis
* SQL-based analytical modeling
* dbt transformation workflows
* Predictive analytics
* Integration with public real-world datasets

These extensions can progressively transform the project from a portfolio case study into a more advanced analytics engineering and business analytics demonstration.
