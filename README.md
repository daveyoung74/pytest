The logfile we will be using is hardcoded into each script, it can be easily made into an arg in the future.
For test data, unzip the elblogs.zip into the same path as these python scripts.

1) To see how many callbacks we received for partner `nyr8nx`: 
python partnerSearch.py nyr8nx

2) To see how many callbacks we received for partner `nyr8nx` for campaign id (cid) `X9KN0`:
python partnerSearch.py nyr8nx -c X9KN0

3) To run API call analysis:
python apiRequestAnalysis.py