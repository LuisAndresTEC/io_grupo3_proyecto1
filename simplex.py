import sys
import os
import collections

"""
Descripcion: Esta funcion elimina el archivo resultado.txt para que no se acumulen los resultados de ejecuciones anteriores
Entradas: Ninguna
Salidas: Ninguna
"""
def removeFile():
    try:
        os.remove("operacion_solucion.txt")
    except OSError:
        pass

"""
Descripcion: Esta funcion lee el archivo de texto y lo asigna a una lista
Entradas: El nombre del archivo de texto
Salidas: Una lista
"""
def readFile(nombre_archivo):
    reader = open(nombre_archivo, 'r')
    file = reader.read()
    reader.close()
    return file

"""
Descripcion: Esta funcion se encarga de escribir en el archivo de solucion un string que se le pasa como parametro de entrada
Entradas: Un string
Salidas: Ninguna
"""
def writeFile(text):
    reader = open("operacion_solucion.txt", 'a')
    if type(text) == type(list):
        for i in text:
            i = str(i)
            reader.write(i)
    else:
        text = str(text)
        reader.write("\n")
        reader.write(text)
    reader.close()

"""
Descripcion: Esta funcion se encarga de leer el archivo de texto y separar los datos en una lista de listas
Entradas: El nombre del archivo de texto
Salidas: Una lista de listas
"""
def separarDatos(nombre_archivo):
    datos = readFile(nombre_archivo)
    datos = datos.split()
    datos2 = []
    for i in range(len(datos)):
        datos2.append(datos[i].split(','))
    return datos2

"""
Descripcion: Esta funcion se encarga de leer una lista e ir conviertiendo cada uno de sus items a floats
Entradas: Una lista
Salidas: Una lista de floats
"""
def intToFloat(lista):
    for i in range(len(lista)):
        if (lista[i] == '<=') | (lista[i] == '>=') | (lista[i] == '=') | (lista[i] == '<') | (lista[i] == '>'):
            lista[i] = lista[i]
        else:
            lista[i] = float(lista[i])
    return lista


"""
Descripcion: Esta funcion se encarga de agregar las variables de holgura a la lista de restricciones
Entradas: Una lista de listas y la cantidad de variables de holgura
Salidas: Una lista de listas con las variables de holgura agregadas
"""
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


