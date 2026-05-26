from flask import Blueprint, render_template, jsonify
from db import run_query

bp = Blueprint("graph", __name__, url_prefix="/graph")


@bp.route("/")
def index():
    """Página de visualización del grafo."""
    return render_template("graph.html")


@bp.route("/api/data")
def data():
    """Devuelve nodos y relaciones en formato JSON para D3."""
    nodes = run_query(
        """
        MATCH (n) WHERE n:Employee OR n:Department
        RETURN id(n) AS id, labels(n)[0] AS label,
               CASE WHEN n:Department THEN n.dname ELSE n.ename END AS name,
               properties(n) AS props
        """
    )
    links = run_query(
        """
        MATCH (a)-[r]->(b)
        WHERE (a:Employee OR a:Department) AND (b:Employee OR b:Department)
        RETURN id(a) AS source, id(b) AS target, type(r) AS type
        """
    )
    return jsonify({"nodes": nodes, "links": links})
