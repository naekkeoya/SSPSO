import tkinter as tk
import random as rd
import time
import os

canvas_w = 100
canvas_h = 40
lotes = 0
reloj = 0
maxLote = 6
procesos = []
procesosEje = []
procesosTer = []
nombres = ['José','Carlos','Carolina','Juan','Gerardo','Daniela']
operaciones = ['+','-','*','/']
global cambioLote

#Definimos nuesta ventana, donde m  is el nombre de la ventana principal
m = tk.Tk()
m.title('Proceso por lotes')

#Validacion
def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

#Definimos los labels y botones para la aplicacion
ingresaLabel = tk.Label(m, text='Ingresa el numero de procesos:',width=25)
enterLotes = tk.Entry(m,validate="key")
enterLotes['validatecommand'] = (enterLotes.register(testVal),'%P','%d')
lotesBtn = tk.Button(m, text='Generar', command=lambda: validarDatos())
iniciarBtn = tk.Button(m, text='Iniciar', command=lambda: procesamientoLotes())
lotesLabel = tk.Label(m, text='Lotes restantes:')
tiempoLabel = tk.Label(m, text='Tiempo:')
lotesLabel.config(text='Lotes faltantes:')
tiempoLabel.config(text='Tiempo:' + str(reloj))
proEsLabel = tk.Label(m,text='Procesos en espera')
proEjLabel = tk.Label(m,text='Procesos en ejecución')
proTeLabel = tk.Label(m,text='Procesos terminados')

#Listbox
listboxProES = tk.Listbox(m)
listboxProEj = tk.Listbox(m)
listboxProTe = tk.Listbox(m)

#Inicializamos las posiciones de los elementos
lotesLabel.pack()
tiempoLabel.pack()
ingresaLabel.pack()
enterLotes.pack()
lotesBtn.pack()
iniciarBtn.pack()
proEsLabel.pack(side = tk.LEFT)
listboxProES.pack(side = tk.LEFT)
proEjLabel.pack(side = tk.LEFT)
listboxProEj.pack(side = tk.LEFT)
proTeLabel.pack(side = tk.LEFT)
listboxProTe.pack(side = tk.LEFT)

#Listas para los procesos
listaEjecucion=[]
listaTerminado=[]

#Creamos la clase para los procesos
#   Donde tme  = Tiempo máximo estimado
class Proceso:
    np = 0
    def __init__(self,programador,operacion,tme,pOper1,pOper2, nLote):
        self.programador = programador
        self.operacion = operacion
        self.tme = tme
        self.pOper1 = pOper1
        self.pOper2	= pOper2
        self.nLote = nLote

#método para saber si hay o no texto
def validarDatos():
    if not enterLotes.get():
        print('No hay datos')
    else:
        del procesos[:]
        listboxProES.delete(0,tk.END)
        lotes = enterLotes.get()
        lotesLabel.config(text=lotes)
        print(lotes)
        crearProcesos(int(lotes))
        #imprimeLista()
        enlistarEnListBoxEs(procesos[0],-1,-1)

#creamos aleatoriamente los procesos
def crearProcesos(lot):
    cont = 1
    lote = 1
    nproceso = 1
    cambioLote = maxLote
    for x in range(0,lot):
        if (cont == maxLote+1):
            cont = 1
            lote += 1
        pName = rd.choice(nombres)
        pOper = rd.choice(operaciones)
        pTME = rd.randrange(1,5)
        pOper1 = rd.randrange(0,30)
        pOper2 = rd.randrange(0,30)
        pLote = lote
        p = Proceso(pName,pOper,pTME,pOper1,pOper2,lote)
        p.np = x+1
        procesos.append(p)
        cont += 1
    guardarProcesos()
    if os.path.exists("Resultado.txt"):
        os.remove("Resultado.txt")
    if os.path.exists("Procesamiento.txt"):
        os.remove("Procesamiento.txt")
    lotesLabel.config(text='Lotes faltantes:'+str(obtenerNLotes(lot)))

#Obtener lotes
def obtenerNLotes(procesos):
    if procesos == 6:
        return 1
    else:
        return round(procesos/maxLote)