"""
Descripcion: Esta funcion se encarga de agregar las variables artificiales a la lista de restricciones, tambien agrega las variables de holgura y las variables de exceso. Tambien agrega la funcion objetivo
Entradas: La funcion objetivo y la lista de restricciones
Salidas: Una lista de listas con las variables artificiales agregadas en 1s y 0s, una lista con la funcion objetivo y la lista de restricciones
"""
def agregarVariablesRestriccionesMin(funcionObjetivo, lista):
    listaFinal = []
    indiceRestas = []
    listaArtificiales = []

    #Este ciclo va a agregar todas las variables antes de la igualdad en una lista de restricciones
    for j in range(len(lista)):
        listaTemporal = []
        listaArtificiales = []
        for i in range(len(lista[j])):
            if lista[j][i] == '<=' or lista[j][i] == '>=' or lista[j][i] == '=':
                break
            else:
                listaTemporal.append(lista[j][i])
                listaArtificiales.append(float(0))
        listaFinal.append(listaTemporal)



    #Este ciclo va a agregar las variables de holgura, exceso y artificial a las restricciones
    for j in range(len(lista)):
        listaTemporal = listaFinal[j]
        for i in range(len(lista[j])):
            if lista[j][i] == '<=':
                #Agrega variable de holgura
                listaTemporal.append(float(1))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
                listaArtificiales.append(float(0))
            elif lista[j][i] == '>=':
                #Agrega variable de exceso
                listaTemporal.append(float(-1))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaArtificiales.append(float(0))
                #Agrega variable artificial
                listaTemporal.append(float(1))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
                indiceRestas.append(j)
                listaArtificiales.append(float(1))
            elif lista[j][i] == '=':
                #Agrega variable artificial
                listaTemporal.append(float(1))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
                indiceRestas.append(j)
                listaArtificiales.append(float(1))
    
    #Este ciclo agrega los iguales y los resultados de cada restricción
    for j in range(len(lista)):
        listaTemporal = []
        listaTemporal = listaFinal[j]
        for i in range(len(lista[j])):
            if lista[j][i] == '>=' or lista[j][i] == '=' or lista[j][i] == '<=':
                #Agrega los simbolos iguales a la lista
                listaTemporal.append('=')
                listaTemporal.append(lista[j][i+1])
                listaFinal[j]=listaTemporal

    
    listaArtificiales.append('=')
    listaArtificiales.append(float(0))

    restriccionesRestas = []
    for j in range(len(indiceRestas)):
        restriccionesRestas.append(listaFinal[indiceRestas[j]])

    listaTemporal = []
    #Agrega los iguales a la listaArtificiales
    for i in range(len(listaArtificiales)):
        if listaArtificiales[i] == "=":
            listaTemporal.append("=")
            listaTemporal.append(float(listaArtificiales[i+1])*-1)
            break
        listaTemporal.append(float(listaArtificiales[i])*-1)


    intToFloat(listaTemporal)
    listaArtificiales = listaTemporal
    funcionTemporal = []
    #Suma los itemes de las restricciones con la funcion objetivo, forma parte de la preparacion de la funcion objetivo en la fase uno
    for i in range(len(restriccionesRestas[0])):
        suma = 0.0000
        if restriccionesRestas[0][i] == "=":
            for k in range(len(restriccionesRestas)):
                suma += float(restriccionesRestas[k][i+1])*-1
            suma += float(listaArtificiales[i+1])*-1
            funcionTemporal.append(suma)
            break
        else:    
            for j in range(len(restriccionesRestas)):
                suma += float(restriccionesRestas[j][i])*-1
            suma += float(listaArtificiales[i])*-1
            funcionTemporal.append(suma)

    intToFloat(funcionTemporal)
    funcionObjetivo = funcionTemporal
    return listaFinal, funcionObjetivo, listaArtificiales


"""
Descripcion: Esta funcion se encarga de agregar las variables artificiales a la lista de restricciones, tambien agrega las variables de holgura y las variables de exceso. Tambien agrega la funcion objetivo
Entradas: La funcion objetivo y la lista de restricciones
Salidas: Una lista con la funcion objetivo y la lista de restricciones
"""
def agregarVariablesRestriccionesMax(funcionObjetivo, lista):
    listaFinal = []
    listaTemporal = []
    for i in range(len(lista)):
        listaTemporal.append(intToFloat(lista[i]))
    lista = listaTemporal
    #Este ciclo va a agregar todas las variables antes de la igualdad en una lista de restricciones
    for j in range(len(lista)):
        listaTemporal = []
        for i in range(len(lista[j])):
            if lista[j][i] == '<=' or lista[j][i] == '>=' or lista[j][i] == '=':
                break
            else:
                listaTemporal.append(lista[j][i])
        listaFinal.append(listaTemporal)

    #Este ciclo va a agregar las variables de holgura, exceso y artificial a las restricciones
    for j in range(len(lista)):
        listaTemporal = listaFinal[j]
        for i in range(len(lista[j])):
            if lista[j][i] == '<=':
                #Agrega variable de holgura
                listaTemporal.append(float(1))
                funcionObjetivo.append(float(0))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
            elif lista[j][i] == '>=':
                #Agrega variable de exceso
                listaTemporal.append(float(-1))
                funcionObjetivo.append(float(0))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                #Agrega variable artificial
                listaTemporal.append(float(1))
                funcionObjetivo.append(float(0))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
            elif lista[j][i] == '=':
                #Agrega variable artificial
                listaTemporal.append(float(1))
                funcionObjetivo.append(float(0))
                for k in range(len(listaFinal)):
                    if k != j:
                        listaFinal[k].append(float(0))
                listaFinal[j]=listaTemporal
   
   
    #Este ciclo agrega los iguales y los resultados de cada restricción
    for j in range(len(lista)):
        listaTemporal = listaFinal[j]
        for i in range(len(lista[j])):
            if lista[j][i] == '>=' or lista[j][i] == '=' or lista[j][i] == '<=':
                listaTemporal.append('=')
                listaTemporal.append(lista[j][i+1])
                listaFinal[j]=listaTemporal
    funcionObjetivo.append('=')
    funcionObjetivo.append(float(0))
    return listaFinal, funcionObjetivo

