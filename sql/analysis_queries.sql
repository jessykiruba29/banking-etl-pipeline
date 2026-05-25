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
SELECT TimePeriod, ROUND(SUM(TransactionAmount),2) as TotalAmt
FROM cleaned_transactions
GROUP BY TimePeriod
ORDER BY TotalAmt DESC;

-- =========================================
-- 8. Channel wise transaction analysis
-- =========================================
SELECT Channel, ROUND(SUM(TransactionAmount),2) as total_amt
FROM cleaned_transactions
GROUP BY Channel;

-- =========================================
-- 9. Customer age-group-wise transaction behavior
-- =========================================
SELECT AgeGroup, ROUND(SUM(TransactionAmount),2) as amt, COUNT(TransactionID) as num, ROUND(AVG(TransactionAmount),2) as avg
FROM cleaned_transactions
GROUP BY AgeGroup
ORDER BY AgeGroup;

--- =========================================
-- 10. Unusually high transaction amounts (potential fraud detection)
-- =========================================
SELECT AccountID, COUNT(UnusualTransaction) as unusual_cnt, ROUND(SUM(TransactionAmount),2) as total_amt
FROM cleaned_transactions
WHERE UnusualTransaction=1
GROUP BY AccountID
ORDER BY total_amt DESC; 

-- =========================================
-- 11. Relationship between login attempts and transaction behavior
-- =========================================
SELECT LoginAttempts, COUNT(TransactionID) as no_of_transactions, ROUND(SUM(TransactionAmount),2) as total_amt, ROUND(AVG(TransactionAmount),2) as avg_amt
FROM cleaned_transactions
GROUP BY LoginAttempts
ORDER BY LoginAttempts;

-- =========================================
-- 12. Top merchants by transaction volume
-- =========================================
SELECT MerchantID, ROUND(SUM(TransactionAmount),2) as volume
FROM cleaned_transactions
GROUP BY MerchantID
ORDER BY volume DESC;

-- =========================================
-- 13. Account balance patterns across different transaction types
-- =========================================
SELECT TransactionType, ROUND(AVG(AccountBalance),2) as acc_bal
FROM cleaned_transactions
GROUP BY TransactionType;

-- =========================================
-- 14. High-value transactions based on a new threshold
-- =========================================
SELECT AccountID, Count(HighTransaction) as count, ROUND(SUM(TransactionAmount),2) as tot_amt
FROM cleaned_transactions
WHERE HighTransaction=1
GROUP BY AccountID
ORDER BY count DESC;

-- =========================================
-- 15. Additional insights
-- =========================================

-- a. Occupation wise transaction analysis
SELECT CustomerOccupation, COUNT(TransactionID) as total_num, ROUND(SUM(TransactionAmount),2) as total_amt
FROM cleaned_transactions
GROUP BY CustomerOccupation
ORDER BY total_num DESC;

--b. Top 10 Transactions with the longest duration
SELECT AccountID, TransactionAmount, TransactionDuration
FROM cleaned_transactions
ORDER BY TransactionDuration DESC
LIMIT 10;

--c. Weekend vs Weekday transaction patterns
SELECT 
	CASE
		WHEN day IN ('Saturday','Sunday') THEN 'Weekend'
        ELSE 'Weekday'
	END AS DayType,
    COUNT(TransactionID) AS total_count,
    ROUND(SUM(TransactionAmount),2) AS total_amt
FROM cleaned_transactions
GROUP BY DayType;


