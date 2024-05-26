import psycopg2
def conexion():
 # Establece la conexión a la base de datos
 conn = psycopg2.connect(
    dbname="airplane",
    user="postgres",
    password="123456",  # Cambia esto por tu contraseña
    host="localhost",  # Cambia esto si tu base de datos está en otro host
    port="5432"  # Cambia esto si tu base de datos utiliza un puerto diferente
    
    
 )
 
 
 return conn
 








