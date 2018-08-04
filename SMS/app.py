from flask import Flask, request, render_template

import SMS.db.api as db_api
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to the Supercalifragilisticexpialidocius Monitoring\
            System (SMS)</h1>'


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
    return render_template('metric.html', resp_list=response_list)
    # TODO return html template

# if __name__ == '__main__':
#     app.run(debug=True)
