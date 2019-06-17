from tkinter import*
import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import queue


import binascii
import sys
import string

import Adafruit_PN532 as PN532


CS   = 8
MOSI = 10
MISO = 9
SCLK = 11



pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)


pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()

pn532.SAM_configuration()

ListaUsuarios=['04b122129c3681','042216129c3681','040317129c3681'] #lista de usuarios
comprobado=0##bandera para verificacion de UID
opcionesServicio=['Pagar','Comprar','Consultar']
opcionesCantidad=[1,2,3,4]
numeros=[0,1,2]
pes=4
cant=0
tiquetesAnteriores=0
tiquetesActuales=0
usuario=bytes()
cancel='no'



def nuevaVentana():
    messagebox.showwarning("","Error en la lectura, por favor aproxime el tag")

def aviso():#aviso para que acerque el tag
    messagebox.showinfo(" ", "Acerque el tag al modulo NFC")

def cancelar():
    global cancel
    cancel=messagebox.askquestion('','Desea cancelar')

def comprobacionUID():
    global usuario
    global comprobado
    usuarioSTRING=usuario.decode('utf-8') ##pasa los bytes de usuario a str

    if usuarioSTRING in ListaUsuarios:
        comprobado=1
        print("usuario identificado")
        
    
def openWindow():
    global tiquetesActuales
    global tiquetesAnteriores
    global usuario


    usuarioSTRING=usuario.decode('utf-8')

    imprUsuario=StringVar()
    imprUsuario.set(usuarioSTRING)
    cantidadActualVar=IntVar()
    cantidadAnterior=IntVar()
    cantidadActualVar.set(tiquetesActuales)
    cantidadAnterior.set(tiquetesAnteriores)
    cantAnterior=Label(font=('arial',15),textvariable=cantidadAnterior).place(x=600,y=200)
    cantActual=Label(font=('arial',15),textvariable=cantidadActualVar).place(x=600,y=250)
    USUARIO=Label(font=('arial',15),textvariable=imprUsuario).place(x=500,y=150)
    
def TransaccionNueva():
    global tiquetesActuales
    global tiquetesAnteriores
    global usuario
    global cant
    global cancel
    cancel='yes'
    usuario=b'00000000000000'
    tiquetesActuales=0
    tiquetesAnteriores=0
    cant=0

    usuarioSTRING=usuario.decode('utf-8')

    imprUsuario=StringVar()
    imprUsuario.set(usuarioSTRING)
    cantidadActualVar=IntVar()
    cantidadAnterior=IntVar()
    cantidadActualVar.set(tiquetesActuales)
    cantidadAnterior.set(tiquetesAnteriores)
    cantAnterior=Label(font=('arial',15),text="         ").place(x=600,y=200)
    cantActual=Label(font=('arial',15),text="      ").place(x=600,y=250)
    USUARIO=Label(font=('arial',15),text="                              ").place(x=500,y=150)

def interfaz():
    global pes
    global cant
    global tiquetesActuales
    global bandera
    
    root=Tk()
    root.geometry("800x480")
    root.title("PantallaNFC")

    Tops=Frame(root,width=1600,height=20, bg="powder blue", relief=SUNKEN)
    Tops.pack(side=TOP)
    ###########colocando la hora######
    localtime=time.asctime(time.localtime(time.time()))
    
    ######Etiquetas######
    lblInfo=Label(Tops,font=('arial',14,'bold'),text='PAGO BUSES',fg="Steel Blue", bd=20,ancho='w')
    lblInfo.grid(row=0,column=0)

    lblInfo=Label(Tops,font=('arial',14,'bold'),text=localtime,fg="Steel Blue", bd=10,ancho='w')
    lblInfo.grid(row=1,column=0)



    Proceso=Label(font=('arial',15),text='Proceso:').place(x=15,y=150)
    Cant=Label(font=('arial',15),text='Cantidad:').place(x=15,y=200)

    
    Usuario=Label(font=('arial',15),text='Usuario:').place(x=400,y=150)
    CantAnterior=Label(font=('arial',15),text='Tiquetes anteriores:').place(x=400,y=200)
    CantActual=Label(font=('arial',15),text='Tiquetes actuales:').place(x=400,y=250)
    

    #########lista desplegable#####
    var=tk.StringVar(root)
    var.set(opcionesServicio[0])
    opcionP=tk.OptionMenu(root,var,*opcionesServicio)
    opcionP.config(width=12)
    opcionP.place(x=110,y=150)
   
    

    var2=tk.StringVar(root)
    var2.set(opcionesCantidad[0])
    opcionC=tk.OptionMenu(root,var2,*opcionesCantidad)
    opcionC.config(width=12)
    opcionC.place(x=110,y=200)

    aglobal=IntVar()
    
    cantidadActualVar=IntVar()

    
    def selproceso():
        global pes
        global cant
        global tiquetesActuales
        cant=var2.get()
        cantidadActualVar.set(tiquetesActuales)
        if var.get()==opcionesServicio[0] :
            aglobal.set(numeros[0])
            pes=numeros[0]
        elif var.get()==opcionesServicio[1] :
            aglobal.set(numeros[1])
            pes=numeros[1]
        elif var.get()==opcionesServicio[2] :
            aglobal.set(numeros[2])
            pes=numeros[2]
        aviso()

            
        
    selectBoton=Button(text="Select",command=selproceso)
    selectBoton.place(x=145,y=250)

    nuevaTransaccion=Button(text="Nueva Transaccion",command=TransaccionNueva)
    nuevaTransaccion.place(x=105,y=300)

    cancelButton=Button(text="Cancelar",command=cancelar)
    cancelButton.place(x=140,y=350)
    
    root.mainloop()
        


