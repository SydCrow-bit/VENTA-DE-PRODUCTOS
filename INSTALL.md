# Guía de Instalación: Sistema de Venta de Electrónicos

Este documento detalla los pasos necesarios para configurar, instalar y ejecutar el entorno de desarrollo local para el Sistema de Venta de Electrónicos.

## 1. Requisitos Previos

Antes de comenzar, asegúrese de tener instalados los siguientes componentes en su sistema:

* Python 3.10 o superior.
* Servidor MySQL (versión 8.0 recomendada).
* Git para el control de versiones.

### Configuración Esperada de Base de Datos

El archivo `config.py` está preconfigurado con los siguientes parámetros de conexión. Asegúrese de que su servidor MySQL coincida con estas credenciales o actualice el archivo `config.py` en consecuencia:

* **Host:** localhost
* **Puerto:** 3306
* **Usuario:** root
* **Contraseña:** 
* **Base de datos:** db_venta_electronicos

Es obligatorio crear la base de datos vacía en MySQL antes de ejecutar las migraciones. Ejecute el siguiente comando en su cliente MySQL:

```sql
CREATE DATABASE db_venta_electronicos;
```

## 2. Configuración del Entorno de Desarrollo

Abra su terminal y siga estos pasos secuenciales:

**Clonar el repositorio:**
```bash
git clone git@github.com:SydCrow-bit/VENTA-DE-PRODUCTOS.git
cd VENTA-DE-PRODUCTOS
```

**Crear el entorno virtual:**
```bash
python -m venv venv
```

**Activar el entorno virtual:**
* En Windows:
```cmd
venv\Scripts\activate
```
* En macOS y Linux:
```bash
source venv/bin/activate
```

**Instalar las dependencias:**
Asegúrese de que el entorno virtual esté activo antes de ejecutar este comando.
```bash
pip install -r requirements.txt
```

## 3. Preparación de la Base de Datos

El proyecto utiliza Flask-Migrate para el control de versiones de la base de datos. No es necesario crear las tablas manualmente.

**Ejecutar las migraciones:**
Este comando leerá los archivos en la carpeta `migrations/` y creará la estructura de tablas (Usuarios, Categorías, Productos) en su base de datos.
```bash
flask db upgrade
```

**Poblar la base de datos (Seeding):**
Para generar datos de prueba y facilitar el desarrollo, ejecute el script de inicialización. Este script interactivo le permitirá insertar categorías y productos base de forma segura.
```bash
python seed.py
```

## 4. Ejecución de la Aplicación

Para iniciar el servidor de desarrollo, ejecute el archivo principal del proyecto:

```bash
python run.py
```

El servidor iniciará en la dirección por defecto: `http://127.0.0.1:5000`

### Credenciales de Acceso por Defecto

Durante la primera ejecución de `run.py`, el sistema creará automáticamente un usuario administrador si este no existe en la base de datos.

* **Usuario:** admin
* **Contraseña:** 1234
* **Rol:** admin

Utilice estas credenciales en la pantalla de inicio de sesión para acceder a los módulos de gestión.