from datetime import datetime as dt
import re

services = {}
timeformat = "%Y-%m-%dT%H:%M:%S,%f"
logfile = None

try:
	logfile = open("/code/log/test.log", "r")
except Exception as e:
	print("Error opening log file: " + str(e))



def parse_log(logfile):
	global services, timeformat
	if(logfile):
		for line in logfile:
			time = line.split()[0]
			request = []
			request_name_id = re.findall("\(.*?\)",line)[0]
			request_name_id = request_name_id.replace('(','')
			request_name_id = request_name_id.replace(')','')
			request_name_id = request_name_id.split(':')
			request_name = request_name_id[0]
			request_id = request_name_id[1]
			if request_name not in services:
				services[request_name] = []
				services[request_name].append({"id":request_id,"entry_time":time}) 
			else:
				request_found = False
				for num, request in enumerate(services[request_name]):
					if request['id'] == request_id:
						services[request_name][num]['exit_time'] = time
						entry = dt.strptime(request['entry_time'], timeformat ) 
						exit = dt.strptime(time,timeformat)
						diff = (exit-entry).total_seconds()
						services[request_name][num]['excecution_time']= diff
						request_found = True	
						break
				if request_found == False:
					request_entry = {'id':request_id,'entry_time':time}
					services[request_name].append(request_entry)



if __name__ == "__main__":
	parse_log(logfile)	
	#print(services)
	print("===============================================")
	for service in services:
		requests = services[service]
		exec_times = []
		for request in requests:
			if(request['excecution_time']):
				exec_times.append(request['excecution_time'])
		print("Service Name: " + str(service))
		print("Number of requests: " + str(len(requests)))
		print("Maximum execution time: " + str(max(exec_times)) + ' seconds')		
		print("-----------------------------------------------")
	print("===============================================")

