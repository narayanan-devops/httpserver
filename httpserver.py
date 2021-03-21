#!/usr/bin/env python3

###############################################################
# Set key "abc-1": curl -XPOST http://localhost:5000/set/abc-1?value=1
# Get key "abc-1": curl -XGET http://localhost:5000/get/abc-1
# Get all        : curl -XGET http://localhost:5000/get
# Clear all      : curl -XGET http://localhost:5000/clear
# Get by Suffix  : curl -XGET http://localhost:5000/search\?suffix\=c-1
# Get by Prefix  : curl -XGET http://localhost:5000/search\?prefix\=ab
###############################################################

from flask import Flask, jsonify, request, Response
import threading
import time

app = Flask(__name__)
lock = threading.Lock()

d = {}
d['data'] = {}
             
def update_thread():
    global d
    while True:
        with lock:
            d['api_server_uptime'] = d.get('api_server_uptime', 0) + 1
        time.sleep(1.0)
        
@app.route('/')
def base():
	status_code = Response(status=200)
	return status_code


@app.route('/clear', methods=['GET'])
def clear():
    global d
    with lock:
        d['data'] = {}
        return jsonify(d)

@app.route('/get', methods=['GET'])
def get():
    with lock:
        return jsonify(d)

@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    with lock:
        return jsonify(d['data'].get(name, {}))

@app.route('/set/<name>', methods=['POST'])
def set(name):
    global d
    with lock:
        d['data'][name] = d['data'].get(name, {})
        d['data'][name]['value'] = request.args.get('value') or float('nan')
        return jsonify(d)
    
@app.route('/search', methods=['GET'])
def search():
    global d
    with lock:
        if 'prefix' in request.args:
            prefix = request.args.get('prefix')
            res = {key:val for key, val in d['data'].items() if key.startswith(prefix)} 
            return jsonify(res)
        elif 'suffix' in request.args:
            suffix = request.args.get('suffix')
            res = {key:val for key, val in d['data'].items() if key.endswith(suffix)} 
            return jsonify(res)
        else:
            return jsonify("search api requires prefix or suffix argument to search")


if __name__ == '__main__':
    threading.Thread(target=update_thread).start()
    app.run(host="0.0.0.0", threaded=True, debug=True)
    

