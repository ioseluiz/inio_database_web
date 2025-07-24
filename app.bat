@echo off
rem Cambia el directorio actual a la carpeta donde se encuentra este archivo .bat
cd /d "%~dp0"

echo "Activando entorno virtual..."
rem Llama al script para activar el entorno virtual
call .\venv\Scripts\activate.bat

echo "Iniciando el servidor de desarrollo..."
echo "Puedes detener el servidor presionando CTRL+C."
rem Ejecuta el servidor de desarrollo de Django
python manage.py runserver

rem Mantiene la ventana abierta al finalizar para que puedas ver cualquier mensaje
pause