from collections import Counter
from itertools import chain

def getAPIRequests(log_fh):
	allAPIRequests = {}
	for line in log_fh:
		#2015-03-10T23:35:55.882667Z prod-ui-mcent-4sep2012 120.180.119.91:54590 10.164.180.106:80 0.000021 0.026886 0.000023 200 200 1019 49 "POST http://mcent.com:80/api/v1/device_info HTTP/1.1"
		#date server ip1 ip2 num1 num2 num3 num4 num5 code1 code2 request
		
		#see if this resembles an api request
		if '/api/' in line:
			words = line.split()
			if allAPIRequests:
				yield allAPIRequests
			
			#see if this is an actual api request
			if '/api/' in words[12]:
				allAPIRequests = {
					"date":words[0],
					"server":words[1],
					"ip1":words[2],
					"ip2":words[3],
					"num1":words[4],
					"num2":words[5],
					"num3":words[6],
					"num4":words[7],
					"num5":words[8],
					"code1":words[9],
					"code2":words[10],
					"request":words[11:14]
				}
	yield allAPIRequests

def apiRequestAnalysis(logfile):
	with open("elblogs.txt") as f:
		apirequests = list(getAPIRequests(f))
		print ("Total API requests: %s" % len(apirequests))
		
		api_calls = []
		for apirequest in apirequests:
			request_url = apirequest['request'][1]
				
			#grab the api string off the request if it's present
			findstr = '/api/'
			api_call = request_url.split(findstr,1)[1] 
			if(api_call != ''):
				#we are going to count up unique api calls later, so tuck this into the api_calls list
				api_calls.append( api_call );

		total_api_calls = len( api_calls )
		
		#get the total counts of the unique keys in the api_calls list, in reverse descending order
		counts = Counter( api_calls ).most_common()
		for api_call, api_call_count in counts:
			pcnt_of_total = (api_call_count / total_api_calls) * 100
			
			#Sample output
			#50.00%  50  api/v1/track_offer_views
			print ('{0:.2f}%\t{1:,}\t{2}'.format(
				round(pcnt_of_total,2),
				api_call_count,
				api_call)
			)
			
		print ('{0:,} Total api requests'.format(total_api_calls))


logfile = "elblogs.txt"
apiRequestAnalysis(logfile)	