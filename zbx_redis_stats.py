#!/usr/bin/python

import sys, redis, json, re, struct, time, socket

zabbix_host = '127.0.0.1'	# Zabbix Server IP
zabbix_port = 10051			# Zabbix Server Port
hostname = 'redis.srv.name'	# Name of monitored server like it shows in zabbix web ui display
redis_port = 6379			# Redis Server port

class Metric(object):
    def __init__(self, host, key, value, clock=None):
        self.host = host
        self.key = key
        self.value = value
        self.clock = clock

    def __repr__(self):
        if self.clock is None:
            return 'Metric(%r, %r, %r)' % (self.host, self.key, self.value)
        return 'Metric(%r, %r, %r, %r)' % (self.host, self.key, self.value, self.clock)

def send_to_zabbix(metrics, zabbix_host='127.0.0.1', zabbix_port=10051):
    
    j = json.dumps
    metrics_data = []
    for m in metrics:
        clock = m.clock or ('%d' % time.time())
        metrics_data.append(('{"host":%s,"key":%s,"value":%s,"clock":%s}') % (j(m.host), j(m.key), j(m.value), j(clock)))
    json_data = ('{"request":"sender data","data":[%s]}') % (','.join(metrics_data))
    data_len = struct.pack('<Q', len(json_data))
    packet = 'ZBXD\x01'+ data_len + json_data
    
    #print packet
    #print ':'.join(x.encode('hex') for x in packet)

    try:
        zabbix = socket.socket()
        zabbix.connect((zabbix_host, zabbix_port))
        zabbix.sendall(packet)
        resp_hdr = _recv_all(zabbix, 13)
        if not resp_hdr.startswith('ZBXD\x01') or len(resp_hdr) != 13:
            print ('Wrong zabbix response')
            return False
        resp_body_len = struct.unpack('<Q', resp_hdr[5:])[0]
        resp_body = zabbix.recv(resp_body_len)
        zabbix.close()

        resp = json.loads(resp_body)
        #print resp
        if resp.get('response') != 'success':
            print ('Got error from Zabbix: %s' % resp)
            return False
        return True
    except:
        print ('Error while sending data to Zabbix')
        return False


def _recv_all(sock, count):
    buf = ''
    while len(buf)<count:
        chunk = sock.recv(count-len(buf))
        if not chunk:
            return buf
        buf += chunk
    return buf



if len(sys.argv) <= 2:
	host = (len(sys.argv) >= 2) and sys.argv[1] or hostname

	client = redis.StrictRedis(host=host, port=redis_port)
	server_info = client.info()

	a = []
	for i in server_info:
		a.append(Metric(host, ('redis[%s]' % i), server_info[i]))

	keys = client.keys('*')
	llensum = 0
	for key in keys:
		llensum += client.llen(key)
	a.append(Metric(host, 'redis[llenall]', llensum))


	send_to_zabbix(a, zabbix_host, zabbix_port)

else:
	host = (len(sys.argv) >= 2) and sys.argv[1] or 'localhost'
	metric = (len(sys.argv) >= 3) and sys.argv[2]
	db = (len(sys.argv) >= 4) and sys.argv[3] or 'none'

	client = redis.StrictRedis(host=host, port=redis_port)
	server_info = client.info()

	if metric:
		if db and db in server_info.keys():
			server_info['key_space_db_keys'] = server_info[db]['keys']
			server_info['key_space_db_expires'] = server_info[db]['expires']
			server_info['key_space_db_avg_ttl'] = server_info[db]['avg_ttl']
		
		def llen():
			print (client.llen(db))

		def llensum():
			keys = client.keys('*')
			llensum = 0
			for key in keys:
				llensum += client.llen(key)
			print (llensum)

		def list_key_space_db():
			if db in server_info:
				print (db)
			else:
				print ('database_detect')

		def default():
			if metric in server_info.keys():
				print (server_info[metric])


		{
			'llen': llen,
		 	'llenall': llensum,
		 	'list_key_space_db': list_key_space_db,
		}.get(metric, default)()

	else:
		print ('Not selected metric');
