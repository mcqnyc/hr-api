import config

from flask import render_template

from models import Employee

app = config.connex_app
app.add_api(config.basedir / "openapi-v1.yml")


@app.route("/")
def home():
    employees = Employee.query.all()
    return render_template("home.html", employees=employees)


@app.route("/status")
def status():
    return {"status": "OK"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
