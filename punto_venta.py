import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

tree = ttk.Treeview
# DONDE SE GUARDARA VENDEDORES
DATA_FILE = "vendedores.txt"
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"
# FUNCION PARA AGREGAR VENDEDORES
def agregar_vendedores():

    def agregar():
        vnombre = nombre.get()
        vtelefono = telefono.get()
        vemail = email.get()

        # Verificar que todos los campos estén completos
        if not vnombre or not vtelefono or not vemail:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            with open(DATA_FILE, "a") as file:
                file.write(f"{vnombre},{vtelefono},{vemail}\n")
                messagebox.showinfo("Vendedor Agregado", "El vendedor fue agregado exitosamente")
                #Cerrar ventana automaticamente
                window_agregar_vendedor.destroy()

        except FileNotFoundError:
            print(f"Error: El archivo {file} no fue encontrado")

    window_agregar_vendedor = tk.Toplevel(root)
    window_agregar_vendedor.title("Agregar vendedores")
    window_agregar_vendedor.geometry("450x300")
    #window_agregar_vendedor.configure(bg="#2E2E2E")

    # Crear los títulos centrados y en color blanco
    title_nombre = tk.Label(window_agregar_vendedor, font="bold", text="Introduzca el nombre del vendedor:",  fg="#2E2E2E")
    title_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    nombre = tk.Entry(window_agregar_vendedor)
    nombre.grid(row=0, column=1, padx=10, pady=10)

    title_telefono = tk.Label(window_agregar_vendedor, font="bold", text="Introduzca el télefono del vendedor:", fg="#2E2E2E")
    title_telefono.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    telefono = tk.Entry(window_agregar_vendedor)
    telefono.grid(row=1, column=1, padx=10, pady=10)

    title_email = tk.Label(window_agregar_vendedor, font="bold", text="Introduzca el email del vendedor:", fg="#2E2E2E")
    title_email.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    email = tk.Entry(window_agregar_vendedor)
    email.grid(row=2, column=1, padx=10, pady=10)

    button = tk.Button(window_agregar_vendedor, font="bold", text="Agregar", command=agregar, bg="#A8D600", fg="black")
    button.grid(row=3, column=0, columnspan=2, pady=10)

    # Centrar todos los elementos
    for i in range(4):
        window_agregar_vendedor.grid_rowconfigure(i, weight=1)
    window_agregar_vendedor.grid_columnconfigure(0, weight=1)
    window_agregar_vendedor.grid_columnconfigure(1, weight=1)

    # Centrar los títulos
    title_frame = tk.Frame(window_agregar_vendedor, bg="#2E2E2E")
    title_frame.grid(row=0, column=0, columnspan=2, pady=10)
    title_frame.grid_rowconfigure(0, weight=1)
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(1, weight=1)

    title_nombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)

    title_telefono.grid(row=1, column=0)
    telefono.grid(row=1, column=1)

    title_email.grid(row=2, column=0)
    email.grid(row=2, column=1)

#FUNCION PARA VER VENDEDORES AGREGADOS
def ver_vendedores():


    def load_list(data=None):
        if data is None:
            data = leer_vendedores()

        for row in tree.get_children():
            tree.delete(row)

#Insertar cada vendedor en la tabla con editar y elimianr
        for idx, item in enumerate(data, start=1):
            tree.insert("", "end", values=(idx, *item, "Editar", "Eliminar"))


    #FUNCIÓN DE BUSCAR

    def buscar():
        query = search_entry.get().lower()
        filtered_data = [v for v in vendedores if str(v[0]).lower() == query or v[0].lower().startswith(query)]
        load_list(filtered_data)

    #FUNCIÓN DE EDITAR
    def editar_vendedor(vendedor):
        pass
    #FUNCIÓN DE ELIMINAR
    def eliminar_vendedor(vendedor):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este vendedor?"):
            index = vendedores.index(vendedor)
            vendedores.pop(index)
            guardar_tareas(vendedores)
            messagebox.showinfo("Vendedor Eliminado", "El vendedor ha sido eliminado correctamente")
            load_list()

    window_ver_vendedores = tk.Toplevel(root)
    window_ver_vendedores.title("Ver Vendedores")
    window_ver_vendedores.geometry("1200x400")
    #Actualizar lista
    global vendedores
    vendedores = leer_vendedores()

    #Campo de busqueda
    search_frame = tk.Frame(window_ver_vendedores)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Buscar (ID o Nombre):").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT)
    tk.Button(search_frame, text="Buscar", command=buscar).pack(side=tk.LEFT)

    #ARMAR TABLA
    columns=("ID", "Nombre", "Teléfono", "Email", "Acciones", "Eliminar")
    tree=ttk.Treeview(window_ver_vendedores, columns=columns, show="headings")

    #Columnas de la tabla
    #Recorrer las columnas y asignarles los nombres correspondientes
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    #ir agregando editar y eliminar por cada fila
    for idx, vendedor in enumerate(vendedores):
        tree.insert("", "end", values=(idx+1, *vendedor, "Editar", "Eliminar"))

    def on_item_click(event):
        #identificar la celda donde se hizo click
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            #identificar la fila que se hizo click
            row_id = tree.identify_row(event.y)
            #identificar la columna que se hizo click
            col_id = tree.identify_column(event.x)
            selected_item = tree.item(row_id)["values"]
            #columna 5 para editar
            if col_id == "#5":
                editar_vendedor(vendedores[selected_item[0]-1])
            #columan 6 para eliminar
            elif col_id == "#6":
                eliminar_vendedor(vendedores[selected_item[0]-1])

    tree.bind("<Button>", on_item_click)
    #Cargar lista automatica
    load_list()

def leer_vendedores():
    if not os.path.exists(DATA_FILE):
        return []
    vendedores = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            nombre, telefono, email= line.strip().split(",")
            vendedores.append((nombre, telefono, email))
    return vendedores

def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as file:
        for contacto in tareas:
            file.write(",".join(contacto) + "\n")

#MENU PRINCIPAL
root = tk.Tk()
root.title("Ventana Principal")
root.geometry("500x500")
# CONFIGURANDO FONDO
root.configure(bg="#2E2E2E")

#AGREGANDO EL TITULO
titulo = tk.Label(root, text="Punto de Venta", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Crear un marco para los botones
frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(pady=20)

# Colores recomendados
button_add_bg = "#28A745"
button_edit_bg = "#FFC107"
button_delete_bg = "#DC3545"
button_fg = "#FFFFFF"
button_hover_bg = "#0056b3"

# Función para cambiar el color al pasar el ratón

def on_enter(e):
    e.widget['background'] = button_hover_bg

def on_leave(e):
    # Restablecer color según el tipo de botón
    if e.widget['text'] == "Agregar Tareas":
        e.widget['background'] = button_add_bg
    elif e.widget['text'] == "Editar Tarea":
        e.widget['background'] = button_edit_bg
    elif e.widget['text'] == "Eliminar Tareas":
        e.widget['background'] = button_delete_bg
    else:
        e.widget['background'] = "#007BFF"  # Color genérico

# Crear botones
buttons = [
    ("Agregar Vendedores", agregar_vendedores, button_add_bg),
    ("Ver Vendedores", ver_vendedores, "#007BFF"),
    ("Salir", root.quit, "#007BFF")
]


for (text, command, bg_color) in buttons:
    button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
    button.pack(pady=5)

    button.bind("<Enter>", on_enter)

    button.bind("<Leave>", on_leave)

root.mainloop()



