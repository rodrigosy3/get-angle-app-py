import tkinter as tk
from math import degrees, sqrt, atan, radians
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

# TAMAÑO DE VENTANA
width = 960
height = 570

# COLOR FONDOS
BG = "#F0F4F8"
BG_PANEL_DATA = "#496989"
BG_ENTRY_DATA = "#FFFFFF"
BG_LABEL_RESULT = "#DDE6ED"
BG_BTN = "#83B7E3"
BG_BTN_HOVER = "#B0D4EF"

# COLOR TEXTOS
LABEL_TITLE = "#002147"
LABEL_DATA = "#FFFFFF"
LABEL_RESULT_TEXT = "#002147"
BTN_TXT = "#FFFFFF"

def centrar_ventana(window, app_width, app_height):
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()
    x = int((window_width / 2) - (app_width / 2))
    y = int((window_height / 2) - (app_height / 2))
    
    return window.geometry(f"{app_width}x{app_height}+{x}+{y}")

def get_max_distance(initial_velocity, initial_height, final_height):
    try:
        gravity = 9.81
        max_distance = (1 + sqrt(1-(4*((gravity)/(initial_velocity**2))*(final_height-initial_height))))/(2*((gravity)/(initial_velocity**2)))
        
        return max_distance
    
    except Exception as e:
        messagebox.showerror("Error", f"Por favor ingrese valores numéricos positivos.\nError: {e}")
        
def get_max_distance_result(label_result, initial_velocity, initial_height, final_height):
    try:
        max_distance = get_max_distance(initial_velocity, initial_height, final_height)
        
        label_result.config(text=f"{max_distance} m")
    
    except Exception as e:
        messagebox.showerror("Error", f"Por favor ingrese valores válidos.\n{e}")
    
def get_angle(initial_velocity, initial_height, final_height, distance):
    try:
        max_distance = get_max_distance(initial_velocity, initial_height, final_height)
        
        if distance > max_distance or distance <= 0:
            messagebox.showerror("Error", f"Por favor ingrese una distancia mayor a 0 y menor a: \n{max_distance} m")
        
        else:  
            gravity = 9.81
            
            x_1 = (distance + sqrt((distance**2)-(4*(1/2)*gravity*((distance**2)/(initial_velocity**2))*((1/2*gravity*((distance**2)/(initial_velocity**2))) - initial_height + final_height)))) / (gravity*((distance**2)/(initial_velocity**2)))
            angle_1 = degrees(atan(x_1))
            
            x_2 = (distance - sqrt((distance**2)-(4*(1/2)*gravity*((distance**2)/(initial_velocity**2))*((1/2*gravity*((distance**2)/(initial_velocity**2))) - initial_height + final_height)))) / (gravity*((distance**2)/(initial_velocity**2)))
            angle_2 = degrees(atan(x_2))
            
            if angle_1 < 45 and angle_1 > 0:
                angle = angle_1
            else:
                angle = angle_2
            
            return angle
    
    except Exception as e:
        messagebox.showerror("Error", f"Por favor ingrese valores válidos.\n{e}")
        
def get_angle_result(label_result, initial_velocity, initial_height, final_height, distance, panel_graphic,):
    try:
        angle = get_angle(initial_velocity, initial_height, final_height, distance)
        angle_radians = radians(angle)
        
        label_result.config(text=f"Ángulo de lanzamiento óptimo: \n{angle}°")
        draw_trajectory(panel_graphic, initial_velocity, initial_height, angle_radians)
        
    except Exception as e:
        messagebox.showerror("Error", f"Por favor ingrese valores válidos.\n{e}")

def reset_data(entry_data_velocity, entry_data_distance, entry_data_height_initial, entry_data_height_final, label_result_max_distance, label_result_angle):
    entry_data_velocity.delete(0, tk.END)
    entry_data_distance.delete(0, tk.END)
    entry_data_height_initial.delete(0, tk.END)
    entry_data_height_final.delete(0, tk.END)
    
    entry_data_height_initial.insert(0, "0.0")
    entry_data_height_final.insert(0, "0.0")
    
    label_result_max_distance.config(text="- m")
    label_result_angle.config(text="-°")
    
