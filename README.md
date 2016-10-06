#pytest

These scripts parse a log file for quick analysis purposes
The logfile we will be using is hardcoded into each script, it can be easily made into an arg in the future.
For test data, unzip the elblogs.zip into the same path as these python scripts.

**To see how many callbacks we received for partner `nyr8nx`:**

python partnerSearch.py nyr8nx

**To see how many callbacks we received for partner `nyr8nx` for campaign id (cid) `X9KN0`:**

python partnerSearch.py nyr8nx -c X9KN0

**To run API call analysis:**

python apiRequestAnalysis.py
