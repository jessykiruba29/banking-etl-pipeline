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
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'],format="mixed")
df["has_time"] = df["TransactionDate"].dt.time != pd.Timestamp("00:00:00").time()
df['year'] = df['TransactionDate'].dt.year
df['month'] = df['TransactionDate'].dt.month
df['day'] = df['TransactionDate'].dt.day_name()
df['hour'] = df['TransactionDate'].dt.hour

df['year'] = df['year'].astype('Int64')
df['month'] = df['month'].astype('Int64')
df['hour'] = df['hour'].astype('Int64')
print("date")
count_missing_time = df['has_time'].value_counts()
print(f"Missing time values: {count_missing_time}")
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

# categorize the amounts
df["AmountCategory"]=pd.cut(df["TransactionAmount"],bins=[0,100,500,1000,5000],labels=["Low","Medium","High","Very High"])

#time of transaction
def get_time_period(hour):
    if pd.isna(hour):
        return "Unknown"
    elif(hour<4):
        return "Late Night"
    elif(hour<7):
        return "Early Morning"
    elif(hour<12):
        return "Morning"
    elif(hour<17):
        return "Afternoon"
    else:
        return "Evening"
df["TimePeriod"]=df["hour"].apply(get_time_period)

#detect unusual transactions based on amount and flag them
mean=df["TransactionAmount"].mean()
std=df["TransactionAmount"].std()
upper_bound=mean+2*std

df["UnusualTransaction"] = (
    ((df["TransactionAmount"] > upper_bound) &
     (df["LoginAttempts"] >= 4))
    |
    ((df["TransactionDuration"] > 280) & 
     (df["TransactionAmount"] < mean))
).astype(int)

#unusual transactions count
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








