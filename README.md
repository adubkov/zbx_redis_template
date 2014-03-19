#zbx_redis_template

Zabbix template for Redis (node.js or python)
##System requirements

### For use node.js version script
- [node.js](https://github.com/joyent/node) 
- [node_redis](https://github.com/mranney/node_redis)

### For use python version script
- [python](http://www.python.org/downloads/) 
- [redis-py](https://github.com/andymccurdy/redis-py)


## Install
You can monitor your redis in zabbix agent mode or through trap-messages.

In zabbix agent mode, zabbix will periodically send request to an agent for every parameter, and agent will answer it.

In trap-message mode, script will be periodically accumulate redis's parameters and will send it to zabbix as a one message.

If you planning to capture many redis parameters and do it often. I would recomend  to use trap-message mode.

Note: trap-message works only on python version of script

### Install in trap-message mode

1) Put `zbx_redis_stats.py` into your monitoring scripts path (like: `/etc/zabbix/script/redis/`).

2) Change next section in zbx_redis_stats.py, to your configuration:
'''
zabbix_host = '127.0.0.1'	# Zabbix Server IP
zabbix_port = 10051			# Zabbix Server Port
hostname = 'redis.srv.name'	# Name of monitored server like it shows in zabbix web ui display
redis_port = 6379			# Redis Server port
'''

3) In script path (`/etc/zabbix/script/redis/`) do:
```
pip install redis
chmod +x zbx_redis_stats.py
```

4) Configure cron to run script every one minute:
'''
$ sudo crontab -e

*/1  *    *   *     *       /etc/zabbix/script/nginx/zbx_redis_module.py
'''

5) Import `zbx_redis_trapper_template.xml` into zabbix in Tepmplate section web gui.

That is all :)

### Install in Zabbix Agent mode

1) Put `zbx_redis.conf` into your `zabbix_agentd.conf` config subdirectory (like: `/etc/zabbix/zabbix_agentd.d/`).

2) Change script name in `zbx_redis.conf` to use `zbx_redis_stats.py` if need it (by default there is a .js version script).

3) Change your zabbix_agentd.conf config so it will include this file:
```
Include=/etc/zabbix/zabbix_agentd.d/
```
4) Put `zbx_redis_stats.js` or `zbx_redis_stats.py` into your `zabbix_agentd.conf` config subdirectory (like: `/etc/zabbix/script/redis/`).

5) Change paths in `zbx_redis.conf` if need it.

6) In working dir (`/etc/zabbix/script/redis/`) do:

For use node.js verson script:
```
npm install redis
chmod +x zbx_redis_stats.js
```

For use python verson script:
```
pip install redis
chmod +x zbx_redis_stats.py
```
7) Import `zbx_redis_template.xml` into zabbix in Tepmplate section web gui.
