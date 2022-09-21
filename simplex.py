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

# pasa los enteros originarios del problema a float
def intToFloat(lista):
    for i in range(len(lista)):
        if (lista[i] == '<=') | (lista[i] == '>=') | (lista[i] == '=') | (lista[i] == '<') | (lista[i] == '>'):
            lista[i] = lista[i]
        else:
            lista[i] = float(lista[i]).__format__('0.4f')
    return lista

# Esta funcion agrega las variables de holgura que necesita el problema
"""cambiar parametro cantidadRestricciones por cantidad de variables"""
def agregarVariablesHolguraFuncionObjetivo(lista, cantidadVariablesHolgura):
    for i in range(cantidadVariablesHolgura):
        lista.append(float(0))
    lista.append('=')
    lista.append(float(0))
    return lista

#ESta función se encarga de vonvertir las desigualdades en igualdades y agrega variables de holgura
def agregarVariablesHolguraRestricciones(lista, cantidadVariablesHolgura):
    listaFinal = []
    contador = 0
    for j in range(len(lista)):
        lista1 = []
        for i in range(len(lista[j])):
            if lista[j][i] == '<=':
                for k in range(contador):
                    lista1.append(float(0))
                lista1.append(float(1))
                for l in range(contador, cantidadVariablesHolgura - 1):
                    lista1.append(float(0))
                contador += 1
                lista1.append('=')
            else:
                lista1.append(lista[j][i])

        listaFinal.append(lista1)
    return listaFinal

# esta función permite agregar las varibles de todos los tipos a las restricciones
def agregarVariablesRestricciones(lista, cantidadVariablesHolgura, cantidadVariablesArtificial, cantidadVariablesExceso):
    listaFinal = []
    lista1 = []
    #Este ciclo va a agregar las variables de holgura con 1 en la posicion correcta y 0 en el resto
    for j in range(len(lista)):
        if cantidadVariablesHolgura[1].__contains__(j):
            contador = 0
            for i in range(len(lista[j])):
                if lista[j][i] == '<=' or lista[j][i] == '>=' or lista[j][i] == '=':
                    for k in range(contador):
                        lista1.append(float(0))
                    lista1.append(float(1))
                    for l in range(contador, cantidadVariablesHolgura[0] - 1):
                        lista1.append(float(0))
                    contador += 1
                    lista1.append('=')
                else:
                    lista1.append(lista[j][i])
            listaFinal.append(lista1)
        else:
            for i in range(len(lista[j])):
                for l in range(cantidadVariablesHolgura[0] - 1):
                    lista1.append(float(0))





# Esta función se encarga de hacer el calculo respectivo al nuevo valor en el proceso de calculo de simplex
def calculaCasilla(casilla,pivote):
    casillaNegada = float(float(casilla) * -1.0).__format__()
    resultado = (float(casilla).__format__('0.4f') + casillaNegada) * float(pivote).__format__('0.4f')
    return resultado

# Esta función se encarga de dirigir el proceso de calculo de simplex
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
        bandera , colMenor = problema.__indiceColumnaMenor__()
        pivote = problema.__determinacionPivote__(colMenor)
        nuevaFila = problema.__nuevaFila__(pivote)
        tablaNueva = problema.__tablaNueva__(nuevaFila, pivote)
        tablaNueva = problema.__simplexMaxCalculo__(pivote, nuevaFila)
        solucionInicial = problema.__solucionSimplexMax__()
        """
        Hay que hacer algo que en la ultima itercion diga solucion optima, en laugar de solucion inicial
        """
        iteracion += 1




