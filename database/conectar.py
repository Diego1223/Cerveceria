import mysql.connector

#Patron singelton porque solo usamos una base de datos y solo queremos una instancia de la clase
class MysqlConnection:
    _instance = None

    def __new__(cls):
        #Verificamos si aun no existe la instancia
        if cls._instance is None:
            #Crear la instancia usando la clase base de python
            cls._instance = super(MysqlConnection, cls).__new__(cls)
            #Inicializamos la conexion solo una vez
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        CONFIG = {
            "host": "localhost",
            "user": "root",
            "password": "tuclave",
            "database":"cerveceria",
            "auth_plugin": "mysql_native_password"
        }

        self.connection = mysql.connector.connect(**CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)


db = MysqlConnection()

