Proyecto: Sistema de Venta de Electrónicos

Este es el inicio de nuestra aplicación web para una tienda de electrónica. El proyecto está hecho con Python y Flask, y está organizado de forma que sea fácil para el resto del equipo seguir agregando sus partes más adelante.

****************************************************************************************************
Integrante: Kevin Stiven Copali Mendieta
Cómo hice mi parte del trabajo

Para empezar este proyecto, me encargué de armar toda la estructura base y dejar funcionando lo más importante: la seguridad y el manejo de usuarios.
Investigación y ayuda de IA

Para que el código saliera limpio y sin errores, estuve investigando bastante en la documentación de Flask. También usé Inteligencia Artificial como apoyo para resolver dudas rápidas, corregir errores de escritura y para que me ayude a diseñar las pantallas de forma que se vean bien. Esto me sirvió mucho para avanzar más rápido y aprender a estructurar mejor las carpetas del grupo.
Lo que agregué y configuré

Yo inicié el proyecto desde cero y me encargué de dejar listo lo siguiente:

    Instalación y Base: Instalé Flask y todas las librerías necesarias. Creé la estructura de carpetas para que todos sepamos dónde guardar cada cosa.

    Base de Datos: Configuré la conexión con MySQL y dejé listo el sistema de "migraciones". Esto sirve para que, si cambiamos algo en las tablas, no se borren los datos de nadie.

    Seguridad de Rutas: Creé protecciones para que nadie pueda entrar a las páginas de administración si no tiene el permiso o si intenta inventar la dirección en el navegador.

    Login y Logout: Hice la pantalla de ingreso al sistema y la función para salir de forma segura.

    Gestión de Usuarios (CRUD): Creé la tabla de usuarios y todas las funciones para poder ver la lista, crear nuevos usuarios, editarlos o borrarlos.

    Diseño Base: Hice el archivo principal (base.html) que tiene el menú lateral y la barra de arriba. Así, cuando mis compañeros hagan sus partes, solo tienen que "heredar" ese diseño y no tienen que volver a programar el menú.

    CSS y Estilo: Escribí todo el código de diseño para que las tablas, los formularios y los avisos se vean modernos y ordenados.

Lo que aprendí en este proceso

Al hacer esta primera parte del sistema, pude aprender varias cosas:

    Flask y Python: Aprendí a usar Blueprints, que es lo que nos permite trabajar en equipo sin que nuestro código se mezcle todo feo.

    Migraciones: Aprendí que con comandos de terminal se pueden actualizar las tablas de la base de datos sin romper nada.

    Diseño Web: Recordé mucho sobre HTML y CSS, especialmente cómo hacer que un menú se quede fijo a un lado y que los formularios se vean limpios.

    Seguridad: Ahora entiendo mejor cómo proteger una página para que solo el administrador pueda ver cosas privadas.

Guía rápida para mis compañeros

Si acabas de bajar el proyecto, haz esto para que te funcione:

    Instala lo necesario: pip install -r requirements.txt

    Revisa que tu MySQL tenga la base de datos creada.

    Ejecuta estos comandos para crear las tablas:

        flask db init

        flask db migrate -m "inicio del proyecto"

        flask db upgrade

    Corre el proyecto con: python run.py

Nota: A partir de aquí, el equipo puede empezar a crear los módulos de Productos, Ventas y Categorías usando la base que ya dejé configurada.
****************************************************************************************************
Segundo Integrante: EDWIN HUANCA ARO
COMO SE IMPLEMENTO EL MODULO
La implementación se basó en una arquitectura MVC (Modelo-Vista-Controlador) utilizando Flask y SQLAlchemy, estructurada de la siguiente manera:

Modelos de Base de Datos: Se definieron las clases Category y Product con una relación de Uno a Muchos. Se utilizó db.relationship con un backref llamado category para que cada producto pudiera acceder fácilmente al nombre de su categoría.

Modularización con Blueprints: Para organizar el código, se registraron todas las rutas de administración bajo un Blueprint llamado routes, lo que permitió prefijar las URLs (ej. /admin/productos) y mantener el archivo principal limpio.

Controladores y Lógica: Se implementaron funciones CRUD completas que permiten:

Filtrar productos y categorías mediante búsquedas en la base de datos.

Validar formularios para la creación y edición de registros.

Gestionar la eliminación segura de datos mediante métodos POST.

Vistas Dinámicas (Jinja2): Se utilizó herencia de plantillas con un archivo base.html que contiene el sidebar y la barra de navegación, asegurando que el diseño sea consistente en todo el sistema.

LO QUE APRENDI 
Con todo lo que nos enseño en clases sobre flask y SQLAlchemy me ayudo a desarrollar los modulos de CATEGORIA Y PRODUCTO tambien aprendi con ayuda de la IA los siguientes puntos.

Manejo de Contextos y Blueprints: Aprendi que al usar Blueprints, las funciones url_for deben incluir el nombre del blueprint como prefijo (ej. url_for('routes.lista_productos')), evitando los errores de tipo BuildError.

Relaciones en SQLAlchemy: Comprendi cómo conectar dos tablas mediante llaves foráneas (ForeignKey) y cómo el backref en el modelo es fundamental para mostrar datos relacionados en el HTML sin hacer consultas manuales extras.

Depuración de Errores de Jinja2: Ahora puedo identificar errores comunes de sintaxis, como el uso incorrecto de comillas en etiquetas de Flask o el acceso a atributos no definidos (UndefinedError) cuando el nombre en el modelo no coincide con la plantilla.

Experiencia de Usuario (UX) en el Admin: Implemente mensajes Flash para dar retroalimentación al usuario (ej. "Categoría creada con éxito") y menús desplegables dinámicos que mantienen seleccionada la opción correcta al editar un producto.

****************************************************************************************************
Tercer Integrante: Luis Fernando Patiño Nina
Módulo de Ventas, Filtros Avanzados y Exportación a PDF

COMO SE IMPLEMENTO EL MODULO
Implementé el módulo de ventas separando la lógica en un Blueprint (`ventas.py`). Para la experiencia de usuario, utilicé `localStorage` mediante JavaScript (`carrito.js`), lo que permite a los usuarios armar su carrito sin hacer peticiones constantes al servidor y no perder los productos que agregó al carrito. Al finalizar, los datos se envían mediante un POST en formato JSON al backend, donde se procesa la transacción y se descuenta el stock interactuando con las tablas `Venta` y `DetalleVenta`.

EL RETO DE EQUIPO: PDF Y FILTROS AVANZADOS
Para cumplir con el reto extra, implementé dos características:
1. Exportación a PDF: Utilicé la librería `fpdf2` en Python. Al procesar la compra o desde el historial, se genera un documento PDF estructurado en memoria iterando sobre las relaciones de SQLAlchemy (`venta.detalles`) y se devuelve directamente al navegador mediante `make_response`.
2. Filtros Avanzados: En el historial de compras, implementé una búsqueda por múltiples criterios (Rango de fechas, ID de pedido y Nombre de comprador si es Admin) utilizando la construcción dinámica de consultas (`query.filter()`) en SQLAlchemy.

LO QUE APRENDI
* Aprendí a integrar JavaScript asíncrono (`fetch`) con Flask para enviar datos JSON de forma segura.
* Comprendí el uso de librerías externas como `fpdf2` para generar documentos al vuelo sin necesidad de guardar archivos temporales en el servidor.
* Reforcé el concepto de consultas avanzadas y relaciones en SQLAlchemy, aprendiendo a filtrar datos dinámicamente dependiendo del rol del usuario autenticado.
****************************************************************************************************