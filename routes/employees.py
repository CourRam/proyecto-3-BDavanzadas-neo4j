from flask import Blueprint, render_template, request, redirect, url_for
from db import run_query, run_write

bp = Blueprint("employees", __name__, url_prefix="/employees")


def _get_departments() -> list[dict]:
    """Devuelve todos los departamentos para los formularios."""
    return run_query(
        "MATCH (d:Department) RETURN d.deptno AS deptno, d.dname AS dname ORDER BY d.deptno"
    )


def _create_works_in(empno: int, deptno: int) -> None:
    """Elimina la relación WORKS_IN previa y crea la nueva."""
    run_write(
        """
        MATCH (e:Employee {empno: $empno})-[r:WORKS_IN]->() DELETE r
        WITH e
        MATCH (d:Department {deptno: $deptno})
        MERGE (e)-[:WORKS_IN]->(d)
        """,
        {"empno": empno, "deptno": deptno}
    )


def _create_reports_to(empno: int, mgr: int | None) -> None:
    """Elimina la relación REPORTS_TO previa y, si hay jefe, crea la nueva."""
    run_write(
        "MATCH (e:Employee {empno: $empno})-[r:REPORTS_TO]->() DELETE r",
        {"empno": empno}
    )
    if mgr:
        run_write(
            """
            MATCH (e:Employee {empno: $empno}), (m:Employee {empno: $mgr})
            MERGE (e)-[:REPORTS_TO]->(m)
            """,
            {"empno": empno, "mgr": mgr}
        )


# ----------------------------------------------------------------
# Rutas
# ----------------------------------------------------------------

@bp.route("/")
def index():
    """Lista todos los empleados con el nombre de su departamento."""
    emps = run_query(
        """
        MATCH (e:Employee)
        OPTIONAL MATCH (e)-[:WORKS_IN]->(d:Department)
        RETURN e.empno AS empno, e.ename AS ename, e.job AS job,
               e.sal AS sal, e.comm AS comm, e.hiredate AS hiredate,
               e.mgr AS mgr, d.dname AS dname, d.deptno AS deptno
        ORDER BY e.empno
        """
    )
    return render_template("employees.html", employees=emps)


@bp.route("/create", methods=["GET", "POST"])
def create():
    """Crea un nuevo nodo Employee y sus relaciones."""
    depts = _get_departments()
    if request.method == "POST":
        empno  = int(request.form["empno"])
        deptno = int(request.form["deptno"])
        mgr    = int(request.form["mgr"]) if request.form.get("mgr") else None

        run_write(
            """
            CREATE (e:Employee {
                empno:    $empno,
                ename:    $ename,
                job:      $job,
                mgr:      $mgr,
                hiredate: $hiredate,
                sal:      $sal,
                comm:     $comm,
                deptno:   $deptno
            })
            WITH e
            MATCH (d:Department {deptno: $deptno})
            MERGE (e)-[:WORKS_IN]->(d)
            """,
            {
                "empno":    empno,
                "ename":    request.form["ename"].upper(),
                "job":      request.form["job"].upper(),
                "mgr":      mgr,
                "hiredate": request.form["hiredate"],
                "sal":      float(request.form["sal"]),
                "comm":     float(request.form["comm"]) if request.form.get("comm") else None,
                "deptno":   deptno,
            }
        )
        _create_reports_to(empno, mgr)
        return redirect(url_for("employees.index"))

    return render_template("emp_form.html", action="Crear", emp=None, depts=depts)


@bp.route("/edit/<int:empno>", methods=["GET", "POST"])
def edit(empno):
    """Actualiza un nodo Employee y recrea sus relaciones."""
    depts = _get_departments()
    if request.method == "POST":
        deptno = int(request.form["deptno"])
        mgr    = int(request.form["mgr"]) if request.form.get("mgr") else None

        run_write(
            """
            MATCH (e:Employee {empno: $empno})
            SET e.ename    = $ename,
                e.job      = $job,
                e.mgr      = $mgr,
                e.hiredate = $hiredate,
                e.sal      = $sal,
                e.comm     = $comm,
                e.deptno   = $deptno
            """,
            {
                "empno":    empno,
                "ename":    request.form["ename"].upper(),
                "job":      request.form["job"].upper(),
                "mgr":      mgr,
                "hiredate": request.form["hiredate"],
                "sal":      float(request.form["sal"]),
                "comm":     float(request.form["comm"]) if request.form.get("comm") else None,
                "deptno":   deptno,
            }
        )
        _create_works_in(empno, deptno)
        _create_reports_to(empno, mgr)
        return redirect(url_for("employees.index"))

    emp = run_query(
        "MATCH (e:Employee {empno: $empno}) "
        "RETURN e.empno AS empno, e.ename AS ename, e.job AS job, e.mgr AS mgr, "
        "e.hiredate AS hiredate, e.sal AS sal, e.comm AS comm, e.deptno AS deptno",
        {"empno": empno}
    )
    return render_template("emp_form.html", action="Editar", emp=emp[0] if emp else None, depts=depts)


@bp.route("/delete/<int:empno>", methods=["POST"])
def delete(empno):
    """Elimina un nodo Employee y todas sus relaciones."""
    run_write(
        "MATCH (e:Employee {empno: $empno}) DETACH DELETE e",
        {"empno": empno}
    )
    return redirect(url_for("employees.index"))
