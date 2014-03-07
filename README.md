#zbx_redis_template

Zabbix template for Redis (node.js or python)
##System requirements

### For use node.js version script
- [node.js](https://github.com/joyent/node) 
- [node_redis](https://github.com/mranney/node_redis)

### For use python version script
- [python](http://www.python.org/downloads/) 
- [redis-py](https://github.com/andymccurdy/redis-py)

##Install

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
