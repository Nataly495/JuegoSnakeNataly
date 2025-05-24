from abc import ABC, abstractmethod
import turtle
import random
import time

# === Productos abstractos ===
class Comida(ABC):
    # Método abstracto para aplicar el efecto de la comida en el juego
    @abstractmethod
    def aplicar_efecto(self, juego):
        pass

    # Método abstracto para definir el color de la comida
    @abstractmethod
    def color(self):
        pass

# === Fábricas abstractas ===
class FabricaComida(ABC):
    # Método abstracto para crear un objeto comida concreto
    @abstractmethod
    def crear_comida(self) -> Comida:
        pass

# === Comidas concretas ===
class ComidaVenenosa(Comida):
    # Reduce la serpiente y disminuye puntaje si la serpiente es mayor a 3 segmentos
    def aplicar_efecto(self, juego):
        if len(juego.serpiente) > 3:
            juego.reducir_serpiente()
        juego.puntaje = max(0, juego.puntaje - 1)

    # Color púrpura para la comida venenosa
    def color(self):
        return "purple"

class ComidaFit(Comida):
    # Hace crecer la serpiente y aumenta el puntaje en 1
    def aplicar_efecto(self, juego):
        juego.crecer_serpiente()
        juego.puntaje += 1

    # Color verde para la comida fit
    def color(self):
        return "green"

class ComidaGrasa(Comida):
    # Hace crecer la serpiente, aumenta puntaje y ralentiza el juego
    def aplicar_efecto(self, juego):
        juego.crecer_serpiente()
        juego.puntaje += 3
        juego.delay += 0.03  # ralentiza la velocidad del juego

    # Color amarillo para la comida grasa
    def color(self):
        return "yellow"

class ComidaReyes(Comida):
    # Hace crecer la serpiente, aumenta puntaje y acelera el juego
    def aplicar_efecto(self, juego):
        juego.crecer_serpiente()
        juego.puntaje += 5
        juego.delay = max(0.05, juego.delay - 0.02)  # acelera la velocidad (límite mínimo)

    # Color naranja para la comida reyes
    def color(self):
        return "orange"

# === Fábricas concretas ===
class FabricaComidaVenenosa(FabricaComida):
    # Crea instancia de ComidaVenenosa
    def crear_comida(self) -> Comida:
        return ComidaVenenosa()

class FabricaComidaFit(FabricaComida):
    # Crea instancia de ComidaFit
    def crear_comida(self) -> Comida:
        return ComidaFit()

class FabricaComidaGrasa(FabricaComida):
    # Crea instancia de ComidaGrasa
    def crear_comida(self) -> Comida:
        return ComidaGrasa()

class FabricaComidaReyes(FabricaComida):
    # Crea instancia de ComidaReyes
    def crear_comida(self) -> Comida:
        return ComidaReyes()

