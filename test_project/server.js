var server = require('http').createServer();
var PythonShell = require('python-shell');

var io = require('socket.io')(server);
io.on('connection', function(client){
    console.log("connected", client.id)
    client.on('chat', function(data) {
        io.emit('chat', data)
        PythonShell.run('./chat.py', {args: [data.email, data.message]}, function (err, data) {
            console.log(err, data)

        });

    });
    client.on('disconnect', function(){});
});
server.listen(3000);