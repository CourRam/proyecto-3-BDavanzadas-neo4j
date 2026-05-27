// Departamentos 
MERGE (d1:Department {deptno: 10}) SET d1.dname = 'ACCOUNTING', d1.loc = 'NEW YORK';
MERGE (d2:Department {deptno: 20}) SET d2.dname = 'RESEARCH',   d2.loc = 'DALLAS';
MERGE (d3:Department {deptno: 30}) SET d3.dname = 'SALES',      d3.loc = 'CHICAGO';
MERGE (d4:Department {deptno: 40}) SET d4.dname = 'OPERATIONS', d4.loc = 'BOSTON';

// WORKS_IN: Empleado -> Departamento 
MATCH (e:Employee), (d:Department) WHERE e.deptno = d.deptno
MERGE (e)-[:WORKS_IN]->(d);

// MANAGES: Empleado -> Jefe directo 
MATCH (e:Employee), (m:Employee) WHERE e.mgr = m.empno
MERGE (e)-[:REPORTS_TO]->(m);

//res
CREATE CONSTRAINT dept_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.deptno IS UNIQUE;

CREATE CONSTRAINT emp_unique IF NOT EXISTS
FOR (e:Employee) REQUIRE e.empno IS UNIQUE;

