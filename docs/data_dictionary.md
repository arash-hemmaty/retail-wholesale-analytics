\# Data Dictionary



\## dim\_date



| Column | Description |

|---|---|

| DateKey | Integer date key used for relationships |

| Date | Gregorian calendar date |

| ShamsiDate | Persian calendar date |

| ShamsiYear | Persian calendar year |

| ShamsiMonth | Persian calendar month number |

| ShamsiMonthName | Persian calendar month name |

| ShamsiDay | Persian calendar day |

| IsHoliday | Indicates official holiday or Friday |

| Season | Persian seasonal classification |



\## dim\_product



| Column | Description |

|---|---|

| ProductKey | Unique product identifier |

| ProductCode | Product business code |

| ProductName | Product name |

| Category | Main product category |

| Subcategory | Product subcategory |

| Color | Product color |

| Size | Product size |

| Brand | Product brand |

| UnitCost | Base unit cost |

| UnitPriceBase | Base unit selling price |

| SupplierID | Supplier identifier |

| SupplierName | Supplier name |

| MinStock | Minimum stock threshold |

| LeadTimeDays | Supplier lead time in days |



\## dim\_customer



| Column | Description |

|---|---|

| CustomerKey | Unique customer identifier |

| CustomerCode | Customer business code |

| ShopName | Customer/shop name |

| OwnerName | Customer owner name |

| City | Customer city |

| Province | Customer province |

| CustomerType | Wholesaler, retailer, or special |

| JoinDate | Customer join date in Persian calendar |

| CreditLimit | Customer credit limit |



\## fact\_sales



| Column | Description |

|---|---|

| InvoiceID | Sales invoice identifier |

| DateKey | Foreign key to dim\_date |

| CustomerKey | Foreign key to dim\_customer |

| ProductKey | Foreign key to dim\_product |

| Quantity | Quantity sold |

| UnitPrice | Actual unit selling price |

| DiscountAmount | Discount amount |

| LineAmount | Net sales amount |



\## fact\_inventory



| Column | Description |

|---|---|

| DateKey | Monthly date key |

| ProductKey | Foreign key to dim\_product |

| QuantityOnHand | Inventory quantity available |

| QuantityOrdered | Quantity ordered |



\## fact\_cost



| Column | Description |

|---|---|

| CostID | Cost record identifier |

| DateKey | Monthly date key |

| CostType | Type of business cost |

| Amount | Cost amount |

| Description | Cost description |



\## Analytical Outputs



\### forecast\_results



Contains the 90-day sales forecasting results generated using Prophet.



\### association\_rules



Contains product association rules generated using Apriori and evaluated using support, confidence, and lift.

