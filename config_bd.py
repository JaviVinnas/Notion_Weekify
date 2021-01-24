from configparser import ConfigParser

def get_db_config(archivo:str = 'bd.ini', seccion:str = 'postgresql'):
    '''Devuelve un dict con lo que saque del archivo bd_ini'''
    parser = ConfigParser()
    parser.read(archivo)
    #vamos a la seccion que nos interesa
    db = {}
    if parser.has_section(seccion):
        parametros = parser.items(seccion)
        for param in parametros:
            db[param[0]] = param[1]
        return db
    else:
        raise Exception('Seccion {0} no encontrada en el archivo {1}'.format(seccion, archivo))