"""
Descripcion: Esta función se encarga de hacer el calculo referente al nuevo valor a asignar en cada casilla en cada iteración 
Entradas: El valor antiguo de la casilla y el pivote
Salidas: El resultado de la operación
"""
def calculaCasilla(casilla,pivote):
    casillaNegada = float(float(casilla) * -1.0).__format__()
    resultado = (float(casilla) + casillaNegada) * float(pivote)
    return resultado

"""
Descripcion: Esta función se encarga de revisar que una lista no tenga itemes repetidos
Entradas: Una lista
Salidas: Verdadero o falso
"""
def itemRepetido(lista):
    if len(lista) != len(set(lista)):
        return True
    else:
        return False

"""
Descripcion: Esta función se encarga de la dirección del flujo de ejecución de los problemas a los que se les aplica el método Simplex 
Entradas: recibe el objeto problema 
Salidas: el problema resuelto
"""
def metodoSimplex(problema):
    if itemRepetido(problema.funcionObjetivo):
        writeFile("Se encontro empate en variables de la funcion objetivo, se realizara un rompimiento de estos!")
    bandera = True
    iteracion = 0
    spacer = "\n-----------------------------------------------------------------------------\n"
    while bandera:
        bandera , colMenor = problema.__indiceColumnaMenor__()
        if bandera == False:
            break
        elif bandera == True and colMenor == 0:
            numero_iteracion = "-----------------------------Iteracion numero: " + str(
                iteracion) + "-----------------------------"
            writeFile(spacer)
            writeFile(numero_iteracion)
            writeFile(spacer)

        numero_iteracion = "-----------------------------Iteracion numero: " + str(iteracion) + "-----------------------------"
        writeFile(spacer)
        writeFile(numero_iteracion)
        writeFile(spacer)
        pivote = problema.__determinacionPivote__(colMenor)
        if len(pivote) == 0:
            break
        nuevaFila = problema.__nuevaFila__(pivote)
        tablaNueva = problema.__tablaNueva__(nuevaFila, pivote)
        tablaNueva = problema.__simplexMaxCalculo__(pivote, nuevaFila)
        solucionInicial = problema.__solucionSimplexMax__()
        iteracion += 1

"""
Descripcion: Esta funcion se encarga de recibir una lista de restricciones y quitarle las variables artificiales para prepararla para la fase dos
Entradas: Recibe la lista de restricciones y el problema
Salidas: La lista de restricciones sin variables artificiales
"""
def eliminarVariablesArtificialesRestricciones(lista, problema):
    for i in range(len(problema.listaArtificiales)):
        if problema.listaArtificiales[i] == "=":
            problema.listaArtificiales.pop(i)
            break
    contador = 0
    while contador < len(problema.listaArtificiales)-1:
        if problema.listaArtificiales[contador] == -1.0:
            for j in range(len(lista)):
                lista[j].pop(contador)
            problema.listaArtificiales.pop(contador)
        else:
            contador += 1
    problema.tablaActual = lista
    return lista

