import json
# from datetime import datetime

from flask import Flask, request

import SMS.db.api as db_api
import SMS.db.models as mods

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to the Supercalifragilisticexpialidocius Monitoring\
            System (SMS)</h1>'


# def json_builder(usage):
#     return {
#         "hostname": usage.hostname,
#         "timestamp": datetime.strftime(usage.timestamp, "%Y-%m-%dT%H:%M:%S"),
#         "metric_type": usage.metric_type,
#         "metric_value": usage.metric_value,
#         "metric_unit": usage.metric_unit
#     }


@app.route('/metrics')
def metrics():
    hostname = None
    m_type = None
    start_time = None
    end_time = None
    query_str = str(request.query_string)
    if 'host' in query_str:
        hostname = request.args['host']
    if 'type' in query_str:
        m_type = request.args['type']
    if 'start_time' in query_str:
        start_time = request.args['start_time']
    if 'end_time' in query_str:
        end_time = request.args['end_time']
    response_list = db_api.resp_flask(hostname=hostname, m_type=m_type,
                                      start_time=start_time,
                                      end_time=end_time)

    response_list = [mods.ModelJsonEncoder(elem) for elem in response_list]
    return json.dumps({'metrics': response_list})

# if __name__ == '__main__':
#     app.run(debug=True)
