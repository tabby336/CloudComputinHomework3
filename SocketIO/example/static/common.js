function news_template(admin) {
    var resp = '<div class="row"> \
            <div class="col s12 m6">\
            <div class="card blue-grey darken-1">\
            <div class="card-content white-text">\
            <span class="card-number">%NUMBER%</span>\
            <span class="card-title">%TITLE%</span>\
            <p>%BODY%</p>\
            </div><form class="card-action" method="POST" action="#">'
    if(!admin) {
        resp += '<button class="btn waves-effect waves-light green" type="submit">Like</button>\
            <button class="btn waves-effect waves-light red" type="submit">Dislike</button>'
    } else {
        resp += '<input class="btn waves-effect waves-light red" type="submit" value="Delete">'
    }
    resp += '</form></div></div></div>'
    return resp
}

function beautify_news(msg,admin=false) {
    placeholders = {'%NUMBER%': msg.count, '%TITLE%': msg.data.title, '%BODY%': msg.data.body}
    var resp = news_template(admin).replace(/%\w+%/g, function(all) {
                        return placeholders[all] || all;
    });
    return resp
}