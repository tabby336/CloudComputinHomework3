$.getScript("static/common.js");

//var person = prompt("Please enter your name", "Batman");

got_old = false;
$(document).ready(function() {
    namespace = '/news';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.emit('get_news');

    socket.on('got_news', function(msg) {
        for(i in msg) {
            v = {'count': i, 'data': msg[i]}
            console.log(v)
            var resp = beautify_news(v);
            $('#log').append(resp).html();
        }
        return
    });
    
    socket.on('my_response', function(msg) {
        return
    });

    socket.on('added_news', function(msg) {
        var resp = beautify_news(msg);
        $('#log').append(resp).html();
    });

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    var max_latency = 0;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('my_ping');
    }, 1000);

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.
    socket.on('my_pong', function() {
        var latency = (new Date).getTime() - start_time;
        if(max_latency < latency) {
            max_latency = latency
        }
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
        $('#cpu-usage').text(max_latency);
    });


});
