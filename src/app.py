import os
import shutil
import tempfile
import time

import redis
from flask import render_template, Flask, request

from utils.pypi import PypiUtil

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index(name=None):
    if request.method == 'POST':
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
        return render_template('pypi-result.html', data=lib_data, time=time.time() - start_time)

    else:
        return render_template('index.html', name=name)


@app.route('/clear-cache')
def clear():
    redis.StrictRedis(host=os.environ['REDIS_HOST'],
                      port=os.environ['REDIS_PORT'],
                      db=os.environ['REDIS_DB'],
                      password=os.environ['REDIS_PASSWORD']).flushdb()

    return "Done!"

# @app.template_filter()
# def format_time_seconds(time: str):
#     return time.
#     pass
