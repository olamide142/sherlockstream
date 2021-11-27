
var socket = io();

socket.on('connect', function() {
    console.log('HIT');
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('my response', function(msg) {
    $('#log').append('<p>Received: ' + msg.data + '</p>');
});