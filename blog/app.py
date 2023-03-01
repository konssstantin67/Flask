from flask import Flask
from flask import request
from flask import g
from time import time

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to my site'


@app.route('/user/')
def read_user():  # put application's code here
    name = request.args.get('name')
    surname = request.args.get('surname')
    return f"Username {name or ['noname']} Usersurname {surname or ['nosurname']}"


@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
    To get response with custom status code
    send request using POST method
    and pass `code` in JSON body / FormData
    """
    print("raw bytes data:", request.data)
    if request.form and "code" in request.form:
        return "code from form", request.form["code"]
    if request.json and "code" in request.json:
        return "code from json", request.json["code"]
    return "", 204


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    return response
