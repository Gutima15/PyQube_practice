#Fecha de creacion: 12/10/2019
#Última modificación: 28/10/2019
#Versión: 3.7.2

# Importación de Librerías

from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import shutil
from os import remove
import tkinter.messagebox
import random

# Definir el límite de letras o porcentaje

globalPuntajeA=0
globalPuntajeB=0
globalPalabra=""
puntuacionA=0
puntuacionB=0
proceso=0
contadorLetras=0
total=0
f1=open("letras.txt","r")
for i in f1:
    n=int(i[2])
    contadorLetras+=n   
total=round((contadorLetras*70)/100)
limiteLetras=contadorLetras-total

# Definición de Funciones

def crearBitacora():
    global varTurno, globalA, globalB, varJugador, globalPuntajeA, globalPuntajeB, globalPalabra
    archivoNuevo=open("bitacora.txt","a")
    turno=varTurno.get()
    nombreA=""
    nombreB=""
    puntuacionA=""
    puntuacionB=""
    palabraA=""
    palabraB=""
    if str(varJugador.get())==str(globalA):
        nombreA=str(globalA)
        puntuacionA=str(globalPuntajeA)
        palabraA=str(globalPalabra)
        archivoNuevo.write("Turno: "+turno+" - Jugador: "+nombreA+" - Puntuación: "+puntuacionA+" - Palabra: "+palabraA+"\n")
    elif str(varJugador.get())==str(globalB):
        nombreB=str(globalB)
        puntuacionB=str(globalPuntajeB)
        palabraB=str(globalPalabra)
        archivoNuevo.write("Turno: "+turno+" - Jugador: "+nombreB+" - Puntuación: "+puntuacionB+" - Palabra: "+palabraB+"\n")
    else:
        print("Error")
    globalPuntajeA=0
    globalPuntajeB=0
    globalPalabra=""
    archivoNuevo.close()
    
def definirSetentaPorciento():
    """
    Entrada: Archivo de texto.
    Funcionalidad: Lee el archivo, suma la cantidad le letras que hay y saca cuanto es el 70% para saber cuando cerrar el programa.
    Salida: Cierra el programa cuando se excede del 70% de las letras del archivo.
    """
    contador=0
    f2=open("letras2.txt","r")
    for i in f2:
        n=int(i[2])
        contador+=n
    if contador<=limiteLetras:
        finalizarJuego(2)
    return 0

def duplicarArchivo():
    """
    Entrada: El archivo con las letras pra el juego.
    Funcionalidad: Duplica el archivo para asi poder modificarlo cada vez que se utiliza una letra.
    Salida: Crea el archivo duplicado.
    """
    try:
        shutil.copy("letras.txt", "letras2.txt")
        print("Archivo duplicado con éxito")
    except:
        return "Error"

def leerArchivoLetras2():
    """
    Entradas: Ninguna.
    Funcinalidad: Lee el segundo archivo de letras y lo convierte en una lista.
    Salidas: Devuelve una lista de listas.
    """
    lista=[]
    listaNueva=[]
    archivo=open("letras2.txt")
    for i in archivo:
        lista.append(i[:5].split(";"))
    for j in lista:
        listaNueva.append(j[0].split(","))
    return listaNueva

def eliminarArchivo():
    """
    Entrada: Archivo nuevo
    Funcionalidad: Elimina el archivo que se habia duplicado
    Salida: Archivo eliminado
    """
    try:
        remove("letras2.txt")
        print("El archivo duplicado se ha eliminado con éxito.")
    except:
        print("Error elimianndo archivo duplicado")

def seleccionarLetra():
    """
    Entrada: Ninguna.
    Funcionalidad: Esta función en resumen, selecciona una letra al azar del archivo duplicado y
    seguidamente lo elimina del mismo.
    Salida: Retorna una letra aleatoria del archivo con letras duplicado.
    """
    try:
        x=0
        letra2=""
        lista=leerArchivoLetras2()
        maximo=len(lista)-1
        numRandom=random.randint(0,maximo)
        for i in range(len(lista)):
            if i==numRandom:
                letra=lista[i]
                letra=letra[0]
        for i in lista:
            if i[0]==letra:
                if int(i[1])>0:
                    letra2=letra
                    archivo = open("letras2.txt", "w")
                    x = int(i[1]) - 1
                    x=str(x)
                    i[1] = x
                    for y in lista:
                        archivo.write(",".join(y) + ";\n")
                    return letra2
                else:
                    seleccionarLetra()
        return 0
    except:
        print("YA NO HAY MÁS LETRAS")

