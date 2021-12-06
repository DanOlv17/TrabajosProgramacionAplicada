import tkinter as tk
from math import sqrt
import time, threading
tiempo_global = time.time()


window = tk.Tk()
window.title("Hello wold")

def saluda_porllamadoatrasado():
    print('Saludando')


button_valvula1 = tk.Button( text="Valvula1")
button_valvula1.pack(side=tk.TOP)
button_valvula2 = tk.Button(text="Valvula2")
button_valvula2.pack(side=tk.TOP)
button_valvula3 = tk.Button(text="Valvula3")
button_valvula3.pack(side=tk.TOP)
label_vacio = tk.Label(text="Vacío")
label_vacio.pack(side=tk.TOP)
label_nivel1 = tk.Label(text="Nivel 1")
label_nivel1.pack(side=tk.TOP)
label_nivel2 = tk.Label(text="Nivel 2")
label_nivel2.pack(side=tk.TOP)

canvas = tk.Canvas(window, width=800, height=800)
canvas.pack(side=tk.BOTTOM)

img = tk.PhotoImage(file="planta.gif")
canvas.create_image(0, 0, anchor=tk.NW, image=img)


class Tanque:

  
    def __init__(self, id,capacidad_total, capacidad_inicial, izquierda, abajo,
                 derecha, arriba):
        self.id=id
        self.capacidad_total = capacidad_total
        self.capacidad_actual = capacidad_inicial
        self.izquierda = izquierda
        self.abajo = abajo
        self.derecha = derecha
        self.arriba = arriba

        alto = abajo - arriba
        altura_liquido = int(alto * self.capacidad_actual /self.capacidad_total)

        self.aire = canvas.create_rectangle(
            izquierda, arriba,
            derecha, abajo - altura_liquido,
            fill='white',
       )
        self.liquido = canvas.create_rectangle(
            izquierda, abajo - altura_liquido,
            derecha, abajo,
            fill='blue',
        )

    def dibujo_tkinter(self):
        capacidad_total = self.capacidad_total
        capacidad_actual = self.capacidad_actual
        izquierda = self.izquierda
        abajo = self.abajo
        derecha = self.derecha
        arriba = self.arriba
        alto = abajo - arriba
        altura_liquido = int(alto * capacidad_actual / capacidad_total)
        # Dibuja un rectángulo para representar la parte ocupada 
        # y otro para el resto
        canvas.coords(
            self.aire,
            izquierda, arriba,
            derecha, abajo - altura_liquido,
        )
        canvas.coords(
            self.liquido,
            izquierda, abajo - altura_liquido,
            derecha, abajo,
        )

        return self

    def adicionar(self, cantidad):
        self.capacidad_actual += cantidad
        self.dibujo_tkinter()

    def deja_salir(self,t):
        S1=10 # area arriba
        S2=0.3  # area de la valvula
        #g=10
        H=self.capacidad_actual/S1

        # según http://www.sc.ehu.es/sbweb/fisica3/fluidos/vaciado/vaciado.html
        #h=(sqrt(H)-S2*sqrt(2*9.8/(S1^2-S2^2))*t/2).^2;
        if H>=0:
            h=(sqrt(H)-S2*sqrt(2*9.8/(S1**2-S2**2))*t/2)**2
        else:
            h=0
        volumen=(H-h)*S1
        print('deja_salir',t,H,sqrt(H),S2*sqrt(2*9.8/(S1**2-S2**2))*t/2)#H,h,S1,volumen
        self.sustraer(volumen)
        return volumen

    def sustraer(self, cantidad):
        self.adicionar(-cantidad)

class Caldera(Tanque):
    def __init__(self, id,capacidad_total, capacidad_inicial, izquierda, abajo,
                 derecha, arriba, valor_vacio, valor_nivel_1, valor_nivel_2 ):
        super().__init__(id,capacidad_total, capacidad_inicial, izquierda, abajo,
                 derecha, arriba)
        self.valor_vacio   = valor_vacio
        self.valor_nivel_1 = valor_nivel_1
        self.valor_nivel_2 = valor_nivel_2

    def esta_vacio(self):
        return (self.capacidad_actual <= self.valor_vacio)
   
    def esta_nivel_1(self):
        return (self.capacidad_actual >= self.valor_nivel_1)
   
    def esta_nivel_2(self):
        return (self.capacidad_actual >= self.valor_nivel_2)
   

class Valvula:

    def color_valvula(self):
        return 'red' if self.valvula_abierta else 'green'

  
    def __init__(self,id, flujo_por_segundo, valvula_abierta, izquierda, abajo,
                 derecha, arriba, tanque_sustrae, tanque_adiciona):
        self.id=id
        self.valvula_abierta = valvula_abierta
        self.flujo_por_segundo = flujo_por_segundo
        self.izquierda = izquierda
        self.abajo = abajo
        self.derecha = derecha
        self.arriba = arriba
        self.tanque_sustrae = tanque_sustrae
        self.tanque_adiciona = tanque_adiciona


        self.dibujo = canvas.create_polygon(
            izquierda, arriba,
            izquierda, abajo,
            derecha, arriba,
            derecha, abajo,
            fill=self.color_valvula(),
        )


    def actualiza_valores(self,tiempo):
        if self.valvula_abierta:
            self.tanque_adiciona.adicionar(self.tanque_sustrae.deja_salir(tiempo))

    def cambia_estado(self):
        #print('cambia_estado',self.valvula_abierta)
        self.valvula_abierta = not(self.valvula_abierta)
        #print('cambia_estado',self.valvula_abierta)
        canvas.itemconfig(self.dibujo,fill=self.color_valvula())


t1 = Tanque(1,400, 300, 65, 142, 184, 37)
t2 = Tanque(2,400, 300, 288, 146, 406, 40)
c  = Caldera(3,100, 0, 155, 295, 325, 196,10,50,80)
t3 = Tanque(4,1000, 0, 295, 452, 488, 353)
v1 = Valvula(5,5,False,143,170,181,160,t1,c)
v2 = Valvula(6,5,False,286,176,325,162,t2,c)
v3 = Valvula(7,5,False,291,330,330,315,c,t3)
button_valvula1.configure(command=v1.cambia_estado)
button_valvula2.configure(command=v2.cambia_estado)
button_valvula3.configure(command=v3.cambia_estado)
#canvas.itemconfig(label_vacio,fill=self.color_valvula())


finaliza = False
def actualizacion_periodica():


    if not finaliza:
        threading.Timer(1, actualizacion_periodica).start()
        global tiempo_global
        #print(time.ctime())
        tiempo_actual = time.time()
        tiempo = tiempo_actual - tiempo_global
        tiempo_global = tiempo_actual
        v1.actualiza_valores(tiempo)
        v2.actualiza_valores(tiempo)
        v3.actualiza_valores(tiempo)
    else:
        print('Finalizó')

actualizacion_periodica()
tk.mainloop()  
finaliza=True
print('Finalizando')