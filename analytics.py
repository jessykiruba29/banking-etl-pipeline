import pandas as pd
import matplotlib.pyplot as plt

# LOAD CLEANED DATASET

df=pd.read_csv("data/processed/cleaned_transactions.csv")

print("DATA LOADED SUCCESSFULLY")
print(df.head())


# -------------------------------
# ANALYSIS 1 - TRANSACTION TYPE
# -------------------------------

transaction_type=df["TransactionType"].value_counts()

plt.figure(figsize=(6,6))
transaction_type.plot(kind='pie', autopct='%1.1f%%')
plt.title("Transaction Type Distribution")

plt.ylabel("")

plt.savefig("outputs/charts/transaction_type_distribution.png")
plt.close()


# -----------------------------------
# ANALYSIS 2 - CHANNEL DISTRIBUTION
# -----------------------------------

channel_analysis=df.groupby("Channel")["TransactionAmount"].sum()

plt.figure(figsize=(6,5))
channel_analysis.plot(kind='bar')

plt.title("Channel-wise Transaction Amount")
plt.xlabel("Channel")
plt.ylabel("Total Transaction Amount")

plt.savefig("outputs/charts/channel_analysis.png")
plt.close()


# -----------------------------------
# ANALYSIS 3 - MONTHLY TRENDS
# -----------------------------------

monthly_analysis=df.groupby("month")["TransactionAmount"].sum()

plt.figure(figsize=(8,5))
monthly_analysis.plot(kind='line', marker='o')

plt.title("Monthly Transaction Trends")
plt.xlabel("Month")
plt.ylabel("Total Transaction Amount")

plt.savefig("outputs/charts/monthly_trends.png")
plt.close()


# -----------------------------------
# ANALYSIS 4 - AGE GROUP ANALYSIS
# -----------------------------------

age_analysis=df.groupby("AgeGroup")["TransactionAmount"].sum()

plt.figure(figsize=(7,5))
age_analysis.plot(kind='bar')

plt.title("Age Group Transaction Analysis")
plt.xlabel("Age Group")
plt.ylabel("Total Transaction Amount")

plt.savefig("outputs/charts/age_group_analysis.png")
plt.close()


# -----------------------------------
# ANALYSIS 5 - TIME PERIOD ANALYSIS
# -----------------------------------

time_analysis=df.groupby("TimePeriod")["TransactionAmount"].sum()

plt.figure(figsize=(8,5))
time_analysis.plot(kind='bar')

plt.title("Transaction Amount by Time Period")
plt.xlabel("Time Period")
plt.ylabel("Total Transaction Amount")

plt.savefig("outputs/charts/time_period_analysis.png")
plt.close()


# -----------------------------------
# ANALYSIS 6 - LOGIN ATTEMPTS
# -----------------------------------

login_analysis=df.groupby("LoginAttempts")["TransactionAmount"].mean()

plt.figure(figsize=(7,5))
login_analysis.plot(kind='bar')

plt.title("Average Transaction Amount by Login Attempts")
plt.xlabel("Login Attempts")
plt.ylabel("Average Transaction Amount")

plt.savefig("outputs/charts/login_attempts_analysis.png")
plt.close()


# -----------------------------------
# ANALYSIS 7 - TOP MERCHANTS
# -----------------------------------

merchant_analysis=(
    df.groupby("MerchantID")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
merchant_analysis.plot(kind='bar')

plt.title("Top 10 Merchants by Transaction Volume")
plt.xlabel("Merchant ID")
plt.ylabel("Total Transaction Amount")

plt.savefig("outputs/charts/top_merchants.png")
plt.close()


# -----------------------------------
# ANALYSIS 8 - WEEKEND VS WEEKDAY
# -----------------------------------

df["DayType"]=df["day"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)

daytype_analysis = df.groupby("DayType")["TransactionAmount"].sum()

plt.figure(figsize=(6,5))
daytype_analysis.plot(kind='pie', autopct='%1.1f%%')

plt.title("Weekend vs Weekday Transactions")
plt.ylabel("")

plt.savefig("outputs/charts/weekend_weekday_analysis.png")
plt.close()


# -----------------------------------
# ANALYSIS 9 - HIGH TRANSACTIONS
# -----------------------------------

high_transactions=(
    df[df["HighTransaction"]==1]
    .groupby("AccountID")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
high_transactions.plot(kind='bar')

plt.title("Top Accounts with High Value Transactions")
plt.xlabel("Account ID")
plt.ylabel("Total High Transaction Amount")

plt.savefig("outputs/charts/high_transaction_accounts.png")
plt.close()


# -----------------------------------
# ANALYSIS 10 - UNUSUAL TRANSACTIONS
# -----------------------------------

unusual_analysis=df["UnusualTransaction"].value_counts()

plt.figure(figsize=(6,6))
unusual_analysis.plot(kind='pie', autopct='%1.1f%%')

plt.title("Unusual Transaction Distribution")
plt.ylabel("")

plt.savefig("outputs/charts/unusual_transaction_distribution.png")
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