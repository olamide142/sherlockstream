$(document).ready(function () {
    
    var socket = io();
    
    socket.on('myz_respzonse', function (msg) {
        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });
    
    $('form#emit').submit(function (event) {
        socket.emit('my event', { data: $('#emit_data').val() });
        return false;
    });
    
    $('form#broadcast').submit(function (event) {
        socket.emit('my broadcast event', { data: $('#broadcast_data').val() });
        return false;
    });

});