#imprimimos elementos en lista
def imprimeLista():
	for elemento in range(0,len(procesos)):
		print(procesos[elemento].programador +','+ str(procesos[elemento].pOper1) + procesos[elemento].operacion + str(procesos[elemento].pOper2) +','+ str(procesos[elemento].tme) )

def enlistarEnListBoxEs(procesoA,np,lote):
    listboxProES.delete(0,1)
    listboxProES.insert(tk.END, str(procesoA.np) + '. ' + procesoA.programador +','+ str(procesoA.pOper1) + procesoA.operacion + str(procesoA.pOper2) +','+ str(procesoA.tme) )
    print(str(np) + '/' + str(lote))
    if (np != -1 and lote != -1):
        x = definirRestantes(np, lote)
        listboxProES.insert(tk.END, x)

#Eliminamos elemento y lo cambiamos de lista; Recibe el listbox inicial y el final ---Vease linea 82
def cambiarDeLista(listboxInicial, listboxFinal):
    #listboxInicial.get(0)
    listboxFinal.insert(tk.END, listboxInicial.get(0))
    listboxInicial.delete(0)

def decrementarTme(listboxActual):
    n = listboxActual.get(0);
    listboxActual.delete(0)
    cont = 0
    x = 0
    y = 0
    numerito = ''
    while(x != len(n)):
        #print(x)
        if(n[x]== ','):
            cont += 1
            #print('son iguales, contador =' + str(cont))
        elif(cont == 2):
            numerito += n[x]
        x += 1
    while (y != len(numerito)):
        n = n[0:-1]
        y += 1
    n = n + str(int(numerito)-1)
    listboxActual.insert(tk.END, n)

#Procesamiento de lotes. El while se realiza desde 0 hasta nuestra cantidad de Procesos
#El for va desde 0 hasta el TME de el proceso actual
#Dentro del for el reloj avanza por cada iteracion y se deberia actualizar en el tiempoLabel ---Alentar la listaEjecucion
#Al finalizar el for deberia usarse el metodo de cambiarDeLista
def procesamientoLotes():
    listboxProTe.delete(0,tk.END)
    cont = 0
    reloj = 0
    ta = 0
    valido = True
    cambiarLote = True
    lotesFaltantes = obtenerNLotes(len(procesos))
    procesoActual = procesos[cont]
    loteActual = procesoActual.nLote


    #cambiarDeLista(listboxProES,listboxProEj)
    while(cont != len(procesos)):
        procesoActual = procesos[cont]
        if(cont > 0):
            enlistarEnListBoxEs(procesoActual,procesoActual.np, lotesFaltantes)
        elif(cont==0):
            cambiarDeLista(listboxProES,listboxProEj)
        listboxProES.delete(0)
        if cont+1 != len(procesos):
            enlistarEnListBoxEs(procesos[cont+1],procesoActual.np, lotesFaltantes)

        for r in range(0,procesoActual.tme):
            if (r == procesoActual.tme):
                break
            reloj += 1
            tiempoLabel.config(text='Tiempo:' + str(reloj))
            tiempoLabel.update()
            guardarProcesamiento(procesoActual.np, procesoActual.tme, reloj)
            #m.after(1000,lambda:procesamientoLotes())
            time.sleep(.5) #Esta funcion de la libreria time crea un delay en el ciclo ---Vease linea 3
            decrementarTme(listboxProEj)
            if (procesoActual.pOper2 == 0):
                valido = False
                break
        if (cont > 0 and cont+1 < len(procesos)):
            if (procesoActual.nLote == procesos[cont-1].nLote):
                #guarda normal
                cambiarLote = False
            else:
                #guarda y cambia lote
                cambiarLote = True
                #loteActual = procesos[cont+1].nLote
                #lotesFaltantes -= 1
                #lotesLabel.config(text='Lotes restantes: ' + str(lotesFaltantes))
                #lotesLabel.update()
        if valido:
            resultado = realizarOperacion(procesoActual.operacion, procesoActual.pOper1, procesoActual.pOper2)
            guardarResultado(loteActual,procesoActual.np, resultado, cambiarLote)
        else:
            guardarResultado(loteActual,procesoActual.np, 'Error en la operación: No se puede dividir por 0', cambiarLote)
        cambiarDeLista(listboxProEj,listboxProTe)
        if "Restantes" in listboxProES.get(0):
            #Nnvalida
            print("algo")
        else:
            cambiarDeLista(listboxProES,listboxProEj)
        lotesFaltantes = cambiarLoteActual(procesoActual.np,lotesFaltantes)
        cont += 1
        valido = True

    lotesLabel.config(text='Lotes restantes: 0')
    lotesLabel.update()
    procesos.clear()


