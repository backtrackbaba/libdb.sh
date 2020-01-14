import os
import shutil
import tempfile
import time

import redis
from flask import render_template, Flask, request, redirect

from utils.node import NodeUtil
from utils.pypi import PypiUtil

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/python', methods=["GET"])
def python():
    return render_template('python/python.html')


@app.route('/python/results', methods=["POST"])
def python_results():
    if request.method == "GET":
        return redirect('/')
    else:
        start_time = time.time()
        raw_data = request.form['nm'].rstrip()
        tmpdir = tempfile.mkdtemp()

        requirements_path = f'{tmpdir}/requirements.txt'
        with open(requirements_path, 'w') as fd:
            fd.write(raw_data)

        pypi = PypiUtil()
        req_object = pypi.parse_requrements(requirements_path)
        lib_data = pypi.fetch_info(req_object)
        shutil.rmtree(tmpdir)
        return render_template('python/result.html', data=lib_data, time=time.time() - start_time)


@app.route('/node', methods=["GET"])
def node():
    return render_template('node/node.html')


@app.route('/node/results', methods=["GET", "POST"])
def node_results():
    if request.method == "GET":
        return redirect('/')
    else:
        start_time = time.time()
        raw_data = request.form['nm'].rstrip()
        tmpdir = tempfile.mkdtemp()

        package_path = f'{tmpdir}/package.json'
        with open(package_path, 'w') as fd:
            fd.write(raw_data)

        node_util = NodeUtil()
        req_object = node_util.parse_package(package_path)
        lib_data = node_util.fetch_info(req_object)
        shutil.rmtree(tmpdir)
        return render_template('node/result.html', data=lib_data, time=time.time() - start_time)


@app.route('/clear-cache')
def clear():
    redis.StrictRedis(host=os.environ['REDIS_HOST'],
                      port=os.environ['REDIS_PORT'],
                      db=os.environ['REDIS_DB'],
                      password=os.environ['REDIS_PASSWORD']).flushdb()

    return "Done!"
