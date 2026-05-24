# Banking Transaction ETL & Analytics Pipeline

## Project Overview

This project implements a complete ETL (Extract, Transform, Load) pipeline using Python, Pandas, and MySQL on a banking transaction dataset.

The objective of this project is to process raw banking transaction data, clean and transform it into an analytics-ready dataset, and perform business analysis using SQL queries.

The project simulates a real-world data engineering workflow involving:

- Data Extraction
- Data Profiling
- Data Cleaning
- Data Transformation
- Feature Engineering
- Data Loading into SQL
- Analytical Querying
- Business Insight Generation

---

# Tech Stack

- Python
- Pandas
- NumPy
- MySQL Workbench
- SQL
- Matplotlib
- Seaborn

---

# Dataset Information

The dataset contains banking transaction records with customer, transaction, channel, and account-related information.

## Original Dataset Columns

- TransactionID
- AccountID
- TransactionAmount
- TransactionDate
- TransactionType
- Location
- DeviceID
- IP Address
- MerchantID
- Channel
- CustomerAge
- CustomerOccupation
- TransactionDuration
- LoginAttempts
- AccountBalance

---

# Project Architecture Flow

```plaintext
Raw Banking Dataset
        ↓
Data Extraction
        ↓
Data Profiling
        ↓
Data Cleaning
        ↓
Data Transformation
        ↓
Feature Engineering
        ↓
Processed Dataset
        ↓
Load into MySQL Workbench
        ↓
SQL Analytics
        ↓
Business Insights
```

---

# Folder Structure

```plaintext
banking-etl-project/
│
├── data/
│   ├── raw/
│   │   └── banking_transactions.csv
│   │
│   └── processed/
│       └── cleaned_transactions.csv
│
├── sql/
│   └── analysis_queries.sql
│
├── docs/
│   └── project_documentation.docx
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Phase 1 — Data Extraction

The first phase involves loading the raw banking transaction dataset into Pandas.

## Tasks Performed

- Loaded the first 10,000 rows from the dataset
- Verified dataset accessibility
- Inspected raw transaction records

---

# Phase 2 — Data Profiling

Data profiling was performed to understand the structure, quality, and characteristics of the dataset.

## Validation Checks Performed

### Duplicate Detection

```python
df.duplicated().sum()
```

### Invalid Transaction Amount Check

```python
(df['TransactionAmount'] < 0).sum()
```

### Invalid Customer Age Check

```python
(df['CustomerAge'] < 18).sum()
```

---

# Data Profiling Observations

- Dataset contained 10,000 transaction records
- No missing values were found
- No duplicate rows were detected
- Transaction amounts were valid
- Customer ages were within acceptable range
- Multiple banking channels and locations were identified

---

# Phase 3 — Data Cleaning & Transformation

This phase converts raw operational data into a structured and analytics-ready dataset.

---

## 1. Datetime Conversion

The `TransactionDate` column was converted into datetime format.

## Code

```python
df['TransactionDate'] = pd.to_datetime(
    df['TransactionDate'],
    errors='coerce'
)
```

## Additional Date Features Extracted

```python
df['year'] = df['TransactionDate'].dt.year
df['month'] = df['TransactionDate'].dt.month
df['day'] = df['TransactionDate'].dt.day_name()
df['hour'] = df['TransactionDate'].dt.hour
```

## Generated Columns

- year
- month
- day
- hour

---

## 2. Text Standardization

Text columns were standardized by:

- removing leading/trailing whitespaces
- applying consistent capitalization

## Code

```python
df['Channel'] = df['Channel'].str.strip().str.title()
df['TransactionType'] = df['TransactionType'].str.strip().str.title()
df['Location'] = df['Location'].str.strip().str.title()
df['CustomerOccupation'] = df['CustomerOccupation'].str.strip().str.title()
```

---

# Phase 4 — Feature Engineering

Feature engineering was performed to create new analytical columns from existing data.

---

## 1. Customer Age Group Classification

Customers were categorized into age groups.

## Code

```python
bins = [0, 18, 30, 45, 60, 100]

labels = [
    '0-18',
    '19-30',
    '31-45',
    '46-60',
    '60+'
]

df['AgeGroup'] = pd.cut(
    df['CustomerAge'],
    bins=bins,
    labels=labels
)
```

## Generated Column

- AgeGroup

---

## 2. High Transaction Detection

Transactions above the 95th percentile were identified as high-value transactions.

## Code

```python
threshold = df["TransactionAmount"].quantile(0.95)

df["HighTransaction"] = (
    df["TransactionAmount"] > threshold
).astype(int)
```

## Generated Column

- HighTransaction

---

## 3. Transaction Amount Categorization

Transactions were categorized based on amount ranges.

## Code

```python
df["AmountCategory"] = pd.cut(
    df["TransactionAmount"],
    bins=[0,100,500,1000,5000],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)
```

## Generated Column

- AmountCategory

---

## 5. Unusual Transaction Detection

Outlier transactions were identified using the Interquartile Range (IQR) method.

## Code

```python
Q1 = df["TransactionAmount"].quantile(0.25)

Q3 = df["TransactionAmount"].quantile(0.75)

IQR = Q3 - Q1

upper_bound = Q3 + 1.5 * IQR

df["UnusualTransaction"] = (
    df["TransactionAmount"] > upper_bound
).astype(int)
```

## Generated Column

- UnusualTransaction

---

# Final Engineered Columns

The following columns were added during transformation and feature engineering:

- year
- month
- day
- hour
- AgeGroup
- HighTransaction
- AmountCategory
- TimePeriod
- UnusualTransaction

---

# Phase 5 — Exporting Processed Dataset

The cleaned dataset was exported for analytical processing.

---

# Business Insights Generated

The project generated several analytical insights, including:

- Top customers based on transaction value
- Most frequently used transaction type
- Most active banking channels
- Peak transaction time periods
- Customer behavior across age groups
- High-value transaction patterns
- Detection of unusual transactions
- Monthly transaction trends

---

# Flow Diagram

## ETL Pipeline Flow

```plaintext
Raw Dataset
    ↓
Extraction
    ↓
Profiling
    ↓
Cleaning
    ↓
Transformation
    ↓
Feature Engineering
    ↓
Processed Dataset
    ↓
MySQL Workbench
    ↓
SQL Analysis
    ↓
Business Insights
```

---

## Transformation Workflow

```plaintext
TransactionDate
    ↓
Datetime Conversion
    ↓
Year / Month / Day / Hour

TransactionAmount
    ↓
Amount Categorization
    ↓
High Transaction Detection
    ↓
Outlier Detection

CustomerAge
    ↓
Age Group Classification

Hour
    ↓
Time Period Classification
```

---

# Conclusion

This project successfully demonstrates a complete end-to-end ETL and analytics workflow using Python and SQL.

The pipeline transformed raw banking transaction data into a structured analytics-ready dataset through profiling, cleaning, transformation, and feature engineering techniques.

The processed data was loaded into MySQL Workbench and analyzed using SQL queries to derive meaningful business insights related to transaction behavior, customer activity, banking channels, and unusual transaction detection.

This project reflects practical data engineering concepts commonly used in real-world financial data processing systems.