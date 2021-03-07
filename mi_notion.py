

from notion.client import NotionClient
from notion.collection import NotionDate
from clases import *


class MiNotion:

    '''Clase con las transacciones que hago en el notion'''

    def __init__(self, token_v2: str, tablasPlantilla: dict):
        self.cliente = NotionClient(token_v2=token_v2)
        self.tablas = {}
        # iteramos en las tablas
        for tabla in Tablas:
            self.tablas[tabla] = self.cliente.get_collection_view(tablasPlantilla[tabla])

    def __str__(self):
        out = "__NotioN_ObjecT__\n"
        out += "Usuario: " + self.cliente.current_user.full_name + "\n"
        out += "Tablas:" + "\n"
        for tabla in self.tablas.values():
            out += "\t" + str(tabla.parent.title) + "\n"

        return out

    def load_asignatura(self, asignatura: Asignatura):
        '''
        Mete en el objeto asignatura una copia del objeto notion que corresponda a dicha asignatura y lo devuelve
        '''
        for asignatura_notion in self.tablas[Tablas.asignaturas].build_query().execute():
            if asignatura_notion.id == asignatura.notion_id:
                asignatura.notion_obj = asignatura_notion
                break
            else:
                asignatura.notion_obj = None
        if asignatura.notion_obj is None:
            raise Exception(
                'Asignatura [' + repr(asignatura) + "] no encontrada")

    def load_profe(self, profe: Profe):
        '''
        Mete en el objeto asignatura una copia del objeto notion que corresponda a dicha asignatura y lo devuelve
        '''
        for profe_notion in self.tablas[Tablas.profesores].build_query().execute():
            if profe_notion.id == profe.notion_id:
                profe.notion_obj = profe_notion
                break
            else:
                profe.notion_obj = None
        if profe.notion_obj is None:
            raise Exception('Profe [' + repr(profe) + "] no encontrada")

    def crear_clase(self, clase: Clase, num_semana: int, year: int = 2021, verbose: bool = True):
        '''
        Crea en notion una clase con una fecha determinada
        Devuelve la clase creada por si se quisiera eliminar
        '''
        # primero preparamos la clase:
        # 1º -> le metemos su objeto asignatura a la asignatura
        self.load_asignatura(clase.asignatura)
        # 2º -> le metemos su objeto profe a los profes de prácticas y teóricas
        if clase.asignatura.profe_teoricas: self.load_profe(clase.asignatura.profe_teoricas)
        if clase.asignatura.profe_practicas: self.load_profe(clase.asignatura.profe_practicas)
        # creamos variables de utilidad
        # estamos en condiciones de crear la clase
        nueva_clase = self.tablas[Tablas.cosas_con_fecha].collection.add_row()
        if verbose: print(">\tFila creada")
        # 1º >> ICONO
        nueva_clase.icon = '👨🏻\u200d🏫'
        if verbose: print(">\t1º -> Icono de {0} creado ({1})".format(repr(clase), nueva_clase.icon))
        # 2º >> TITULO
        titulo = 'P' if clase.practica else 'T'
        titulo += str((clase.asignatura.num_practicas + 1) if clase.practica else (clase.asignatura.num_teoricas + 1))
        titulo += ' '
        titulo += repr(clase.asignatura)
        nueva_clase.title = titulo
        if verbose: print(">\t2º -> Título de {0} creado ({1})".format(repr(clase),nueva_clase.title))
        # 3º >> FECHA
        datetime_inicio, datetime_fin = clase.duracion.get_datetimes(
            clase.dia_semana, num_semana, year)
        nueva_clase.fecha = NotionDate(datetime_inicio, datetime_fin)
        if verbose: print(">\t3º -> Fecha de {0} creada ({1},{2})".format(repr(clase),datetime_inicio, datetime_fin))
        # 4º >> DIA SEMANA
        nueva_clase.dia_semana = clase.dia_semana.value[str]
        if verbose: print(">\t4º -> Dia de la semana de {0} creado ({1})".format(repr(clase), nueva_clase.dia_semana))
        # 5º >> MAIN_TIPO
        nueva_clase.main_tipo = 'Clase'
        if verbose: print(">\t5º -> Main tipo de {0} creado ({1})".format(repr(clase),nueva_clase.main_tipo))
        # 6º >> TEORICA_PRACTICA
        nueva_clase.teorica_practica = 'Práctica' if clase.practica else 'Teórica'
        if verbose: print(">\t6º -> Teorica_practica de {0} creada ({1})".format(repr(clase),nueva_clase.teorica_practica))
        # 7º >> PRESENCIALIDAD
        nueva_clase.presencialidad = 'Presencial' if clase.presencial else 'No Presencial'
        if verbose: print(">\t7º -> Presencialidad de {0} creada ({1})".format(repr(clase),nueva_clase.presencialidad))
        # 8º >> ASIGNATURA
        nueva_clase.asignatura = [clase.asignatura.notion_obj]
        nueva_clase.tipo_asignatura = repr(clase.asignatura)
        if verbose: print(">\t8º -> Asignatura de {0} creada ({1})".format(repr(clase),nueva_clase.asignatura))
        # 9º >>PROFE
        if clase.practica:
        #si hubiera un profe
            if clase.asignatura.profe_practicas != None:
                nueva_clase.profes = [clase.asignatura.profe_practicas.notion_obj]
        else:
            if clase.asignatura.profe_teoricas != None:
                nueva_clase.profes= [clase.asignatura.profe_teoricas.notion_obj]
        if verbose: print(">\t9º -> Profe de {0} creada ({1})".format(repr(clase),nueva_clase.profes))
        # 10º >> UBICACION SI HUBIERA
        if clase.ubicacion:
            nueva_clase.ubicacion = clase.ubicacion
            if verbose: print(">\t10 -> Ubicación de {0} creada ({1})".format(repr(clase),nueva_clase.ubicacion))
        # 11º >> INDICACION PARA PONER RESUMEN
        nueva_clase.resumen = 'PONER_QUE_SE_VIO'
        if verbose: print(">\t11 -> Indicación de poner resumen de {0} creada".format(repr(clase)))
        #devolvemos la clase
        return nueva_clase

    def get_clases_existentes(self):
        '''
        devuelve una lista con las clases hasta ahora
        '''
        result = []
        for clase_notion in self.tablas[Tablas.cosas_con_fecha].build_query().execute():
            if clase_notion.main_tipo == 'Clase':
                result.append(clase_notion)
        return result

    def get_profes(self):
        '''
        Devuelve un lista de tuplas (id, nombre) con los profes que se tengan guardados en notion
        '''
        profes = []
        for profe_notion in self.tablas[Tablas.profesores].build_query().execute():
            profes.append((profe_notion.id, profe_notion.title))
        return profes
