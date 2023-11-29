'''
 ============================================================================
 Nombre: Librería pySQLino
 Autor:  Carlos Ricardo Cuellar Klingenberger
 ============================================================================
 '''
import os
import serial
import serial.tools.list_ports
import subprocess
import serial
import time
import threading
#funciones

#función para buscar el puerto donde esta conectado el arduino
def find_arduino_port():
    # Lista de los puertos seriales disponibles
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        # Se revisa que este conectado un arduino uno
        if "Arduino Uno" in port.description:
            return port.device

    return None

#funcion para aceptar conexión con arduino
def connect_to_arduino(port):
    try:
        # Se abre una conexión serial hacia el arduino
        ser = serial.Serial(port, 9600)  # Adjust baudrate as needed
        print(f"Connected to Arduino Uno on {port}")

        # Add your Arduino communication logic here

        #while True:
        #    a=0

        # Close the serial connection when done
        #ser.close()
    except Exception as e:
        print(f"Error conectando al Arduino: {e}")
        raise
    return ser

#clases
#Clase de intereaccion de ArduinoUno con entrono de SQL
class UNO_SQL:
    def __init__(self, server_name, user, psswd,board_name,serial_port=None, DB=None):
        # Se inician los atributos de la clase
        #Estos son las credenciales para el servidor y el puerto serial del objeto
        self.server_name = server_name
        self.user = user
        self.psswd = psswd
        self.serial_port=serial_port
        self.board_name=board_name
        self.input_pins=None
        self.output_pins=None
        self.analogin_pins=None 
        self.Dig_Inp=[None,None,None,None,None,None]
        self.Dig_Out=[None,None,None,None,None,None]
        self.An_Inp=[None,None,None,None,None,None]