def realizarOperacion(operacion,operador1, operador2):
    resultado = 0
    resultadoT = 'vacio'
    if (operacion== '+'):
        #suma
        resultado = operador1 + operador2
        return str(resultado)
    elif (operacion == '-'):
        #resta
        resultado = operador1 - operador2
        return str(resultado)
    elif (operacion == '*'):
        #multiplicacion
        resultado = operador1 * operador2
        return str(resultado)
    elif (operacion == '/'):
        #division
        if (operador2 == 0):
            resultadoT = 'No se puede dividir por 0: Error'
        else:
            resultado = operador1 / operador2

    else:
        resultadoT = 'datos erroneos'
    resultadoT = str(resultado)
    return resultadoT

def cambiarLoteActual(nproceso, lotesFaltantes):
    #cambioLote = cambioLote -1
    #n = "Restantes: " + str(cambioLote)
    #listboxProES.delete(1)
    #listboxProES.insert(tk.END, n)
    if nproceso % 6 == 0:
        print('Comienza un nuevo lote')
        cambioLote = maxLote
        lotesFaltantes -= 1
        lotesLabel.config(text='Lotes restantes: ' + str(lotesFaltantes))
        lotesLabel.update()
    return lotesFaltantes

def definirRestantes(nproceso, lotesFaltantes):
    if nproceso % maxLote == 0:
        cambioLote = maxLote
        lotesFaltantes -= 1
    restantes = maxLote - (nproceso % maxLote) if lotesFaltantes > 1 else len(procesos) - nproceso
    restantes = "Restantes: " + str(restantes)
    return restantes

def actualizarReloj(reloj):
    #print('funciono¿')
    tiempoLabel.config(text=reloj)

#guardamos los procesos en la listbox inicial(espera)
def enlistarEnListbox():
	listboxProES.delete(0,tk.END)

#guardamos los procesos en un text
def guardarProcesos():
    contl = 1
    loteActual = 1
    f = open('Lotes.txt','w+')
    f.writelines(f'Lote #{loteActual}\n')
    for proceso in procesos:
        #print(loteActual)
        if (loteActual != proceso.nLote):
            #print(proceso.nLote)
            loteActual = proceso.nLote
            f.writelines(f'Lote #{loteActual}\n')
        f.writelines(f'{proceso.np}. {proceso.programador} \n {proceso.pOper1} {proceso.operacion} {proceso.pOper2} \n TME: {proceso.tme} \n')
        #f.writelines(proceso.programador +','+ str(proceso.pOper1) +','+proceso.operacion +','+ str(proceso.pOper2) +','+ str(proceso.tme) +','+ str(proceso.np) + '\n' )
    f.close()

def guardarProcesamiento(proceso, tiempoTotal, reloj):
    f = open('Procesamiento.txt','a')
    f.write(f' Trabajando el proceso: {proceso}, TME: {tiempoTotal}, Reloj: {reloj} \n')

def guardarResultado(loteActual, proceso, operacion, cambiar):
    loteActual = 1
    f = open('Resultado.txt','a')
    if (cambiar):
        print()
        loteActual = procesos[proceso].nLote
        f.writelines(f'Lote #{loteActual}\n')
    f.writelines(f'{proceso}.- Operación:{operacion} \n')
    f.close()

#Loop infinito hasta que la aplicación se cierre
m.mainloop()