def draw_trajectory(panel_graphic, initial_velocity, initial_height, angle):
    gravity = 9.81
    t_flight = (initial_velocity * np.sin(angle) + np.sqrt((initial_velocity * np.sin(angle))**2 + 2 * gravity * initial_height)) / gravity
    t = np.linspace(0, t_flight, num=500)
    
    x = initial_velocity * np.cos(angle) * t
    y = initial_height + initial_velocity * np.sin(angle) * t - 0.5 * gravity * t**2
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Altura (m)')
    ax.set_title('Trayectoria del Proyectil')
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=panel_graphic)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)



class AppGetAngle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.paneles()
        self.content_panel_left()
        
    def config_window(self):
        self.title = "Calculo del Ángulo de Lanzamiento"
        self.width = width
        self.height = height
        self.background = BG
        centrar_ventana(self, self.width, self.height)
    
    def paneles(self):
        self.panel_datos = tk.Frame(self, bg=BG_PANEL_DATA, width=250)
        self.panel_datos.pack(side=tk.LEFT, fill="both", expand=False)
        
        self.panel_graphic = tk.Frame(self, bg=BG_ENTRY_DATA)
        self.panel_graphic.pack(side=tk.RIGHT, fill="both", expand=True, padx=30, pady=30)
        draw_trajectory(self.panel_graphic, 0, 0, 0)
        
    def on_enter(self, event, button):
            button.config(bg=BG_BTN_HOVER, fg=BTN_TXT)
    
    def on_leave(self, event, button):
            button.config(bg=BG_BTN, fg=BTN_TXT)
            
    def content_panel_left(self):
        self.labelTitle = tk.Label(self.panel_datos, text="CALCULAR ÁNGULO", font=("Arial", 16, "bold"), fg=LABEL_TITLE, bg=BG_PANEL_DATA)
        self.labelTitle.grid(row=0, columnspan=3, ipady=15, sticky="ew")
        
        #VELOCIDAD INICIAL
        self.labelDataVelocity = tk.Label(self.panel_datos, text="Velocidad inicial: ", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataVelocity.grid(row=1, column=0, padx=(10, 0), sticky="w")
        self.entryDataVelocity = tk.Entry(self.panel_datos, relief="flat", bg=BG_ENTRY_DATA, justify="center")
        self.entryDataVelocity.grid(row=1, column=1)
        self.labelDataVelocityMagnitude = tk.Label(self.panel_datos, text="m/s", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataVelocityMagnitude.grid(row=1, column=2, padx=(0, 10), sticky="w")
        
        #ALTURA INICIAL
        # height_initial = tk.DoubleVar()
        self.labelDataHeightInitial = tk.Label(self.panel_datos, text="Altura inicial (opcional): ", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataHeightInitial.grid(row=2, column=0, padx=(10, 0), sticky="w")
        self.entryDataHeightInitial = tk.Entry(self.panel_datos, relief="flat", bg=BG_ENTRY_DATA, justify="center")
        self.entryDataHeightInitial.insert(0, "0.0")
        self.entryDataHeightInitial.grid(row=2, column=1)
        self.labelDataHeightInitialMagnitude = tk.Label(self.panel_datos, text="m", fg=LABEL_DATA, bg=BG_PANEL_DATA, justify="left")
        self.labelDataHeightInitialMagnitude.grid(row=2, column=2, padx=(0, 10), sticky="w")
        
        #ALTURA FINAL
        # height_initial = tk.DoubleVar()
        self.labelDataHeightFinal = tk.Label(self.panel_datos, text="Altura final (opcional): ", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataHeightFinal.grid(row=3, column=0, padx=(10, 0), sticky="w")
        self.entryDataHeightFinal = tk.Entry(self.panel_datos, relief="flat", bg=BG_ENTRY_DATA, justify="center")
        self.entryDataHeightFinal.insert(0, "0.0")
        self.entryDataHeightFinal.grid(row=3, column=1)
        self.labelDataHeightFinalMagnitude = tk.Label(self.panel_datos, text="m", fg=LABEL_DATA, bg=BG_PANEL_DATA, justify="left")
        self.labelDataHeightFinalMagnitude.grid(row=3, column=2, padx=(0, 10), sticky="w")
        
        #BOTÓN CALCULAR DISTANCIA MÁXIMA
        self.buttonMaxDistance = tk.Button(self.panel_datos, text="Calcular máxima distancia a esta velocidad", fg=BTN_TXT, bg=BG_BTN, relief="flat", command=lambda: get_max_distance_result(self.labelResultMaxDistance, float(self.entryDataVelocity.get()), float(self.entryDataHeightInitial.get()), float(self.entryDataHeightFinal.get())))
        self.buttonMaxDistance.grid(row=4, columnspan=3, pady=(10, 5), padx=10)
        self.buttonMaxDistance.bind("<Enter>", lambda event: self.on_enter(event, self.buttonMaxDistance))
        self.buttonMaxDistance.bind("<Leave>", lambda event: self.on_leave(event, self.buttonMaxDistance))
        
        #RESULTADO DE MÁXIMA DISTANCIA
        self.labelResultMaxDistance = tk.Label(self.panel_datos, text="- m", fg=LABEL_RESULT_TEXT, font=("Arial", 12, "bold"))
        self.labelResultMaxDistance.grid(row=5, columnspan=3, sticky="nsew", pady=(0, 30), padx=20)
        
        #DISTANCIA A ALCANZAR
        self.labelDataDistance = tk.Label(self.panel_datos, text="Distancia esperada: ", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataDistance.grid(row=6, column=0, padx=(10, 0), sticky="w")
        self.entryDataDistance = tk.Entry(self.panel_datos, relief="flat", bg=BG_ENTRY_DATA, justify="center")
        self.entryDataDistance.grid(row=6, column=1, sticky="w")
        self.labelDataDistanceMagnitude = tk.Label(self.panel_datos, text="m", fg=LABEL_DATA, bg=BG_PANEL_DATA)
        self.labelDataDistanceMagnitude.grid(row=6, column=2, padx=(0, 10), sticky="w")
        
        #CONTENEDOR DE BOTONES
        self.frameButtonContainer = tk.Frame(self.panel_datos, bg=BG_PANEL_DATA)
        self.frameButtonContainer.grid(row=8, columnspan=3, pady=15)
        
        #BOTÓN REESTABLECER
        self.buttonReset = tk.Button(self.frameButtonContainer, text="Reestablecer datos", fg=BTN_TXT, bg=BG_BTN, relief="flat", command=lambda: reset_data(self.entryDataVelocity, self.entryDataDistance, self.entryDataHeightInitial, self.entryDataHeightFinal, self.labelResultMaxDistance, self.labelResultAngle))
        self.buttonReset.grid(row=1, column=0, padx=10)
        self.buttonReset.bind("<Enter>", lambda event: self.on_enter(event, self.buttonReset))
        self.buttonReset.bind("<Leave>", lambda event: self.on_leave(event, self.buttonReset))
        
        #BOTÓN CALCULAR
        self.buttonCalculate = tk.Button(self.frameButtonContainer, text="Calcular", fg=BTN_TXT, bg=BG_BTN, relief="flat", command=lambda: get_angle_result(self.labelResultAngle, float(self.entryDataVelocity.get()), float(self.entryDataHeightInitial.get()), float(self.entryDataHeightFinal.get()), float(self.entryDataDistance.get()), self.panel_graphic))
        self.buttonCalculate.grid(row=1, column=1, padx=10)
        self.buttonCalculate.bind("<Enter>", lambda event: self.on_enter(event, self.buttonCalculate))
        self.buttonCalculate.bind("<Leave>", lambda event: self.on_leave(event, self.buttonCalculate))
        
        #RESULTADO DEL ÁNGULO
        self.labelResultAngle = tk.Label(self.panel_datos, text="-°", fg=LABEL_RESULT_TEXT, font=("Arial", 12, "bold"))
        self.labelResultAngle.grid(row=7, columnspan=3, sticky="nsew", pady=10, padx=20)

app = AppGetAngle()
app.mainloop()