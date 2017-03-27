$.getScript("static/common.js");

$(document).ready(function() {

    namespace = '/news';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('my_response', function(msg) {
        return false;
    });

    $('form#news').submit(function(event) {
        socket.emit('add_news', { title: $('#emit_news_title').val(),
                                   body: $('#emit_news_body').val() });
        return false;
    });


    socket.on('added_news', function(msg) {
        var resp = beautify_news(msg, true);
        $('#log').append(resp).html();
    });
});