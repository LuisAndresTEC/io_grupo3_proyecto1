from asyncore import write
from mailbox import NoSuchMailboxError
import numpy as np
import sys
import os

# Esta funcion se encargará de eliminar el archivo txt para borrar todo su contenido
def removeFile():
    try:
        os.remove("resultado.txt")
    except OSError:
        pass

# Este será un lector de archivos txt
def readFile(nombre_archivo):
    reader = open(nombre_archivo, 'r')
    file = reader.read()
    reader.close()
    return file

# Esta funcion se encargar de escribir en el archivo txt
def writeFile(text):
    reader = open("resultado.txt", 'a')
    if type(text) == type(list):
        for i in text:
            #reader.write("\n")
            i = str(i)
            reader.write(i)

    else:
        text = str(text)
        reader.write("\n")
        reader.write(text)
    reader.close()



# Esta función se encargará de separar los datos del archivo txt
def separarDatos(nombre_archivo):
    datos = readFile(nombre_archivo)
    datos = datos.split()
    datos2 = []
    for i in range(len(datos)):
        datos2.append(datos[i].split(','))
    return datos2


def setNumeros(lista):
    for i in range(len(lista)):
        if (lista[i] == '<=') | (lista[i] == '>=') | (lista[i] == '=') | (lista[i] == '<') | (lista[i] == '>'):
            lista[i] = lista[i]
        else:
            lista[i] = float(lista[i]).__format__('0.4f')
    return lista


# Esta funcion agrega las variables de augura que necesita el problema


def agregar_variables_augura_objetivo(lista, cantidadRestricciones):
    for i in range(cantidadRestricciones):
        lista.append(float(0))
    lista.append('=')
    lista.append(float(0))
    return lista


def agregar_variables_augura_restricciones(lista, cantidadRestricciones):
    listaFinal = []
    contador = 0
    for j in range(len(lista)):
        lista1 = []
        for i in range(len(lista[j])):
            if lista[j][i] == '<=':
                for k in range(contador):
                    lista1.append(float(0))
                lista1.append(float(1))
                for l in range(contador, cantidadRestricciones - 1):
                    lista1.append(float(0))
                contador += 1
                lista1.append('=')
            else:
                lista1.append(lista[j][i])

        listaFinal.append(lista1)
    return listaFinal

def calculaCasilla(casilla,pivote):
    casillaNegada = float(float(casilla) * -1.0).__format__()
    resultado = (float(casilla).__format__('0.4f') + casillaNegada) * float(pivote).__format__('0.4f')
    #print("------Casilla: ", casilla, "Pivote: ", pivote, "Resultado: ", resultado,"------")
    writeFile("------Casilla: " + str(casilla) + "Pivote: " + str(pivote) + "Resultado: " + str(resultado) + "------")
    return resultado


def metodoSimplex(problema):
    bandera = True
    iteracion = 0
    spacer = "\n-----------------------------------------------------------------------------\n"

    while bandera:
        numero_iteracion = "-----------------------------Iteracion numero: " + str(iteracion) + "-----------------------------"
        #print(spacer)
        #print(numero_iteracion)
        #print(spacer)
        writeFile(spacer)
        writeFile(numero_iteracion)
        writeFile(spacer)
        bandera , colMenor = problema.__indexColumnaMenor__()
        pivote = problema.__determinacionPivote__(colMenor)
        nuevaFila = problema.__nuevaFila__(pivote)#problemas
        #problema.__grabarTabla__()
        tablaNueva = problema.__tablaNueva__(nuevaFila, pivote)
        tablaNueva = problema.__simplexCalculo__(pivote, nuevaFila)
        solucionInicial = problema.__solucionInicial__()
        iteracion += 1












