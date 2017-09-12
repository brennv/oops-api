
from flask import Flask, jsonify, redirect


app = Flask(__name__)



@app.route('/')
def index():
    return 'hello'  # redirect('/api/spec/')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
