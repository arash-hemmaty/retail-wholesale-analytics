\# Data Model



The project uses a star-schema-oriented analytical model.



\## Relationships



```text

dim\_date

&#x20;  │

&#x20;  ├── fact\_sales

&#x20;  ├── fact\_inventory

&#x20;  ├── fact\_cost

&#x20;  └── forecast\_results



dim\_product

&#x20;  │

&#x20;  ├── fact\_sales

&#x20;  └── fact\_inventory



dim\_customer

&#x20;  │

&#x20;  └── fact\_sales