class problema:
    def __init__(self, lista):
        self.metodo = lista[0][0]
        self.optimizacion = lista[0][1]
        self.cant_v_decision = lista[0][2]
        self.cant_restricciones = lista[0][3]
        self.funcion_objetivo = self.__despejarFuncionObjetivo__(lista[1])
        self.restricciones = lista[2:]
        self.tablaActual = []
        self.tablaSiguiente = []
        self.ordenFilas = []

    def __despejarFuncionObjetivo__(self, lista):
        for i in range(len(lista)):
            if lista[i] == '=':
                lista[i] = lista[i]
            else:
                lista[i] = float(lista[i]) * -1
        return lista

    def __makeOrdenFilas__(self):
        orden = []
        orden.append("U")
        for i in range(len(self.restricciones)):
            orden.append(i + 1 + int(self.cant_v_decision))
        self.ordenFilas = orden
        #print("Orden de las filas: ", self.ordenFilas)
        writeFile("\nOrden de las filas: ")
        writeFile(self.ordenFilas)
        return self

    def __updateOrdenFilas__(self, pivote):
        self.ordenFilas[pivote[1][0]] = int(pivote[1][1])+1
        #print("Orden de las filas: ", self.ordenFilas)
        writeFile("\nOrden de las filas: " + str(self.ordenFilas))

    def __getRestricciones__(self):
        restricciones = []
        for i in range(len(self.restricciones)):
            restricciones.append(self.restricciones[i])
        for j in range(len(restricciones)):
            restricciones[j] = setNumeros(restricciones[j])
        self.restricciones = restricciones
        return self.restricciones

    def __agregarVariablesSimplex__(self):
        self.objetivo = agregar_variables_augura_objetivo(self.funcion_objetivo, int(self.cant_restricciones))
        self.objetivo = setNumeros(self.objetivo)
        self.restricciones = agregar_variables_augura_restricciones(self.restricciones, int(self.cant_restricciones))
        self.__getRestricciones__()
        return self

    def __tabularProblema__(self):
        tabla = []
        tabla1 = []
        for j in range(len(self.funcion_objetivo)):
            if self.funcion_objetivo[j] != '=':
                tabla1.append(float(self.funcion_objetivo[j]).__format__('0.4f'))
        tabla.append(tabla1)
        for i in range(len(self.restricciones)):
            tabla2 = []
            for j in range(len(self.restricciones[i])):
                if self.restricciones[i][j] != '=':
                    tabla2.append(float(self.restricciones[i][j]).__format__('0.4f'))
            tabla.append(tabla2)
        self.tablaActual = tabla
        return tabla

    def __printTabla__(self, opcion):
        if opcion == 1:
            tabla = self.tablaActual
            self.tablaActual = tabla
        else:
            tabla = self.tablaSiguiente
        for i in range(len(tabla)):
            writeFile(tabla[i])
            #print(tabla[i])

    def __print__(self):
        informacionProblemaText = ("\nMetodo: " + self.metodo + "\n" +
              "Optimizacion: " + self.optimizacion + "\n" +
              "Cantidad de variables de decision: " + self.cant_v_decision + "\n" +
              "Cantidad de restricciones: " + self.cant_restricciones + "\n" +
              "Funcion objetivo: " + str(self.funcion_objetivo) + "\n" +
              "Restricciones: " + str(self.restricciones))
        #print(informacionProblemaText)
        writeFile(informacionProblemaText)

    #arreglar para trabajar ordenFilas
    def __solucionInicial__(self):

        solucion = []
        solucion.append(float(self.tablaActual[0][-1]).__format__('0.4f'))
        auxiliar = []
        resultados = []
        for i in range(1, len(self.tablaActual)):
            resultados.append(self.tablaActual[i][-1])
        #print("Resultados: ", resultados)
        writeFile("\nResultados: " + str(resultados))
        for i in range(len(self.funcion_objetivo)-2):
            auxiliar.append(float(0).__format__('0.4f'))
        for j in range(len(auxiliar)+1):
            for k in self.ordenFilas:
                if j == k:
                    auxiliar[j-1] = resultados[self.ordenFilas.index(k)-1]
        solucion.append(auxiliar)
        #print("Solucion inicial: ", solucion)
        writeFile("\nSolucion inicial: " + str(solucion))
        return solucion

    def __indexColumnaMenor__(self):
        negativos = []

        for i in range(len(self.tablaActual[0])-1):
            if float(self.tablaActual[0][i]) < 0:
                negativos.append(self.tablaActual[0][i])

        if len(negativos) < 1:
            return False , 0
        else:
            resultado = max(negativos)
            #print("Minimo: " , float(self.tablaActual[0].index(resultado)).__format__('0.4f') , " Valor: " , float(resultado).__format__('0.4f'))
            writeFile("Minimo: " + str(float(self.tablaActual[0].index(resultado)).__format__('0.4f')) + " Valor: " + str(float(resultado).__format__('0.4f')))
            return True , int(self.tablaActual[0].index(resultado))

    def __determinacionPivote__(self, columna):
        tabla = self.tablaActual
        divisiones = []
        for i in range(len(tabla) - 1):
            if tabla[i + 1][columna] > float(0).__format__('0.4f'):
                casilla = float(tabla[i + 1][-1])
                pivote = float(tabla[i + 1][columna])
                pair = [float(casilla/pivote).__format__('0.4f'), [i+1, columna]]
                divisiones.append(pair)

        pivote = divisiones[0]
        for i in range(len(divisiones)):
            if divisiones[i][0] < pivote[0]:
                pivote = divisiones[i]
        return pivote

    def __nuevaFila__(self, pivote):
        tabla = self.tablaActual
        fila = pivote[1][0]
        columna = pivote[1][1]
        nuevaFila = []
        for i in range(len(tabla[fila])):
            nuevaFila.append(float(
                float(tabla[int(fila)][i]) / float(tabla[int(fila)][columna])).__format__('0.4f'))
        #print("Nueva fila: ", nuevaFila)
        writeFile("Nueva Fila: ")
        writeFile(nuevaFila)
        return nuevaFila

    def __tablaNueva__(self, nuevaFila, pivote):
        tabla = []
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                fila = []
                for j in range(len(self.funcion_objetivo)-1):
                    fila.append(float(0).__format__('0.4f'))
                tabla.append(fila)
            else:
                tabla.append(nuevaFila)
        self.tablaSiguiente = tabla
        return tabla

    #Esta función, no sirve necesita reparación solo escribe taxto no listas
    def __grabarTabla__(self):
        tabla = self.tablaActual
        writeFile(tabla)

    def __simplexCalculo__(self, pivote, nuevaFila):
        tablaActual = self.tablaActual
        tablaNueva = self.tablaSiguiente
        tablaActualText = "\n--------------------------------Tabla Actual---------------------------------"
        writeFile(tablaActualText)
        #print(tablaActualText)
        self.__printTabla__(1)
        writeFile("\nPivote: " + str(pivote))
        #print("\nPivote: " + str(pivote))
        tablaCerosText = "\n---------------------------Tabla nueva - ceros ------------------------------"
        writeFile(tablaCerosText)
        #print(tablaCerosText)
        self.__printTabla__(2)
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                nuevaFila = []
                for j in range(len(self.funcion_objetivo)-1):
                    casilla = float(tablaActual[i][j]) + (float(tablaActual[i][pivote[1][1]])*-1 * float(tablaNueva[pivote[1][0]][j]))
                    if casilla == float(-0).__format__('0.4f'):
                        casilla = float(0).__format__('0.4f')
                    nuevaFila.append(float(casilla).__format__('0.4f'))
                tablaNueva[i] = nuevaFila
        tablaNuevaText = "\n-------------------------Tabla nueva - calculada ----------------------------"
        writeFile(tablaNuevaText)
        #print(tablaNuevaText)
        self.__printTabla__(2)
        self.tablaActual = tablaNueva
        self.tablaSiguiente = []
        self.__updateOrdenFilas__(pivote)
        return tablaNueva



