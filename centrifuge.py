from flask import Flask, abort, g, jsonify, request
app = Flask(__name__)

import sqlite
from crossdomain import crossdomain

SELECT_ALL_HISCORES = 'select * from hiscores order by score desc'
INSERT_NEW_HISCORE = 'insert into hiscores (username, score) values (?, ?)'
REPORT_ERROR = 'insert into errors values (?, ?, ?, ?)'

@app.route('/centrifuge/api/hiscores', methods=['GET'])
@crossdomain(origin='*')
def get_hiscores():
  return jsonify(hiscores=sqlite.query_db(SELECT_ALL_HISCORES))

@app.route('/centrifuge/api/hiscores', methods=['PUT'])
@crossdomain(origin='*')
def put_hiscore():
  if not request.json:
    abort(400)
  if not 'username' in request.json or not 'score' in request.json:
    abort(400)

  sqlite.query_db(INSERT_NEW_HISCORE, (request.json.get('username'),
                                       request.json.get('score')))
  return jsonify({'result': 'success'})

@app.route('/centrifuge/api/errors', methods=['PUT'])
@crossdomain(origin='*')
def put_error():
  if not request.json:
    abort(400)
  j = request.json
  sqlite.query_db(REPORT_ERROR, (j.get('message'), j.get('url'),
                                 j.get('line'), j.get('column')))
  return jsonify({'result': 'success'})

if __name__ == '__main__':
  app.run(debug=True)

