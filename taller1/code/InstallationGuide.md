## Guía de instalación del entorno para el proyecto

1. **Creación del entorno virtual**
   ```powershell
   python -m venv .venv
   ```
2. **Activación del entorno en PowerShell (Windows)**
   ```powershell
   .venv\Scripts\activate
   ```
3. **Actualización de **``** a la versión más reciente**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Instalación de la dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Registrar las librerías**
     ```powershell
     pip freeze --local > requirements.txt
     ```

### Opiniones y recomendaciones

- **Permisos de escritura**: Ejecutar PowerShell como administrador o ajustar permisos de carpeta para evitar errores al redirigir la salida.
- **Orden de actualización**: Actualizar `pip` inmediatamente tras activar el entorno asegura instalar paquetes con la herramienta más reciente.
- **Gestión de dependencias**: Mantener `requirements.txt` al día tras cada cambio de paquetes:
  ```powershell
  pip freeze --local > requirements.txt
  ```
- **Control de versiones**: Incluir la carpeta `.venv/` en `.gitignore` para evitar subir el entorno virtual al repositorio.
- **Consistencia de comandos**: Usar `python -m pip` en lugar de invocar `pip` directamente para evitar confusiones con múltiples versiones de Python.

