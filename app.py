"""
app.py
Aplicacion Flask para operaciones CRUD sobre Neo4j
Esquema: SCOTT (Department, Employee)
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from neo4j import GraphDatabase
import os

# ----------------------------------------------------------------
# Configuracion de la conexion a Neo4j
# Ajusta las variables de entorno o modifica los valores por defecto
# ----------------------------------------------------------------
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

app = Flask(__name__)
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ================================================================
# Funciones auxiliares para ejecutar consultas Cypher
# ================================================================

def run_query(cypher, parameters=None):
    """Ejecuta una consulta Cypher y devuelve todos los registros."""
    with driver.session() as session:
        result = session.run(cypher, parameters or {})
        return [record.data() for record in result]


def run_write(cypher, parameters=None):
    """Ejecuta una escritura Cypher (CREATE / MERGE / SET / DELETE)."""
    with driver.session() as session:
        session.run(cypher, parameters or {})


# ================================================================
# Rutas de la aplicacion
# ================================================================

@app.route("/")
def index():
    """Pagina principal: muestra resumen de nodos en la base de datos."""
    dept_count = run_query("MATCH (d:Department) RETURN count(d) AS total")[0]["total"]
    emp_count  = run_query("MATCH (e:Employee)   RETURN count(e) AS total")[0]["total"]
    return render_template("index.html", dept_count=dept_count, emp_count=emp_count)


# ----------------------------------------------------------------
# CRUD: Departamentos
# ----------------------------------------------------------------

@app.route("/departments")
def departments():
    """Lista todos los departamentos."""
    depts = run_query(
        "MATCH (d:Department) RETURN d.deptno AS deptno, d.dname AS dname, d.loc AS loc "
        "ORDER BY d.deptno"
    )
    return render_template("departments.html", departments=depts)


@app.route("/departments/create", methods=["GET", "POST"])
def create_department():
    """Crea un nuevo nodo Department."""
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
        return redirect(url_for("departments"))
    return render_template("dept_form.html", action="Crear", dept=None)


@app.route("/departments/edit/<int:deptno>", methods=["GET", "POST"])
def edit_department(deptno):
    """Actualiza un nodo Department existente."""
    if request.method == "POST":
        run_write(
            "MATCH (d:Department {deptno: $deptno}) SET d.dname = $dname, d.loc = $loc",
            {
                "deptno": deptno,
                "dname":  request.form["dname"].upper(),
                "loc":    request.form["loc"].upper(),
            }
        )
        return redirect(url_for("departments"))
    dept = run_query(
        "MATCH (d:Department {deptno: $deptno}) RETURN d.deptno AS deptno, d.dname AS dname, d.loc AS loc",
        {"deptno": deptno}
    )
    return render_template("dept_form.html", action="Editar", dept=dept[0] if dept else None)


@app.route("/departments/delete/<int:deptno>", methods=["POST"])
def delete_department(deptno):
    """Elimina un nodo Department y sus relaciones."""
    run_write(
        "MATCH (d:Department {deptno: $deptno}) DETACH DELETE d",
        {"deptno": deptno}
    )
    return redirect(url_for("departments"))


# ----------------------------------------------------------------
# CRUD: Empleados
# ----------------------------------------------------------------

@app.route("/employees")
def employees():
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


@app.route("/employees/create", methods=["GET", "POST"])
def create_employee():
    """Crea un nuevo nodo Employee y sus relaciones."""
    depts = run_query("MATCH (d:Department) RETURN d.deptno AS deptno, d.dname AS dname ORDER BY d.deptno")
    if request.method == "POST":
        empno  = int(request.form["empno"])
        deptno = int(request.form["deptno"])
        mgr    = request.form.get("mgr")
        mgr    = int(mgr) if mgr else None

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
        # Crear relacion REPORTS_TO si tiene jefe
        if mgr:
            run_write(
                """
                MATCH (e:Employee {empno: $empno}), (m:Employee {empno: $mgr})
                MERGE (e)-[:REPORTS_TO]->(m)
                """,
                {"empno": empno, "mgr": mgr}
            )
        return redirect(url_for("employees"))
    return render_template("emp_form.html", action="Crear", emp=None, depts=depts)


@app.route("/employees/edit/<int:empno>", methods=["GET", "POST"])
def edit_employee(empno):
    """Actualiza un nodo Employee y recrea sus relaciones."""
    depts = run_query("MATCH (d:Department) RETURN d.deptno AS deptno, d.dname AS dname ORDER BY d.deptno")
    if request.method == "POST":
        deptno = int(request.form["deptno"])
        mgr    = request.form.get("mgr")
        mgr    = int(mgr) if mgr else None

        # Actualizar propiedades
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
        # Recrear relacion WORKS_IN
        run_write(
            """
            MATCH (e:Employee {empno: $empno})-[r:WORKS_IN]->() DELETE r
            WITH e
            MATCH (d:Department {deptno: $deptno})
            MERGE (e)-[:WORKS_IN]->(d)
            """,
            {"empno": empno, "deptno": deptno}
        )
        # Recrear relacion REPORTS_TO
        run_write("MATCH (e:Employee {empno: $empno})-[r:REPORTS_TO]->() DELETE r", {"empno": empno})
        if mgr:
            run_write(
                """
                MATCH (e:Employee {empno: $empno}), (m:Employee {empno: $mgr})
                MERGE (e)-[:REPORTS_TO]->(m)
                """,
                {"empno": empno, "mgr": mgr}
            )
        return redirect(url_for("employees"))

    emp = run_query(
        "MATCH (e:Employee {empno: $empno}) RETURN e.empno AS empno, e.ename AS ename, "
        "e.job AS job, e.mgr AS mgr, e.hiredate AS hiredate, e.sal AS sal, "
        "e.comm AS comm, e.deptno AS deptno",
        {"empno": empno}
    )
    return render_template("emp_form.html", action="Editar", emp=emp[0] if emp else None, depts=depts)


@app.route("/employees/delete/<int:empno>", methods=["POST"])
def delete_employee(empno):
    """Elimina un nodo Employee y todas sus relaciones."""
    run_write(
        "MATCH (e:Employee {empno: $empno}) DETACH DELETE e",
        {"empno": empno}
    )
    return redirect(url_for("employees"))


# ----------------------------------------------------------------
# Vista de grafo (datos JSON para visualizacion)
# ----------------------------------------------------------------

@app.route("/graph")
def graph():
    """Pagina de visualizacion del grafo."""
    return render_template("graph.html")


@app.route("/api/graph-data")
def graph_data():
    """Devuelve nodos y relaciones en formato JSON para D3."""
    nodes_raw = run_query(
        """
        MATCH (n) WHERE n:Employee OR n:Department
        RETURN id(n) AS id, labels(n)[0] AS label,
               CASE WHEN n:Department THEN n.dname ELSE n.ename END AS name,
               properties(n) AS props
        """
    )
    rels_raw = run_query(
        """
        MATCH (a)-[r]->(b)
        WHERE (a:Employee OR a:Department) AND (b:Employee OR b:Department)
        RETURN id(a) AS source, id(b) AS target, type(r) AS type
        """
    )
    return jsonify({"nodes": nodes_raw, "links": rels_raw})


# ----------------------------------------------------------------
# Punto de entrada
# ----------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
