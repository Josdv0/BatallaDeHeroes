import random
import customtkinter as ctk
import os # Necesario para manejar rutas de archivos
from PIL import Image, ImageTk 

# --- RUTAS DE ARCHIVOS LOCALES (PARA USO EN VS CODE) ---
# Si ejecutas esto en tu computadora, asegúrate de tener una carpeta 'sprites/'
# en el mismo directorio que este script con los archivos especificados.
IMAGE_PATHS = {
    "Keren": "img/keren.png",
    "Damian": "img/damian.png",
    "Nicole": "img/nicole.png",
    "Joss": "img/joss.png",
}

# --- Eliminamos las funciones de Base64 ya que usaremos el sistema de archivos ---

#Heroes
class NodoHeroe:
# ... [El resto del código de la clase NodoHeroe permanece igual]
    def __init__(self, nombre = None, PV = None, ataque = None, ataqueEsp = None, defensa = None, next = None):
        self.nombre = nombre
        self.nivel = 1
        self.PV = PV
        self.PVmax = PV
        self.ataque = ataque
        self.ataqueEsp = ataqueEsp 
        self.defensa = defensa
        self.defact = False
        self.estado = "vivo"
        self.xp = 0
        self.xpmax = 100
        self.next = next
        
    #se selecciona un objetivo especifico 
    def atacar_objetivo(self, objetivo, turnos):
# ... [El resto del código de la función atacar_objetivo permanece igual]
        if self.PV <= 0 or self.estado != "vivo":
            print(f"{self.nombre} no puede atacar: está debilitado.")
            return
        if objetivo.PV <= 0 or objetivo.estado != "vivo":
            print(f"{objetivo.nombre} ya está debilitado.")
            return
            
        # Almacenar la defensa original del objetivo para el cálculo del daño
        defensa_usada = objetivo.defensa
            
        daño_base = self.ataque - (defensa_usada * 0.6)
        daño = max(1, int(daño_base * random.uniform(0.85, 1.15)))
        
        objetivo.PV -= daño
        
        if objetivo.PV <= 0:
            objetivo.PV = 0
            objetivo.estado = "muerto"
            print(f"{self.nombre} ataca a {objetivo.nombre} e inflige {daño} de daño ⚔️ ¡{objetivo.nombre} ha caído!")
            turnos.eliminarTurno(objetivo.nombre)
        else:
            print(f"{self.nombre} ataca a {objetivo.nombre} e inflige {daño} de daño 💥 Vida restante: {objetivo.PV}")
            
        self.ganarXP(daño/8)

    def curar(self):
# ... [El resto del código de la función curar permanece igual]
        if self.PV <= 0 or self.estado != "vivo":
            print(f"{self.nombre} no puede curarse: está debilitado.")
            return
        cantidad = int(self.ataque * random.uniform(0.8, 1.2))
        self.PV += cantidad
        if self.PV > self.PVmax:
            self.PV = self.PVmax
        print(f"{self.nombre} se cura {cantidad} puntos de vida.  (Vida actual: {self.PV}/{self.PVmax})")
        self.ganarXP(cantidad/8)

    def pasarTurno(self):
          print(f"{self.nombre} decide no actuar este turno... ⏳")

    def ganarXP(self, cantidad):
# ... [El resto del código de la función ganarXP permanece igual]
        # Asegurarse de que la cantidad de XP sea un entero para evitar incrementos muy pequeños
        self.xp += int(cantidad) 
        print(f"{self.nombre} gana {int(cantidad)} puntos de experiencia. (Total XP: {self.xp}/{self.xpmax})")
        
        # Bucle para manejar múltiples subidas de nivel si la XP es muy alta
        while self.xp >= self.xpmax:
            self.nivel += 1
            self.xp -= self.xpmax # Restar la XP necesaria para el nivel
            
            # Ajustar la XP máxima para el siguiente nivel
            if self.nivel % 2 == 0: # Nivel par, usa la fórmula 2x xpmax
                 self.xpmax = self.xpmax * 2
                 self.PVmax += 1000
                 self.ataque += 200
                 self.defensa += 200
            else: # Nivel impar, usa la fórmula normal
                 self.xpmax += 100
                 self.PVmax += 500
                 self.ataque += 100
                 self.defensa += 100
            
            print(f"🌟 ¡{self.nombre} sube de nivel a {self.nivel}! PV: {self.PVmax}, ATK: {self.ataque}, DEF: {self.defensa}.")
    
    # se multiplica la defensa ×1.5 
    def defender(self):
# ... [El resto del código de la función defender permanece igual]
        if self.PV <= 0 or self.estado != "vivo":
            print(f"{self.nombre} no puede defenderse: está debilitado.")
            return
        # Solo aplicamos la defensa si no está defendiendo ya
        if not self.defact:
            self.defensa_temp = self.defensa # Guardamos la defensa base en un atributo temporal
            self.defensa = int(self.defensa * 1.5)
            self.defact = True
            print(f"{self.nombre} levanta su defensa 🛡️ (Defensa aumentada temporalmente a {self.defensa}).")
        else:
            print(f"{self.nombre} ya está en posición defensiva.")

    def restablecer_defensa(self):
# ... [El resto del código de la función restablecer_defensa permanece igual]
        """Restaura la defensa a su valor base si estaba activada."""
        if self.defact:
            # Asegurarse de que self.defensa_base esté definido (se define en seleccionar_jugador)
            self.defensa = self.defensa_base 
            self.defact = False
            print(f"La defensa de {self.nombre} vuelve a la normalidad ({self.defensa}).")

    def mostrar(self):
        print(f"{self.nombre} | Nivel {self.nivel} | PV: {self.PV}/{self.PVmax} | Ataque: {self.ataque} | Defensa: {self.defensa} | Estado: {self.estado} | XP: {self.xp}/{self.xpmax}")

