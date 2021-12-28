
$(document).ready(function(){
    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/sherlock');

    //receive details from server
    var data_received = [];

    socket.on('response', function(msg) {
        if (data_received.length >= 100){
            data_received.shift()
        }
        console.log(msg)
        var temp = msg.last_output.split("\r\n")
         for (var j = 0; j < temp.length; j++){
            var data_string = '<p>' + temp[j] + '</p>';
            $('#log').append(data_string);
        }
    });


    socket.on('connect', function() {
        console.log('HI');
    });


    $("#start_btn").click(function(){
        socket.emit("start_btn", {data:''});
    });
});