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