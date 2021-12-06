# Requerimientos básicos:
# Realizar la simulación de la variación interactiva del volumen de un tanque de agua. 
# Hay que visualizar el tanque y su volumen actual. 
# Además, en una gráfica, visualizar el histórico de los volúmenes.
label_advertencia["El nivel del agua en el tanque alcanzo el maximo"]

import tkinter as tk
import time,math

# # Constantes
# ## Dimensiones del Canvas
width=600
height=600


# # Ventana y componentes con tkinter
master = tk.Tk()
deslizador_1 = tk.Scale(master, from_=-0, to=10, length=600,tickinterval=1, orient=tk.HORIZONTAL)
deslizador_1.pack()
deslizador_2 = tk.Scale(master, from_=-10, to=0, length=600,tickinterval=1, orient=tk.HORIZONTAL)
deslizador_2.pack()
canvas = tk.Canvas(master, width=width, height=height)
canvas.pack()
img = tk.PhotoImage(file="planta.gif")
canvas.create_image(0, 0, anchor=tk.NW, image=img)

class Tanque: 
  

  
    def __init__(self,capacidad_total, capacidad_actual, izquierda, abajo,derecha, arriba):
        self.capacidad_total = capacidad_total
        self.capacidad_actual = capacidad_actual
        self.izquierda = izquierda
        self.abajo = abajo
        self.derecha = derecha
        self.arriba = arriba

        alto = abajo - arriba
        altura_liquido = int(alto * self.capacidad_actual/self.capacidad_total)

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

    def deja_salir(t,S2):
        '''
        Entradas
        --------
        t:float; indica el tiempo en segundos transcurrido
        S2:float; indica el area de la válvula que permite el paso del caudal
        Salidas
        -------
        volumen:float; indica el volumen de agua que salió o entro en ese tiempo 
        Descripción 
        ----------
        En caso que el valor de la válvula negativo sale el líquido usando el modelo físico correspondiente 
        En caso que el valor sea positivo entra liquido proporciona a la apertura y al tiempo
        '''
        S1=11 # Área superior del tanque
        H=capacidad_actual/S1 # Altura del líquido

        # según http://www.sc.ehu.es/sbweb/fisica3/fluidos/vaciado/vaciado.html
        #h=(sqrt(H)-S2*sqrt(2*9.8/(S1^2-S2^2))*t/2).^2;
        h=(math.sqrt(H)-S2*math.sqrt(2*9.8/(S1**2-S2**2))*t/2)**2
        volumen=(H-h)*S1

        if (capacidad_actual-volumen)<0:
                volumen=capacidad_actual
        return volumen

    def actualiza_nivel(self):
        # Ejercicio realizar los comentarios de esta rutina
        '''
        Esta rutina permite hacer la actualizacion de los rectangulos cada 100ms. La rutina actualizacion periodica hace la actualizacion de la variable capacidad_actual, y como las coordenadas de los rectangulos aire y liquido dependen de dicha variable, es necesario redibujarlos para poder ver correctamente la animacion del tanque llenandose y vaciandose.

        '''
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

    


t=Tanque(100, 30, 155, 300, 325, 200)


tiempo_global= time.time()
label_tiempo = tk.Label(canvas, text=tiempo_global)
label_tiempo.place(x=0, y=0)
def actualizacion_periodica():
        global tiempo_global,capacidad_actual
        label_tiempo.after(100, actualizacion_periodica) #= tk.Label(text=time.time())
        tiempo_actual = time.time()
        label_tiempo['text'] =  str(tiempo_actual)
        tiempo = tiempo_actual - tiempo_global
        tiempo_global = tiempo_actual
        # 

        S2=deslizador_2.get()
        if S2<0:
            capacidad_actual += Tanque.deja_salir(tiempo,S2)
        else:
          S2=deslizador_1.get()
          if S2>0:
            capacidad_actual += tiempo*S2*1
        #label_volumen['text'] =  str(capacidad_actual)
        Tanque.actualiza_nivel()


label_tiempo.after(100, actualizacion_periodica)

tk.mainloop()

# #Recomendaciones
# # No se puede usar el mismo deslizador para el líquido que entra y el que sale
# #    Un deslizador para el líquido que entra
# #    Otro deslizador para el líquido que sale
# # El volumen del líquido no puede superar el volumen del tanque
# # Comentar la rutina que le falta el comentario
# # Crear una clase (`class`) para el tanque
# # Además, en una gráfica, visualizar el histórico de los volúmenes.