
from configparser import ConfigParser

import pgdb

from clases import *


class BaseDatos():
    def __init__(self, archivo_conf: str = 'bd.ini', seccion_archivo_conf: str = 'postgresql'):
        self.archivo_conf = archivo_conf
        self.seccion_archivo_conf = seccion_archivo_conf

    def __str__(self):
        return 'Base de datos con los parámetros de' + self.seccion_archivo_conf + ' la sección del' + self.archivo_conf

    def get_conexion(self):
        '''Consigue una conexión con la base de datos'''
        parser = ConfigParser()
        parser.read(self.archivo_conf)
        # vamos a la seccion que nos interesa
        db_conf = {}
        if parser.has_section(self.seccion_archivo_conf):
            parametros = parser.items(self.seccion_archivo_conf)
            for param in parametros:
                db_conf[param[0]] = param[1]
            return pgdb.connect(**db_conf)
        else:
            raise Exception('Seccion {0} no encontrada en el archivo {1}'.format(
                self.seccion_archivo_conf, self.archivo_conf))

    def get_metadatos(self):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        token_v2, tablas = '', {}
        try:
            cursor.execute(
                "select token_v2, tabla_asignaturas as asignaturas, tabla_cosas_con_fecha as cosas_con_fecha, tabla_profesores as profesores from metadatos")
            token_v2, asignaturas, cosas_con_fecha, profesores = cursor.fetchone()
            tablas = {Tablas.profesores: profesores,
                      Tablas.cosas_con_fecha: cosas_con_fecha, Tablas.asignaturas: asignaturas}
            cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.close()
            return token_v2, tablas

    def get_profe(self, id_profe: str):
        if type(id_profe) is not type('hola'):
            return None
        result = None
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "select notion_id as id, nombre from profes where notion_id = %s", (id_profe,))
            id, nombre = cursor.fetchone()
            result = Profe(id, nombre)
            cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.close()
            return result

    def get_profes(self):
        result = []
        conexion = self.get_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("select notion_id as id, nombre from profes")
            for id, nombre in cursor.fetchall():
                result.append(Profe(id, nombre))
            cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.close()
            return result

    def get_asignaturas(self, curso: Curso, cuatri: Cuatri):
        assert cuatri in [Cuatri.primero, Cuatri.segundo]
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        result = []
        try:
            cursor.execute("select notion_id as id, nombre_completo,nombre_abreviado,cuatri,numero_teoricas,numero_practicas,activas_teoricas,activas_practicas,profe_teoricas,profe_practicas from asignaturas where curso = %s and (cuatri = %s or cuatri = %s)",
                           (curso.value[str], cuatri.value[str], Cuatri.anual.value[str]))
            filas_tabla = cursor.fetchall()
            for (id, nombre_completo, nombre_abreviado, cuatri_text, numero_teoricas, numero_practicas, activas_teoricas, activas_practicas, id_profe_teoricas, id_profe_practicas) in filas_tabla:
                # preparamos los datos para introducirlos en el objeto asignatura
                nuevo_cuatri = None
                if cuatri.value[str] == cuatri_text:
                    nuevo_cuatri = cuatri
                else:
                    nuevo_cuatri = Cuatri.anual
                result.append(Asignatura(id, nombre_completo, nombre_abreviado, curso, nuevo_cuatri, numero_teoricas, numero_practicas,
                                         activas_teoricas, activas_practicas, self.get_profe(id_profe_teoricas), self.get_profe(id_profe_practicas)))
            cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.close()
            return result

    def get_clases(self, curso: Curso, cuatri: Cuatri, excluir_terminadas: bool = True):
        assert cuatri in [Cuatri.primero, Cuatri.segundo]
        conexion = self.get_conexion()
        result = Horario()
        try:
            # iteramos sobre las asignaturas que tengamos
            for asignatura in self.get_asignaturas(curso, cuatri):
                # si estuvieran activas las teoricas las enseñaríamos
                show_teoricas = asignatura.activas_teoricas or excluir_terminadas
                # lo mismo con las prácticas
                show_practicas = asignatura.activas_practicas or excluir_terminadas
                # si no hubiera que añadir prácticas ni teóricas continuamos
                if not show_practicas and not show_teoricas:
                    continue
                cursor = conexion.cursor()
                consulta = "select dia_semana, hora_inicio, hora_fin, presencial, practica, ubicacion from clases where asignatura = '{0}'".format(
                    asignatura.notion_id)
                consulta += " and practica" if not show_teoricas else ""
                consulta += " and not practica" if not show_practicas else ""
                # iteramos en el resultado
                for dia_semana, hora_inicio_mdm, hora_fin_mdm, presencial, practica, ubicacion in cursor.execute(consulta).fetchall():
                    for dia_semana_1 in DiaSemana:
                        if dia_semana == dia_semana_1.value[str]:
                            dia_semana = dia_semana_1
                            break

                    clase = Clase(asignatura, dia_semana, Duracion(Hora(min_desde_medianoche=hora_inicio_mdm), Hora(
                        min_desde_medianoche=hora_fin_mdm)), presencial, practica, ubicacion)
                    result.add_clase(clase)
                cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.close()
            return result

    def refresh_cuentas_asignatura(self, asignatura:Asignatura):
        '''
        Para una asignatura actualiza sus cuentas de clases
        '''
        conexion = self.get_conexion()
        try:
            cursor = conexion.cursor()
            num_teoricas, num_practicas = cursor.execute("select numero_teoricas, numero_practicas from asignaturas where notion_id = %s",(asignatura.notion_id,)).fetchone()
            asignatura.num_teoricas = num_teoricas
            asignatura.num_practicas = num_practicas
            cursor.close()
        except Exception as e:
            print("Error: {0}".format(e))
        finally:
            conexion.close()
    
    def cambiar_cuenta_asignatura(self, asignatura:Asignatura, practica:bool, valor:int = 1, absoluto:bool = False):
        '''Cambia el valor de la cuenta de clases de una asignatura en la bd y en el objeto asignatura'''
        col_actualizar = "numero_practicas" if practica else "numero_teoricas"
        consulta = "update asignaturas set {0} =".format(col_actualizar)
        #si no fuera absoluto
        consulta += " {0} +".format(col_actualizar) if not absoluto else ""
        consulta += " {0} where notion_id = '{1}'".format(valor, asignatura.notion_id)
        conexion = self.get_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            cursor.close()
        except Exception as error:
            print("Error: {0}".format(error))
        finally:
            conexion.commit()
            conexion.close()


if __name__ == '__main__':
    bd = BaseDatos()

    print(bd.get_clases(Curso.tercero, Cuatri.primero, False))
    print(bd.get_metadatos())