def excepcionSeleccionarLetra():
    """
    Entrada: Ninguna.
    Funcionalidad: Valida con try except para evitar cualquier error.
    Salida: Retorna la función seleccionarLetra si no hay ningún error.
    """
    try:
        return seleccionarLetra()
    except:
        return "ERROR"

def moverMatriz(col, fil):
    """
    Entrada: La pocicion por columna y por fila del boton.
    Funcionalidad: Valida que los botones esten vacios para poder escribir la palabra deseada.
    Salida: Si el boton esta vacio se rellena con la letra seleccionada y si no lo esta tira un error. 
    """
    global botonMatriz, palabra, varJugador, varJugadorA, varJugadorB, colorBoton
    if botonMatriz[col][fil]['text'] == "" or botonMatriz[col][fil]['text'] == "red":
        colorBoton=botonMatriz[col][fil]['text']
        botonMatriz[col][fil].configure(fg="black")
        botonMatriz[col][fil]['text'] = setLetra()
        eliminarDeCombobox()
        definirSetentaPorciento()
        guardarPalabra(botonMatriz[col][fil]['text'])
        
    else:
        tkinter.messagebox.showinfo("Advertencia", "Ya hay una letra aquí")

def guardarPalabra(letra):
    """
    Entrada: La letra puesta en la matriz de botones.
    Funcionalidad: Fora la palabra para ser guardada en la bitacora.
    Salida: La palabra que va formando y el puntaje obtenido.
    """
    global palabra, varJugador, colorBoton, globalA, globalB, globalPuntajeA, globalPuntajeB, globalPalabra
    puntaje=0
    f=open("letras2.txt","r")
    if varJugador.get()==globalA:
        palabra+=letra
        jugadorA=palabra
        for i in f:
            if colorBoton == "red" and i[0]==letra:
                puntaje=((puntaje+int(i[4])*2))
                globalPuntajeA+=puntaje
                globalPalabra=jugadorA
                print("Multiplicador")
            elif i[0]==letra:
                puntaje=puntaje+int(i[4])
                globalPuntajeA+=puntaje
                globalPalabra=jugadorA
        puntajeJugador1(puntaje)
        return globalA+" "+jugadorA+" Puntaje: "+str(puntaje)
    elif varJugador.get()==globalB:
        palabra+=letra
        jugadorB=palabra
        for i in f:
            if colorBoton == "red" and i[0]==letra:
                puntaje=((puntaje+int(i[4])*2))
                globalPuntajeB+=puntaje
                globalPalabra=jugadorB
                print("Multiplicador")
            elif i[0]==letra:
                puntaje=puntaje+int(i[4])
                globalPuntajeB+=puntaje
                globalPalabra=jugadorB
        puntajeJugador2(puntaje)
        return globalB+" "+jugadorB+" Puntaje: "+str(puntaje)
def puntajeJugador1(num):
    """
    Entrada: El valor de la letra colocada en el tablero por el jugador 1.
    Funcionalidad: Guarda el valor y va sumando los nuevos valores que entran.
    Salida: El total de puntos que obtuvo el jugador 1 
    """
    global varPuntajeA, puntuacionA
    puntuacionA+=num
    varPuntajeA.set(puntuacionA)
    return puntuacionA

def puntajeJugador2(num):
    """
    Entrada: El valor de la letra colocada en el tablero por el jugador 2.
    Funcionalidad: Guarda el valor y va sumando los nuevos valores que entran.
    Salida: El total de puntos que obtuvo el jugador 2. 
    """
    global varPuntajeB, puntuacionB
    puntuacionB+=num
    varPuntajeB.set(puntuacionB)
    return puntuacionB

