#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import xlsxwriter


def read_input(path):
	d = []
	try:

		with open (path) as f:
			lines = f.readlines()
			for line in lines:
				d.append(line.rstrip('\n'))
			f.close()

	except Exception as e:
		print e
	
	finally:
		return d
def export_results (targets,ports):
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	try:
		print "Exporting the results in an excel"
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('sh0d4n.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "IP")
		worksheet.write(row, col+1, "Ports")
		row += 1
		# Iterate over the data and write it out row by row.
		for target in targets:
				col = 0
				worksheet.write(row, col, target)
				worksheet.write(row, col+1, ports[i])
				row += 1
				i += 1

		#Close the excel
		workbook.close()


	except Exception as e:
		print "Error in export_results" + str(e)

def manage_response (data):
	try:

		ports = str(data['ports']).replace("[","").replace("]","")
		print "\n[*]Target: " + str(data['ip_str'])
		print "Ports:"+ str(ports)
	except Exception as e:
		print "Error in manage_response" + str(e)

	finally:
		return ports

		
def send_request (url):

	response = None

	try:

		response = requests.get(url,timeout=5,allow_redirects =True)
	except Exception as e:
		print e

	finally:
		return response.json()

def banner():

	print"\n"
	print """
	                                                                                                              
		                                                           dddddddd                                   
		        hhhhhhh                  000000000                 d::::::d      444444444                    
		        h:::::h                00:::::::::00               d::::::d     4::::::::4                    
		        h:::::h              00:::::::::::::00             d::::::d    4:::::::::4                    
		        h:::::h             0:::::::000:::::::0            d:::::d    4::::44::::4                    
	    ssssssssss   h::::h hhhhh       0::::::0   0::::::0    ddddddddd:::::d   4::::4 4::::4  nnnn  nnnnnnnn    
	  ss::::::::::s  h::::hh:::::hhh    0:::::0     0:::::0  dd::::::::::::::d  4::::4  4::::4  n:::nn::::::::nn  
	ss:::::::::::::s h::::::::::::::hh  0:::::0     0:::::0 d::::::::::::::::d 4::::4   4::::4  n::::::::::::::nn 
	s::::::ssss:::::sh:::::::hhh::::::h 0:::::0 000 0:::::0d:::::::ddddd:::::d4::::444444::::444nn:::::::::::::::n
	 s:::::s  ssssss h::::::h   h::::::h0:::::0 000 0:::::0d::::::d    d:::::d4::::::::::::::::4  n:::::nnnn:::::n
	   s::::::s      h:::::h     h:::::h0:::::0     0:::::0d:::::d     d:::::d4444444444:::::444  n::::n    n::::n
	      s::::::s   h:::::h     h:::::h0:::::0     0:::::0d:::::d     d:::::d          4::::4    n::::n    n::::n
	ssssss   s:::::s h:::::h     h:::::h0::::::0   0::::::0d:::::d     d:::::d          4::::4    n::::n    n::::n
	s:::::ssss::::::sh:::::h     h:::::h0:::::::000:::::::0d::::::ddddd::::::dd         4::::4    n::::n    n::::n
	s::::::::::::::s h:::::h     h:::::h 00:::::::::::::00  d:::::::::::::::::d       44::::::44  n::::n    n::::n
	 s:::::::::::ss  h:::::h     h:::::h   00:::::::::00     d:::::::::ddd::::d       4::::::::4  n::::n    n::::n
	  sssssssssss    hhhhhhh     hhhhhhh     000000000        ddddddddd   ddddd       4444444444  nnnnnn    nnnnnn
		                                                                                                      
                                                                                                              
                                                                                                              
	"""
	print """
	** Tool to obtain information about the open ports throught API's Shodan.
    	** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    	** DISCLAMER This tool was developed for educational goals. 
    	** The author is not responsible for using to others goals.
    	** A high power, carries a high responsibility!
    	** Version 1.0"""

def main(argv):

	banner()
	target = str(sys.argv[1])
	API="YOUR_API_KEY"
	r = None
	ports = []
	array = read_input(target) 
	try:
		for ip in array:
			url = "https://api.shodan.io/shodan/host/"+ip+"?key="+API
			#Sent request
			r = send_request(url)
			# Manage the response
			port = manage_response(r)
			ports.append(port)

		#Export results		
		export_results(array,ports)

	except Exception as e:
		print "Error in main function" + str(e)


if __name__ == "__main__":
    main(sys.argv[1:])