# === Juego Snake ===
class JuegoSnake:
    def __init__(self):
        # Configuración inicial de la ventana del juego
        self.ventana = turtle.Screen()
        self.ventana.title("Snake Abstract Factory")
        self.ventana.bgcolor("black")
        self.ventana.setup(width=600, height=600)
        self.ventana.tracer(0)  # Desactiva el refresco automático para mejor control

        # Inicialización de variables del juego
        self.puntaje = 0
        self.delay = 0.15  # Tiempo de espera entre movimientos (velocidad)
        self.direccion = "stop"
        self.serpiente = []

        # Creación del segmento cabeza de la serpiente
        cabeza = turtle.Turtle()
        cabeza.shape("square")
        cabeza.color("white")
        cabeza.penup()
        cabeza.goto(0, 0)
        self.serpiente.append(cabeza)

        # Configuración del texto para mostrar el puntaje
        self.texto = turtle.Turtle()
        self.texto.speed(0)
        self.texto.color("white")
        self.texto.penup()
        self.texto.hideturtle()
        self.texto.goto(0, 260)
        self.texto.write("Puntaje: 0", align="center", font=("Courier", 20, "normal"))

        # Configuración del objeto comida (visual)
        self.comida = turtle.Turtle()
        self.comida.shape("circle")
        self.comida.penup()
        self.fabrica_actual = None
        self.generar_nueva_comida()  # Genera la primera comida

        # Configuración de controles de teclado para mover la serpiente
        self.ventana.listen()
        self.ventana.onkey(lambda: self.cambiar_direccion("up"), "Up")
        self.ventana.onkey(lambda: self.cambiar_direccion("down"), "Down")
        self.ventana.onkey(lambda: self.cambiar_direccion("left"), "Left")
        self.ventana.onkey(lambda: self.cambiar_direccion("right"), "Right")

    def cambiar_direccion(self, dir):
        # Cambia la dirección de la serpiente sin permitir reversa inmediata
        if dir == "up" and self.direccion != "down":
            self.direccion = "up"
        elif dir == "down" and self.direccion != "up":
            self.direccion = "down"
        elif dir == "left" and self.direccion != "right":
            self.direccion = "left"
        elif dir == "right" and self.direccion != "left":
            self.direccion = "right"

    def mover(self):
        # Mueve cada segmento de la serpiente siguiendo al anterior
        for i in range(len(self.serpiente)-1, 0, -1):
            x = self.serpiente[i-1].xcor()
            y = self.serpiente[i-1].ycor()
            self.serpiente[i].goto(x, y)

        # Mueve la cabeza en la dirección actual
        cabeza = self.serpiente[0]
        x, y = cabeza.xcor(), cabeza.ycor()

        if self.direccion == "up":
            cabeza.sety(y + 20)
        elif self.direccion == "down":
            cabeza.sety(y - 20)
        elif self.direccion == "left":
            cabeza.setx(x - 20)
        elif self.direccion == "right":
            cabeza.setx(x + 20)

    def crecer_serpiente(self):
        # Añade un nuevo segmento a la serpiente
        nuevo = turtle.Turtle()
        nuevo.shape("square")
        nuevo.color("white")
        nuevo.penup()
        self.serpiente.append(nuevo)

    def reducir_serpiente(self):
        # Elimina el último segmento de la serpiente si hay más de uno
        if len(self.serpiente) > 1:
            segmento = self.serpiente.pop()
            segmento.hideturtle()

    def verificar_colision_comida(self):
        # Verifica si la cabeza colisiona con la comida
        if self.serpiente[0].distance(self.comida) < 20:
            efecto = self.fabrica_actual.crear_comida()
            efecto.aplicar_efecto(self)  # Aplica el efecto correspondiente
            self.actualizar_puntaje()
            self.generar_nueva_comida()

    def generar_nueva_comida(self):
        # Selecciona aleatoriamente una fábrica de comida y posiciona la comida
        fabricas = [
            FabricaComidaVenenosa(),
            FabricaComidaFit(),
            FabricaComidaGrasa(),
            FabricaComidaReyes()
        ]
        self.fabrica_actual = random.choice(fabricas)
        comida = self.fabrica_actual.crear_comida()
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.comida.goto(x, y)
        self.comida.color(comida.color())

    def actualizar_puntaje(self):
        # Actualiza el texto del puntaje en pantalla
        self.texto.clear()
        self.texto.goto(0, 260)
        self.texto.write(f"Puntaje: {self.puntaje}", align="center", font=("Courier", 20, "normal"))

    def verificar_colision_bordes(self):
        # Verifica si la cabeza salió de los límites de la ventana
        cabeza = self.serpiente[0]
        x, y = cabeza.xcor(), cabeza.ycor()
        return abs(x) > 290 or abs(y) > 290

    def verificar_colision_cuerpo(self):
        # Verifica si la cabeza colisiona con algún segmento del cuerpo
        cabeza = self.serpiente[0]
        for segmento in self.serpiente[1:]:
            if cabeza.distance(segmento) < 20:
                return True
        return False

    def loop(self):
        # Bucle principal del juego
        while True:
            self.ventana.update()  # Actualiza pantalla
            self.mover()  # Mueve serpiente
            self.verificar_colision_comida()  # Verifica si comió comida

            # Verifica colisiones que terminan el juego
            if self.verificar_colision_bordes() or self.verificar_colision_cuerpo():
                break  # Sale del bucle (fin del juego)

            time.sleep(self.delay)  # Espera según la velocidad

        self.ventana.bye()  # Cierra la ventana al finalizar el juego

# === Ejecutar juego ===
if __name__ == "__main__":
    juego = JuegoSnake()  # Crea instancia del juego
    juego.loop()          # Inicia el bucle principal
