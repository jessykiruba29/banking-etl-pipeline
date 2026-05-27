import pandas as pd
import matplotlib.pyplot as plt
from seaborn.objects import Count

# LOAD CLEANED DATASET

df=pd.read_csv("data/processed/cleaned_transactions.csv")

print("DATA LOADED SUCCESSFULLY")
print(df.head())

#1. Top 10 Accounts by Total Amount

top_accounts = df.groupby("AccountID")["TransactionAmount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_accounts.plot(kind="bar")
plt.title("Top 10 Accounts by Total Transaction Amount")
plt.ylabel("Total Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/top10_accounts.png")
plt.close()

# 2. Most Frequent Transaction Type

txn_type = df["TransactionType"].value_counts()

plt.figure(figsize=(6,4))
txn_type.plot(kind="bar")
plt.title("Transaction Type Frequency")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/charts/txn_type_frequency.png")
plt.close()

# 3. Channel Distribution (COUNT + AMOUNT → 2 GRAPHS)

channel_count = df["Channel"].value_counts()

plt.figure(figsize=(6,4))
channel_count.plot(kind="bar")
plt.title("Channel Usage Count")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/charts/channel_count.png")
plt.close()

channel_amt = df.groupby("Channel")["TransactionAmount"].sum()

plt.figure(figsize=(6,4))
channel_amt.plot(kind="bar")
plt.title("Channel Transaction Volume")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.savefig("outputs/charts/channel_amount.png")
plt.close()

# 4. Top 3 Locations by Volume

top_locations = df.groupby("Location")["TransactionAmount"].sum().sort_values(ascending=False).head(3)

plt.figure(figsize=(6,4))
top_locations.plot(kind="bar")
plt.title("Top 3 Locations by Transaction Volume")
plt.ylabel("Total Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/top_locations.png")
plt.close()

# 5. Avg Transaction Type

avg_txn = df.groupby("TransactionType")["TransactionAmount"].mean()

plt.figure(figsize=(6,4))
avg_txn.plot(kind="bar")
plt.title("Average Transaction Amount by Type")
plt.ylabel("Avg Amount")
plt.tight_layout()
plt.savefig("outputs/charts/avg_txn_type.png")
plt.close()

# 6. Monthly Trends (2 GRAPHS)

monthly = df.groupby(["year","month"]).agg(
    count=("TransactionID","count"),
    amount=("TransactionAmount","sum")
).reset_index()

monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str)

plt.figure(figsize=(12,5))
plt.plot(monthly["period"], monthly["count"], marker="o")
plt.title("Monthly Transaction Count Trend")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("outputs/charts/monthly_count_trend.png")
plt.close()

plt.figure(figsize=(12,5))
plt.plot(monthly["period"], monthly["amount"], marker="o")
plt.title("Monthly Transaction Amount Trend")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("outputs/charts/monthly_amount_trend.png")
plt.close()

# 7. Time Period Analysis
time_period = df[df["has_time"] == True].groupby("TimePeriod")["TransactionAmount"].sum().sort_values(ascending=False)
plt.figure(figsize=(6,4))
time_period.plot(kind="bar")
plt.title("Transaction by Time Period")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.savefig("outputs/charts/time_period.png")
plt.close()

# 8. Channel Amount Analysis

channel_amt2 = df.groupby("Channel")["TransactionAmount"].sum()

plt.figure(figsize=(6,4))
channel_amt2.plot(kind="bar")
plt.title("Channel Transaction Volume")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.savefig("outputs/charts/channel_amount2.png")
plt.close()

# 9. Age Group Analysis (3 METRICS → 2 GRAPHS)

age = df.groupby("AgeGroup").agg(
    amt=("TransactionAmount","sum"),
    count=("TransactionID","count"),
    avg=("TransactionAmount","mean")
)

plt.figure(figsize=(6,4))
age["amt"].plot(kind="bar")
plt.title("Age Group - Total Amount")
plt.tight_layout()
plt.savefig("outputs/charts/age_amount.png")
plt.close()

plt.figure(figsize=(6,4))
age["count"].plot(kind="bar")
plt.title("Age Group - Transaction Count")
plt.tight_layout()
plt.savefig("outputs/charts/age_count.png")
plt.close()

