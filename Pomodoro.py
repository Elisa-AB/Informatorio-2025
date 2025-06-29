import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import time
import winsound

materias = ["Diseño de Sistemas", "Bases de Datos", "Complejidad", "Comunicación"]
pomodoro_counts = {m: 0 for m in materias}

# Valores iniciales en minutos
estudio_minutos = 25
descanso_minutos = 5

temporizador_actual = estudio_minutos * 60
modo_estudio = True
pausado = False
ventana_temporizador = None
ventana_config = None

# Funciones

def actualizar_reloj():
    hora_actual = time.strftime("%H:%M:%S")
    reloj.config(text=hora_actual)
    app.after(1000, actualizar_reloj)

def reproducir_sonido():
    try:
        winsound.Beep(1000, 300)
    except:
        pass

def actualizar_tiempo():
    global temporizador_actual, modo_estudio

    if pausado or not ventana_temporizador:
        return

    minutos = temporizador_actual // 60
    segundos = temporizador_actual % 60
    tiempo_str = f"{minutos:02d}:{segundos:02d}"
    label_tiempo.config(text=tiempo_str)

    if temporizador_actual > 0:
        temporizador_actual -= 1
        ventana_temporizador.after(1000, actualizar_tiempo)
    else:
        reproducir_sonido()
        if modo_estudio:
            # Se suma el pomodoro completado internamente pero no se muestra
            materia = var_materia.get()
            if materia in pomodoro_counts:
                pomodoro_counts[materia] += 1
            modo_estudio = False
            temporizador_actual = descanso_minutos * 60
            label_mensaje.config(text="Tomate un descanso, lo mereces")
            ventana_temporizador.config(bg="#F5DEB3")
            label_tiempo.config(bg="#F5DEB3")
            label_mensaje.config(bg="#F5DEB3")
        else:
            modo_estudio = True
            temporizador_actual = estudio_minutos * 60
            label_mensaje.config(text="Hora de estudiar")
            ventana_temporizador.config(bg="#ADD8E6")
            label_tiempo.config(bg="#ADD8E6")
            label_mensaje.config(bg="#ADD8E6")
        actualizar_tiempo()

def iniciar_temporizador():
    global modo_estudio, temporizador_actual, pausado, ventana_temporizador
    cerrar_temporizador()

    modo_estudio = True
    temporizador_actual = estudio_minutos * 60
    pausado = False

    ventana_temporizador = tk.Toplevel(app)
    ventana_temporizador.title(var_materia.get())
    ventana_temporizador.geometry("300x250")
    ventana_temporizador.config(bg="#ADD8E6")
    ventana_temporizador.protocol("WM_DELETE_WINDOW", cerrar_temporizador)

    global label_tiempo, label_mensaje
    label_tiempo = tk.Label(ventana_temporizador, text=f"{estudio_minutos:02d}:00", font=("Arial", 40), bg="#ADD8E6", fg="black")
    label_tiempo.pack(pady=5)

    label_mensaje = tk.Label(ventana_temporizador, text="Hora de estudiar", font=("Arial", 14), bg="#ADD8E6", fg="black")
    label_mensaje.pack(pady=10)

    # Frame para botones
    boton_frame = tk.Frame(ventana_temporizador, bg="#ADD8E6")
    boton_frame.pack(pady=10)

    btn_pausar = tk.Button(boton_frame, text="Pausar", command=pausar_reanudar, bg="khaki", fg="black")
    btn_pausar.pack(side="left", padx=5)

    btn_reiniciar = tk.Button(boton_frame, text="Reiniciar", command=iniciar_temporizador, bg="lightgreen", fg="black")
    btn_reiniciar.pack(side="left", padx=5)

    actualizar_tiempo()

def cerrar_temporizador():
    global ventana_temporizador
    if ventana_temporizador:
        ventana_temporizador.destroy()
        ventana_temporizador = None

def pausar_reanudar():
    global pausado
    pausado = not pausado
    if not pausado:
        actualizar_tiempo()

def actualizar_menu():
    menu_materias['menu'].delete(0, 'end')
    for m in materias:
        menu_materias['menu'].add_command(label=m, command=tk._setit(var_materia, m))
    if materias:
        var_materia.set(materias[0])
    else:
        var_materia.set("")

def agregar_materia():
    nueva = simpledialog.askstring("Agregar materia", "Ingrese el nombre de la materia:")
    if nueva:
        if nueva not in materias:
            materias.append(nueva)
            pomodoro_counts[nueva] = 0
            actualizar_menu()
        else:
            messagebox.showinfo("Materia duplicada", "La materia ya existe")

def eliminar_materia():
    seleccionada = var_materia.get()
    if seleccionada in materias:
        materias.remove(seleccionada)
        pomodoro_counts.pop(seleccionada, None)
        actualizar_menu()
    else:
        messagebox.showwarning("!!", "No seleccionó ninguna materia")

