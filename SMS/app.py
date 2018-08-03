from flask import Flask, request
import SMS.db.api as db_api
from SMS.db import session as session_utils
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to the Supercalifragilisticexpialidocius Monitoring\
            System (SMS)</h1>'


@session_utils.ensure_session
@app.route('/metrics')
def metrics():
    query_str = str(request.query_string)
    if 'host' in query_str:
        hostname = request.args['host']
    if 'type' in query_str:
        m_type = request.args['type']
    return db_api.resp_flask(hostname=hostname, m_type=m_type).__str__()
    # TODO return html template

# if __name__ == '__main__':
#     app.run(debug=True)
