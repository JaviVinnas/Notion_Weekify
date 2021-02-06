from enum import Enum
from datetime import datetime, date
from notion.collection import CollectionRowBlock


class Tablas(Enum):
    asignaturas = 0
    profesores = 1
    cosas_con_fecha = 2


class Curso(Enum):
    tercero = {str: 'Tercero', int: 3}
    cuarto = {str: 'Cuarto', int: 4}


class Cuatri(Enum):
    anual = {str: 'Anual', int: 0}
    primero = {str: 'Primero', int: 1}
    segundo = {str: 'Segundo', int: 2}


class DiaSemana(Enum):
    lunes = {str: 'Lunes', int: 1}
    martes = {str: 'Martes', int: 2}
    miercoles = {str: 'Miercoles', int: 3}
    jueves = {str: 'Jueves', int: 4}
    viernes = {str: 'Viernes', int: 5}
    sabado = {str: 'Sabado', int: 6}
    domingo = {str: 'Domingo', int: 7}


class Hora:
    '''
    Representación de una hora
    '''

    def __init__(self, **kwargs):
        '''
        puede ser como
        > hora + min (24h)
        > minutos desde medianoche
        '''
        self.hora = None
        self.min = None
        if len(kwargs) == 0:
            self.hora = 0
            self.min = 0
        elif len(kwargs) == 1:
            min_desde_medianoche = kwargs.get('min_desde_medianoche', None)
            hora = self.hora = kwargs.get('hora', None)
            if min_desde_medianoche != None:
                self.hora = min_desde_medianoche // 60
                self.min = min_desde_medianoche % 60
            elif hora != None:
                self.hora = hora
                self.min = 0
        elif len(kwargs) == 2:
            self.hora = kwargs.get('hora', None)
            self.min = kwargs.get('min', None)
            assert self.hora != None and type(
                self.hora) == int and self.min != None and type(self.min) == int
            # arreglamos minutos negativos fruto de restar duraciones
            if self.min < 0:
                self.hora -= 1
                # es negativo recordamos
                self.min = 60 + self.min
        else:
            raise Exception('Formato de hora incorrecto ->' + str(kwargs))

    def __str__(self):
        '''imprime la hora en formato 12 horas (am-pm)'''
        out = ''
        if self.hora > 12:
            out += str(self.hora-12) + ':' + ('0' if self.min <
                                              10 else '') + str(self.min) + ' pm'
        else:
            out += (str(self.hora)) + ':' + ('0' if self.min <
                                             10 else '') + str(self.min) + ' am'
        return out

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        return Hora(hora=self.hora - other.hora, min=self.min - other.min)

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        if self.hora != other.hora:
            return self.hora < other.hora
        else:
            return self.min < other.min

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        return self.hora == other.hora and self.min == other.min

    def get_datetime(self, dia_semana: DiaSemana, num_semana: int,  year: int = 2021):
        fecha = date.fromisocalendar(year, num_semana, dia_semana.value[int])
        return datetime(fecha.year, fecha.month, fecha.day, self.hora, self.min)


class Duracion:
    '''Representación de lo que dura cada clase, con un intervalo de dos horas'''

    def __init__(self, inicio: Hora, fin: Hora):
        self.inicio = inicio
        self.fin = fin
        self.duracion = self.fin - self.inicio

    def __repr__(self):
        return '{0} -> {1}'.format(self.inicio.__repr__(), self.fin.__repr__())

    def __str__(self):
        return self.__repr__() + ' [dura {0}'.format(self.duracion.hora) + (' hora' if self.duracion.hora == 1 else ' horas') + (' y {0} minutos]'.format(self.duracion.min) if self.duracion.min != 0 else ']')

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        # comparamos horas de inicio y si son iguales horas de fin
        if self.inicio != other.inicio:
            return self.inicio < other.inicio
        else:
            return self.fin < other.fin

    def get_datetimes(self, dia_semana: DiaSemana, num_semana: int,  year: int = 2021):
        '''
        Devuelve una tupla con las fechas de inicio y fin
        '''
        return self.inicio.get_datetime(dia_semana, num_semana, year), self.fin.get_datetime(dia_semana, num_semana, year)


class Profe:
    def __init__(self, notion_id: str, nombre: str, notion_obj: CollectionRowBlock = None):
        self.notion_id = notion_id
        self.nombre = nombre
        self.notion_obj = notion_obj

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return self.nombre


