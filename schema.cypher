// Restriccion de unicidad para nodos Department
CREATE CONSTRAINT dept_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.deptno IS UNIQUE;

// Restriccion de unicidad para nodos Employee
CREATE CONSTRAINT emp_unique IF NOT EXISTS
FOR (e:Employee) REQUIRE e.empno IS UNIQUE;

