from flask import Blueprint, render_template, request, redirect, url_for
from db import run_query, run_write

bp = Blueprint("departments", __name__, url_prefix="/departments")


@bp.route("/")
def index():
    depts = run_query(
        "MATCH (d:Department) "
        "RETURN d.deptno AS deptno, d.dname AS dname, d.loc AS loc "
        "ORDER BY d.deptno"
    )
    return render_template("departments.html", departments=depts)


@bp.route("/create", methods=["GET", "POST"])
def create():
    
    if request.method == "POST":
        data = {
            "deptno": int(request.form["deptno"]),
            "dname":  request.form["dname"].upper(),
            "loc":    request.form["loc"].upper(),
        }
        run_write(
            "CREATE (d:Department {deptno: $deptno, dname: $dname, loc: $loc})",
            data
        )
        return redirect(url_for("departments.index"))
    return render_template("dept_form.html", action="Crear", dept=None)


@bp.route("/edit/<int:deptno>", methods=["GET", "POST"])
def edit(deptno):
    if request.method == "POST":
        run_write(
            "MATCH (d:Department {deptno: $deptno}) SET d.dname = $dname, d.loc = $loc",
            {
                "deptno": deptno,
                "dname":  request.form["dname"].upper(),
                "loc":    request.form["loc"].upper(),
            }
        )
        return redirect(url_for("departments.index"))

    dept = run_query(
        "MATCH (d:Department {deptno: $deptno}) "
        "RETURN d.deptno AS deptno, d.dname AS dname, d.loc AS loc",
        {"deptno": deptno}
    )
    return render_template("dept_form.html", action="Editar", dept=dept[0] if dept else None)


@bp.route("/delete/<int:deptno>", methods=["POST"])
def delete(deptno):
    run_write(
        "MATCH (d:Department {deptno: $deptno}) DETACH DELETE d",
        {"deptno": deptno}
    )
    return redirect(url_for("departments.index"))
