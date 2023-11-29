'''
 ============================================================================
 Nombre: Implementacion pySQLino
 Autor:  Carlos Ricardo Cuellar Klingenberger
 ============================================================================
 '''
from pySQLino import *
import time
# Crea una instancia de la clase UNO_SQL
sql_server_instance = UNO_SQL(server_name='desktop-iv90g7d', user='FernandoAlonso', psswd='Realmadridcf10', board_name='ArdJonathan')
# Se establece conexión al server SQL
sql_server_instance.check_server_conn()
#Se establece la conexión con el arduino
sql_server_instance.board_conn()
#Se crea una base de datos con el nombre ArdUno
sql_server_instance.create_board_DB('DemoTesis')
#Se cierra la tabla dentro de la DB creada
sql_server_instance.create_table()
#Configuracion de pines
sql_server_instance.config_dig_input(6)
sql_server_instance.config_dig_output(6)
#Lectura de pines
sql_server_instance.read_dig_inputs()
#Escritura de pines
sql_server_instance.write_dig_output(1,0)
sql_server_instance.write_dig_output(2,0)
sql_server_instance.write_dig_output(3,0)
sql_server_instance.write_dig_output(4,0)
sql_server_instance.write_dig_output(5,0)
sql_server_instance.write_dig_output(6,0)
estado=1
for x in range(200):
    estado = x % 2
    sql_server_instance.read_dig_inputs()
    sql_server_instance.write_dig_output(1,estado)
    sql_server_instance.write_dig_output(2,estado)
    sql_server_instance.write_dig_output(3,estado)
    sql_server_instance.read_an_inputs(3)
    print(f'Corrida {x}')
    #time.sleep(.5)
    pass
#Cierre de conexión serial
sql_server_instance.close_board_conn()

print('FIN')