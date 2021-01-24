from clases import Cuatri, Curso
from main import main
from base_datos import BaseDatos
from mi_notion import MiNotion


class App:
    '''Interfaz de todas las funciones que puedo hacer'''

    def __init__(self):
        self.bd = BaseDatos()
        token_v2, tablas = self.bd.get_metadatos()
        self.notion = MiNotion(token_v2, tablas)

    def __str__(self):
        out = '__APLICACION__' + '\n'
        out += '*) Base de datos: \n'
        out += str(self.bd) + '\n'
        out += '*) Notion: \n'
        out += str(self.notion)
        return out

    def crear_clases(self, curso:Curso, cuatri:Cuatri , numero_semana:int, year:int = 2021, excluir_terminadas:bool = True, verbose:bool=True):
        '''
        Crea el horario de un curso-cuatri para una semana concreta y devuelve una lista con los objetos notion creados
        '''
        #pillamos las clases que no se hubieran terminado
        clases = sorted(self.bd.get_clases(curso, cuatri, excluir_terminadas).clases_as_list)
        clases_creadas = []
        if verbose: print("> Comenzando creación del horario...")
        count = 0
        for clase in clases:
            #refrescamos la clase pos si hubiera aumentado su contador de clases
            self.bd.refresh_cuentas_asignatura(clase.asignatura)
            count += 1
            if verbose: print("> [[PASO {0}/{1} -> creando {2}]]".format(count, len(clases), repr(clase)))
            #creamos la clase y la metemos en la lista
            clase_creada = self.notion.crear_clase(clase, numero_semana, year, verbose)
            clases_creadas.append((clase_creada, clase))
            #subimos el contador de clases
            self.bd.cambiar_cuenta_asignatura(clase.asignatura, clase.practica)
        if verbose: print("> [[HORARIO CREADO]]")
        return clases_creadas

    def borrar_clases(self, clases_creadas:list, verbose:bool=True):
        '''
        Elimina la lista de clases pasada como argumento y restaura los contadores de la base de datos
        '''
        count = 0
        for clase_creada, clase in clases_creadas:
            count += 1
            if verbose: print("PASO {0}/{1} -> creando {2}".format(count, len(clases_creadas), repr(clase)))
            #eliminamos la clase de notion
            clase_creada.remove()
            #restauramos el contador uno hacia atrás de postgres
            self.bd.cambiar_cuenta_asignatura(clase.asignatura, clase.practica, -1)
        if verbose: print("> BORRADO TERMINADO")


    def test(self):
        '''
        # vemos si asignamos bien objetos de notion a las asignaturas
        asignaturas_bd = self.bd.get_asignaturas(Curso.tercero, Cuatri.primero)
        print('Asignaturas:')
        for asignatura_bd in asignaturas_bd:
            self.notion.load_asignatura(asignatura_bd)
            print(asignatura_bd.notion_obj)
        # lo mismo con los profes
        profes_bd = self.bd.get_profes()
        print('Profes:')
        for profe_bd in profes_bd:
            self.notion.load_profe(profe_bd)
            print(profe_bd.notion_obj)
        # imprimimos las clases de la bd
        print(self.notion.get_clases_existentes())
        #insertamos una clase de prueba
        clase_prueba = self.bd.get_clases(Curso.tercero, Cuatri.primero).clases_as_list[4]
        clase_prueba.mostrar_dia_semana = True
        print(clase_prueba)
        clase_notion = self.notion.crear_clase(clase_prueba, 4)
        input('Creada. Introduce algo para borrar: ')
        clase_notion.remove()
        '''
        #creamos y borramos un horario
        clases_creadas = self.crear_clases(Curso.tercero, Cuatri.primero, 7)
        input('Comprueba que todo fue bien')
        self.borrar_clases(clases_creadas)

if __name__ == '__main__':
    App().test()
