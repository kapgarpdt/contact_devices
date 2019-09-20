
#!/usr/bin/env python
#
# Copyright (c) 2016, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests
import json
import pandas
import datetime
import requests
import sys
import csv

#Your PagerDuty API key.  A read-only key will work for this.
AUTH_TOKEN = 'Msz4iBvMUp4FMRCm_Mr5'
#The API base url, make sure to include the subdomain
URL = 'https://api.pagerduty.com/users?include%5B%5D=contact_methods'
csvfile = "users_phone.csv"
PD_EMAIL = 'kapgar@pagerduty.com'

HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=AUTH_TOKEN),
		'Content-type': 'application/json',
		'From': PD_EMAIL
	}


user_count = 0

def get_user_count():
	global user_count
	count = requests.get(
		URL,
		headers=HEADERS
	)
	#print('Status Code: {code}'.format(code=count.status_code))
	#print(count.json())
	user_count = len(count.json()['users'])
	print(user_count)
        
def get_users(offset):
	global user_count
	params = {
		'offset':offset
	}
	all_users = requests.get(URL, headers=HEADERS, params=params)
	print "Exporting all users to " + csvfile
	for user in all_users.json()['users']:
		print(user['name'])
		for devices in user['contact_methods']:
			print(devices['type'])
			if devices['type'] == "sms_contact_method":
				phone = 'Yes Phone'
				break
			else:
				phone = 'No Phone'
		print(phone)
		with open(csvfile, "a") as output:
				writer = csv.writer(output, lineterminator='\n')
				writer.writerow([user['name'] + ', ' + phone])

def main(argv=None):
	if argv is None:
		argv = sys.argv
	get_user_count()
	for offset in xrange(0,user_count):
		if offset % 25 == 0:
			get_users(offset)

if __name__=='__main__':
	sys.exit(main())		







	