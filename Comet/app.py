#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import json
import unicodedata

app = Flask(__name__, static_url_path = "", static_folder = "static")

NEWS_COUNT = 0
OLD_COUNT = 0
NEWS = {}


@app.route('/', methods = ['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/admin', methods = ['GET'])
def admin():
	return app.send_static_file('admin.html')

@app.route('/js.js', methods = ['GET'])
def js():
	return app.send_static_file('js.js')

@app.route('/add_news', methods = ['POST'])
def add_news():
	global NEWS_COUNT, NEWS_COUNT
	NEWS_COUNT += 1
	NEWS[NEWS_COUNT] = {'text':request.json, 'liked':[]}
	#NEWS[NEWS_COUNT]['liked'] = []
	return jsonify({'count': NEWS_COUNT, 'data': NEWS[NEWS_COUNT]});

@app.route('/reacted', methods = ['POST'])
def reacted():
	print request.json
	return "caca"

@app.route('/longpoller', methods = ['GET'])
def longpoller():
	global OLD_COUNT, NEWS_COUNT, NEWS
	if OLD_COUNT <= NEWS_COUNT:
		new_dict = [{"count": k, "data": NEWS[k]} for k in range(1,NEWS_COUNT+1) if k >= OLD_COUNT]
		print OLD_COUNT, NEWS_COUNT
		print new_dict
		OLD_COUNT = NEWS_COUNT + 1
		return jsonify(new_dict)
	else:
		return "no"

if __name__ == '__main__':
    app.run(debug = True)