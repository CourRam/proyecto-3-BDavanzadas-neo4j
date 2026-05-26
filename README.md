# SCOTT DB — Neo4j CRUD con Flask

Aplicacion web para realizar operaciones CRUD sobre una base de datos de grafos Neo4j,
modelando el esquema clasico SCOTT (Departamentos y Empleados).

---

## Estructura del proyecto

```
proyecto/
├── app.py                  # Aplicacion Flask principal
├── requirements.txt        # Dependencias Python
├── schema.cypher           # Restricciones e indices en Neo4j
├── seed_data.cypher        # Datos iniciales del esquema SCOTT
└── templates/
    ├── base.html           # Plantilla base (layout y estilos)
    ├── index.html          # Panel principal
    ├── departments.html    # Lista de departamentos
    ├── dept_form.html      # Formulario crear/editar departamento
    ├── employees.html      # Lista de empleados
    ├── emp_form.html       # Formulario crear/editar empleado
    └── graph.html          # Visualizacion del grafo con D3.js
```

---

## Requisitos previos

- Python 3.10 o superior
- Neo4j 5.x instalado y en ejecucion (Community o AuraDB)
- pip

---

## 1. Instalar Neo4j

### Opcion A — Neo4j Desktop (recomendado para desarrollo local)
1. Descargar Neo4j Desktop desde https://neo4j.com/download/
2. Crear un nuevo proyecto y una base de datos local.
3. Establecer la contrasena (por ejemplo: `password`).
4. Iniciar la base de datos. El servidor queda disponible en `bolt://localhost:7687`.

### Opcion B — Neo4j AuraDB (nube gratuita)
1. Crear una cuenta en https://neo4j.com/cloud/platform/aura-graph-database/
2. Crear una instancia gratuita (AuraDB Free).
3. Copiar la URI de conexion, el usuario y la contrasena que se generan.

---

## 2. Configurar la base de datos en Neo4j

Abrir Neo4j Browser (http://localhost:7474 en instalacion local) y ejecutar los
siguientes archivos Cypher en orden:

Copiar y pegar el contenido de `schema.cypher` en el browser y ejecutar.

### Paso 2 — Cargar datos iniciales
Copiar y pegar el contenido de `seed_data.cypher` en el browser y ejecutar.

Verificar la carga con:
```cypher
MATCH (n) RETURN labels(n), count(n);
```
Debe mostrar 4 Department y 14 Employee.

---

## 3. Instalar dependencias Python

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Puedes modificar los valores directamente en `app.py` o usar variables de entorno:

```bash
# Linux / Mac
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=tu_contrasena

# Windows (CMD)
set NEO4J_URI=bolt://localhost:7687
set NEO4J_USER=neo4j
set NEO4J_PASSWORD=tu_contrasena
```

Si usas AuraDB, la URI tiene el formato:
```
neo4j+s://<id>.databases.neo4j.io
```

---

## 5. Ejecutar la aplicacion

```bash
python app.py
```

Abrir el navegador en: http://localhost:5000

---

## 6. Funcionalidades

| Ruta                          | Descripcion                              |
|-------------------------------|------------------------------------------|
| `/`                           | Panel principal con contadores           |
| `/departments`                | Listar departamentos (Read)              |
| `/departments/create`         | Crear departamento (Create)              |
| `/departments/edit/<deptno>`  | Editar departamento (Update)             |
| `/departments/delete/<deptno>`| Eliminar departamento (Delete)           |
| `/employees`                  | Listar empleados (Read)                  |
| `/employees/create`           | Crear empleado (Create)                  |
| `/employees/edit/<empno>`     | Editar empleado (Update)                 |
| `/employees/delete/<empno>`   | Eliminar empleado (Delete)               |
| `/graph`                      | Visualizacion interactiva del grafo      |
| `/api/graph-data`             | Endpoint JSON con nodos y relaciones     |

---

## 7. Modelo de datos en Neo4j

### Nodos
- `:Department` — propiedades: `deptno`, `dname`, `loc`
- `:Employee`   — propiedades: `empno`, `ename`, `job`, `mgr`, `hiredate`, `sal`, `comm`, `deptno`

### Relaciones
- `(:Employee)-[:WORKS_IN]->(:Department)` — empleado pertenece a un departamento
- `(:Employee)-[:REPORTS_TO]->(:Employee)` — empleado reporta a su jefe directo

---

## 8. Consultas Cypher de referencia

```cypher
-- Todos los empleados con su departamento
MATCH (e:Employee)-[:WORKS_IN]->(d:Department)
RETURN e.ename, e.job, d.dname ORDER BY e.ename;

-- Jerarquia: empleado y su jefe
MATCH (e:Employee)-[:REPORTS_TO]->(m:Employee)
RETURN e.ename AS empleado, m.ename AS jefe;

-- Empleados por departamento
MATCH (e:Employee)-[:WORKS_IN]->(d:Department)
RETURN d.dname, count(e) AS total ORDER BY total DESC;

-- Empleados con salario mayor a 2000
MATCH (e:Employee) WHERE e.sal > 2000
RETURN e.ename, e.sal ORDER BY e.sal DESC;
```

---

## Notas

- El campo `mgr` en Employee almacena el `empno` del jefe; la relacion `REPORTS_TO`
  modela esto como arista en el grafo, lo cual es la representacion nativa en Neo4j.
- Al eliminar un departamento con `DETACH DELETE`, se eliminan tambien todas sus
  relaciones. Asegurate de reasignar empleados antes si es necesario.
