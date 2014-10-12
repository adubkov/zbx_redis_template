#!/usr/bin/python

import sys, redis, json, re, struct, time, socket, argparse

parser = argparse.ArgumentParser(description='Zabbix Redis status script')
parser.add_argument('hostname',nargs='?')
parser.add_argument('metric',nargs='?')
parser.add_argument('db',default='none',nargs='?')
parser.add_argument('-p','--port',dest='redis_port',action='store',help='Redis server port',default=6379,type=int)
parser.add_argument('-a','--auth',dest='redis_pass',action='store',help='Redis server pass',default=None)
args = parser.parse_args()

zabbix_host = '127.0.0.1'	# Zabbix Server IP
zabbix_port = 10051			# Zabbix Server Port
hostname = 'redis.srv.name'	# Name of monitored server like it shows in zabbix web ui display

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



if args.hostname and args.metric:
        client = redis.StrictRedis(host=args.hostname, port=args.redis_port, password=args.redis_pass)
	server_info = client.info()

	if args.metric:
		if args.db and args.db in server_info.keys():
			server_info['key_space_db_keys'] = server_info[args.db]['keys']
			server_info['key_space_db_expires'] = server_info[args.db]['expires']
			server_info['key_space_db_avg_ttl'] = server_info[args.db]['avg_ttl']
		
		def llen():
			print (client.llen(args.db))

		def llensum():
			keys = client.keys('*')
			llensum = 0
			for key in keys:
				llensum += client.llen(key)
			print (llensum)

		def list_key_space_db():
			if args.db in server_info:
				print (args.db)
			else:
				print ('database_detect')

		def default():
			if args.metric in server_info.keys():
				print (server_info[args.metric])


		{
			'llen': llen,
		 	'llenall': llensum,
		 	'list_key_space_db': list_key_space_db,
		}.get(args.metric, default)()

	else:
		print ('Not selected metric');
else:

	client = redis.StrictRedis(host=args.hostname, port=args.redis_port, password=args.redis_pass)
	server_info = client.info()

	a = []
	for i in server_info:
		a.append(Metric(args.hostname, ('redis[%s]' % i), server_info[i]))

	keys = client.keys('*')
	llensum = 0
	for key in keys:
		llensum += client.llen(key)
	a.append(Metric(args.hostname, 'redis[llenall]', llensum))


	send_to_zabbix(a, zabbix_host, zabbix_port)
