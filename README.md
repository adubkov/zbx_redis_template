#zbx_redis_template

Zabbix template for Redis (written on node.js)
##System requirements

- [node.js](https://github.com/joyent/node)
- [node_redis](https://github.com/mranney/node_redis)

##Install

1) Put `zbx_redis.conf` into your `zabbix_agentd.conf` config subdirectory (like: `/etc/zabbix/zabbix_agentd.d/`).

2) Change your zabbix_agentd.conf config so it will include this file:
```
Include=/etc/zabbix/zabbix_agentd.d/
```
3) Put `zbx_redis_stats.js` into your `zabbix_agentd.conf` config subdirectory (like: `/etc/zabbix/script/redis/`).

4) Change paths in `zbx_redis.conf` if need it.

5) In working dir (`/etc/zabbix/script/redis/`) do:
```
chmod +x zbx_redis_stats.js
npm install redis
```
6) Import `zbx_redis_template.xml` into zabbix in Tepmplate section web gui.