def ejecutarSimplex(nombre_archivo):
    removeFile()
    datos = separarDatos(nombre_archivo)
    problema_simplex = problema(datos)
    problema_simplex.__agregarVariablesSimplex__()
    problema_simplex.__makeOrdenFilas__()
    problema_simplex.__tabularProblema__()
    problema_simplex.__print__()
    if problema_simplex.metodo == '1':  # Es simplex
        tablaInicialText = "\n---------------------------Tabla inicial------------------------------------\n"
        writeFile(tablaInicialText)
        #print(tablaInicialText)
        problema_simplex.__printTabla__(1)
        metodoSimplex(problema_simplex)
        


def main():
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        print("No se han ingresado parametros ni archivos de entrada por lo que el programa se cerrara")
        exit(0)
    if sys.argv[1] == "-h":
        if len(sys.argv) <= 2:
            print("No se ha ingresado el nombre del archivo de entrada")
            exit(0)
        else:
            print("Bienvenido al programa de Simplex, usted ha seleccionado la opcion " +
            "de ayuda por lo que se le mostrara un poco de informacion \nsobre el programa!")
            nombre_archivo = sys.argv[2]
            ejecutarSimplex(nombre_archivo)
    else:
        nombre_archivo = sys.argv[1]
        ejecutarSimplex(nombre_archivo)
    exit(0)





main()