class problema:
    def __init__(self, lista):
        self.metodo = lista[0][0]
        self.optimizacion = lista[0][1]
        self.cant_v_decision = lista[0][2]
        self.cant_restricciones = lista[0][3]
        self.cant_v_holgura = lista[0][3]
        self.cant_v_artificial = []
        self.cant_v_exceso = []
        self.funcion_objetivo = self.__despejarFuncionObjetivoMax__(lista[1])
        self.restricciones = lista[2:]
        self.tablaActual = []
        self.tablaSiguiente = []
        self.ordenFilas = []

    #pasa a negativo los valores de la funcion objetivo
    """uptate Dos Faces"""
    def __despejarFuncionObjetivoMax__(self, lista):
        for i in range(len(lista)):
            if lista[i] == '=':
                lista[i] = lista[i]
            else:
                lista[i] = float(lista[i]) * -1
        return lista

    # Esta función se encarga de inicializar la lista de orden de las filas = ["U",3,4,5]
    """uptate Dos Faces"""
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

    #Esta función se encarga de actualizar la lista de orden de las filas
    """uptate Dos Faces"""
    def __actualizarOrdenFilas__(self, pivote):
        self.ordenFilas[pivote[1][0]] = int(pivote[1][1])+1
        #print("Orden de las filas: ", self.ordenFilas)
        writeFile("\nOrden de las filas: " + str(self.ordenFilas))

    # Esta función se encarga de pasar los numeros de las restricciones a la funcion que los convierte en float
    """uptate Dos Faces"""
    def __setRestriccionesFloats__(self):
        for i in range(len(self.restricciones)):
            self.restricciones[i] = intToFloat(self.restricciones[i])

    #Esta función trabaja como coordinadora en el proceso de agregado de variables de holgura, enn restricciones y en la funcion objetivo
    """ver self.objetivo y intToFloat"""
    def __agregarVariablesHolguraSimplexMax__(self):
        self.objetivo = agregarVariablesHolguraFuncionObjetivo(self.funcion_objetivo, int(self.cant_v_holgura))
        self.objetivo = intToFloat(self.objetivo)
        self.restricciones = agregarVariablesHolguraRestricciones(self.restricciones, int(self.cant_restricciones))
        self.__setRestriccionesFloats__()
        return self

    # Esta función se encarga de dar el formato a la tabla a base en las listas de restriccciones y funcion objetivo
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

    # Esta función se encarga de imprimir y registrar en el txt la tabla actual
    """Se debería de borrar pero se va a usar para pruebas"""
    def __printTabla__(self, opcion):
        if opcion == 1:
            tabla = self.tablaActual
            self.tablaActual = tabla
        else:
            tabla = self.tablaSiguiente
        for i in range(len(tabla)):
            writeFile(tabla[i])
            #print(tabla[i])

    # Esta función se encarga de imprimir y registrar en el txt los valores que ocupan el objeto problema
    """Se debería de borrar pero se va a usar para pruebas"""
    def __print__(self):
        informacionProblemaText = ("\nMetodo: " + self.metodo + "\n" +
              "Optimizacion: " + self.optimizacion + "\n" +
              "Cantidad de variables de decision: " + self.cant_v_decision + "\n" +
              "Cantidad de restricciones: " + self.cant_restricciones + "\n" +
              "Funcion objetivo: " + str(self.funcion_objetivo) + "\n" +
              "Restricciones: " + str(self.restricciones))
        #print(informacionProblemaText)
        writeFile(informacionProblemaText)

    #Esta función se encarga de cacular y retornar la solucion que se generó con base a la iteracion actual
    def __solucionSimplexMax__(self):

        solucion = []
        solucion.append(float(self.tablaActual[0][-1]).__format__('0.4f'))
        auxiliar = []
        resultados = []
        for i in range(1, len(self.tablaActual)):
            resultados.append(self.tablaActual[i][-1])
        for i in range(len(self.funcion_objetivo)-2):
            auxiliar.append(float(0).__format__('0.4f'))
        for j in range(len(auxiliar)+1):
            for k in self.ordenFilas:
                if j == k:
                    auxiliar[j-1] = resultados[self.ordenFilas.index(k)-1]
        solucion.append(auxiliar)
        writeFile("\nSolucion actual: " + str(solucion))
        return solucion

    #Esta función se encarga de deteriminar cual va a ser la columna pivote
    def __indiceColumnaMenor__(self):
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

    #Esta función se encarga de deteriminar cual va a ser el pivote dado el indice de la columna pivote que se va a usar
    #retorna una lista con la estructura [menor que resulta de las divisiones, [fila del pivote, columna del pivote]]
    """No es muy eficiente pero tocarla implica una parida por los tipos de datos"""
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

    #Esta función se encarga de generar la nueva fila pivote a base del pivote dado
    """uptate Dos Faces"""
    def __nuevaFila__(self, pivote):
        tabla = self.tablaActual
        fila = pivote[1][0]
        columna = pivote[1][1]
        nuevaFila = []
        for i in range(len(tabla[fila])):
            nuevaFila.append(float(
                float(tabla[int(fila)][i]) / float(tabla[int(fila)][columna])).__format__('0.4f'))
        return nuevaFila

    #Esta función se encarga de generar la nueva tabla a base de la fila pivote y los campos restantes lo rellena con ceros
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

    #Esta función coordina el calculo la iteracion del metodo simplex
    def __simplexMaxCalculo__(self, pivote, nuevaFila):
        tablaActual = self.tablaActual
        tablaNueva = self.tablaSiguiente
        tablaActualText = "\n--------------------------------Tabla Actual---------------------------------"
        writeFile(tablaActualText)
        self.__printTabla__(1)
        writeFile("\nPivote: " + str(pivote))
        tablaCerosText = "\n---------------------------Tabla nueva - ceros ------------------------------"
        writeFile(tablaCerosText)
        self.__printTabla__(2)
        for i in range(int(self.cant_restricciones) + 1):#cambiarlo por cantidad de variables
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
        self.__actualizarOrdenFilas__(pivote)
        return tablaNueva

    # Esta función va a verificar que simlos traen las restricciones y dira la cantidad de las diferentes variables que se necesitan
    def cantidadVariablesRestricciones(self):
        vHolgura = 0
        holguras = []
        vArtificial = 0
        artificiales = []
        vExceso = 0
        excesos = []
        for i in range(len(self.restricciones)):
            for j in range(len(self.restricciones[i])):
                if self.restricciones[i][j] == '<=':
                    vHolgura += 1
                    holguras.append(i)
                elif self.restricciones[i][j] == '>=':
                    vArtificial += 1
                    artificiales.append(i)
                    vExceso += 1
                    excesos.append(i)
                elif self.restricciones[i][j] == '=':
                    vArtificial += 1
                    artificiales.append(i)

        self.cant_v_holgura = [vHolgura, holguras]
        self.cant_v_artificial = [vArtificial, artificiales]
        self.cant_v_exceso = [vExceso, excesos]