"""
Descripcion: Esta función se encarga de la dirección del flujo de ejecución de los problemas a los que se les aplica el método Dos Fases
Entradas: Recibe el objeto problema y un contador
Salidas: Ninguna
"""
def metodoDosFases(problema, contador):
    if itemRepetido(problema.funcionObjetivo):
        writeFile("Se encontro empate en variables de la funcion objetivo, se realizara un rompimiento de estos!")
    bandera = True
    iteracion = 0
    spacer = "\n-----------------------------------------------------------------------------\n"
    while bandera:
        bandera , colMenor = problema.__indiceColumnaMenor__()
        if bandera == False:
            if contador == 1:
                break
            listaTemporal = []
            nuevaTablaSinRestriccinesArtificiales = eliminarVariablesArtificialesRestricciones(problema.tablaActual, problema)
            problema.restricciones = nuevaTablaSinRestriccinesArtificiales[1:]
            problema.funcionObjetivo = nuevaTablaSinRestriccinesArtificiales[0]
            problema.funcionObjetivo = remplazarFuncionObjetivoFaseDos(problema)
            problema.tablaActual[0] = operarFuncionObjetivoFaseDos(problema)
            problema.funcionObjetivo = problema.tablaActual[0]
            listaFinal = []
            negativos = []
            for i in range(len(problema.tablaActual[0]) - 1):
                if int(problema.tablaActual[0][i]) < 0:
                    negativos.append(problema.tablaActual[0][i])
            if len(negativos) == 0 and problema.tablaActual[0][-1] < 0:
                writeFile("\n\n\n Este sería el resultado final de la ejecución del método 2 fases")
                writeFile(problema.ordenFilas)
                problema.__printTabla__(1)
                problema.__solucionSimplexMax__()
            else:
                metodoDosFases(problema, 1)
            break
        numero_iteracion = "-----------------------------Iteracion numero: " + str(iteracion) + "-----------------------------"
        writeFile(spacer)
        writeFile(numero_iteracion)
        writeFile(spacer)
        pivote = problema.__determinacionPivote__(colMenor)
        nuevaFila = problema.__nuevaFilaDosFases__(pivote)
        tablaNueva = problema.__tablaNuevaDosFases__(nuevaFila, pivote)
        tablaNueva = problema.__simplexMinCalculo__(pivote, nuevaFila)
        solucionInicial = problema.__solucionSimplexMax__()
        """
        Hay que hacer algo que en la ultima itercion diga solucion optima, en laugar de solucion inicial
        """
        iteracion += 1



"""
Descripcion:esta funcion cambia la función objetivo de de acuerdo a las necesidades en la segunda face de dos faces 
Entradas: recibe el objeto problema
Salidas: nueva funcion objetivo con los valores renovados
"""
def remplazarFuncionObjetivoFaseDos(problema):
    listaTemporal = []
    listaAuxiliar = []

    for i in range(len(problema.funcionObjetivoPrimaria)):
        listaTemporal.append(problema.funcionObjetivoPrimaria[i]*-1)
    problema.funcionObjetivoPrimaria = listaTemporal
    for j in range(len(problema.funcionObjetivoPrimaria)):
        problema.funcionObjetivo[j] = listaTemporal[j]
    for k in range(len(problema.funcionObjetivo)):
        if problema.funcionObjetivo[k] != "=":
            listaAuxiliar.append(problema.funcionObjetivo[k])
    return listaAuxiliar


"""
Descripcion: Esta función hace cero las actualizaciones de función objetivo en la tabla 
Entradas: Recibe el objeto llamdo problema
Salidas: Nueva fila de encabezado para la tabla
"""
def operarFuncionObjetivoFaseDos(problema):
    lista = problema.tablaActual[0]
    for w in range(len(problema.funcionObjetivoPrimaria)):
        menor = 0
        for i in range(len(problema.funcionObjetivoPrimaria)):
            if problema.funcionObjetivoPrimaria[menor] > problema.funcionObjetivoPrimaria[i]:
                menor = i
        problema.funcionObjetivoPrimaria[menor] = (problema.funcionObjetivoPrimaria[menor] * 5000)
        listaTemporal = []
        for j in range(len(problema.tablaActual)):
            if problema.tablaActual[j][menor] == 1:
                filaPivote = problema.tablaActual[j]
        listaCalculada = []
        if len(lista) == 0:
            lista = problema.tablaActual[0]
        for k in range(len(lista)):
            listaCalculada.append(float(lista[k]) + (float(lista[menor]*-1) * float(filaPivote[k])))
        lista = listaCalculada
    return lista






