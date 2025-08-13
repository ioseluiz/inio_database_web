@echo off
REM Activa el entorno virtual de Python
echo Activando entorno virtual...
call .\venv\Scripts\activate.bat

REM Ejecuta el primer script de importacion
echo ==========================================================
echo Ejecutando importacion de SIA...
echo ==========================================================
python manage.py import_SIA

REM Pausa de 10 segundos para estabilizar conexiones
echo.
echo Esperando 10 segundos para actualizar conexiones...
timeout /t 10 /nobreak

REM Ejecuta el segundo script de importacion de transacciones
echo  ==========================================================
echo Ejecutando importacion de transacciones (ultimos 30 dias)...
echo ==========================================================
python manage.py import_transacciones --days 30

REM Pausa de 10 segundos
echo.
echo Esperando 10 segundos...
timeout /t 10 /nobreak

REM Ejecuta el tercer script para actualizar horas de SIA
echo ==========================================================
echo Ejecutando actualizacion de horas SIA...
echo ==========================================================
python manage.py actualizar_horas_sia

echo.
echo Esperando 10 segundos...
timeout /t 10 /nobreak

REM Copia el archivo de Licitaciones desde la red a la carpeta local
echo ==========================================================
echo Copiando archivo de Licitaciones...
echo ==========================================================
copy "\\mendozas-07\Files\Licitaciones\Licitaciones_AFActual.csv" "C:\Users\jlmunoz\OneDrive - Autoridad del Canal de Panama\Documents\INIO-CE\web_apps\data"

REM Pausa de 10 segundos
echo.
echo Esperando 10 segundos...
timeout /t 10 /nobreak

REM Ejecuta el script para importar las licitaciones
echo ==========================================================
echo Ejecutando importacion de Licitaciones...
echo ==========================================================
python manage.py import_licitaciones .\data\Licitaciones_AFActual.csv

echo.
echo ==========================================================
echo Todos los scripts han finalizado.
echo ==========================================================

REM Desactiva el entorno virtual (opcional)
call deactivate

REM Mantiene la ventana abierta para ver los resultados
pause