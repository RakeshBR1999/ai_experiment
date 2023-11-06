from flask import Flask
from flask import render_template, request

app = Flask(__name__)

from model.model import myGpt
input_function = myGpt()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = input_function.main(user_input)
        print(response)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