"""
Descripcion: Clase problema, integra todos los datos del problema a resolver
Entradas: Ninguna
Salidas: Ninguna
"""
class problema:
    """
    Descripcion: Funcion que inicia todos las variables
    Entradas: Ninguna
    Salidas: Ninguna
    """
    def __init__(self, lista):
        self.metodo = lista[0][0]
        self.optimizacion = lista[0][1]
        self.cant_v_decision = lista[0][2]
        self.cant_restricciones = lista[0][3]
        self.funcionObjetivoPrimaria = lista[1]
        self.cant_v_holgura = []
        self.cant_v_artificial = []
        self.cant_v_exceso = []
        self.funcionObjetivo = self.__despejarFuncionObjetivoMax__(lista[1])
        self.restricciones = lista[2:]
        self.tablaActual = []
        self.tablaSiguiente = []
        self.ordenFilas = []
        self.listaArtificiales = []

    """
    Descripcion: Funcion que despeja la funcion objetivo para maximizar
    Entradas: El problema y una lista
    Salidas: Una lista
    """
    def __despejarFuncionObjetivoMax__(self, lista):
        for i in range(len(lista)):
            if lista[i] == '=':
                lista[i] = lista[i]
            else:
                lista[i] = float(lista[i]) * -1
        return lista

    """
    Descripcion: Funcion que determina el orden de las filas
    Entradas: El problema
    Salidas: El problema cambiado
    """
    def __makeOrdenFilas__(self):
        orden = []
        orden.append("U")
        if (self.cant_v_exceso[0] > 0):
            #se hace  alista de los indices d elas variables identificadoras de los numeros
            for i in range(int(self.cant_restricciones)):
                if self.cant_v_exceso[1].__contains__(i):
                    orden.append(i + 2 + int(self.cant_v_decision))
                else:
                    orden.append(i + 1 + int(self.cant_v_decision))
        else:
            for i in range(len(self.restricciones)):
                orden.append(i + 1 + int(self.cant_v_decision))
        self.ordenFilas = orden
        writeFile("\nOrden de las filas: ")
        writeFile(self.ordenFilas)
        return self

    """
    Descripcion: Funcion que actualiza el orden de las filas
    Entradas: El problema, un pivote
    Salidas: Ninguna
    """
    def __actualizarOrdenFilas__(self, pivote):
        self.ordenFilas[pivote[1][0]] = int(pivote[1][1])+1
        writeFile("\nOrden de las filas: " + str(self.ordenFilas))

    """
    Descripcion: esta funcion cambia el tipo de las restricciones
    Entradas: obtiene  las restricciones del objeto de la clase
    Salidas: cambia el tipo de los nuemros en las restriccines
    """
    def __setRestriccionesFloats__(self):
        for i in range(len(self.restricciones)):
            self.restricciones[i] = intToFloat(self.restricciones[i])

    """
    Descripcion: Funcion que determina la cantidad de variables de holgura en el caso de maximizar
    Entradas: El problema
    Salidas: El problema cambiado
    """
    def __agregarVariablesHolguraSimplexMax__(self):
        self.funcionObjetivo = intToFloat(self.funcionObjetivo)
        listaTemporal = []
        for i in range(len(self.restricciones)):
            listaTemporal.append(intToFloat(self.restricciones[i]))
        self.restricciones = listaTemporal
        tablaCompleta = agregarVariablesRestriccionesMax(self.funcionObjetivo, self.restricciones)
        self.restricciones = tablaCompleta[0]
        self.funcionObjetivo = tablaCompleta[1]
        self.funcionObjetivo = intToFloat(self.funcionObjetivo)
        self.__setRestriccionesFloats__()
        return self

    """
    Descripcion: Funcion que determina la cantidad de variables de holgura en el caso de maximizar
    Entradas: El problema
    Salidas: El problema cambiado
    """
    def __agregarVariablesHolguraSimplexMin__(self):
        tablaCompleta = agregarVariablesRestriccionesMin(self.funcionObjetivo, self.restricciones)
        self.restricciones = tablaCompleta[0]
        self.funcionObjetivo = tablaCompleta[1]
        self.listaArtificiales = tablaCompleta[2]
        self.funcionObjetivo = intToFloat(self.funcionObjetivo)
        self.__setRestriccionesFloats__()
        return self

    """
    Descripcion: Función que genera la tabla o al menos la organiza
    Entradas: Toma la los datos del objeto de la clase 
    Salidas: Asiga la tabla al espacio en el objeto establacido para ella
    """
    def __tabularProblema__(self):
        tabla = []
        tabla1 = []
        for j in range(len(self.funcionObjetivo)):
            if self.funcionObjetivo[j] != '=':
                tabla1.append(float(self.funcionObjetivo[j]))
        tabla.append(tabla1)
        for i in range(len(self.restricciones)):
            tabla2 = []
            for j in range(len(self.restricciones[i])):
                if self.restricciones[i][j] != '=':
                    tabla2.append(float(self.restricciones[i][j]))
            tabla.append(tabla2)
        self.tablaActual = tabla
        return tabla

    """
    Descripcion: Imprime la tabla en el archivo de solución 
    Entradas: Un entero que dice si se quieres imprimir la tabla actual o la tabla siguiente
    Salidas: La tabla deseada impresa
    """
    def __printTabla__(self, opcion):
        if opcion == 1:
            tabla = self.tablaActual
            self.tablaActual = tabla
        else:
            tabla = self.tablaSiguiente
        for i in range(len(tabla)):
            writeFile(tabla[i])

    """
    Descripcion: Imprime el problema al principio de la solucion
    Entradas: El problema
    Salidas: Ninguna
    """
    def __print__(self):
        informacionProblemaText = ("\nMetodo: " + self.metodo + "\n" +
              "Optimizacion: " + self.optimizacion + "\n" +
              "Cantidad de variables de decision: " + self.cant_v_decision + "\n" +
              "Cantidad de restricciones: " + self.cant_restricciones + "\n" +
              "Funcion objetivo: " + str(self.funcionObjetivo) + "\n" +
              "Restricciones: " + str(self.restricciones))
        writeFile(informacionProblemaText)

    """
    Descripcion: Método que genera el resultado solucion correspondiente a la tabla actual 
    Entradas: El problema
    Salidas: Imprime en el archivo solución la solucion para esa tabla 
    """
    def __solucionSimplexMax__(self):

        solucion = []
        solucion.append(float(self.tablaActual[0][-1]))
        auxiliar = []
        resultados = []
        for i in range(1, len(self.tablaActual)):
            resultados.append(self.tablaActual[i][-1])
        for i in range(len(self.funcionObjetivo)-2):
            auxiliar.append(float(0))
        for j in range(len(auxiliar)+1):
            for k in self.ordenFilas:
                if j == k:
                    auxiliar[j-1] = resultados[self.ordenFilas.index(k)-1]
        solucion.append(auxiliar)
        solucion[0] = float((solucion[0]).__format__('0.4f'))
        for j in range(len(solucion[1])):
            solucion[1][j] = float((solucion[1][j]).__format__('0.4f'))
        writeFile("\nSolucion actual: " + str(solucion))
        return solucion

    """
    Descripcion: Busca si existe un indice por debajo de cero o negativo para seguir operando Simplex
    Entradas: El problema
    Salidas: La bandera de si se debe seguir operando, y el resultado de la busqueda
    """
    def __indiceColumnaMenor__(self):
        negativos = []

        for i in range(len(self.tablaActual[0])-1):
            if float(self.tablaActual[0][i]) < 0:
                negativos.append(self.tablaActual[0][i])
        if len(negativos) < 1:
            return False , 0
        elif float(self.tablaActual[0][-1]) < 0 and len(negativos) < 1 :
            return True , 0
        else:
            resultado = max(negativos)
            writeFile("Minimo: " + str(float(self.tablaActual[0].index(resultado))) + " Valor: " + str(float(resultado)))
            return True , int(self.tablaActual[0].index(resultado))

    """
    Descripcion: Funcion que determina el pivote a seleccionar
    Entradas: El problema, el indice de la columna
    Salidas: El pivote
    """
    def __determinacionPivote__(self, columna):
        tabla = self.tablaActual
        divisiones = []
        for i in range(1,len(tabla)):
            if tabla[i][columna] > float(0):
                casilla = tabla[i][-1]
                pivote = tabla[i][columna]
                division = float(casilla) / float(pivote)
                division = float(division)
                pair = [division, [i, columna]]
                divisiones.append(pair)

        for w in range(len(divisiones)):
            for e in range(len(divisiones)):
                if divisiones[w][0] == divisiones[e][0] and w != e:
                    writeFile("En este caso se presenta de solución degenerada")
        if len(divisiones) == 0:
            return divisiones
        pivote = divisiones[0]
        for i in range(len(divisiones)):
            if divisiones[i][0] < pivote[0]:
                pivote = divisiones[i]
        return pivote

    """
    Descripcion: Metodo que genera la fila pivote a base de la casilla pivote
    Entradas: El problema y la tupla que indica los datos del pivote
    Salidas: La nueva fila operada con el pivote
    """
    def __nuevaFila__(self, pivote):
        tabla = self.tablaActual
        fila = pivote[1][0]
        columna = pivote[1][1]
        nuevaFila = []
        for i in range(len(tabla[fila])):
            nuevaFila.append(float(
                float(tabla[int(fila)][i]) / float(tabla[int(fila)][columna])))
        return nuevaFila

    """
    Descripcion: Metodo que calcula la nueva fila en el caso de que se esté ejecutando el método de las dos fases
    Entradas: Arreglo con los datos del pivote y el objeto problema 
    Salidas: La nueva fila calculada
    """
    def __nuevaFilaDosFases__(self, pivote):
        tabla = self.tablaActual
        fila = pivote[1][0]
        columna = pivote[1][1]
        nuevaFila = []
        for i in range(len(tabla[fila])):
            nuevaFila.append(float(
                float(tabla[int(fila)][i]) / float(tabla[int(fila)][columna])))
        return nuevaFila


    """
    Descripcion: Funcion que realiza la operacion de Gauss-Jordan
    Entradas: El problema, el pivote y una fila de ceros
    Salidas: La tabla actualizada
    """
    def __tablaNueva__(self, nuevaFila, pivote):
        tabla = []
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                fila = []
                for j in range(len(self.tablaActual[0])):
                    fila.append(float(0))
                tabla.append(fila)
            else:
                tabla.append(nuevaFila)
        self.tablaSiguiente = tabla
        return tabla


    """
    Descripcion: Funcion que realiza la operacion de Gauss-Jordan
    Entradas: El problema, el pivote y una fila de ceros
    Salidas: La tabla actualizada
    """
    def __tablaNuevaDosFases__(self, nuevaFila, pivote):
        tabla = []
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                fila = []
                for j in range(len(self.funcionObjetivo)):
                    fila.append(float(0))
                tabla.append(fila)
            else:
                tabla.append(nuevaFila)
        self.tablaSiguiente = tabla
        return tabla
    
    """
    Descripcion: Funcion que se encarga de calcular la tabla siguiente con base a la tabla de ceros o tabla nueva y la actual
    Entradas: El problema, la fila de ceros o la fila nueva y el pivote
    Salidas: La tabla nueva del siguiente paso
    """
    def __simplexMinCalculo__(self, pivote, nuevaFila):
        tablaActual = self.tablaActual
        tablaNueva = self.tablaSiguiente
        tablaActualText = "\n--------------------------------Tabla Actual---------------------------------"
        writeFile(tablaActualText)
        self.__printTabla__(1)
        writeFile("\nPivote: " + str(pivote))
        tablaCerosText = "\n---------------------------Tabla nueva - ceros ------------------------------"
        writeFile(tablaCerosText)
        self.__printTabla__(2)
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                nuevaFila = []
                for j in range(len(self.funcionObjetivo)):
                    casilla = float(tablaActual[i][j]) + (float(tablaActual[i][pivote[1][1]])*-1 * float(tablaNueva[pivote[1][0]][j]))
                    if casilla == float(-0):
                        casilla = float(0)
                    nuevaFila.append(float(casilla))
                tablaNueva[i] = nuevaFila
        tablaNuevaText = "\n-------------------------Tabla nueva - calculada ----------------------------"
        writeFile(tablaNuevaText)
        self.__printTabla__(2)
        self.tablaActual = tablaNueva
        self.tablaSiguiente = []
        self.__actualizarOrdenFilas__(pivote)
        return tablaNueva

    """
    Descripcion: Funcion que se encarga de calcular la tabla siguiente con base a la tabla de ceros o tabla nueva y la actual
    Entradas: El problema, la fila de ceros o la fila nueva y el pivote
    Salidas: La tabla nueva del siguiente paso
    """
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
        for i in range(int(self.cant_restricciones) + 1):
            if i != pivote[1][0]:
                nuevaFila = []
                for j in range(len(self.funcionObjetivo)-1):
                    casilla = float(tablaActual[i][j]) + (float(tablaActual[i][pivote[1][1]])*-1 * float(tablaNueva[pivote[1][0]][j]))
                    if casilla == float(-0):
                        casilla = float(0)
                    nuevaFila.append(float(casilla))
                tablaNueva[i] = nuevaFila
        tablaNuevaText = "\n-------------------------Tabla nueva - calculada ----------------------------"
        writeFile(tablaNuevaText)
        self.__printTabla__(2)
        self.tablaActual = tablaNueva
        self.tablaSiguiente = []
        self.__actualizarOrdenFilas__(pivote)
        return tablaNueva


    """
    Descripcion: Funcion que registra la cantidad de variables no basicas que tiene una tabla
    Entradas: El problema
    Salidas: Ninguna
    """
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

    """
    Descripcion: Funcion que se encarga de invertir o cambiar el signo de las restricciones para preparar fase uno
    Entradas: El problema
    Salidas: Ninguna
    """
    def __cambiarSignoRestricciones__(self):
        for i in range(len(self.restricciones)):
            for j in range(len(self.restricciones[i])):
                if self.restricciones[i][j] == '>=':
                    self.restricciones[i][j] = '<='
                    self.restricciones[i][-1] = float(self.restricciones[i][-1]) * -1
    """
    Descripcion: Funcion que cambia el signo de la funcion objetivo para preparar fase uno
    Entradas: El problema
    Salidas: Ninguna
    """
    def __cambiarSignoFuncionObjetivo__(self):
        for i in range(len(self.funcionObjetivo)):
            if self.funcionObjetivo[i] == '>=':
                self.funcionObjetivo[i] = '<='
                self.funcionObjetivo[-1] = float(self.funcionObjetivo[-1]) * -1


