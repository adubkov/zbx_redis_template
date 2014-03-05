#!/usr/local/bin/node
#
# This content is licensed GNU GPL v2
# Author: Alexey Dubkov <alexey.dubkov@gmail.com>
#

var host = process.argv[2] || 'localhost',
    port = 6379,
    metric = process.argv[3],
    db = process.argv[4];

var client = require('redis').createClient(port, host);

client.on("error", function(err){
    console.log('Error: ' + err);
});

client.on("ready", function(err){

    if (metric) {

        if (db && client.server_info.hasOwnProperty(db)) {
            var t = client.server_info[db].match("keys=(\\d+),expires=(\\d+),avg_ttl=(\\d+)");
            client.server_info.key_space_db_keys = t[1];
            client.server_info.key_space_db_expires = t[2];
            client.server_info.key_space_db_avg_ttl = t[3];
        }

        switch(metric) {
            case 'llen':
                client.llen(process.argv[4], function(err, res){console.log(res);});
                break;
            case 'list_key_space_db':
                if (client.server_info.db0) {
                    console.log('db0');
                } else
                    console.log('database_detect');
                break;
            default:
                if (client.server_info.hasOwnProperty(metric))
                    console.log(client.server_info[metric]);
                break;
        }
    } else {
        console.log("Not selected metri");
    }

    client.quit();

});