# 10. High Transaction Accounts

high = df[df["UnusualTransaction"]==1].groupby("AccountID")["TransactionAmount"].agg(["count","sum"]).sort_values("count",ascending=False).head(5)

plt.figure(figsize=(8,4))
high["count"].plot(kind="bar")
plt.title("Unusual High Value Transactions - Top Accounts")
plt.tight_layout()
plt.savefig("outputs/charts/high_txn_accounts2.png")
plt.close()

# 11. Login Attempts Analysis (2 GRAPHS)

login = df.groupby("LoginAttempts").agg(
    count=("TransactionID","count"),
    amount=("TransactionAmount","sum"),
    avg=("TransactionAmount","mean")
)
plt.figure(figsize=(6,4))
login["count"].plot(kind="bar")
plt.title("Login Attempts vs Transaction Count")
plt.tight_layout()
plt.savefig("outputs/charts/login_count.png")
plt.close()

plt.figure(figsize=(6,4))
login["avg"].plot(kind="bar")
plt.title("Login Attempts vs Avg Amount")
plt.tight_layout()
plt.savefig("outputs/charts/login_avg.png")
plt.close()

# 12. Merchant Analysis

merchant = df.groupby("MerchantID")["TransactionAmount"].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(6,4))
merchant.plot(kind="bar")
plt.title("Top Merchants by Volume")
plt.tight_layout()
plt.savefig("outputs/charts/merchant.png")
plt.close()

# 13. Account Balance vs Transaction Type

bal = df.groupby("TransactionType")["AccountBalance"].mean()

plt.figure(figsize=(6,4))
bal.plot(kind="bar")
plt.title("Avg Account Balance by Transaction Type")
plt.tight_layout()
plt.savefig("outputs/charts/account_balance.png")
plt.close()

#14. own threshold for high transactions and identify top accounts with high transaction amounts

high_transactions=(
    df[df["HighTransaction"]==1]
    .groupby("AccountID")["TransactionAmount"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure(figsize=(10,5))
high_transactions.plot(kind='bar')

plt.title("Top Accounts with High Value Transactions")
plt.xlabel("Account ID")
plt.ylabel("Average High Transaction Amount")

plt.savefig("outputs/charts/high_transaction_accounts.png")
plt.close()

# 15 a. Occupation Analysis

occ = df.groupby("CustomerOccupation")["TransactionAmount"].mean().sort_values(ascending=False)

plt.figure(figsize=(6,4))
occ.plot(kind="bar")
plt.title("Occupation vs Average Transaction Amount")
plt.tight_layout()
plt.savefig("outputs/charts/occupation.png")
plt.close()

# 15 b. Weekend vs Weekday

df["DayType"] = df["day"].apply(lambda x: "Weekend" if x in ["Saturday","Sunday"] else "Weekday")

daytype = df.groupby("DayType")["TransactionAmount"].sum()

plt.figure(figsize=(6,4))
daytype.plot(kind="bar")
plt.title("Weekend vs Weekday Transactions")
plt.tight_layout()
plt.savefig("outputs/charts/daytype.png")
plt.close()


# -----------------------------------
# REPORT GENERATION
# -----------------------------------

report="""
BANKING TRANSACTION ANALYTICS REPORT
===================================

1. Transaction Type Analysis
- Shows distribution of Debit and Credit transactions.

2. Channel Analysis
- Identifies which banking channel contributes the highest transaction amount.

3. Monthly Trends
- Displays month-wise transaction growth and activity.

4. Age Group Analysis
- Shows which customer age group contributes the most transactions.

5. Time Period Analysis
- Identifies peak transaction periods during the day.

6. Login Attempt Analysis
- Analyzes relationship between login attempts and transaction amounts.

7. Merchant Analysis
- Identifies top merchants based on transaction volume.

8. Weekend vs Weekday Analysis
- Compares banking activity between weekends and weekdays.

9. High Transaction Detection
- High transactions were identified using 95th percentile threshold.

10. Unusual Transaction Detection
- Outliers were detected using the IQR method.
"""

with open("outputs/reports/analysis_report.txt", "w") as file:
    file.write(report)

print("REPORT GENERATED SUCCESSFULLY")

print("ALL CHARTS SAVED INSIDE outputs/charts/")