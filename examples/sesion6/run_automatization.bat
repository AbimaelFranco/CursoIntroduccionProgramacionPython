@echo off
REM Ir a la carpeta del proyecto
cd /d C:\Users\asana\Desktop\CursoPython\CursoIntroduccionProgramacionPython-Privado

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar el script
python examples\sesion6\automatization.py

REM Cerrar automáticamente
exit