def validarFinDeJuegoPorTurno():
    """
    Entrada: Ninguna.
    Funcionalidad: Valida el turno actual, si llega a turno 20 llama la función para finalizar
    el programa.
    Salida: Retorna la función finalizarJuego turno es 20, sino retorna 0.
    """
    global varTurno
    if int(varTurno.get())==20:
        return finalizarJuego(3)
    else:
        return 0

def finalizarJuego(num):
    """
    Entrada: Un número entero positivo como opción.
    Funcionalidad: Verifica con el número que recibe por parámetro, la razón por la cual el juego
    se está finalizando y devuelve un mensaje del ganador seguido de cerrar el programa.
    Salida: Retorna quién fue el ganador y la razón por la que terminó el juego.
    """
    global varJugador, globalA, globalB, varPuntajeA, varPuntajeB
    crearBitacora()
    variable=0
    varPuntajeA=int(varPuntajeA.get())
    varPuntajeB=int(varPuntajeB.get())
    if num==0:
        if varJugador.get()==globalA:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR RENDICIÓN", "Ganador: "+globalB)
            variable=1
        else:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR RENDICIÓN", "Ganador: "+globalA)
            variable=1
    elif num==1:
        if varPuntajeA>varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TIEMPO", "Ganador: "+globalA)
            variable=1
        elif varPuntajeB>varPuntajeA:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TIEMPO", "Ganador: "+globalB)
            variable=1
        elif varPuntajeA==varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TIEMPO", "EMPATE")
            variable=1
    elif num==2:
        if varPuntajeA>varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR FALTA DE FICHAS", "Ganador: "+globalA)
            variable=1
        elif varPuntajeB>varPuntajeA:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR FALTA DE FICHAS", "Ganador: "+globalB)
            variable=1
        elif varPuntajeA==varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR FALTA DE FICHAS", "EMPATE")
            variable=1
    elif num==3:
        if varPuntajeA>varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TURNO 20", "Ganador: "+globalA)
            variable=1
        elif varPuntajeB>varPuntajeA:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TURNO 20", "Ganador: "+globalB)
            variable=1
        elif varPuntajeA==varPuntajeB:
            tkinter.messagebox.showinfo("FIN DE JUEGO POR TURNO 20", "EMPATE")
            variable=1
    if variable==1:
        return cerrarPrograma()
    else:
        return 0

def cerrarPrograma():
    """
    Entrada: Ninguna.
    Funcionalidad: Llama función eliminarArchivo() y cierra el programa.
    Salida: Retorna error si lo hay.
    """
    global principal
    try:
        eliminarArchivo()
        principal.destroy()
    except:
        return "No se pudo eliminar el archivo duplicado"

def imprimir():
    """
    Entrada: Ninguna.
    Funcionalidad: Recorre la matriz y la imprime en consola.
    Salida: Retorna en consola la matriz actual.
    """
    global botonMatriz
    for x in range(15):
        for y in range(15):
            print("[" + str(botonMatriz[x][y]['text']), end=']')
        print("")

def habilitarBotones():
    """
    Entrada: Ninguna.
    Funcionalidad: Recorre la matriz y habilita todos los botones.
    Salida: Ninguna.
    """
    for y in range(15):
        for x in range(15):
            botonMatriz[y][x].config(state=NORMAL)

def leerArchivoLetras():
    """
    Entrada: Ninguna.
    Funcionalidad: Lee el archivo de las letras.
    Salida: Una lista con las letras, su cantidad y el puntaje de cada una.
    """
    lista = []
    listaNueva = []
    archivo = open("letras.txt")
    for i in archivo:
        lista.append(i[:5].split(";"))
    for j in lista:
        listaNueva.append(j[0].split(","))
    return listaNueva

def segundos(contador=29):
    """
    Entrada: Variable del contador ya definida en la misma función.
    Funcionalidad: Cronómetro que resta de uno en uno un contador y este se muestra en una
    etiqueta de la ventana de juego cada vez que es actualizado.
    Salida: Ninguna.
    """
    global proceso, lbl_Segundos
    lbl_Segundos['text'] = contador
    proceso=lbl_Segundos.after(1000, segundos, (contador-1))
    if contador==0:
        lbl_Segundos.after_cancel(proceso)
        segundos()
        finalizarTurno()
        