#########Se crean métodos##################
    #Método para verificar conexión al server
    def check_server_conn(self):
        # Se establece la conexión
        connection_string = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "GO" """
        #connection_string = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "CREATE DATABASE Prueba" """

        try:
            # Se ejecuta la conxión por medio del cmd
            subprocess.run(connection_string, shell=True, check=True)
            print(f"Conexión exitosa al servidor {self.server_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error al conectar al servidor: {e}")
    #Método para establecer conexión al board de arduino
    def board_conn(self):
        arduino_port = find_arduino_port()
        if arduino_port:
            # Se conecta al arduino por medio del puerto serial de la clase
            self.serial_port=connect_to_arduino(arduino_port)
        else:
            raise RuntimeError("Fallo la conexion hacia el Arduino Uno.")
        response = b''
        #Ciclo que espera respuesta por parte del arduino  
        while True:
            response=self.serial_port.readline().decode().strip()
            #self.serial_port.write("connrequest\n".encode())
            #Decodificación de la respuesta
            print(response)
            if response=='connrequest':
                self.serial_port.write("connconfirmed\n".encode())
                break
            #Lógica para proceder únicamente bajo la respuesta esperada por la recepciíon
                #de establecimiento de repsuesta
            if response.endswith('\n'):
                decoded_response = response.decode().strip()
                print(f"Received: {decoded_response}")
                if decoded_response == 'connrequest':
                    print("Arduino confirmed connection.")
                    break
                response = b''  # Reset response for the next line
    #Método para desconexión con el board
    def close_board_conn(self):
        self.serial_port.close()
    #Función para crear una base de datos para el arduino conectado
    #Método para crear la base de datos del board
    def create_board_DB(self,DB_name):
        #Ingreso de query para crear DB
        self.DB=DB_name
        comando_cmd=f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "CREATE DATABASE {DB_name}" """
        try:
            subprocess.run(comando_cmd, shell=True, check=True)
            print(f"Database {DB_name} creada o existente.")
        except subprocess.CalledProcessError as e:
            print(f"Error creando database: {e}")
    #Metodo para crear la tabla respectiva. Se hace en función te los valores ingresados para la clase
    def create_table(self):
        #comando_cmd=f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "CREATE TABLE {self.DB}.dbo.{self.board_name}_Digtial_IO (date DATETIME DEFAULT GETDATE(),Input_1 NVARCHAR(255) NULL,Input_2 NVARCHAR(255) NULL,Input_3 NVARCHAR(255) NULL,Input_4 NVARCHAR(255) NULL,Input_5 NVARCHAR(255) NULL,Input_6 NVARCHAR(255) NULL,Output_1 NVARCHAR(255) NULL,Output_2 NVARCHAR(255) NULL,Output_3 NVARCHAR(255) NULL,Output_4 NVARCHAR(255) NULL,Output_5 NVARCHAR(255) NULL,Output_6 NVARCHAR(255) NULL);" """
        comando_cmd=f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "CREATE TABLE {self.DB}.dbo.{self.board_name}_All_IO (date DATETIME DEFAULT GETDATE(),Input_1 NVARCHAR(255) NULL,Input_2 NVARCHAR(255) NULL,Input_3 NVARCHAR(255) NULL,Input_4 NVARCHAR(255) NULL,Input_5 NVARCHAR(255) NULL,Input_6 NVARCHAR(255) NULL,Output_1 NVARCHAR(255) NULL,Output_2 NVARCHAR(255) NULL,Output_3 NVARCHAR(255) NULL,Output_4 NVARCHAR(255) NULL,Output_5 NVARCHAR(255) NULL,Output_6 NVARCHAR(255) NULL,Analog_1 NVARCHAR(255) NULL,Analog_2 NVARCHAR(255) NULL,Analog_3 NVARCHAR(255) NULL,Analog_4 NVARCHAR(255) NULL,Analog_5 NVARCHAR(255) NULL,Analog_6 NVARCHAR(255) NULL);" """
        try:
            subprocess.run(comando_cmd, shell=True, check=True)
            print(f"Tabla {self.board_name} creada o existente.")

        except subprocess.CalledProcessError as e:
            print(f"Error creando Tabla: {e}")     
    #Se configurar los inputs digitales. Se pueden tener unicamente 6 inputs digitales
    #Se ingresa la CANTIDAD de pines que se desan configurar
    #Se pueden tener unicamente un maximo de 6 pines de entrada digital
    #Los pines posibles son del pin 8 al 13 de los GPIO de arduino
    def config_dig_input(self,pins):
        self.serial_port.reset_input_buffer()
        while True:
            if pins<=0:
                print('Se ingreso un número incorrecto de pines')
                break
            self.serial_port.write(f"input_{pins}\n".encode())
            response=self.serial_port.readline().decode().strip()
            if response=='inputdone':
                self.input_pins=pins
                break
     #Se configurar los outputs digitales. Se pueden tener unicamente 6 outputs digitales
    #Se ingresa la CANTIDAD de pines que se desan configurar
    #Se pueden tener unicamente un maximo de 6 pines de entrada digital
    #Los pines posibles son del pin 2 al 7 de los GPIO de arduino           
    def config_dig_output(self,pins):
        self.serial_port.reset_input_buffer()
        while True:
            if pins<=0:
                print('Se ingreso un número incorrecto de pines')
                break
            self.serial_port.write(f"output_{pins}\n".encode())
            response=self.serial_port.readline().decode().strip()
            if response=='outputdone':
                self.output_pins=pins
                break
    #Se solicita leer los pines digitales
    #Se lee automaticamente según la cantidad de pines congifurados previamente
    def read_dig_inputs(self):
        self.serial_port.reset_input_buffer()
        flag_break=0
        while True:
            
            if self.input_pins==None:
                print('No se han configurado pines de entrada')
                break
    #Se lee automáticamente según los pines asignados a la clase
    #A continuación se tiene la logica para leer la infomración esperada
            self.serial_port.write(f"readinput:\n".encode())
            response=self.serial_port.readline().decode().strip()
            if (response.startswith("readinput:")) & (len(response)==21):
                valores=response.split(":")[1].split("_")
                
                for i in range(len(self.Dig_Inp)):
                    if valores[i]=="N":
                        self.Dig_Inp[i]=None
                    else:
                        self.Dig_Inp[i]=valores[i]
                    if i==5:
                        flag_break=1
            if flag_break==1:
                self.serial_port.write(f"readingdone\n".encode())
                print(f'Los valores de los pines de entrada son: {self.Dig_Inp}')
                comando_cmd = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "INSERT INTO {self.DB}.dbo.{self.board_name}_All_IO (Input_1, Input_2, Input_3, Input_4, Input_5, Input_6, Output_1, Output_2, Output_3, Output_4, Output_5, Output_6,Analog_1,Analog_2,Analog_3,Analog_4,Analog_5,Analog_6) VALUES ({', '.join(['NULL' if val is None else str(val) for val in self.Dig_Inp + self.Dig_Out + self.An_Inp])});" """
                subprocess.run(comando_cmd, shell=True, check=True)
                break
    #Se escribe de manera individual al pin y el estado que se quiere escribir
    #Se protege el codigo para unicamente recibir pines dentro del tango de configuracion

    def write_dig_output(self, pin, state):
        self.serial_port.reset_input_buffer()
        while True:
            if (pin>self.output_pins) or (pin==0):
                print("Se ingreso un numero incorrecto de pin de salida")
                break
            '''if state!=0 or state!=1:
                print("Se ingreso un estado incorrecto")
                break'''
            if self.output_pins==None:
                print('No se han configurado pines de salida')
                break
            self.serial_port.write(f"writeoutput:{pin}_{state}\n".encode())
            #print(f"writeoutput:{pin}_{state}")
            response=self.serial_port.readline().decode().strip()
            print(response)
            if response=='outputwritedone':
                print(f"Se escribio el pin {pin} en {state}")
                self.Dig_Out[pin-1]=state
                # Assuming Dig_Inp and Dig_Out are lists of values or None
                #comando_cmd = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "INSERT INTO {self.DB}.dbo.{self.board_name}_Digtial_IO (Input_1, Input_2, Input_3, Input_4, Input_5, Input_6, Output_1, Output_2, Output_3, Output_4, Output_5, Output_6) VALUES ({', '.join(['NULL' if val is None else str(val) for val in self.Dig_Inp + self.Dig_Out])});" """
                comando_cmd = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "INSERT INTO {self.DB}.dbo.{self.board_name}_All_IO (Input_1, Input_2, Input_3, Input_4, Input_5, Input_6, Output_1, Output_2, Output_3, Output_4, Output_5, Output_6,Analog_1,Analog_2,Analog_3,Analog_4,Analog_5,Analog_6) VALUES ({', '.join(['NULL' if val is None else str(val) for val in self.Dig_Inp + self.Dig_Out + self.An_Inp])});" """



                subprocess.run(comando_cmd, shell=True, check=True)
    
                break
    #Se lee la entrada de inputs analogicos
    #Por la arcquitecura de arduino estos no requieren de un setup previo para congigurar
    #Se puede recibir unicamente como analogico info de los pones AO a A5 del arduino UNO
    #Se utiliza la misma logica para separar datos que en la entrada digital, son emnbargo con distintos delimitadores
    def read_an_inputs(self, pins):
        self.serial_port.reset_input_buffer()
        self.analogin_pins=pins
        flag_break=0
        while True:
            if self.analogin_pins==None:
                print('No se han configurado pines de entrada analo')
                break
            self.serial_port.write(f"analoginput_{self.analogin_pins}\n".encode())
            response=self.serial_port.readline().decode().strip()
            if (response.startswith("readanaloginput:")) & (response.endswith("END")):
                valores=response.split(":")[1].split("_")
                for i in range(len(self.An_Inp)):
                    print(f'LOS VALORES SON: {valores}')
                    if valores[i]=="N":
                        self.An_Inp[i]=None
                    else:
                        self.An_Inp[i]=valores[i]
                    if i==self.analogin_pins:
                        flag_break=1
                    
            if flag_break==1:
                self.serial_port.write(f"readingdone\n".encode())
                print(f'Los valores de los pines analogicos de entrada son: {self.An_Inp}')
                comando_cmd = f"""sqlcmd -S {self.server_name} -U {self.user} -P {self.psswd} -Q "INSERT INTO {self.DB}.dbo.{self.board_name}_All_IO (Input_1, Input_2, Input_3, Input_4, Input_5, Input_6, Output_1, Output_2, Output_3, Output_4, Output_5, Output_6,Analog_1,Analog_2,Analog_3,Analog_4,Analog_5,Analog_6) VALUES ({', '.join(['NULL' if val is None else str(val) for val in self.Dig_Inp + self.Dig_Out+self.An_Inp])});" """
                subprocess.run(comando_cmd, shell=True, check=True)
                break