def abrir_configuracion():
    global ventana_config
    if ventana_config and ventana_config.winfo_exists():
        ventana_config.lift()
        return

    ventana_config = tk.Toplevel(app)
    ventana_config.title("Configuración")
    ventana_config.geometry("300x300")

    main_frame = tk.Frame(ventana_config)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame_interno = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")

    tk.Label(frame_interno, text="Tiempo de estudio (minutos):").pack(pady=(10, 0))
    tiempo_estudio_var = tk.IntVar(value=estudio_minutos)
    estudio_options = list(range(5, 61, 5))  # 5,10,...60
    estudio_menu = ttk.Combobox(frame_interno, values=estudio_options, textvariable=tiempo_estudio_var, state="readonly")
    estudio_menu.pack()

    tk.Label(frame_interno, text="Tiempo de descanso (minutos):").pack(pady=(20, 0))
    tiempo_descanso_var = tk.IntVar(value=descanso_minutos)
    descanso_options = list(range(1, 11))  # 1 a 10
    descanso_menu = ttk.Combobox(frame_interno, values=descanso_options, textvariable=tiempo_descanso_var, state="readonly")
    descanso_menu.pack()

    def aplicar_config():
        global estudio_minutos, descanso_minutos, temporizador_actual
        estudio_minutos = tiempo_estudio_var.get()
        descanso_minutos = tiempo_descanso_var.get()
        temporizador_actual = estudio_minutos * 60
        messagebox.showinfo("Configuración", "Configuración guardada con éxito.")
        ventana_config.destroy()

    btn_ok = tk.Button(frame_interno, text="OK", command=aplicar_config)
    btn_ok.pack(pady=20)

def agregar_tarea():
    tarea = simpledialog.askstring("Agregar pregunta", "Ingrese la pregunta:")
    if tarea:
        listbox_tareas.insert(tk.END, tarea)

def eliminar_tarea():
    seleccion = listbox_tareas.curselection()
    if seleccion:
        listbox_tareas.delete(seleccion[0])
    else:
        messagebox.showwarning("¡Atención!", "Seleccione una pregunta para eliminar.")

def actualizar_lista_tareas():
    pass  # Por ahora no hace nada

def materia_cambiada(*args):
    actualizar_lista_tareas()

# Ventana principal
app = tk.Tk()
app.title("Pomodoro Timer")
app.geometry("500x600")
app.configure(background="lightblue")

frame_central = tk.Frame(app, bg="lightblue")
frame_central.pack(expand=True, fill="both")

frame_inferior = tk.Frame(app, bg="lightblue")
frame_inferior.pack(fill="x", side="bottom")

# Menú desplegable de materias
var_materia = tk.StringVar()
var_materia.set(materias[0])
var_materia.trace_add("write", materia_cambiada)

label = tk.Label(frame_central, text="Seleccioná la materia que querés estudiar:", font=("Arial", 12), bg="lightblue", fg="black")
label.pack(pady=(20, 5))

menu_materias = tk.OptionMenu(frame_central, var_materia, *materias)
menu_materias.config(bg="lightgray", fg="black", font=("Arial", 12))
menu_materias['menu'].config(bg="lightgray", fg="black", activebackground="white", activeforeground="black")
menu_materias.pack(pady=5)

# Botones de acción para materias
btn_frame = tk.Frame(frame_central, bg="lightblue")
btn_frame.pack(pady=(5, 10))

btn_agregar = tk.Button(btn_frame, text="Agregar materia", command=agregar_materia, bg="lightgreen", fg="black")
btn_agregar.pack(side="left", padx=5)

btn_eliminar = tk.Button(btn_frame, text="Eliminar materia", command=eliminar_materia, bg="tomato", fg="black")
btn_eliminar.pack(side="left", padx=5)

# Botón para iniciar temporizador
btn_comenzar = tk.Button(frame_central, text="Comenzar", command=iniciar_temporizador, bg="skyblue", fg="black")
btn_comenzar.pack(pady=5)

# Botón configuración con engranaje unicode ⚙
btn_config = tk.Button(frame_central, text="⚙ Configuración", command=abrir_configuracion, bg="lightgray", fg="black")
btn_config.pack(pady=5)

# Lista de tareas (preguntas)
label_tareas = tk.Label(frame_central, text="Preguntas surgidas en el estudio:", font=("Arial", 12), bg="lightblue", fg="black")
label_tareas.pack(pady=(20, 5))

# Frame para listbox + scrollbar
frame_tareas = tk.Frame(frame_central)
frame_tareas.pack(expand=True, fill="both", padx=10, pady=5)

scrollbar_tareas = tk.Scrollbar(frame_tareas)
scrollbar_tareas.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tareas = tk.Listbox(frame_tareas, yscrollcommand=scrollbar_tareas.set)
listbox_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_tareas.config(command=listbox_tareas.yview)

# Botones para lista de tareas
btn_tareas_frame = tk.Frame(frame_central, bg="lightblue")
btn_tareas_frame.pack(pady=10)

btn_agregar_tarea = tk.Button(btn_tareas_frame, text="Agregar pregunta", command=agregar_tarea, bg="lightgreen", fg="black")
btn_agregar_tarea.pack(side="left", padx=5)

btn_eliminar_tarea = tk.Button(btn_tareas_frame, text="Eliminar pregunta", command=eliminar_tarea, bg="tomato", fg="black")
btn_eliminar_tarea.pack(side="left", padx=5)

# Reloj simple abajo
reloj = tk.Label(frame_inferior, font=("Arial", 12), bg="lightblue", fg="black")
reloj.pack(side="left", padx=10, pady=10)

actualizar_reloj()
actualizar_lista_tareas()
actualizar_menu()

app.mainloop()
