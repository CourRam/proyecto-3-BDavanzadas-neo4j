from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_query(cypher: str, parameters: dict = None) -> list[dict]:

    with driver.session() as session:
        result = session.run(cypher, parameters or {})
        return [record.data() for record in result]

def run_write(cypher: str, parameters: dict = None) -> None:
    with driver.session() as session:
        session.run(cypher, parameters or {})
