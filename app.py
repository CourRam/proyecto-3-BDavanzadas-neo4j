from flask import Flask, render_template
from db import run_query

# Importar blueprints
from routes.departments import bp as departments_bp
from routes.employees   import bp as employees_bp

app = Flask(__name__)


app.register_blueprint(departments_bp)
app.register_blueprint(employees_bp)

@app.route("/")
def index():
    dept_count = run_query("MATCH (d:Department) RETURN count(d) AS total")[0]["total"]
    emp_count  = run_query("MATCH (e:Employee)   RETURN count(e) AS total")[0]["total"]
    return render_template("index.html", dept_count=dept_count, emp_count=emp_count)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
