# pySQLino
Repositorio público de la librería encargada de automatizar y sincronizar el uso de sistemas embebidos y bases de datos por medio de Python.

# Software Previo
->Tener descargado SQL Server y garantizar que se puede acceder tanto por SQL Server Security User como por Windows Authentication
->Las librerías internas de pySQLino son nativas con la instalación estándar de python. En caso de errores verificar la sección de imports
del código y completar el catálogo de librerías faltantes importadas en esa sección.
->ArduinoIDE para poder cargar el archivo con el código .ino a una placa ARDUINO UNO excluisvamente.


# Uso de pySQLino
->Clonar el repositorio o descargar los siguientes dos archivos: pySQLino.py  y pySQLino.ino
->Poner el archivo de pySQLino.py en el mismo directorio activo que el archivo con el
código de python a implementar la librería.
->Cargar el código contenido en pySQLino.ino a una placa ARDUINO UNO. Para cada nuevo uso de la placa con una
instancia de proceso nuevo utilizando la librería de python, se recomienda fuertemente apachar el botón de reset de la placa.

*Como referencia se influye un archivo pruebaslib.py en donde se puede observar como se implementa la librería con todas sus funciones*