def cambioTurno():
    """
    Entrada: Ninguna.
    Funcionalidad: Cambia el turno del juego, específicamente cambia la etiqueta con los turnos
    cada vez que los dos jugadores realizan una acción.
    Salida: Ninguna.
    """
    global varTurno, contador1, contador2
    contador1+=1
    if contador1%2==0:
        contador2 += 1
        varTurno.set(contador2)

def cambioJugador():
    """
    Entrada: Ninguna.
    Funcionalidad: Cambia el nombre del jugador cada vez que finaliza el turno.
    Salida: Ninguna.
    """
    global varJugador, comboboxA, comboboxB, globalA, globalB

    if varJugador.get() == "":
        varJugador.set(globalA)

    elif varJugador.get() == globalA:
        varJugador.set(globalB)

    elif varJugador.get() == globalB:
        varJugador.set(globalA)

def validarNombres(jugadorA, jugadorB):
    """
    Entrada: Recibe dos palabras.
    Funcionalidad: Verifica palabras ingresadas, si su cantidad de caracteres es mayor a 5 corta
    la palabra y si son menos de 5, le agrega "_" por cada caracter faltante.
    Salida: Retorna la función ventanaJuego junto con las palabras(nombre de jugadores) ya validados.
    """
    global principal, ventanaIni
    if len(jugadorA) >= 5:
        nombreAValidado=(jugadorA[:5])
    elif len(jugadorA) <= 5:
        nombreAValidado=(jugadorA+ "_"*(5 - len(jugadorA)))
    if len(jugadorB) >= 5:
        nombreBValidado=(jugadorB[:5])
    elif len(jugadorB) <= 5:
        nombreBValidado=(jugadorB+ "_"*(5 - len(jugadorB)))
    return ventanaJuego(nombreAValidado, nombreBValidado)
    
def llenarComboboxInicio():
    """
    Entrada: Ninguna.
    Funcionalidad: Verifica si los combobox estan llenos o vacios.
    Salida: Si estan vacios llama a las funciones que los llenan.
    """
    global contador1, comboboxA
    if contador1 == "1":
        llenarComboboxA()
        llenarComboboxB()
    else:
        return 0

def llenarComboboxA():
    """
    Entrada: Ninguna.
    Funcionalidad: Llena por primera vez el combobox del jugador A con 7 letras aleatorias.
    Salida: Retorna una lista.
    """
    global comboboxA
    listaNueva = []
    contador = 7
    while contador > 0:
        letra = str(excepcionSeleccionarLetra())
        if letra != "0":
            listaNueva.append(letra)
            contador -= 1
    comboboxA['values'] = listaNueva
    return listaNueva

def llenarComboboxA2():
    """
    Entradas: Ninguna.
    Funcionalidad: Llena el combobox A según las fichas que le falten con letras aleatorias.
    Salidas: Retorna 0.
    """
    global comboboxA, varJugadorA
    contador = 0
    listaNueva = []
    for i in comboboxA['values']:
        contador += 1
    if contador < 7:
        for i in comboboxA['values']:
            listaNueva.append(i)
        while contador < 7:
            letra = str(excepcionSeleccionarLetra())
            if letra != "0":
                listaNueva.append(letra)
                contador += 1
    comboboxA['values'] = listaNueva
    return 0

def llenarComboboxB():
    """
    Entrada: Ninguna.
    Funcionalidad: Llena por primera vez el combobox del jugador B con 7 letras aleatorias.
    Salida: Retorna una lista.
    """
    global comboboxB
    listaNueva = []
    contador = 7
    while contador > 0:
        letra = str(excepcionSeleccionarLetra())
        if letra != "0":
            listaNueva.append(letra)
            contador -= 1
    comboboxB['values'] = listaNueva
    return listaNueva

def llenarComboboxB2():
    """
    Entradas: Ninguna.
    Funcionalidad: Llena el combobox B según las fichas que le falten con letras aleatorias.
    Salidas: Retorna 0.
    """
    global comboboxB, varJugadorB
    contador = 0
    listaNueva = []
    for i in comboboxB['values']:
        contador += 1
    if contador < 7:
        for i in comboboxB['values']:
            listaNueva.append(i)
        while contador < 7:
            letra=str(excepcionSeleccionarLetra())
            if letra !="0":
                listaNueva.append(letra)
                contador += 1
    comboboxB['values'] = listaNueva
    return 0