#Esta función ejecuta el algoritmo del metodo simplex
def ejecutarSimplex(nombre_archivo):
    removeFile()
    datos = separarDatos(nombre_archivo)
    problema_simplex = problema(datos)
    problema_simplex.cantidadVariablesRestricciones()
    if problema_simplex.metodo == '1':  # Es simplex
        if (problema_simplex.optimizacion == "max") \
            and (problema_simplex.cant_v_artificial == 0) \
            and (problema_simplex.cant_v_exceso == 0) :  # Es maximizacion
            problema_simplex.__agregarVariablesHolguraSimplexMax__()
            problema_simplex.__makeOrdenFilas__()
            problema_simplex.__tabularProblema__()
            problema_simplex.__print__()
            metodoSimplex(problema_simplex)
    elif problema_simplex.metodo == '2': # Es dos fases

        print("No implementado")

    else:
        print("No existe el metodo ingresado")
        
def main():
    helpMessage = ("Bienvenido al programa de Simplex, usted ha seleccionado la opcion " +
            "de ayuda por lo que se le mostrara un poco de informacion \nsobre el programa!"+
            "\n\nEl programa se ejecuta de la siguiente manera: \npython3 simplex.py -h <nombre_archivo.txt> \n\n"+
            "El archivo de texto debe tener la siguiente estructura: \n"+
            "NOTA: Los datos deben estar separados por comas \n"+
            "1. El primer numero es el metodo a utilizar, 1 para simplex y 2 para dos fases \n"+
            "2. Despues se pone si se desea maximizar o minimizar \n"+
            "3. El segundo numero es el numero de variables \n"+
            "4. Se debe ingresar un salto de linea y despues ingresar la funcion objetivo \n"+
            "5. Se debe ingresar un salto de linea y luego poner cada restriccion con un salto de linea de por medio\n"+
            "\nEl programa se deberia ver algo asi: \n"+
            "\n1,max,2,3"+
            "\n16,15"+
            "\n40,31,<=,124"+
            "\n-1,1,<=,1"+
            "\n1,0,<=,3\n\n")
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        print("No se han ingresado parametros ni archivos de entrada por lo que el programa se cerrara")
        exit(0)
    if sys.argv[1] == "-h":
        if len(sys.argv) <= 2:
            print(helpMessage)
            print("El sistema se cerrara sin realizar el problema ya que no se ha ingresado ningun documento de texto!")
            exit(0)
        else:
            print(helpMessage)
            print("El sistema se ejecutara con el archivo de texto: " + sys.argv[2])
            print("El resultado se guardara en el archivo: resultado.txt")
            nombre_archivo = sys.argv[2]
            ejecutarSimplex(nombre_archivo)
    else:
        nombre_archivo = sys.argv[1]
        ejecutarSimplex(nombre_archivo)
    exit(0)





main()