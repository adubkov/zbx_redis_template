#!/usr/bin/env node

// This software is licensed GNU GPL v2
// Author: Alexey Dubkov <alexey.dubkov@gmail.com>

var host = process.argv[2] || 'localhost',
    port = 6379,
    metric = process.argv[3],
    db = process.argv[4] || 'none';

var client = require('redis').createClient(port, host);

var llenall = i = rlen = 0;

client.on('llenall', function(v) {
    llenall += v;
    if (i == rlen) {
        console.log(llenall);
        client.emit('quit');
    }
});

client.on('ready', function(err) {

    if (metric) {

        if (db && client.server_info.hasOwnProperty(db)) {
            var t = client.server_info[db]
                .match('keys=(\\d+),expires=(\\d+),avg_ttl=(\\d+)');
            client.server_info.key_space_db_keys = t[1];
            client.server_info.key_space_db_expires = t[2];
            client.server_info.key_space_db_avg_ttl = t[3];
        }

        switch (metric) {
            case 'llen':
                client.llen(db, function(err, res) {
                    console.log(res);
                    client.emit('quit');
                });
                break;
            case 'llenall':
                client.keys('*', function(err, res) {
                    rlen = res.length;
                    res.map(function(v) {
                        client.llen(v, function(err, res) {
                            i++;
                            client.emit('llenall', res);
                        });
                    });
                });

                break;
            case 'list_key_space_db':
                if (client.server_info.db0) {
                    console.log('db0');
                } else
                    console.log('database_detect');
                client.emit('quit');
                break;
            case 'dbsize':
                if (client.server_info.db0) {
                    var res = {};
                    client.server_info.db0.split(',').map(function(el){
                        var _el = el.split('=');
                        res[_el[0]] = _el[1];
                    });
                    console.log(res.keys);
                } else
                    console.log('database_detect');
                client.emit('quit');
                break;
            default:
                if (client.server_info.hasOwnProperty(metric))
                    console.log(client.server_info[metric]);
                client.emit('quit');
                break;
        }
    } else {
        console.log('Not selected metric');
        client.emit('quit');
    }

});

client.on('error', function(err) {
    console.log('Error: ' + err);
});

client.on('quit', function() {
    client.quit();
});