"""
Descripcion: Funcion que llama a metodoSimplex y se encarga de verificar a quien llamar especificamente en funcion de las entradas del usuario
Entradas: El nombre del archivo 
Salidas: Ninguna
"""
def ejecutarSimplex(nombre_archivo):
    removeFile()
    datos = separarDatos(nombre_archivo)
    problema_simplex = problema(datos)
    problema_simplex.cantidadVariablesRestricciones()
    if problema_simplex.metodo == '1':  # Es simplex
        if (problema_simplex.optimizacion == "max"):
            problema_simplex.__agregarVariablesHolguraSimplexMax__()
            problema_simplex.__makeOrdenFilas__()
            problema_simplex.__tabularProblema__()
            problema_simplex.__print__()
            metodoSimplex(problema_simplex)
        elif (problema_simplex.optimizacion == "min"):
            print("No se puede resolver minimizacion con el metodo simplex")
    elif problema_simplex.metodo == '2': # Es dos fases
        if (problema_simplex.optimizacion == "max"):
            problema_simplex.__agregarVariablesHolguraSimplexMax__()
            problema_simplex.__makeOrdenFilas__()
            problema_simplex.__tabularProblema__()
            problema_simplex.__print__()
            metodoDosFases(problema_simplex, 0)
        elif (problema_simplex.optimizacion == "min"):
            problema_simplex.__agregarVariablesHolguraSimplexMin__()
            problema_simplex.__makeOrdenFilas__()
            problema_simplex.__tabularProblema__()
            problema_simplex.__print__()
            metodoDosFases(problema_simplex, 0)

    else:
        print("No existe el metodo ingresado")

"""
Descripcion: Funcion que se encarga de llamar a los metodos de simplex y de dos fases
Entradas: Ninguna
Salidas: Ninguna
"""      
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
        print("El sistema se ejecutara con el archivo de texto: " + sys.argv[1])
        print("El resultado se guardara en el archivo: resultado.txt")
        nombre_archivo = sys.argv[1]
        ejecutarSimplex(nombre_archivo)
    exit(0)




#Se llama a la funcion main
main()