def comprar(cantidad):
    global pes
    global tiquetesActuales
    global tiquetesAnteriores
    global usuario
    global cancel
    global comprobado
    pes=7
    ##cantidad=int(input("\n\nDigite la cantidad de tiquetes a comprar: "))
    print("\n\nAcerque el tag nfc")
    uid = pn532.read_passive_target()
    contador=0
    salir=0
    while uid is None:
        uid = pn532.read_passive_target()
        data = pn532.mifare_classic_read_block(4)
        if data is None:
            print('Tag no detectado')
            print('Por favor aproxime su tag NFC \n\n')
            contador=contador+1
            if cancel =='yes':
                salir=1
                TransaccionNueva()
                cancel='no'
                return
            if(contador==6):
                nuevaVentana()
                contador=0
            continue
        
    if salir==1:
        salir=0
        return
    usuario=binascii.hexlify(uid)
    print('')
    print('UID: de tag 0x{0}'.format(binascii.hexlify(uid)))
    print('')
    print("Cantidad de tiquetes actuales: "+str(data[1]))
    print('')
    print('')
    print('==============================================================')
    print('Por favor no remueva el tag hasta terminar la transaccion!')
    print('==============================================================\n\n')
    tiquetesAnteriores=data[1]
    suma = data[1]+cantidad
    if suma > 255:
        print('')
        print('Transaccion invalida')
        print('La cantidad de tiquetes totales es prohibida')
        return
    data[1]=data[1]+cantidad
    pn532.mifare_classic_write_block(4, data)
    tiquetesActuales=data[1]
    print('Transaccion finalizada con exito')
    print("\nCantidad de tiquetes actuales: "+str(data[1])+'\n\n')
    
  

    
    
def pagar(cantidad):
    global tiquetesActuales
    global pes
    global tiquetesAnteriores
    global usuario
    global cancel
    salir=0
    pes=7
    ##cantidad=int(input("Digite la cantidad de tiquetes a pagar: "))
    print("\nAcerque el tag nfc")
    uid = pn532.read_passive_target()
    contador=0
    while uid is None:
        uid = pn532.read_passive_target()
        data = pn532.mifare_classic_read_block(4)
        if data is None:          
            print('Tag no detectado!')
            print('Por favor aproxime su tag NFC\n\n')
            contador=contador+1
            if cancel =='yes':
                salir=1
                TransaccionNueva()
                cancel='no'
                return
            if(contador==6):
                nuevaVentana()
                contador=0
            continue
    if salir==1:
        salir=0
        return
    usuario=binascii.hexlify(uid)
    print('UID: de tag 0x{0}'.format(binascii.hexlify(uid)))
    print('')
    print("Cantidad de tiquetes antes de realizar la transaccion: "+str(data[1]))
    print('')
    print('')
    print('==============================================================')
    print('Por favor no remueva el tag hasta terminar la transaccion!')
    print('==============================================================')
    print('')
    tiquetesAnteriores=data[1]
    if cantidad > data[1]:
        print("Transaccion invalida")
        return
    data[1]=data[1]-cantidad
    pn532.mifare_classic_write_block(4, data)
    tiquetesActuales=data[1]
    print('Transaccion finalizada con exito')
    print('')
    print("Cantidad de tiquetes actuales: "+str(data[1])+'\n\n')

def consultar():
    global tiquetesAnteriores
    global tiquetesActuales
    global pes
    global usuario
    global cancel
    global comprobado
    salir=0
    
    pes=7
    print('')
    print("Acerque el tag nfc")
    
    uid = pn532.read_passive_target()
    contador=0
    while uid is None:
        uid = pn532.read_passive_target()
        data = pn532.mifare_classic_read_block(4)
        if data is None:
        
            print('Tag no detectado!')
            print('Por favor aproxime su tag NFC')
            print('')
            print('')
            contador=contador+1
            if cancel =='yes':
                salir=1
                TransaccionNueva()
                cancel='no'
                return
            if(contador==6):
                nuevaVentana()
                contador=0
            continue
        
    if salir==1:
        salir=0
        return
    
    tiquetesAnteriores=None
    tiquetesActuales=data[1]
    usuario=binascii.hexlify(uid)
    print('UID: de tag 0x{0}'.format(binascii.hexlify(uid)))
    print('')
    print("Cantidad de tiquetes actuales: "+str(data[1])+'\n\n')
    

def nfc():
    print('\n\n Que desea realizar \n\n')
    print('0-Pagar\n')
    print('1-Comprar\n')
    print('2-Consultar\n\n')
    
    while True:
        global pes
        global cant
        global usuario
        cantidad=cant
        cantidad =int(cantidad)
        global cancel
        cancel='no'
        if pes<=2:
            if pes == 0 :
                print("Iniciando pago")
                pagar(cantidad)

            elif pes == 1 :
                print("Iniciando compra")
                comprar(cantidad)
                        
            elif pes == 2 :
                print("Iniciando consulta")
                consultar()
            openWindow()
            
        


hilonfc=threading.Thread(target=nfc)
hilonfc.start()
        
hilo=threading.Thread(target=interfaz)
hilo.start()


    