class Asignatura:
    def __init__(self, notion_id: str, nombre_completo: str, nombre_abreviado: str, curso: Curso, cuatri: Cuatri, num_teoricas: int = 0, num_practicas: int = 0, activas_teoricas: bool = False, activas_practicas: bool = False, profe_teoricas: Profe = None, profe_practicas: Profe = None, notion_obj: CollectionRowBlock = None):
        self.notion_id = notion_id
        self.nombre_completo = nombre_completo
        self.nombre_abreviado = nombre_abreviado
        self.curso = curso
        self.cuatri = cuatri
        self.num_teoricas = num_teoricas
        self.num_practicas = num_practicas
        self.activas_teoricas = activas_teoricas
        self.activas_practicas = activas_practicas
        self.profe_teoricas = profe_teoricas
        self.profe_practicas = profe_practicas
        self.notion_obj = notion_obj

    def __str__(self):
        out = ''
        if self.nombre_abreviado:
            out += str(self.nombre_abreviado) + ' => ' + \
                str(self.nombre_completo) + '\n'
        else:
            out += str(self.nombre_completo) + '\n'
        out += '\t' + 'Curso -> ' + self.curso.value[str] + '\n'
        out += '\t' + 'Cuatri -> ' + self.cuatri.value[str] + '\n'
        # info teoricas
        out += '\t' + 'TEORICAS --> ' + \
            str(self.num_teoricas) + ' clases dadas'
        if self.profe_teoricas:
            out += ' por ' + repr(self.profe_teoricas)
        if not self.activas_teoricas:
            out += ' (No están activas)'
        out += '\n'
        # info practicas
        out += '\t' + 'PRÁCTICAS --> ' + \
            str(self.num_practicas) + ' clases dadas'
        if self.profe_practicas:
            out += ' por ' + repr(self.profe_practicas)
        if not self.activas_practicas:
            out += ' (No están activas)'
        out += '\n'
        # acabado
        return out

    def __repr__(self):
        return self.nombre_abreviado.upper() if self.nombre_abreviado else self.nombre_completo


class Clase:
    def __init__(self, asignatura: Asignatura, dia_semana: DiaSemana, duracion: Duracion, presencial: bool = False, practica: bool = False, ubicacion: str = None, mostrar_dia_semana: bool = False):
        self.asignatura = asignatura
        self.dia_semana = dia_semana
        self.duracion = duracion
        self.presencial = presencial
        self.practica = practica
        self.ubicacion = ubicacion
        self.mostrar_dia_semana = mostrar_dia_semana

    def __str__(self):
        out = ''
        out += ('Práctica' if self.practica else 'Teórica') + ' ' + \
            ('presencial' if self.presencial else 'telemática') + \
            ' de ' + self.asignatura.__repr__() + '\n'
        out += '\t' + 'Duracion: ' + str(self.duracion) + '\n'
        if self.ubicacion:
            out += '\t' + 'Lugar: ' + self.ubicacion + '\n'
        if self.mostrar_dia_semana:
            out += '\t' + 'Dia de la semana: ' + self.dia_semana.value[str]
        return out

    def __repr__(self):
        return ('P' if self.practica else 'T') + self.dia_semana.value[str] + self.asignatura.__repr__() + str(self.duracion.inicio.hora)

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        # comparamos dias de semana
        if self.dia_semana != other.dia_semana:
            return self.dia_semana.value[int] < other.dia_semana.value[int]
        else:
            return self.duracion < other.duracion


class Horario:
    '''Horario como conjunto de clases agrupadas por días'''

    def __init__(self):
        self.clases = {}
        self.clases_as_list = []
        self.cuenta = 0
        for dia_semana in DiaSemana:
            self.clases[dia_semana] = []

    def add_clase(self, clase: Clase):
        assert clase.dia_semana != None
        self.clases[clase.dia_semana].append(clase)
        self.clases_as_list.append(clase)

    def __str__(self):
        out = ''
        for dia_semana, clases_horario in self.clases.items():
            out += '='*8 + dia_semana.value[str] + '='*8 + '\n'
            cuenta = 1
            for clase in sorted(clases_horario):
                out += '[[{0}]]:\t'.format(cuenta) + str(clase) + '\n'
                cuenta += 1
        return out

    def vacio(self):
        '''Devuelve si el horario está vacio'''
        return not ('Una clase al menos' in ['Sin clases ese día' if len(clases_dia) == 0 else 'Una clase al menos' for clases_dia in self.clases.values()])


if __name__ == '__main__':
    duracion = Duracion(Hora(hora=9), Hora(hora=10))
    print(duracion.get_datetimes(DiaSemana.jueves, 4))
