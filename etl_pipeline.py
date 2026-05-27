import pandas as pd
import numpy as np


# PHASE 1 - EXTRACTION

df=pd.read_csv('data/raw/banking_transactions.csv',nrows=10000)
print("FIRST 5 ROWS OF THE DATASET:")
print(df.head())


# PHASE 2 -DATA PROFILING

print("\nDATASET INFO:")
print(df.info())
print("\nDATASET SHAPE:")
print(df.shape)
print("\nUNIQUE VALUES:")
print(df.nunique())
print("\nSUMMARY:")
print(df.describe())

print("\nDUPLICATE VALUES:")
print(df.duplicated().sum())
print("\nDATA TYPES:")
print(df.dtypes)
print("\nNULL VALUES:")
print(df.isnull().sum())
print("\nINVALID AMOUNT VALUES:")
print((df['TransactionAmount']<0).sum())
print("Age less than 18:")
print((df["CustomerAge"]<18).sum())


# PHASE 3 - TRANSFORMATION AND CLEANING

#convert to datetime and extract year, month, day, hour
df["has_time"] = df["TransactionDate"].astype(str).str.contains(":")
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'],format="mixed")
df['year'] = df['TransactionDate'].dt.year
df['month'] = df['TransactionDate'].dt.month
df['day'] = df['TransactionDate'].dt.day_name()
df['hour'] = df['TransactionDate'].dt.hour

df['year'] = df['year'].astype('Int64')
df['month'] = df['month'].astype('Int64')
df['hour'] = df['hour'].astype('Int64')

#strip whitespaces and standardize text
df['Channel']=df['Channel'].str.strip().str.title()
df['TransactionType']=df['TransactionType'].str.strip().str.title()
df['Location']=df['Location'].str.strip().str.title()
df['CustomerOccupation']=df['CustomerOccupation'].str.strip().str.title() 

#create age groups
bins=[0,18,30,45,60,100]
labels=['0-18','19-30','31-45','46-60','60+']
df['AgeGroup']=pd.cut(df['CustomerAge'],bins=bins,labels=labels)

#transaction flags to identify high transaction amounts
threshold=df["TransactionAmount"].quantile(0.95)
df["HighTransaction"]=(df["TransactionAmount"]>threshold).astype(int)
print(" threshold for high transaction amount:",threshold)

# categorize the amounts
df["AmountCategory"]=pd.cut(df["TransactionAmount"],bins=[0,100,500,1000,5000],labels=["Low","Medium","High","Very High"])

#time of transaction
def get_time_period(hour):
    if pd.isna(hour):
        return "Unknown"
    elif(hour>=22 and hour<4):
        return "Late Night"
    elif(hour>=4 and hour<7):
        return "Early Morning"
    elif(hour>=7 and hour<12):
        return "Morning"
    elif(hour>=12 and hour<17):
        return "Afternoon"
    else:
        return "Evening"
df["TimePeriod"]=df["hour"].apply(get_time_period)


# FRAUD DETECTION FEATURE ENGINEERING
# ------------------------------------------
# 1. SORT CHRONOLOGICALLY (CRITICAL)
# ------------------------------------------
df["TransactionDate"]=pd.to_datetime(df["TransactionDate"])
df = df.sort_values(["AccountID", "TransactionDate"])

# ------------------------------------------
# 2. HISTORY COUNTER
# ------------------------------------------
df["past_transaction_count"] = df.groupby("AccountID").cumcount()
has_enough_history = df["past_transaction_count"] >= 3

# ------------------------------------------
# 3. LOGIN BEHAVIOR BASELINE
# ------------------------------------------
df["past_mean_login"] = (
    df.groupby("AccountID")["LoginAttempts"]
    .transform(lambda x: x.expanding().mean().shift(1))
)

df["past_mean_login"] = df["past_mean_login"].fillna(1.0)

# ------------------------------------------
# 4. IP BEHAVIOR (LOCAL + GLOBAL RISK)
# ------------------------------------------
df["ip_past_occurrences"] = df.groupby(["AccountID", "IP Address"]).cumcount()
df["is_new_ip"] = (df["ip_past_occurrences"] == 0).astype(int)

# ------------------------------------------
# 5. TRANSACTION AMOUNT BASELINE (STABLE)
# ------------------------------------------
df["past_mean_amt"] = (
    df.groupby("AccountID")["TransactionAmount"]
    .transform(lambda x: x.expanding().mean().shift(1))
)

df["past_std_amt"] = (
    df.groupby("AccountID")["TransactionAmount"]
    .transform(lambda x: x.expanding().std().shift(1))
)

# GLOBAL FALLBACK (SAFE FOR COLD START)
global_mean = df["TransactionAmount"].mean()
global_std = df["TransactionAmount"].std()

df["past_mean_amt"] = df["past_mean_amt"].fillna(global_mean)
df["past_std_amt"] = df["past_std_amt"].fillna(global_std)

df["amt_upper_bound"] = df["past_mean_amt"] + (2 * df["past_std_amt"])

# ------------------------------------------
# 6. DERIVED FEATURES
# ------------------------------------------
login_spike = df["LoginAttempts"] > (df["past_mean_login"] + 2)
amount_anomaly = df["TransactionAmount"] > df["amt_upper_bound"]
print("upper bound for transaction amount:",df["amt_upper_bound"])

# ------------------------------------------
# 7. FRAUD RULES
# ------------------------------------------

# Strong amount anomaly (low history-safe)
cond1 = amount_anomaly & (df["LoginAttempts"] > 4)

# Behavioral anomaly (only when history is reliable)
cond2 = login_spike & amount_anomaly & has_enough_history

# Behavioral + contextual IP risk
cond3 = login_spike & df["is_new_ip"] & has_enough_history

# ------------------------------------------
# 8. FINAL LABEL
# ------------------------------------------
df["UnusualTransaction"] = (cond1 | cond2 | cond3).astype(int)

# ------------------------------------------
# 9. CLEANUP
# ------------------------------------------
df = df.drop(columns=[
    "past_transaction_count",
    "past_mean_login",
    "ip_past_occurrences",
    "is_new_ip",
    "past_mean_amt",
    "past_std_amt",
    "amt_upper_bound"
])

# unusual transactions count
print("\nUNUSUAL TRANSACTIONS COUNT:")
print(df["UnusualTransaction"].value_counts())


# PHASE 4 - LOADING
print("\nCLEANED DATASET SHAPE:")
print(df.shape)
print("\nCLEANED DATASET:")
print(df.head())
print("\nNULL VALUES IN CLEANED DATASET:")
print(df.isnull().sum())

print("\nDATA TYPES:")
print(df.dtypes)

#df.to_csv("data/processed/cleaned_transactions.csv",index=False)
#print("succesfully saved cleaned dataset to data/processed/cleaned_transactions.csv")