# 🔹 Esta clase permanece prácticamente igual entre versiones.
class ListaHeroes:
# ... [El resto del código de la clase ListaHeroes permanece igual]
    def __init__(self):
        self.head = None

    
    def is_empty(self):
        return self.head == None

    
    def agregarHeroe(self, nombre, PV, ataque, ataqueEsp, defensa):
        nuevo_nodo = NodoHeroe(nombre, PV, ataque, ataqueEsp, defensa, self.head)
        self.head = nuevo_nodo

    def eliminarHeroe(self, nombre):
        if self.is_empty():
            return
        
        if self.head.nombre == nombre:
            self.head = self.head.next
            # Si era el único nodo, self.head se convierte en None.
            return
        
        nodo_actual = self.head
        while nodo_actual.next != None:
            if nodo_actual.next.nombre == nombre:
                nodo_actual.next = nodo_actual.next.next
                return
            nodo_actual = nodo_actual.next
        # print(f"No existe el héroe {nombre} en la lista de héroes\n")

    
    def buscarHeroe(self, nombre):
        #se recorre toda la lista con un solo while  
        nodo_actual = self.head
        while nodo_actual != None:
            if nodo_actual.nombre == nombre:
                return nodo_actual
            nodo_actual = nodo_actual.next
        return None

    
    def mostarLista(self):
        node = self.head
        while node != None:
            if node.estado == "vivo":
                # Usar el método mostrar del héroe para una salida uniforme
                node.mostrar()
            node = node.next
        print("\n")

    
    def mostarListaFinal(self):
        node = self.head
        while node != None:
            print(f"heroe: {node.nombre} | Nivel: {node.nivel} | PV: {node.PV}/{node.PVmax} | Estado: {node.estado}")
            node = node.next

    
    def heroeGanador(self):
        # Este método no se usa en el flujo actual pero se mantiene por si acaso
        if self.head is None:
            return None
        ganador = self.head
        nodo_actual = self.head
        while nodo_actual.next != None:
            if nodo_actual.next.PV > ganador.PV:
                ganador = nodo_actual.next
            nodo_actual = nodo_actual.next
        return ganador
    
    def obtener_lista_heroes(self):
        """Retorna una lista de diccionarios con la información actual de todos los héroes."""
        heroes_data = []
        node = self.head
        while node is not None:
            heroes_data.append({
                "nombre": node.nombre,
                "pv": node.PV,
                "pv_max": node.PVmax,
                "nivel": node.nivel,
                "estado": node.estado
            })
            node = node.next
        return heroes_data

#rondas de batalla
class NodoTurno:
# ... [Clase NodoTurno permanece igual]
    def __init__(self, nombre = None, next = None):
        self.nombre = nombre
        self.next = next

class listaCircularTurnos:
# ... [Clase listaCircularTurnos permanece igual]
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head == None

    def agregarTurno(self, nombre_heroe):
        node = NodoTurno(nombre_heroe)
        if self.is_empty():
            self.head = node
            node.next = self.head
        else:
            cur = self.head
            # Mueva el puntero al nodo de cola (el que apunta a head)
            while cur.next is not self.head:
                cur = cur.next
            # El nodo de cola apunta al nuevo nodo
            cur.next = node
            # El nuevo nodo apunta al nodo principal original
            node.next = self.head
            # El nuevo nodo pasa a ser el nodo principal
            self.head = node
        self.size += 1

    def eliminarTurno(self, nombre_heroe):
        if self.is_empty():
            return
            
        cur = self.head
        pre = None
        
        # Caso: Solo queda un héroe y es el que se va a eliminar
        if cur.next == self.head and cur.nombre == nombre_heroe:
            self.head = None
            self.size = 0
            return
            
        # Caso: El nodo a eliminar es el head
        if cur.nombre == nombre_heroe:
            while cur.next != self.head:
                cur = cur.next
            cur.next = self.head.next
            self.head = self.head.next
            self.size -= 1
            return

        # Caso: Nodo intermedio
        # Buscar el nodo a eliminar
        temp_start = self.head.next
        pre = self.head
        while temp_start != self.head and temp_start.nombre != nombre_heroe:
            pre = temp_start
            temp_start = temp_start.next
        
        if temp_start.nombre == nombre_heroe:
            pre.next = temp_start.next
            self.size -= 1
            
    
    def mostarTurnos(self):
        if self.is_empty():
            return
        cur = self.head
        # Imprime el primero
        output = cur.nombre
        # Recorre los demás hasta volver al head
        cur = cur.next
        while cur != self.head:
            output += f" -> {cur.nombre}"
            cur = cur.next
        print(output)

    
    def quedaUltimoHeroe(self):
        return self.size == 1