def llenarCombobox():
    """
    Entradas: Ninguna.
    Funcionalidad: Verifica y valida si faltan fichas a los combobox de los jugadores y los llena
    según el turno y las letras faltantes, con un máximo de 7 fichas/letras.
    Salidas: Retorna 0.
    """
    global comboboxA, comboboxB, varJugador, globalA, globalB
    llenarComboboxInicio()
    contador = 0
    try:
        if varJugador.get() == globalA:
            for i in comboboxA['values']:
                contador += 1
            if contador < 7:
                llenarComboboxA2()
        elif varJugador.get() == globalB:
            for i in comboboxB['values']:
                contador += 1
            if contador < 7:
                llenarComboboxB2()
    except:
        return 0

def eliminarDeComboboxA():
    """
    Entradas: Ninguna.
    Funcionalidad: Elimina letra usada del combobox A.
    Salidas: Retorna 0.
    """
    global varJugadorA, comboboxA
    try:
        listaNueva = []
        for i in comboboxA['values']:
            listaNueva.append(i)
        listaNueva.remove(varJugadorA.get())
        comboboxA['values'] = listaNueva
        varJugadorA.set("")
    except:
        return 0

def eliminarDeComboboxB():
    """
    Entradas: Ninguna.
    Funcionalidad: Elimina letra usada del combobox B.
    Salidas: Retorna 0.
    """
    global varJugadorB, comboboxB
    try:
        listaNueva = []
        for i in comboboxB['values']:
            listaNueva.append(i)
        listaNueva.remove(varJugadorB.get())
        comboboxB['values'] = listaNueva
        varJugadorB.set("")
    except:
        return 0

def eliminarDeCombobox():
    """
    Entradas: Ninguna.
    Funcionalidad: Función que llama ambas funciones de eliminar.
    Salidas: Ninguna.
    """
    eliminarDeComboboxA()
    eliminarDeComboboxB()

def setLetra():
    """
    Entradas: Ninguna.
    Funcionalidad: Agarra letra del combobox y la coloca en la matriz de botones.
    Salidas: Retorna letra utilizada en el botón.
    """
    global varJugador, varJugadorA, varJugadorB, globalA, globalB
    palabra = ""
    if varJugador.get() == globalA:
        palabra = varJugadorA.get()
    elif varJugador.get() == globalB:
        palabra = varJugadorB.get()
    return palabra

def cambioCombobox():
    """
    Entradas: Ninguna.
    Funcionalidad: Habilita o deshabilita el combobox de los jugadores según el turno de cada uno.
    Salidas: Ninguna.
    """
    global comboboxA, comboboxB, varJugador, globalA, globalB
    if varJugador.get()=="":
        comboboxA.configure(state='normal')
        comboboxB.configure(state='disabled')
    elif varJugador.get()==globalA:
        comboboxB.configure(state='disabled')
        comboboxA.configure(state='normal')
    elif varJugador.get()==globalB:
        comboboxB.configure(state='normal')
        comboboxA.configure(state='disabled')

def iniciarTurno():
    """
    Entradas: Ninguna.
    Funcionalidad: Función que llama otras funciones necesarias para iniciar el programa.
    Salidas: Ninguna.
    """
    cambioTurno()
    cambioJugador()
    segundos()

def finalizarTurno():
    """
    Entradas: Ninguna.
    Funcionalidad: Función que llama otras funciones necesarias para realizar el cambio de
    turno.
    Salidas: Retorna 0 si hay algún error. 
    """
    global palabra, puntaje1, proceso, lbl_Segundos
    try:
        palabra=""
        puntaje1=0
        crearBitacora()
        cambioTurno()
        cambioJugador()
        llenarCombobox()
        definirSetentaPorciento()
        lbl_Segundos.after_cancel(proceso)
        validarFinDeJuegoPorTurno()
        cambioCombobox()
        segundos()
    except:
        return 0

