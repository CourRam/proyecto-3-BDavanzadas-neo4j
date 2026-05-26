// ============================================================
// schema.cypher
// Crear restricciones e indices para el esquema SCOTT en Neo4j
// ============================================================

// Restriccion de unicidad para nodos Department
CREATE CONSTRAINT dept_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.deptno IS UNIQUE;

// Restriccion de unicidad para nodos Employee
CREATE CONSTRAINT emp_unique IF NOT EXISTS
FOR (e:Employee) REQUIRE e.empno IS UNIQUE;

// Indice en nombre de empleado para busquedas rapidas
CREATE INDEX emp_ename IF NOT EXISTS
FOR (e:Employee) ON (e.ename);

// Indice en nombre de departamento
CREATE INDEX dept_dname IF NOT EXISTS
FOR (d:Department) ON (d.dname);
