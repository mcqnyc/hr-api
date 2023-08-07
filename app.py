from flask import render_template
import config
from models import Employee

app = config.connex_app
app.add_api(config.basedir / "openapi-v1.yml")


@app.route("/")
def home():
    print('home fires')
    employees = Employee.query.all()
    print(employees)
    return render_template("home.html", employees=employees)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)