#clase principal ctk
class JuegoGUI(ctk.CTk):
# ... [El resto del código de la clase JuegoGUI permanece igual]
    def __init__(self):
        super().__init__()
        #configuracion de la ventana 
        self.title("Batalla de Héroes 💫")
        self.geometry("1200x900")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=("#CDEDFD", "#1E2A35"))
        self.heroes = ListaHeroes()
        self.turnos = listaCircularTurnos()
        self.controlado = None #heroe que se controla
        self.defensa_base = {} # Diccionario para guardar la defensa original
        
        # Guardar el log de la partida
        self.log_content = [] 
        
        self.personajes_disponibles = {
            "Keren": {"vida": 6800, "ataque": 2000, "ataqueEsp": 0, "defensa": 1000},
            "Damian": {"vida": 7600, "ataque": 2500, "ataqueEsp": 0, "defensa": 1000},
            "Nicole": {"vida": 9600, "ataque": 1150, "ataqueEsp": 0, "defensa": 1000},
            "Joss": {"vida": 6800, "ataque": 1500, "ataqueEsp": 0, "defensa": 2500}
        }
        
        self.imagenes_heroes_ctk = {} # Almacenar objetos CTkImage
        self.cargar_imagenes_locales() # Cargar las imágenes desde archivos locales
        
        self.crear_pantalla_seleccion() #inicia con la pantalla de seleccion

    def cargar_imagenes_locales(self):
        """Carga las imágenes desde las rutas de archivo locales."""
        for nombre, ruta_archivo in IMAGE_PATHS.items():
            try:
                # 1. Verificar si el archivo existe (Importante para depuración local)
                if not os.path.exists(ruta_archivo):
                    print(f"ERROR: Archivo no encontrado en la ruta: {ruta_archivo}")
                    self.imagenes_heroes_ctk[nombre] = None
                    continue
                
                # 2. Cargar PIL Image desde la ruta de archivo
                pil_image = Image.open(ruta_archivo)
                
                # 3. Convertir PIL Image a CTkImage
                self.imagenes_heroes_ctk[nombre] = ctk.CTkImage(
                    pil_image, size=(80, 80)
                )
            except Exception as e:
                # En caso de error (p.ej., formato de imagen inválido)
                print(f"Error al cargar imagen local para {nombre} ({ruta_archivo}): {e}")
                self.imagenes_heroes_ctk[nombre] = None
        print("Imágenes locales cargadas. Asegúrate de que las rutas sean correctas.")
        
    #crear pantalla donde se selleciona el heroe
    def crear_pantalla_seleccion(self):
       # Recorre todos los widgets que hay dentro de la ventana y los elimina
        for w in self.winfo_children():
            w.destroy()
            
        # Resetear el log
        self.log_content = [] 
            
        titulo = ctk.CTkLabel(self, text="⚔️ Elige tu Héroe (serás quien controles) ⚔️", font=("Comic Sans MS", 28, "bold"), text_color=("#0B3C5D", "#CDEDFD"))
        titulo.pack(pady=20)
        
        # Frame principal para los botones
        frame = ctk.CTkFrame(self, fg_color=("#CDEDFD", "#1E2A35")) #tupla de colores
        frame.pack(pady=10)
        
        # Crea un botón por cada heroe con su imagen
        for nombre, stats in self.personajes_disponibles.items():
            
            # Obtener la imagen
            img_ctk = self.imagenes_heroes_ctk.get(nombre)
            
            # Crear el frame contenedor para el héroe
            hero_frame = ctk.CTkFrame(frame, fg_color=("#EAF6FF", "#263645"), corner_radius=12)
            hero_frame.pack(padx=15, pady=10, side="left", fill="y", expand=True)

            # Nombre y stats
            name_label = ctk.CTkLabel(hero_frame, text=nombre, font=("Comic Sans MS", 18, "bold"), text_color=("#0B3C5D", "#CDEDFD"))
            name_label.pack(pady=(10, 5))
            
            # Imagen (Si existe)
            if img_ctk:
                img_label = ctk.CTkLabel(hero_frame, image=img_ctk, text="")
                img_label.pack(pady=5)
            else:
                 # Mensaje de error si la imagen no se cargó
                img_label = ctk.CTkLabel(hero_frame, text="[IMAGEN FALTANTE]", text_color="red")
                img_label.pack(pady=5)


            # Stats
            stats_text = (
                f"PV: {stats['vida']}\n"
                f"ATK: {stats['ataque']}\n"
                f"DEF: {stats['defensa']}"
            )
            stats_label = ctk.CTkLabel(hero_frame, text=stats_text, font=("Comic Sans MS", 12), text_color=("#0B3C5D", "#CDEDFD"))
            stats_label.pack(pady=(5, 10))

            # Botón de selección
            ctk.CTkButton(hero_frame, text="Elegir", command=lambda n=nombre: self.seleccionar_jugador(n), 
                          fg_color=("#2C6E91", "#4CA3C7"), hover_color=("#1E5878", "#62B8D9"), 
                          text_color="white", corner_radius=8, width=150, height=35, 
                          font=("Comic Sans MS", 14, "bold")).pack(padx=10, pady=(0, 15))


     # lista de héroes y el orden de los turnos
    def seleccionar_jugador(self, nombre):
        self.controlado = nombre
        self.heroes = ListaHeroes()
        self.turnos = listaCircularTurnos()
        self.defensa_base = {}
        self.log_content = [] # Reiniciar el log al comenzar una nueva partida
        
        for n, s in self.personajes_disponibles.items():
            self.heroes.agregarHeroe(n, s["vida"], s["ataque"], s["ataqueEsp"], s["defensa"])
            self.defensa_base[n] = s["defensa"] # Guardar la defensa base
            
        # Asegurarse de que cada NodoHeroe tenga acceso a su defensa base
        current_hero = self.heroes.head
        while current_hero is not None:
            current_hero.defensa_base = self.defensa_base[current_hero.nombre]
            current_hero = current_hero.next
            
        nombres_en_orden = tuple(self.personajes_disponibles.keys())
        self.turnos = listaCircularTurnos()
        for n in reversed(nombres_en_orden):
            self.turnos.agregarTurno(n)
            
        self.crear_interfaz()
        
    #interfaz principal 
    def crear_interfaz(self):
        for w in self.winfo_children():
            w.destroy()
            
        # Contenedor principal para la estructura
        main_container = ctk.CTkFrame(self, fg_color=("#CDEDFD", "#1E2A35"))
        main_container.pack(pady=12, padx=20, fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(main_container, text=f"⚔️ Batalla - Controlas: {self.controlado} ⚔️", font=("Comic Sans MS", 24, "bold"), text_color=("#0B3C5D", "#CDEDFD"))
        titulo.pack(pady=12)
        
        # Frame de Información (Turno y Orden)
        self.frame_info = ctk.CTkFrame(main_container, fg_color=("#BBDDEE", "#22303C"), corner_radius=12)
        self.frame_info.pack(pady=8, padx=20, fill="x")
        
        self.label_turno_actual = ctk.CTkLabel(self.frame_info, text="Turno Actual: ", font=("Comic Sans MS", 16, "bold"), text_color=("#0B3C5D", "white"))
        self.label_turno_actual.pack(side="left", padx=10, pady=5)
        
        self.label_orden_turnos = ctk.CTkLabel(self.frame_info, text="Orden de Turnos: ", font=("Comic Sans MS", 14), text_color=("#0B3C5D", "white"))
        self.label_orden_turnos.pack(side="left", padx=10, pady=5)
        
        # Frame de Acciones (Botones)
        self.frame_acciones = ctk.CTkFrame(main_container, fg_color=("#CDEDFD", "#1E2A35"))
        self.frame_acciones.pack(pady=8)
        
        estilo_boton = {
            "corner_radius": 12,
            "fg_color": ("#2C6E91", "#4CA3C7"),
            "hover_color": ("#1E5878", "#62B8D9"),
            "text_color": "white",
            "font": ("Comic Sans MS", 14, "bold"),
            "width": 180,
            "height": 45
        }
        
        # **Ajuste para el botón de ataque - Ahora usará un color diferente cuando se selecciona para atacar**
        self.btn_atacar = ctk.CTkButton(self.frame_acciones, text="Atacar 💥", command=self.jugador_atacar_prompt, **estilo_boton)
        self.btn_curar = ctk.CTkButton(self.frame_acciones, text="Curar ✨", command=self.jugador_curar, **estilo_boton)
        self.btn_defender = ctk.CTkButton(self.frame_acciones, text="Defender 🛡️", command=self.jugador_defender, **estilo_boton)
        self.btn_pasar_turno = ctk.CTkButton(self.frame_acciones, text="Pasar Turno 🚶", command=self.jugador_pasar_turno, **estilo_boton)
        
        self.btn_atacar.grid(row=0, column=0, padx=8, pady=8)
        self.btn_curar.grid(row=0, column=1, padx=8, pady=8)
        self.btn_defender.grid(row=0, column=2, padx=8, pady=8)
        self.btn_pasar_turno.grid(row=0, column=3, padx=8, pady=8)
        
        # Frame de Selección de Objetivos (Inicialmente oculto)
        self.frame_objetivos = ctk.CTkFrame(main_container, fg_color=("#F0F8FF", "#304050"), corner_radius=12)
        self.label_seleccionar_objetivo = ctk.CTkLabel(self.frame_objetivos, text="🎯 Selecciona un objetivo:", font=("Comic Sans MS", 14, "bold"), text_color=("#0B3C5D", "white"))
        self.label_seleccionar_objetivo.pack(side="left", padx=10, pady=10)
        
        # Lo empaquetamos y lo ocultamos inmediatamente.
        self.frame_objetivos.pack(pady=5, padx=20, fill="x")
        self.frame_objetivos.pack_forget() 

        self.set_botones_estado(False)
        
        # Frame de Personaje y Stats
        self.frame_personaje = ctk.CTkFrame(main_container, fg_color=("#BBDDEE", "#22303C"), corner_radius=12)
        self.frame_personaje.pack(pady=8, padx=20, fill="x")

        # Imagen del personaje controlado
        img = self.imagenes_heroes_ctk.get(self.controlado)
        self.label_imagen = ctk.CTkLabel(self.frame_personaje, image=img, text="")
        self.label_imagen.grid(row=0, column=0, rowspan=4, padx=15, pady=10)

        # Labels de estadísticas (se actualizarán en self.actualizar_stats_personaje)
        self.label_nombre = ctk.CTkLabel(self.frame_personaje, text=f"{self.controlado}",
                                         font=("Comic Sans MS", 20, "bold"), text_color=("#0B3C5D", "white"))
        self.label_nombre.grid(row=0, column=1, sticky="w")

        self.label_nivel = ctk.CTkLabel(self.frame_personaje, text="Nivel:", font=("Comic Sans MS", 14), text_color=("#0B3C5D", "white"))
        self.label_nivel.grid(row=1, column=1, sticky="w")

        self.label_vida = ctk.CTkLabel(self.frame_personaje, text="PV:", font=("Comic Sans MS", 14), text_color=("#0B3C5D", "white"))
        self.label_vida.grid(row=2, column=1, sticky="w")
        
        self.label_ataque = ctk.CTkLabel(self.frame_personaje, text="ATK/DEF:", font=("Comic Sans MS", 14), text_color=("#0B3C5D", "white"))
        self.label_ataque.grid(row=3, column=1, sticky="w")
        
        # Separador y progreso de XP
        self.label_xp = ctk.CTkLabel(self.frame_personaje, text="XP: ", font=("Comic Sans MS", 14), text_color=("#0B3C5D", "white"))
        self.label_xp.grid(row=4, column=1, sticky="w", pady=(5, 10))
        
        self.progress_xp = ctk.CTkProgressBar(self.frame_personaje, orientation="horizontal", width=250, height=15)
        self.progress_xp.set(0) # Inicializar en 0
        self.progress_xp.grid(row=4, column=2, sticky="w", padx=10, pady=(5, 10))


        # Cuadro de texto para mensajes de Log
        self.texto = ctk.CTkTextbox(main_container, width=900, height=300, fg_color=("#EAF6FF", "#263645"), text_color=("#0B3C5D", "#CDEDFD"), font=("Courier", 13), wrap="word")
        self.texto.pack(pady=12, padx=20, fill="both", expand=True)

        self.actualizar_stats_personaje() # Muestra los stats iniciales
        self.actualizar_info_turnos()
        self.after(300, self.procesar_siguiente_turno)
        
    def actualizar_stats_personaje(self):
        """Actualiza todos los labels de estadísticas del héroe controlado."""
        heroe = self.heroes.buscarHeroe(self.controlado)
        if heroe:
            # Stats principales
            self.label_nivel.configure(text=f"Nivel: {heroe.nivel}")
            # Determinar el color de la vida
            pv_color = "red" if heroe.PV < heroe.PVmax * 0.2 else "yellow" if heroe.PV < heroe.PVmax * 0.5 else "green"
            # Configurar color de vida
            text_color_pv = pv_color if ctk.get_appearance_mode() == "Light" else "white" 
            if ctk.get_appearance_mode() == "Dark" and heroe.PV < heroe.PVmax * 0.5:
                 text_color_pv = pv_color 

            self.label_vida.configure(text=f"PV: {heroe.PV}/{heroe.PVmax}", text_color=text_color_pv)
            self.label_ataque.configure(text=f"Ataque: {heroe.ataque} | Defensa: {heroe.defensa}")
            
            # XP y barra de progreso
            progress_value = heroe.xp / heroe.xpmax if heroe.xpmax > 0 else 0
            self.progress_xp.set(progress_value)
            self.label_xp.configure(text=f"XP: {heroe.xp} / {heroe.xpmax}")

    #Activa o desactiva los botones
    def set_botones_estado(self, habilitar: bool):
        state = "normal" if habilitar else "disabled"
        
        # Restaurar color de botón de ataque al deshabilitar
        if not habilitar:
             self.btn_atacar.configure(fg_color=("#2C6E91", "#4CA3C7"), hover_color=("#1E5878", "#62B8D9"))
             
        self.btn_atacar.configure(state=state)
        self.btn_curar.configure(state=state)
        self.btn_defender.configure(state=state)
        self.btn_pasar_turno.configure(state=state)

    def ocultar_seleccion_objetivo(self):
        """Oculta el frame de selección de objetivo y limpia sus botones."""
        if self.frame_objetivos.winfo_ismapped():
            self.frame_objetivos.pack_forget()
            
        # Elimina todos los widgets excepto el label de título
        for widget in self.frame_objetivos.winfo_children():
            # Asegura que solo se eliminen los botones de objetivos, no el label de título
            if widget != self.label_seleccionar_objetivo:
                widget.destroy()
        
    # objetivos para atacar
    def mostrar_seleccion_objetivo(self, atacante_nombre):
        """Muestra los botones de los objetivos disponibles."""
        self.ocultar_seleccion_objetivo()
        current_hero_node = self.heroes.head
        objetivos_disponibles_nombres = []
        
        while current_hero_node is not None:
            # En una batalla de todos contra todos, el jugador solo puede atacar a los otros héroes vivos.
            if current_hero_node.nombre != atacante_nombre and current_hero_node.estado == "vivo":
                objetivos_disponibles_nombres.append(current_hero_node.nombre)
            current_hero_node = current_hero_node.next
            
        if not objetivos_disponibles_nombres:
            self.log("No hay objetivos válidos para atacar. Pasando turno automáticamente.")
            self.avanzar_turno_y_continuar()
            return

        # Vuelve a empaquetar el frame de objetivos
        self.frame_objetivos.pack(pady=5, padx=20, fill="x")
        
        for objetivo_nombre in objetivos_disponibles_nombres:
            btn = ctk.CTkButton(self.frame_objetivos, text=objetivo_nombre, 
                                command=lambda obj_n=objetivo_nombre: self.jugador_atacar(obj_n), 
                                fg_color=("#A34C4C", "#C76262"), hover_color=("#783939", "#D97B7B"), # Color de ataque (rojo)
                                text_color="white", corner_radius=8, width=120, height=35, 
                                font=("Comic Sans MS", 12, "bold"))
            # Usar grid para un mejor control del espaciado horizontal de los objetivos
            btn.pack(side="left", padx=5, pady=10)

    def ejecutar_y_capturar_prints(self, func, *args, **kwargs):
        """Ejecuta una función y redirige su salida (print) al log de la GUI."""
        from contextlib import redirect_stdout
        import io
        buf = io.StringIO()
        with redirect_stdout(buf):
            # Restaurar defensa si la función a ejecutar es 'atacar_objetivo' o 'curar'
            # Esta lógica ya está en jugador_curar/pasar_turno. Para el ataque, solo restaurar si estaba defendiendo
            if func.__name__ == 'atacar_objetivo' or func.__name__ == 'curar' or func.__name__ == 'pasarTurno':
                 heroe = self.heroes.buscarHeroe(self.controlado)
                 if heroe and heroe.defact:
                    # Usar la función de instancia, pero con redirect_stdout
                    # Usamos self.log directo para que no se duplique
                    self.log(f"La defensa de {heroe.nombre} vuelve a la normalidad ({heroe.defensa_base}).")
                    heroe.defensa = heroe.defensa_base
                    heroe.defact = False

            func(*args, **kwargs)
            
        salida = buf.getvalue()
        if salida:
            for linea in salida.splitlines():
                self.log(linea)

    # --- Acciones del Jugador ---

    def jugador_atacar_prompt(self):
        """Prepara el ataque, deshabilitando botones y mostrando objetivos."""
        if self.turnos.head is None or self.turnos.head.nombre != self.controlado:
            self.log("No es tu turno para atacar.")
            return
        her = self.heroes.buscarHeroe(self.controlado)
        if her is None or her.PV <= 0:
            self.log("No puedes atacar: estás debilitado.")
            return
            
        # Cambiar el color del botón para indicar que está activo/en espera
        self.btn_atacar.configure(fg_color=("#A00000", "#C76262"), hover_color=("#780000", "#D97B7B"))
        
        # Desactivar botones de acción y mostrar selección de objetivos
        self.set_botones_estado(False)
        self.mostrar_seleccion_objetivo(self.controlado)
        
    def jugador_atacar(self, objetivo_nombre):
        """Ejecuta la acción de atacar sobre el objetivo seleccionado."""
        
        # Restaurar color del botón de ataque inmediatamente
        self.btn_atacar.configure(fg_color=("#2C6E91", "#4CA3C7"), hover_color=("#1E5878", "#62B8D9"))

        self.ocultar_seleccion_objetivo()
        her = self.heroes.buscarHeroe(self.controlado)
        objetivo = self.heroes.buscarHeroe(objetivo_nombre)
        
        if her is None or her.PV <= 0 or objetivo is None or objetivo.PV <= 0:
            self.log("Error al procesar el ataque (héroe o objetivo inválido).")
            self.avanzar_turno_y_continuar()
            return
            
        # La lógica de restablecer_defensa ahora está en ejecutar_y_capturar_prints
        self.ejecutar_y_capturar_prints(her.atacar_objetivo, objetivo, self.turnos)
        self.avanzar_turno_y_continuar()

    def jugador_curar(self):
        """Ejecuta la acción de curar."""
        if self.turnos.head is None or self.turnos.head.nombre != self.controlado:
            self.log("No es tu turno para curar.")
            return
        her = self.heroes.buscarHeroe(self.controlado)
        if her is None or her.PV <= 0:
            self.log("No puedes curar: estás debilitado.")
            return
        
        # La lógica de restablecer_defensa ahora está en ejecutar_y_capturar_prints
        self.ocultar_seleccion_objetivo()
        self.ejecutar_y_capturar_prints(her.curar)
        self.avanzar_turno_y_continuar()

    def jugador_defender(self):
        """Ejecuta la acción de defender."""
        if self.turnos.head is None or self.turnos.head.nombre != self.controlado:
            self.log("No es tu turno para defender.")
            return
        her = self.heroes.buscarHeroe(self.controlado)
        if her is None or her.PV <= 0:
            self.log("No puedes defender: estás debilitado.")
            return
            
        self.ocultar_seleccion_objetivo()
        # Aseguramos que la defensa se restablezca si el jugador defiende y vuelve a defender.
        if her.defact:
            self.ejecutar_y_capturar_prints(her.restablecer_defensa)
            
        self.ejecutar_y_capturar_prints(her.defender)
        self.avanzar_turno_y_continuar()

    def jugador_pasar_turno(self):
        """Ejecuta la acción de pasar turno."""
        if self.turnos.head is None or self.turnos.head.nombre != self.controlado:
            self.log("No es tu turno para pasar.")
            return
        her = self.heroes.buscarHeroe(self.controlado)
        if her is None or her.PV <= 0:
            self.log("No puedes pasar el turno: estás debilitado.")
            return
            
        # La lógica de restablecer_defensa ahora está en ejecutar_y_capturar_prints
        self.ocultar_seleccion_objetivo()
        self.ejecutar_y_capturar_prints(her.pasarTurno)
        self.avanzar_turno_y_continuar()
    # ---------------------------

    def avanzar_turno_y_continuar(self):
        """Avanza al siguiente héroe en la lista circular de turnos y continúa el ciclo."""
        self.set_botones_estado(False)
        self.ocultar_seleccion_objetivo()
        
        # Si la lista de turnos no está vacía, avanzamos el head
        if self.turnos.head is not None:
            self.turnos.head = self.turnos.head.next
            
        self.actualizar_stats_personaje() # Actualizar stats del jugador por si subió de nivel
        self.mostrar_estado()
        self.actualizar_info_turnos()
        
        # Comprobar la defensa de todos los héroes y restaurarla antes de continuar
        current_hero_node = self.heroes.head
        while current_hero_node is not None:
            # Restauración de defensa para bots al final del turno
            if current_hero_node.defact and current_hero_node.nombre != self.controlado:
                 from contextlib import redirect_stdout
                 import io
                 buf = io.StringIO()
                 with redirect_stdout(buf):
                     current_hero_node.restablecer_defensa()
                 salida = buf.getvalue()
                 if salida:
                     for linea in salida.splitlines():
                         self.log(linea)

            current_hero_node = current_hero_node.next
            
        # IMPORTANTE: Comprobar fin de partida antes de llamar al siguiente turno
        if self.comprobar_fin_partida():
            return
            
        self.after(500, self.procesar_siguiente_turno)

    def procesar_siguiente_turno(self):
        """Gestiona la lógica del turno actual (jugador o bot)"""
        
        if self.turnos.is_empty():
            # Si la lista de turnos está vacía, el juego ya debería haber terminado,
            # pero lo revisamos por si acaso.
            self.comprobar_fin_partida()
            return
            
        if self.comprobar_fin_partida():
            return
            
        cur_turno_node = self.turnos.head
        nombre_actual = cur_turno_node.nombre
        her = self.heroes.buscarHeroe(nombre_actual)
        
        # Manejar héroes caídos o no encontrados
        if her is None or her.PV <= 0 or her.estado != "vivo":
            if her and her.PV <= 0:
                self.log(f"Saltando turno de {nombre_actual} (caído).")
            else:
                self.log(f"Saltando turno de {nombre_actual} (no encontrado).")
            # Asegurarse de que el héroe es eliminado de los turnos antes de continuar
            self.turnos.eliminarTurno(nombre_actual) 
            self.mostrar_estado()
            self.actualizar_info_turnos()
            
            # Comprobar la victoria/derrota después de eliminar un héroe
            if self.comprobar_fin_partida():
                return
                
            self.after(250, self.procesar_siguiente_turno) # Llamar de nuevo para el siguiente héroe
            return
            
        # --- Turno del Jugador ---
        if nombre_actual == self.controlado:
            # Restaurar defensa si estaba activa al final del turno del jugador
            if her.defact:
                self.ejecutar_y_capturar_prints(her.restablecer_defensa)
                
            self.log(f"\n--- ⭐️ ¡Es el turno de {nombre_actual} (tú)! Elige tu acción. ⭐️ ---")
            self.set_botones_estado(True)
            self.actualizar_info_turnos()
            return # Esperar la acción del jugador
            
        # --- Turno del Bot ---
        else:
            self.log(f"\n--- Turno de {nombre_actual}  🤖 ---")
            
            # Restaurar defensa si estaba activa (solo bots)
            if her.defact:
                # El restablecimiento de la defensa del bot se maneja en avanzar_turno_y_continuar para que dure 1 turno completo
                pass 
            
            # Lógica de acción automática para el bot
            eleccion = random.choices([1, 2, 3, 4], weights=[70, 15, 5, 10], k=1)[0] # Atacar: 70%, Curar: 15%, Pasar: 5%, Defender: 10%
            
            if eleccion == 1: # Atacar
                objetivo_bot = self.seleccionar_objetivo_bot(her.nombre)
                if objetivo_bot:
                    self.ejecutar_y_capturar_prints(her.atacar_objetivo, objetivo_bot, self.turnos)
                else:
                    self.log(f"{her.nombre} intentó atacar, pero no encontró objetivos. Pasa el turno.")
                    self.ejecutar_y_capturar_prints(her.pasarTurno)
            elif eleccion == 2: # Curar (si PV no es max)
                if her.PV < her.PVmax * 0.8:
                    self.ejecutar_y_capturar_prints(her.curar)
                else:
                    self.log(f"{her.nombre} decidió no curarse (Vida alta). Ataca en su lugar.")
                    objetivo_bot = self.seleccionar_objetivo_bot(her.nombre)
                    if objetivo_bot:
                        self.ejecutar_y_capturar_prints(her.atacar_objetivo, objetivo_bot, self.turnos)
                    else:
                        self.ejecutar_y_capturar_prints(her.pasarTurno)
            elif eleccion == 3: # Pasar Turno
                self.ejecutar_y_capturar_prints(her.pasarTurno)
            elif eleccion == 4: # Defender
                self.ejecutar_y_capturar_prints(her.defender)
                
            # Avanzar el turno
            if self.turnos.head is not None:
                self.turnos.head = self.turnos.head.next
            
            self.actualizar_stats_personaje() # Por si un bot subió de nivel
            self.mostrar_estado()
            self.actualizar_info_turnos()
            
            # Comprobar la victoria/derrota
            if self.comprobar_fin_partida():
                return
                
            self.after(1000, self.procesar_siguiente_turno) # Esperar 1 segundo y pasar al siguiente turno

    def seleccionar_objetivo_bot(self, atacante_nombre):
        """Selecciona un objetivo aleatorio que esté vivo y no sea el atacante."""
        current_hero_node = self.heroes.head
        posibles_objetivos = []
        
        while current_hero_node is not None:
            if current_hero_node.nombre != atacante_nombre and current_hero_node.estado == "vivo":
                posibles_objetivos.append(current_hero_node)
            current_hero_node = current_hero_node.next
            
        if not posibles_objetivos:
            return None
            
        # Elegir un héroe al azar de la lista de posibles objetivos
        return random.choice(posibles_objetivos)

    def comprobar_fin_partida(self):
        """
        Verifica las condiciones de victoria o derrota.
        Termina la partida si el héroe controlado muere o si es el único vivo.
        """
        vivos_count = 0
        jugador_vivo = False
        jugador_node = self.heroes.buscarHeroe(self.controlado)
        
        if jugador_node and jugador_node.PV > 0 and jugador_node.estado == "vivo":
            jugador_vivo = True
            
        nodo = self.heroes.head
        while nodo is not None:
            if nodo.PV > 0 and nodo.estado == "vivo":
                vivos_count += 1
            nodo = nodo.next
            
        partida_terminada = False
        
        # --- CONDICIÓN 1: DERROTA (El jugador está muerto) ---
        if not jugador_vivo:
            partida_terminada = True
            self.set_botones_estado(False)
            self.log(f"💀 TU PERSONAJE ({self.controlado}) HA SIDO ELIMINADO 💀")
            self.mostrar_pantalla_final("Derrota")
        
        # --- CONDICIÓN 2: VICTORIA (Solo queda el jugador vivo) ---
        elif jugador_vivo and vivos_count == 1:
            partida_terminada = True
            self.set_botones_estado(False)
            self.log("🎉 ¡FELICIDADES! ¡ERES EL ÚNICO HÉROE EN PIE! 🎉")
            self.mostrar_pantalla_final("Victoria")

        # --- CONDICIÓN 3: EMPATE / OTRO ---
        elif vivos_count <= 1 and not jugador_vivo:
             # Este caso cubre el 0 vivos (empate) si por alguna razón falló el chequeo anterior.
            partida_terminada = True
            self.set_botones_estado(False)
            self.log("La batalla terminó sin ganadores claros (Todos caídos o solo queda un bot).")
            self.mostrar_pantalla_final("Empate/Sin ganador")
            
        return partida_terminada
        
    #estado de los heroes en el cuadro de texto
    def mostrar_estado(self):
        """Muestra el estado actual de los héroes en el log."""
        from contextlib import redirect_stdout
        import io
        buf = io.StringIO()
        with redirect_stdout(buf):
            if hasattr(self.heroes, "mostarLista"):
                self.heroes.mostarLista()
        salida = buf.getvalue()
        
        self.log("\n--- ESTADO ACTUAL DE LOS HÉROES ---")
        if salida:
            for linea in salida.splitlines():
                self.log(linea)
        self.log("-----------------------------------\n")

    #actualizar turnos en la interfaz
    def actualizar_info_turnos(self):
        """Actualiza el label del turno actual y la lista de turnos."""
        
        # 1. Actualizar stats del héroe controlado
        self.actualizar_stats_personaje()
        
        # 2. Actualizar información de turnos
        if self.turnos.is_empty():
            self.label_turno_actual.configure(text="Turno Actual: Nadie")
            self.label_orden_turnos.configure(text="Orden de Turnos: Vacío")
            return
            
        turno_actual_nombre = self.turnos.head.nombre
        self.label_turno_actual.configure(text=f"Turno Actual: {turno_actual_nombre}")
        
        # Cadena de orden de turnos
        orden_str_temp = ""
        current = self.turnos.head
        is_first = True
        
        # Evitar bucle infinito si la lista es circular pero el head es None
        if current is None:
             self.label_orden_turnos.configure(text="Orden de Turnos: Vacío")
             return
             
        # Recorrer la lista circular una vez
        while True:
            heroe_en_lista = self.heroes.buscarHeroe(current.nombre)
            # Solo mostrar héroes que estén vivos y sean parte de la lista de turnos
            if heroe_en_lista and heroe_en_lista.estado == "vivo":
                if not is_first:
                    orden_str_temp += " -> "
                orden_str_temp += current.nombre
                is_first = False
                
            current = current.next
            if current == self.turnos.head:
                break
                
        self.label_orden_turnos.configure(text=f"Orden de Turnos: {orden_str_temp}")

    def log(self, mensaje):
        """Añade un mensaje al cuadro de texto de log y lo guarda."""
        self.log_content.append(mensaje) # Guarda el mensaje
        # Si el widget de texto existe, lo actualiza
        if hasattr(self, 'texto') and self.texto.winfo_exists():
            self.texto.insert("end", mensaje + "\n")
            self.texto.see("end")
        
    #pantalla de resultado
    def mostrar_pantalla_final(self, resultado):
        """Muestra la pantalla final de la partida, incluyendo el top 3."""
        for w in self.winfo_children():
            w.destroy()
            
        if resultado == "Victoria":
            mensaje = "🎉 ¡FELICITACIONES! HAS GANADO LA BATALLA! 🎉"
            color = "#0B5D0B" # Verde oscuro
        elif resultado == "Derrota":
            mensaje = "💀 FUISTE ELIMINADO... MEJOR SUERTE LA PRÓXIMA 💀"
            color = "#A00000" # Rojo oscuro
        else:
             mensaje = "La batalla ha terminado."
             color = "#2C6E91"

        final_label = ctk.CTkLabel(self, text=mensaje, font=("Comic Sans MS", 30, "bold"), text_color=color)
        final_label.pack(pady=30)
        
        # --- Obtener y calcular el Top 3 ---
        all_heroes = self.heroes.obtener_lista_heroes()
        
        # 1. Ordenar héroes por PV (descendente)
        # Los héroes con PV <= 0 se ponen al final de la lista
        def sort_key(hero):
            return hero['pv'] if hero['pv'] > 0 else -1
            
        heroes_ordenados = sorted(all_heroes, key=sort_key, reverse=True)
        top_3 = heroes_ordenados[:3]
        
        # 2. Formatear el Top 3
        top_3_text = "🏆 CLASIFICACIÓN FINAL (TOP 3) 🏆\n"
        for i, hero in enumerate(top_3):
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            estado_pv = f"PV: {hero['pv']}/{hero['pv_max']}"
            if hero['estado'] == 'muerto':
                estado_pv = f"CAÍDO ({hero['pv']}/{hero['pv_max']})"
            
            top_3_text += f"{emoji} {hero['nombre']} | Nivel {hero['nivel']} | {estado_pv}\n"

        
        # Frame y Textbox para el Top 3
        top_frame = ctk.CTkFrame(self, fg_color=("#BBDDEE", "#22303C"), corner_radius=12)
        top_frame.pack(pady=10, padx=20, fill="x")
        
        top_label = ctk.CTkLabel(top_frame, text=top_3_text, justify="left",
                                 font=("Courier", 16, "bold"), text_color=("#0B3C5D", "white"))
        top_label.pack(padx=15, pady=15)
        
        # Cuadro de texto para el log completo
        self.texto_final = ctk.CTkTextbox(self, width=800, height=300, 
                                        fg_color=("#EAF6FF", "#263645"), text_color=("#0B3C5D", "#CDEDFD"), 
                                        font=("Courier", 13), wrap="word")
        self.texto_final.pack(pady=10, padx=20, fill="x")
        
        # Mostrar el log de la partida guardado en self.log_content
        self.texto_final.insert("end", "--- REGISTRO DE EVENTOS DE LA BATALLA ---\n")
        self.texto_final.insert("end", "\n".join(self.log_content))
        self.texto_final.insert("end", "\n--------------------------------------\n")
        
        # Botón de volver al inicio
        volver_boton = ctk.CTkButton(self, text="Volver al inicio", command=self.crear_pantalla_seleccion, 
                                     fg_color=("#2C6E91", "#4CA3C7"), hover_color=("#1E5878", "#62B8D9"), 
                                     text_color="white", corner_radius=12, width=200, height=50, 
                                     font=("Comic Sans MS", 18, "bold"))
        volver_boton.pack(pady=30)

if __name__ == "__main__":
    app = JuegoGUI()
    app.mainloop()