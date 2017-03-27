var name = prompt("Please enter your name", "Batman");

function tryy(num) {
	$.ajax({
		type:'POST',
		contentType:"application/json",
		url: "/reacted",
		async: false,
		data: JSON.stringify('{"user":"' + name + '"", "news":"' + num + '""}'),
		success: function(result) {
			console.log(result)
		}
	});
	console.log("am here")
	console.log(num)
}

function append_news(result) {
	data = JSON.parse(result.data.text)
	resp = '<form class="new" action="javascript:tryy('+result.count+')"> \
			<div class="row"> \
            <div class="col s12 m6">\
            <div class="card blue-grey darken-1">\
            <div class="card-content white-text">\
            <span class="card-number">' + result.count +'</span>\
            <span class="card-title">' + data.title + '</span>\
            <p>' + data.body + '</p>\
            <input class="like btn waves-effect waves-light green" type="submit" value="Like">\
            </div></div></div></div></form>'
    return resp
}

function add_news() {
	$.ajax({
		type: 'POST',
		contentType: "application/json",
		url: '/add_news',
		async: false,
		data: JSON.stringify('{"title":"' + $('#emit_news_title').val() + '",\
			"body":"' + $('#emit_news_body').val()+ '" }'),
		success: function(result) {
			console.log(result)
			$('#log').append(append_news(result)).html();
		}
	});

}