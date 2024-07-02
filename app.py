import os
import logging
from time import sleep
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask.logging import create_logger
from werkzeug.serving import make_server

# CONFIG
port = os.environ.get("PORT", 8080)
host = os.environ.get("HOST", "0.0.0.0")

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = create_logger(app)


@app.route("/", methods=["GET"])
def starting_point():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    # Get the data from the form
    data = request.form

    # Print the data to the console
    for key, value in data.items():
        logger.debug(f"{key}: {value}")

    # Calculate the result using model (display waiting screen)
    sleep(2)    # Simulate a long calculation
    result = "69.420 €"

    # Return the result
    return redirect(url_for("result", result=result))


@app.route("/result", methods=["GET"])
def result():
    return render_template("result.html", result=request.args.get("result"))


def run_flask_app(app):
    global server
    server = make_server(host, port, app)
    logger.info(f'Starting server on http://{host}:{port}')
    server.serve_forever()


if __name__ == "__main__":
    run_flask_app(app)