def puntajeLetras():
    """
    Entradas: Ninguna.
    Funcionalidad: Es la ventana donde se muestran las letras del archivo de texto y lo
    que valen.
    Salidas: Ninguna. 
    """
    letras = Tk()
    letras.title("Pantalla Juego")
    letras.resizable(FALSE, FALSE)
    letras.geometry("150x600")
    lista1=[]
    f = open("letras.txt", "r")
    for i in f:
        lista1.append("         "+i[0]+" = "+i[4]+"\n")
    lbl_letras = Label(letras, text=lista1)
    lbl_letras.config(font=("Arial Black", "10"))
    lbl_letras.place(x=-24, y=5)
    letras.mainloop()

def segundosTiempo(segund=59):
    """
    Entradas: Entero positivo.
    Funcionalidad: Función que modifica los segundos y minutos del contador principal del juego.
    Salidas: Retorna finalizarJuego() si los minutos llegan a 0.
    """
    global proceso2, lbl_SegundosTiempo, varMinutos
    num=int(varMinutos.get())
    lbl_SegundosTiempo['text'] = segund
    proceso2=lbl_SegundosTiempo.after(1000, segundosTiempo, (segund-1))
    if num>=0:
        if segund==0:
            num-=1
            lbl_SegundosTiempo.after_cancel(proceso2)
            varMinutos.set(str(num))
            segundosTiempo()
    else:
        varMinutos.set(0)
        lbl_SegundosTiempo.after_cancel(proceso2)
        return finalizarJuego(1)
        
def ventanaIniAJuego(a, b):
    """
    Entradas: Dos palabras/nombres de jugadores.
    Funcionalidad: Valida que esten los entries llenos y que no sean nombres repetidos, luego
    llama la siguiente función de validar nombres.
    Salidas: Retorna la función validarNombres() si no hay ningún error.
    """
    global ventanaIni
    if a!="" and b!="":
        if a!=b:
            ventanaIni.destroy()
            return validarNombres(a, b)
        else:
            tkinter.messagebox.showerror("Advertencia", "Debe colocar nombres distintos")
    else:
        tkinter.messagebox.showerror("Advertencia", "Debe llenar los espacios en blanco")

def ventanaInicio():
    """
    Entradas: Ninguna.
    Funcionalidad: Ventana principal donde se colocan los nombres de los jugadores.
    Salidas: Ninguna.
    """
    global ventanaIni, btn_jugar, lbl_validar, entryJugadorA, entryJugadorB
    ventanaIni = Tk()
    ventanaIni.title("Ventana Principal")
    ventanaIni.resizable(FALSE, FALSE)
    ventanaIni.geometry("750x422")
    load = Image.open('imagenIni.png')
    render = ImageTk.PhotoImage(load)
    imagen=Label(ventanaIni, image=render)
    imagen.image = render
    imagen.place(x=-1, y=-1)
    frameColor1 = Frame(ventanaIni, height=124, width=224, bg="orchid1")
    frameColor1.place(x=48, y=135)
    frameColor11 = Frame(ventanaIni, height=120, width=220, bg="turquoise")
    frameColor11.place(x=50, y=137)
    lbl_NombreA= Label(ventanaIni, text="Jugador 1", font="system 30 bold", bg="turquoise")
    lbl_NombreA.place(x=60, y=150)
    entryJugadorA=Entry(ventanaIni, justify="center", font="system 16 bold")
    entryJugadorA.place(x=75, y=220)
    frameColor2 = Frame(ventanaIni, height=124, width=224, bg="turquoise")
    frameColor2.place(x=458, y=135)
    frameColor22 = Frame(ventanaIni, height=120, width=220, bg="orchid1")
    frameColor22.place(x=460, y=137)
    lbl_NombreB= Label(ventanaIni, text="Jugador 2", font="system 30 bold", bg="orchid1")
    lbl_NombreB.place(x=470, y=150)
    entryJugadorB=Entry(ventanaIni, justify="center", font="system 16 bold")
    entryJugadorB.place(x=487, y=220)
    btn_jugar = Button(ventanaIni, height=61, width=146, text="Jugar", font="system 12 bold", relief=FLAT, command=lambda: ventanaIniAJuego(entryJugadorA.get(),entryJugadorB.get()))
    btn_jugar.place(x=286, y=320)
    
    img = PhotoImage(file="botonPic.png") 
    btn_jugar.config(image=img)

    ventanaIni.mainloop()
    

