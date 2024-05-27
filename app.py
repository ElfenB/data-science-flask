from time import sleep
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def starting_point():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    # Get the data from the form
    data = request.form

    # Print the data to the console
    for key, value in data.items():
        print(f"{key}: {value}")

    # Calculate the result using model (display waiting screen)
    sleep(2)    # Simulate a long calculation
    result = "69.420 €"

    # Return the result
    return redirect(url_for("result", result=result))


@app.route("/result", methods=["GET"])
def result():
    return render_template("result.html", result=request.args.get("result"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
