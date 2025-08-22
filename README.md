# MediTurno

Este repositorio fue creado para alojar el trabajo de la materia **Seminario de Tecnología** por alumnos de la carrera de **Licenciatura en Gestión de Tecnología de la Información**.

**MediTurno** es una aplicación web de turnos médicos. Permite a **usuarios**, **médicos** y **clínicas** gestionar sus turnos de forma simple y centralizada.


## 🚀 Features
- Registro e inicio de sesión de usuarios.
- Gestión de agendas de médicos (días y horarios disponibles).
- Solicitud y cancelación de turnos.
- Panel de administración para clínicas y médicos.
- Recordatorios y notificaciones.
- Roles diferenciados: `usuario`, `medic`, `clinic`, `admin`.


## 🛠️ Tecnologías utilizadas

- [Python 3](https://www.python.org/)
- [Django 5](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/) (por defecto)


## ⚙️ Instalación
 1. Clonar el repositorio.
```bash
git clone https://github.com/Kagushutchi/MediTurno
```
 2. Cambiar el directorio al del proyecto.
```bash
cd MediTurno
```
 3. Crear entorno virtual (opcional pero recomendado)
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
 4. Instalar los requerimientos.
```bash
pip install -r requirements.txt
```
 5. Hacer las migraciones.
```bash
python3 manage.py makemigrations
```
 6. Migrar.
```bash
python3 manage.py migrate
```
 7. Crear un super usuario para probar el django admin (opcional).
```bash
python3 manage.py createsuperuser
```
 8. Correr el proyecto en localhost.
```bash
python3 manage.py runserver
```

## 👨‍💻 Autores
- Flac222
- Kagushutchi
- Audine-Matias-Gabriel

## 📄 Licencia
Este proyecto fue desarrollado con fines académicos en el marco de la materia Seminario de Tecnología.