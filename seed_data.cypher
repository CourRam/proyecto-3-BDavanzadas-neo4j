// Departamentos 
MERGE (d1:Department {deptno: 10}) SET d1.dname = 'ACCOUNTING', d1.loc = 'NEW YORK';
MERGE (d2:Department {deptno: 20}) SET d2.dname = 'RESEARCH',   d2.loc = 'DALLAS';
MERGE (d3:Department {deptno: 30}) SET d3.dname = 'SALES',      d3.loc = 'CHICAGO';
MERGE (d4:Department {deptno: 40}) SET d4.dname = 'OPERATIONS', d4.loc = 'BOSTON';

//  Empleados 
MERGE (e1:Employee {empno: 7839})
SET e1.ename = 'KING',   e1.job = 'PRESIDENT', e1.mgr = null,
    e1.hiredate = '1981-11-17', e1.sal = 5000, e1.comm = null, e1.deptno = 10;

MERGE (e2:Employee {empno: 7698})
SET e2.ename = 'BLAKE',  e2.job = 'MANAGER',   e2.mgr = 7839,
    e2.hiredate = '1981-05-01', e2.sal = 2850, e2.comm = null, e2.deptno = 30;

MERGE (e3:Employee {empno: 7782})
SET e3.ename = 'CLARK',  e3.job = 'MANAGER',   e3.mgr = 7839,
    e3.hiredate = '1981-06-09', e3.sal = 2450, e3.comm = null, e3.deptno = 10;

MERGE (e4:Employee {empno: 7566})
SET e4.ename = 'JONES',  e4.job = 'MANAGER',   e4.mgr = 7839,
    e4.hiredate = '1981-04-02', e4.sal = 2975, e4.comm = null, e4.deptno = 20;

MERGE (e5:Employee {empno: 7654})
SET e5.ename = 'MARTIN', e5.job = 'SALESMAN',  e5.mgr = 7698,
    e5.hiredate = '1981-09-28', e5.sal = 1250, e5.comm = 1400, e5.deptno = 30;

MERGE (e6:Employee {empno: 7499})
SET e6.ename = 'ALLEN',  e6.job = 'SALESMAN',  e6.mgr = 7698,
    e6.hiredate = '1981-02-20', e6.sal = 1600, e6.comm = 300,  e6.deptno = 30;

MERGE (e7:Employee {empno: 7844})
SET e7.ename = 'TURNER', e7.job = 'SALESMAN',  e7.mgr = 7698,
    e7.hiredate = '1981-09-08', e7.sal = 1500, e7.comm = 0,    e7.deptno = 30;

MERGE (e8:Employee {empno: 7900})
SET e8.ename = 'JAMES',  e8.job = 'CLERK',     e8.mgr = 7698,
    e8.hiredate = '1981-12-03', e8.sal = 950,  e8.comm = null, e8.deptno = 30;

MERGE (e9:Employee {empno: 7521})
SET e9.ename = 'WARD',   e9.job = 'SALESMAN',  e9.mgr = 7698,
    e9.hiredate = '1981-02-22', e9.sal = 1250, e9.comm = 500,  e9.deptno = 30;

MERGE (e10:Employee {empno: 7902})
SET e10.ename = 'FORD',  e10.job = 'ANALYST',  e10.mgr = 7566,
    e10.hiredate = '1981-12-03', e10.sal = 3000, e10.comm = null, e10.deptno = 20;

MERGE (e11:Employee {empno: 7369})
SET e11.ename = 'SMITH', e11.job = 'CLERK',    e11.mgr = 7902,
    e11.hiredate = '1980-12-17', e11.sal = 800, e11.comm = null, e11.deptno = 20;

MERGE (e12:Employee {empno: 7788})
SET e12.ename = 'SCOTT', e12.job = 'ANALYST',  e12.mgr = 7566,
    e12.hiredate = '1987-04-19', e12.sal = 3000, e12.comm = null, e12.deptno = 20;

MERGE (e13:Employee {empno: 7876})
SET e13.ename = 'ADAMS', e13.job = 'CLERK',    e13.mgr = 7788,
    e13.hiredate = '1987-05-23', e13.sal = 1100, e13.comm = null, e13.deptno = 20;

MERGE (e14:Employee {empno: 7934})
SET e14.ename = 'MILLER', e14.job = 'CLERK',   e14.mgr = 7782,
    e14.hiredate = '1982-01-23', e14.sal = 1300, e14.comm = null, e14.deptno = 10;

// WORKS_IN: Empleado -> Departamento 
MATCH (e:Employee), (d:Department) WHERE e.deptno = d.deptno
MERGE (e)-[:WORKS_IN]->(d);

// MANAGES: Empleado -> Jefe directo 
MATCH (e:Employee), (m:Employee) WHERE e.mgr = m.empno
MERGE (e)-[:REPORTS_TO]->(m);
