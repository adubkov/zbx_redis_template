#!/usr/bin/python
#
# This content is licensed GNU GPL v2
# Author: Alexey Dubkov <alexey.dubkov@gmail.com>
#
import sys, redis, json, re

host = (len(sys.argv) >= 2) and sys.argv[1] or 'localhost'
port = 6379
metric = (len(sys.argv) >= 3) and sys.argv[2]
db = (len(sys.argv) >= 4) and sys.argv[3] or 'none'

client = redis.StrictRedis(host=host, port=port)
server_info = client.info()

if metric:
	if db and db in server_info.keys():
		server_info['key_space_db_keys'] = server_info[db]['keys']
		server_info['key_space_db_expires'] = server_info[db]['expires']
		server_info['key_space_db_avg_ttl'] = server_info[db]['avg_ttl']
	
	def llen():
		print client.llen(db)

	def llensum():
		keys = client.keys('*')
		llensum = 0
		for key in keys:
			llensum += client.llen(key)
		print llensum

	def list_key_space_db():
		if db in server_info:
			print db
		else:
			print 'database_detect'

	def default():
		if metric in server_info.keys():
			print server_info[metric]


	{'llen': llen,
	 'llenall': llensum,
	 'list_key_space_db': list_key_space_db,
	}.get(metric, default)()

else:
	print 'Not selected metric';