def ventanaJuego(nombreA, nombreB):
    """
    Entradas: Recibe los nombres de los jugadores ya validados.
    Funcionalidad: Ventana de juego donde se localiza la matriz de botones.
    Salidas: Ninguna.
    """
    global varMinutos, lbl_SegundosTiempo, globalA, globalB, varJugadorA, varJugadorB, comboboxA, comboboxB, botonMatriz, sec, lbl_Segundos, palabra, varMatriz, principal, varPuntajeA, varPuntajeB, lbl_Jugador, varJugador, contador1, contador2, varTurno, varLetra
    palabra = ""
    globalA=nombreA
    globalB=nombreB
    contador1 = -1
    contador2 = 0
    principal = Tk()
    botonMatriz = list()
    principal.title("S K U L L   F E I T Z")
    principal.resizable(FALSE, FALSE)
    principal.geometry("1400x900")
    load = Image.open('imagen.png')
    render = ImageTk.PhotoImage(load)
    imagen=Label(principal, image=render)
    imagen.image = render
    imagen.place(x=-1, y=-1)
    # principal.attributes('-fullscreen', True)
    duplicarArchivo()
    frameA=Frame(principal, height=38, width=62, bg="orchid1")
    frameA.place(x=184, y=16)
    frameB=Frame(principal, height=38, width=62, bg="orchid1")
    frameB.place(x=400, y=16)
    frameW=Frame(principal, height=78, width=286, bg="white")
    frameW.place(x=720, y=496)
    lbl_Nombre = Label(principal, text="Skull Feitz", font="system 40 bold", bg="orchid1")
    lbl_Nombre.place(x=724, y=500)
    lbl_Segundos = Label(principal, font="system 20 bold", text="0:00", bg="orchid1", fg="black")
    lbl_Segundos.place(x=35, y=16)
    lbl_T = Label(principal, text="Turno:", font="system 20 bold", bg="orchid1")
    lbl_T.place(x=145, y=16)
    varTurno = StringVar()
    varTurno.set(contador2)
    lbl_Turno = Label(principal, textvariable=varTurno, font="system 20 bold", bg="orchid1")
    lbl_Turno.place(x=245, y=16)
    lbl_J = Label(principal, text="Jugador:", font="system 20 bold", bg="orchid1")
    lbl_J.place(x=315, y=16)
    varJugador = StringVar()
    lbl_Jugador = Label(principal, textvariable=varJugador, font="system 20 bold", bg="orchid1")
    lbl_Jugador.place(x=445, y=16)
    iniciarTurno()
    frameColor3 = Frame(principal, height=274, width=300, bg="orchid1")
    frameColor3.place(x=1055, y=20)
    frameColor4 = Frame(principal, height=254, width=270, bg="white")
    frameColor4.place(x=1070, y=30)
    lbl_Puntaje1 = Label(principal, text=nombreA, font="system 20 bold", bg="orchid1")
    lbl_Puntaje1.place(x=1160, y=40)
    varPuntajeA=StringVar()
    varPuntajeA.set(0)
    lbl_PuntajeA = Label(principal, textvariable=varPuntajeA, font="system 20 bold", bg="white")
    lbl_PuntajeA.place(x=1190, y=110)
    lbl_Puntaje2 = Label(principal, text=nombreB, font="system 20 bold", bg="orchid1")
    lbl_Puntaje2.place(x=1160, y=180)
    varPuntajeB=StringVar()
    varPuntajeB.set(0)
    lbl_PuntajeB = Label(principal, textvariable=varPuntajeB, font="system 20 bold", bg="white")
    lbl_PuntajeB.place(x=1190, y=240)
    frameColor1 = Frame(principal, height=638, width=608, bg="orchid1")
    frameColor1.place(x=37.4, y=72.5)
    frameColor5 = Frame(principal, height=160, width=300, bg="orchid1")
    frameColor5.place(x=1055, y=310)
    frameColor6 = Frame(principal, height=140, width=270, bg="white")
    frameColor6.place(x=1070, y=320)
    varMinutos=StringVar()
    varMinutos.set(14)
    lbl_Tiempo = Label(principal, font="system 40 bold", textvariable=varMinutos, bg="white")
    lbl_Tiempo.place(x=1122, y=355)
    lbl_puntos=Label(principal, font="system 40 bold", text=":", bg="white")
    lbl_puntos.place(x=1195.2, y=352)
    lbl_SegundosTiempo=Label(principal, font="system 40 bold", text="00", bg="white")
    lbl_SegundosTiempo.place(x=1220, y=355)
    segundosTiempo()
    frameLetras=Frame(principal, height=360, width=290, bg="orchid1")
    frameLetras.place(x=700, y=20)
    frameLetras2=Frame(principal, height=356, width=286, bg="white")
    frameLetras2.place(x=702, y=22)
    lbl_letDisp = Label(principal, text="Letras Disponibles", font="system 18 bold", bg="white")
    lbl_letDisp.place(x=720, y=45)
    lbl_jugA = Label(principal, text=nombreA, font="system 18 bold", bg="white")
    lbl_jugA.place(x=794, y=120)
    lbl_jugB = Label(principal, text=nombreB, font="system 18 bold", bg="white")
    lbl_jugB.place(x=794, y=240)
    
    # ESTILO DE LOS COMBOBOX

    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'gray',
                                       'fieldbackground': 'orchid1',
                                       'background': 'gray'
                                       }}}
                         )
    combostyle.theme_use('combostyle') 

    # COMBOBOX JUGADOR A
    
    varJugadorA = StringVar()
    comboboxA = ttk.Combobox(principal, textvariable=varJugadorA, width=20, height=20, state='disabled')
    comboboxA.place(x=765, y=180)

    # COMBOBOX JUGADOR B

    varJugadorB = StringVar()
    comboboxB = ttk.Combobox(principal, textvariable=varJugadorB, width=20, height=20, state='disabled')
    comboboxB.place(x=765, y=310)

    # Funciones Combobox A y B

    llenarCombobox()
    cambioCombobox()
    
    # Botones principales de la ventana
    
    btn_Letras = Button(principal, height=2, width=20, bg="white", text="Ver Letras", font="system 12 bold", command=puntajeLetras)
    btn_Letras.place(x=1160, y=550)
    btn_TerminarTurno = Button(principal, height=2, width=20, bg="white", text="Finalizar Turno", font="system 12 bold",command=finalizarTurno)
    btn_TerminarTurno.place(x=1160, y=600)
    btn_ImpMatriz = Button(principal, height=2, width=20, bg="white", text="Imprimir Matriz", font="system 12 bold", command=imprimir)
    btn_ImpMatriz.place(x=1160, y=650)
    btn_TerminarPartida = Button(principal, height=2, width=20, bg="white", text="Terminar Partida", font="system 12 bold", command=lambda:finalizarJuego(0))
    btn_TerminarPartida.place(x=1160, y=700)

    # Se crea la matriz con botones
    
    for y in range(15):
        botonMatriz.append(list())
        auxY = y + 1.8
        posYBoton = auxY * 42
        for x in range(15):
            auxX = x + 1
            posXBoton = auxX * 40
            botonMatriz[y].append(Button(principal, height=2, width=4, text="", bg="white", font="system 12 bold"))
            botonMatriz[y][x].place(x=posXBoton, y=posYBoton)
            
    # Se recorre la matriz y se llama una función
    for x in range(15):
        for y in range(15):
            botonMatriz[7][7].configure(bg="orange")
            botonMatriz[x][y].configure(command=lambda col=x, fil=y: moverMatriz(col, fil))
    contador123=0
    while contador123<10:
        xRand=random.randint(0,14)
        yRand=random.randint(0,14)
        for x in range(15):
            for y in range(15):
                botonMatriz[xRand][yRand].configure(text="red", fg="white")
        contador123+=1

    principal.mainloop()

ventanaInicio()
