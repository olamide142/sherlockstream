
$(document).ready(function(){
    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/sherlock');

    //receive details from server
    var data_received = 0;

    socket.on('response', function(msg) {
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


    // Load File
    $.ajax({
        url: 'http://' + document.domain + ':' + location.port + '/fileview',
        type: 'GET',
        dataType: 'json', // added data type
        data: {"filename":"sherlock/code_viewer.py", "startline": 9, "endline":20},
        success: function(res) {
            $("#source_view").append(res.lines)
            console.log(res)
            var tarea = document.getElementById('source_view');
            selectTextareaLine(tarea,3);
        }

    });
});


function selectTextareaLine(tarea,lineNum) {
    lineNum--; // array starts at 0
    var lines = tarea.value.split("\n");

    // calculate start/end
    var startPos = 0, endPos = tarea.value.length;
    for(var x = 0; x < lines.length; x++) {
        if(x == lineNum) {
            break;
        }
        startPos += (lines[x].length+1);

    }

    var endPos = lines[lineNum].length+startPos;

    // do selection
    // Chrome / Firefox

    if(typeof(tarea.selectionStart) != "undefined") {
        tarea.focus();
        tarea.selectionStart = startPos;
        tarea.selectionEnd = endPos;
        return true;
    }

    // IE
    if (document.selection && document.selection.createRange) {
        tarea.focus();
        tarea.select();
        var range = document.selection.createRange();
        range.collapse(true);
        range.moveEnd("character", endPos);
        range.moveStart("character", startPos);
        range.select();
        return true;
    }

    return false;
}
