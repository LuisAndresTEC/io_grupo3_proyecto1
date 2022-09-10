#Estas primeras funciones se van dedicar a la lestura y escritura en los txt
import os
#este será un lector de archivos txt
def read_file():
    reader = open(operacion.txt, 'r')
    file = reader.read()
    reader.close()
    return file

#este será un escritor de archivos txt
def write_file(text):
    reader = open(operacion.txt, 'r')
    reader.write(text)
    reader.close()


def main():
    #aqui se va a leer el archivo
    text = read_file()
    if len(text) > 0: #"El archivo esta vacio"
        #aqui se va a escribir el archivo
        print("este es el texto: "+ text)
        response = "Ya se logra escribir un texto"
        write_file(response)
