from app import App
from clases import *
import re


def main():
    '''Donde empieza la interacción con el usuario'''
    #creamos variables de utilidad
    salir = False
    curso_opcion = None
    cuatri_opcion = None
    opcion = ""
    app = App()
    #fin de la inicialización
    while not salir:
        if curso_opcion is None or cuatri_opcion is None:
            print('__MENU_PRINCIPAL_DE_NOTION_WEEKIFY__')
            print('Selecciona:')
            print('a) Ver los profes que hay en notion')
            print('b) Ver un curso(3-4)-cuatri(1-2), por ejemplo b:3->1')
            print('S) Salir')
            opcion = input('Escribe tu opción: ')
            if list(opcion)[0] in ['a', 'b', 'S']:
                if list(opcion)[0] == 'a':
                    for id, nombre in app.get_profes():
                        print("{0} -> {1}".format(id, nombre))
                elif list(opcion)[0] == 'b':
                    if re.search("^b:[34]->[12]$", opcion) != None:
                        #obtenemos el curso
                        for curso in Curso:
                            if curso.value[int] == int(opcion.split('->')[0][-1]):
                                curso_opcion = curso
                                break
                        for cuatri in Cuatri:
                            if cuatri.value[int] == int(opcion.split('->')[1]):
                                cuatri_opcion = cuatri
                                break
                        print('Curso y cuatri cargados satisfactoriamente...')
                    else:
                        print("ERROR: la cadena '{0}' no sigue el patron establecido".format(opcion))
                elif list(opcion)[0] == 'S':
                    salir = True
                    print("Saliendo...")
            else:
                print('Opción no válida')
        else:
            #se han cargado curso y cuatri
            print("__MENÚ_DE_CURSO_{0}_CUATRI_{1}__".format(curso_opcion.value[str].upper(),cuatri_opcion.value[str].upper()))
            print('Selecciona:')
            print('a) Ver asignaturas')
            print('b) Ver el horario')
            print("c) Crear un horario para una semana concreta (ej: 'c:7')")
            print("S) Volver al menú principal")
            opcion = input('Escribe tu opción: ')
            if list(opcion)[0] in ['a', 'b', 'c', 'S']:
                if list(opcion)[0] == 'a':
                    for asignatura in app.get_asignaturas(curso_opcion, cuatri_opcion):
                        print('')
                        print(asignatura)
                elif list(opcion)[0] == 'b':
                    #imprimimos el horario incluyendo las terminadas
                    print(app.get_clases(curso_opcion, cuatri_opcion, False))
                elif list(opcion)[0] == 'c':
                    if re.search("^c:[1-9]$|^c:[1-5][0-9]$", opcion) != None:
                        num_semama = int(opcion.split(':')[1])
                        if input('El número de semana escogido es {0}. Desea continuar? (Y/n): '.format(num_semama)) == 'Y':
                            clases_creadas = app.crear_clases(curso_opcion, cuatri_opcion, num_semama, 2021)
                            if input("IMPORTANTE: quieres confirmar las clases creadas? (Y/n): ") == 'Y':
                                print("Clases confirmadas ✅")
                            else:
                                app.borrar_clases(clases_creadas)
                        else:
                            print("Cancelando creación de clases...")
                    else:
                        print("ERROR: la cadena '{0}' no sigue el patron establecido".format(opcion))
                elif list(opcion)[0] == 'S':
                    curso_opcion = None
                    cuatri_opcion = None
            else:
                print("Opción no válida")
        #ponemos un separador
        print('-'*50)



if __name__ == '__main__':
    main()
