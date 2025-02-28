import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog

# from tkcalendar import DateEntry
# instalar calendario pip install tkcalendar view/toolwindows/terminal
tree = ttk.Treeview
# donde se guardara
DATA_FILE = "clientes.txt"


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"


# FUNCION GESTION DE CLIENTES
def clientes():

    def agregar_cliente():  # AGREGAR UN NUEVO CLIENTE
        try:
            nid = id.get()
            nnombre = nombre.get()
            ndireccion = direccion.get()
            ntelefono = telefono.get()
            nemail = email.get()

            with open(DATA_FILE, "a") as file:
                file.write(f"{nid},{nnombre},{ndireccion},{ntelefono},{nemail}\n")
                messagebox.showinfo("Cliente agregado", "El cliente fue agregado exitosamente.")
        except FileNotFoundError:
            print(f"Error: El archivo {file} no fue encontrado,")

        #menu_cliente = tk.Toplevel(menu_cliente)
        #menu_cliente.title("Agregar cliente")
        #menu_cliente.geometry("400x400")
        # ETIQUETAS
        label = tk.Label(menu_cliente, text="Introduce ID:")
        label.grid(row=0, column=0, padx=10, pady=10)
        label.bind("<Return>", focus_next_widget)

        label = tk.Label(menu_cliente, text="Introduce Nombre:")
        label.grid(row=1, column=0, padx=10, pady=10)
        label.bind("<Return>", focus_next_widget)

        label = tk.Label(menu_cliente, text="Introduce Dirección:")
        label.grid(row=2, column=0, padx=10, pady=10)
        label.bind("<Return>", focus_next_widget)

        label = tk.Label(menu_cliente, text="Introduce Teléfono:")
        label.grid(row=3, column=0, padx=10, pady=10)
        label.bind("<Return>", focus_next_widget)

        label = tk.Label(menu_cliente, text="Introduce Email:")
        label.grid(row=4, column=0, padx=10, pady=10)
        label.bind("<Return>", focus_next_widget)

        # CUADROS DE TEXTO
        id = tk.Entry(menu_cliente)
        id.grid(row=0, column=1, padx=10, pady=10)
        id.bind("<Return>", focus_next_widget)

        nombre = tk.Entry(menu_cliente)
        nombre.grid(row=1, column=1, padx=10, pady=10)
        nombre.bind("<Return>", focus_next_widget)

        direccion = tk.Entry(menu_cliente)
        direccion.grid(row=2, column=1, padx=10, pady=10)
        direccion.bind("<Return>", focus_next_widget)

        telefono = tk.Entry(menu_cliente)
        telefono.grid(row=3, column=1, padx=10, pady=10)
        telefono.bind("<Return>", focus_next_widget)

        email = tk.Entry(menu_cliente)
        email.grid(row=4, column=1, padx=10, pady=10)
        email.bind("<Return>", focus_next_widget)

        button = tk.Button(menu_cliente, text="Agregar", command=agregar_cliente)
        button.grid(row=6, column=1, columnspan=1, pady=10)
        button.configure(background="#d1a453")

    def modificar_cliente():  # MODIFICAR INFORMACION DE UN CLIENTE EXISTENTE
        pass

    def eliminar_cliente():  # ELIMINAR CLIENTE
        pass

    def buscar_cliente():  # BUSCAR POR NOMBRE O ID
        pass

    def mostrar_clientes():  # MOSTRAR LA LISTA DE CLIENTES
        def load_list():
            clientes = leer_clientes()

            # limpiar datos en el Treeview
            for row in tree.get_children():
                tree.delete(row)
            # insertar datos en el Treeview
            for item in clientes:
                tree.insert("", "end", values=item)

        #menu_cliente = tk.Toplevel(root)
        #menu_cnte.title("Ver clientes")
        #menu_cliente.geometry("600x300")

        # crear el treeview
        columns = ("ID", "Nombre", "Direccion", "Telefono", "Email")
        tree = ttk.Treeview(menu_cliente, columns=columns, show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Direccion", text="Direccion")
        tree.heading("Telefono", text="Telefono")
        tree.heading("Email", text="Email")
        tree.grid(row=0, column=0, sticky="nsew")

        # anadir una barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(menu_cliente, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # configurar el grid
        menu_cliente.grid_rowconfigure(0, weight=0)
        menu_cliente.grid_columnconfigure(0, weight=1)

        # botonpara cargar la lista
        button2 = tk.Button(menu_cliente, text="Cargar lista", command=load_list)
        button2.grid(row=2, column=1, pady=10)
        button2.configure(background="#97701e")

    def leer_clientes():
        if not os.path.exists(DATA_FILE):
            return []
        clientes = []

        with open(DATA_FILE, "r") as file:
            for i, line in enumerate(file, start=1):
                datos = line.strip().split(",")
                if len(datos) == 5:
                    id, nombre, direccion, telefono, email = datos
                    clientes.append((id, nombre, direccion, telefono, email))
        return clientes


    menu_cliente = tk.Tk()
    menu_cliente.title("Menu clientes")
    menu_cliente.geometry("800x800")
    menu_bar = tk.Menu(menu_cliente)
    menu_cliente.config(menu=menu_bar)
    #menu_cliente = tk.Menu(menu_bar, tearoff=0)
    #menu_cliente.add_command(label="Agregar cliente", command=agregar_cliente)
    menu_mostrar = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Agregar",command=agregar_cliente)
    menu_bar.add_cascade(label="Modificar", command=modificar_cliente)
    menu_bar.add_cascade(label="Eliminar", command=eliminar_cliente)
    menu_bar.add_cascade(label="Buscar", command=buscar_cliente)
    menu_bar.add_cascade(label="Mostrar",command=mostrar_clientes)

    #menu_mostrar.add_command(label="Mostrar cliente", command=mostrar_clientes)


# FUNCION PARA VER TAREAS
def ver_clientes():
    pass


def leer_clientes():
    if not os.path.exists(DATA_FILE):
        return []
    clientes = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            nombre, estado, descripcion, fecha = line.strip().split(",")
            clientes.append((nombre, estado, descripcion, fecha))
    return clientes


# FUNCION PARA ELIMINAR TAREAS
def eliminar_clientes():
    pass


def guardar_clientes(clientes):
    with open(DATA_FILE, "w") as file:
        for contacto in clientes:
            file.write(",".join(contacto) + "\n")


# FUNCIONES FALTANTES:
# 1. Asignar una tarea por medio del numero
def cambiar_estado():
    pass


# 2. Editar tarea
def editar_tarea():
    pass


# 3. Mostrar clientes completadas
def mostrar_completadas():
    pass


root = tk.Tk()
root.title("Ventana Principal")
root.geometry("500x500")
# CONFIGURANDO FONDO
root.configure(bg="#2E2E2E")

# AGREGANDO EL TITULO
titulo = tk.Label(root, text="Administración de Tareas", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
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
    ("Gestión de Clientes", clientes, button_add_bg),
    ("Gestión de vendedores", ver_clientes, "#007BFF"),  # Azul genérico
    ("Gestión de Productos", eliminar_clientes, button_delete_bg),
    ("Registro de Facturas", cambiar_estado, "#007BFF"),
    ("Gestión de Usuarios", editar_tarea, button_edit_bg),
    ("Salir", root.quit, "#007BFF")
]

for (text, command, bg_color) in buttons:
    button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
    button.pack(pady=5)

    button.bind("<Enter>", on_enter)

    button.bind("<Leave>", on_leave)

root.mainloop()