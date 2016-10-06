import argparse

def getCallbacks(log_fh):
	allCallbacks = {}
	for line in log_fh:
		#2015-03-10T23:35:55.882667Z prod-ui-mcent-4sep2012 120.180.119.91:54590 10.164.180.106:80 0.000021 0.026886 0.000023 200 200 1019 49 "POST http://mcent.com:80/api/v1/device_info HTTP/1.1"
		#date server ip1 ip2 num1 num2 num3 num4 num5 code1 code2 request
		
		#see if this line is a callback. If so, split it up into parts and tuck into the allCallbacks data structure
		if '/aff/callback/' in line:
			words = line.split()
			if allCallbacks:
				yield allCallbacks
			
			allCallbacks = {
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
	yield allCallbacks

def partnerCampaignAnalysis(logfile,find_partner_id,find_partner_campaign_id):
	with open(logfile) as f:
		callbacks= list(getCallbacks(f))
		#print ("Total Callbacks: %s" % len(callbacks))
		
		find_partner_count = 0
		find_partner_campaign_count = 0
		
		for callback in callbacks:
			#/aff/callback/<partner_id>?<campaign_attributes>
			request_url = callback['request'][1]
			
			#grab the url params
			findstr = '/aff/callback/'
			url_attributes = request_url.split(findstr,1)[1] 
			
			#grab the partnerid and campaign attributes
			params_list = url_attributes.split('?')
			partner_id = params_list[0]
			pure_attributes = params_list[1]
			#print (partner_id)
			
			if (partner_id == find_partner_id):
				find_partner_count = find_partner_count + 1
				
				if(find_partner_campaign_id != ''):
					#break up the url key value pairs into campaign attributes
					campaign_attributes = dict(e.split('=') for e in pure_attributes.split('&'))
					
					#see if we have a campaign id in the attributes. If so, see if it's one we are looking for and count it
					if 'cid' in campaign_attributes:
						if (campaign_attributes['cid']==find_partner_campaign_id):
							find_partner_campaign_count = find_partner_campaign_count + 1
				
		print("Total callbacks for partner_id {0}: {1:,}".format(find_partner_id,find_partner_count))
		
		if(find_partner_campaign_id != ''):
			print("Total callbacks for partner_id {0} campaign {1}: {2:,}".format(find_partner_id,find_partner_campaign_id,find_partner_campaign_count))

#Main Program
parser = argparse.ArgumentParser(description='Search for partners and optionally, campaigns in a log file.')
parser.add_argument('p', help='a partner_id to search for')
parser.add_argument('-c', help='(optional) a campaign_id to search for')

args = parser.parse_args()
logfile = "elblogs.txt"

#sample data values
#find_partner_id = "nyr8nx"
#find_partner_campaign_id = "X9KN0"

find_partner_id = ""
find_partner_campaign_id = ""

if (args.p):
	find_partner_id = args.p
	
if (args.c):
	find_partner_campaign_id = args.c
	
partnerCampaignAnalysis(logfile,find_partner_id,find_partner_campaign_id)				
	