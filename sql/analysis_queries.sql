-- =========================================
-- BANKING ETL ANALYTICAL QUERIES
-- =========================================

USE banking_etl;

-- =========================================
-- 1. Top 10 Accounts by Total Transaction Amount
-- =========================================
SELECT AccountID,ROUND(SUM(TransactionAmount),2) as total_amount
FROM cleaned_transactions
GROUP BY AccountID
ORDER BY total_amount DESC
LIMIT 10;

-- =========================================
-- 2. Most frequent Transaction Type
-- =========================================
SELECT TransactionType, COUNT(*) as frequency
FROM cleaned_transactions
GROUP BY TransactionType
ORDER BY frequency DESC
LIMIT 1;

-- =========================================
-- 3. Transaction distribution across channels
-- =========================================
SELECT Channel, COUNT(TransactionType) as total_num
FROM cleaned_transactions
GROUP BY Channel;

-- =========================================
-- 4. Locations with the highest transaction volume
-- =========================================
SELECT Location, ROUND(SUM(TransactionAmount),2) as TransactionVolume
FROM cleaned_transactions
GROUP BY Location
ORDER BY TransactionVolume DESC;

-- =========================================
-- 5. Average transaction amount for each transaction type
-- =========================================
SELECT TransactionType, ROUND(AVG(TransactionAmount),2) as average
FROM cleaned_transactions
GROUP BY TransactionType;

-- =========================================
-- 6. Monthly transaction trends
-- =========================================
SELECT year, month, COUNT(TransactionID) as Num_of_Transactions,
ROUND(SUM(TransactionAmount)) as Total_Amount 
FROM cleaned_transactions
GROUP BY year,month
ORDER BY year,month;

-- =========================================
-- 7. Peak transaction periods based on volume
-- =========================================



