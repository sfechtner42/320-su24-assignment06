# Test Results
The table summarizes of the performance of both databases measured by speed (in milliseconds or seconds). 
Some of the tests in SQL were done 3 times over and the last round is reported in order to get an accurate time.
Otherwise, tests were done 3 times in order to get a reported average run time below.

Function | SQL   | MongoDB
-----|-------|-----
Load user CSV | 5.2s  | 306.8ms
Load status CSV | 43.6s | 18.2s
Add user | 5.9ms | 5.7 ms
Update user | 9.2ms | 1.0 ms
Search user | 1.0ms | 0.3ms
Delete user | 1.9ms | 0.3ms
Add status | 1.0ms | 1.1ms
Update status | 1.9ms | 0.6ms
Search status | 1.0ms | 0.3ms
Delete status | 1.0ms | 0.3ms

# Conclusion
My MongoDB significantly outperforms my SQL database  on loading the account and status updates csv.
Some of my functions in SQL would report a 0.0ms run time suggesting that the function execute and return so quickly to record accurate times. 
That is why I've programed the functions to run 3 times before reporting a time.
Therefore, I suspect that the SQL database is actually faster than the MongoDB for most of the functions except loading the CSV files.

# Recommendation
If the databases continue to grow but the CSV load needs to be maintained, then the need for performance is priority and **MongoDB is the way to go**. 
However, I recognize the SQL database is a little more rigid using primary keys.
All the QC checks (like checking for duplicates) or deleting data associated with a key (delete a user) were easier for me to handle in SQL than in MongoDB.
Thus, I'd favor the SQL database for smaller datasets.
