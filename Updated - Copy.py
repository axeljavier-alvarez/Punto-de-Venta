import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog
from tkcalendar import DateEntry

# instalar calendario pip install tkcalendar view/toolwindows/terminal
tree = ttk.Treeview
# donde se guardara
DATA_FILE = "tareas.txt"
DATA_FILE_CLIENTES = "clientes.txt"
import re


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"


# FUNCION PARA AGREGAR
def agregar_tareas():
    pass


# FUNCION PARA VER TAREAS
def ver_tareas():
    pass


def leer_tareas():
    if not os.path.exists(DATA_FILE):
        return []
    tareas = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            nombre, estado, descripcion, fecha = line.strip().split(",")
            tareas.append((nombre, estado, descripcion, fecha))
    return tareas


# FUNCION PARA LEER CLIENTES
def leer_clientes():
    """Lee los clientes desde el archivo."""
    if not os.path.exists(DATA_FILE_CLIENTES):
        return []
    clientes = []
    with open(DATA_FILE_CLIENTES, "r") as file:
        for line in file:
            datos = line.strip().split(",")
            if len(datos) >= 5:
                clientes.append(datos[:5])
    return clientes


# AUTOINCREMENTO ID
def obtener_siguiente_id():
    clientes = leer_clientes()
    max_id = 0
    for cliente in clientes:
        try:
            current_id = int(cliente[0])
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            continue
    return max_id + 1


# FUNCION PARA ELIMINAR TAREAS
def eliminar_tareas():
    pass


def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as file:
        for contacto in tareas:
            file.write(",".join(contacto) + "\n")


# ------------------------------Agregado
def guardar_clientes(clientes):
    with open(DATA_FILE_CLIENTES, "w") as file:
        for cliente in clientes:
            file.write(f"{cliente[0]},{cliente[1]},{cliente[2]},{cliente[3]},{cliente[4]}\n")


# -------------------------------Agregado
def ResultBusqueda(clientes, pal_buscar, par_busqueda):
    resultado = []

    print(f"Buscando: {pal_buscar} en campo {par_busqueda}")

    for cliente in clientes:
        if par_busqueda == 0:
            if str(cliente[0]) == pal_buscar:
                resultado.append(cliente)
        elif par_busqueda == 1:
            if re.search(f".*{pal_buscar}.*", cliente[1], re.IGNORECASE):
                resultado.append(cliente)
        else:
            pass

    return resultado


# FUNCIONES FALTANTES:
# 1. Asignar una tarea por medio del numero
def cambiar_estado():
    pass


# 2. Editar tarea
def editar_tarea():
    pass


# 3. Mostrar tareas completadas
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


# ---------------------------Ventana Principal para gestion de clientes
def show_gestion_clientes():
    def ocultar_indicador():
        ingresar_indicador.config(bg="#0477BF")
        gestionar_indicador.config(bg="#0477BF")

    def mostrar_indicador(indicador, frame):
        ocultar_indicador()
        indicador.config(bg="#D97A07")
        frame.tkraise()

    # Ajustar ventana
    window_gestion_clientes = tk.Toplevel(root)
    window_gestion_clientes.title("Gestión de Clientes")
    window_gestion_clientes.geometry("850x360")
    window_gestion_clientes.configure(bg="#2E2E2E")

    con_menu = tk.Frame(window_gestion_clientes, background="#0477BF")
    con_menu.pack(fill=tk.X)
    con_menu.pack_propagate(False)
    con_menu.configure(height=40)

    btn_ingresar = tk.Button(con_menu, text="Ingresar", font=('Bold', 10), bd=0, background="#0477BF",command=lambda: mostrar_indicador(ingresar_indicador, con_add_client))
    btn_ingresar.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ingresar_indicador = tk.Label(con_menu, text='', bg='#D97A07')
    ingresar_indicador.place(x=10, y=35, width=55, height=10)

    btn_gestionar = tk.Button(con_menu, text="Gestionar Clientes", font=('Bold', 10), bd=0, background="#0477BF", command=lambda: mostrar_indicador(gestionar_indicador, con_gestion_clientes))
    btn_gestionar.pack(side=tk.LEFT, fill=tk.Y)
    gestionar_indicador = tk.Label(con_menu, text='', bg='#0477BF')
    gestionar_indicador.place(x=73.25, y=35, width=128, height=10)

    # Panel para Registrar clientes
    margin_x = 100
    con_add_client = tk.Frame(window_gestion_clientes, background="#2E2E2E")
    con_add_client.place(x=0, y=40, width=850, height=320)
    lbl_margin_y = tk.Label(con_add_client, text="", bg="#2E2E2E")
    lbl_margin_y.pack(anchor="w", pady=4)

    lbl_id = tk.Label(con_add_client, text="ID:", fg="white", background="#2E2E2E")
    lbl_id.pack(anchor="w", padx=margin_x)
    id_var = tk.StringVar(value=str(obtener_siguiente_id()))
    id_entry = tk.Entry(con_add_client, textvariable=id_var, state="readonly")  # SOLO VISTA
    id_entry.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_nombre = tk.Label(con_add_client, text="Nombre del Cliente: ", fg="white", background="#2E2E2E")
    lbl_nombre.pack(anchor="w", padx=margin_x)
    nombre_cliente = tk.Entry(con_add_client)
    nombre_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_direccion = tk.Label(con_add_client, text="Dirección del Cliente: ", fg="white", background="#2E2E2E")
    lbl_direccion.pack(anchor="w", padx=margin_x)
    direccion_cliente = tk.Entry(con_add_client)
    direccion_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_telefono = tk.Label(con_add_client, text="Teléfono del Cliente: ", fg="white", background="#2E2E2E")
    lbl_telefono.pack(anchor="w", padx=margin_x)
    telefono_cliente = tk.Entry(con_add_client)
    telefono_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_email = tk.Label(con_add_client, text="E-mail del Cliente: ", fg="white", background="#2E2E2E")
    lbl_email.pack(anchor="w", padx=margin_x)
    email_cliente = tk.Entry(con_add_client)
    email_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    btn_agregar = tk.Button(con_add_client, text="Agregar Cliente", command=lambda: agregar_cliente(id_var, nombre_cliente, direccion_cliente, telefono_cliente, email_cliente, window_gestion_clientes))
    btn_agregar.pack(side='left', padx=margin_x)

    btn_cancelar = tk.Button(con_add_client, text="Cancelar")
    btn_cancelar.pack(side='right', padx=margin_x)

    def buscar():
        if (no_tarea.get() == ""):
            load_list()
        else:
            if (lista_menu.get() == "Buscar por:"):
                messagebox.showerror("Error", "Por favor seleccione un parámetro de búsqueda")
            else:
                par_busqueda = -1
                if (lista_menu.get() == "ID"):
                    par_busqueda = 0
                    pal_buscar = str(no_tarea.get())
                elif (lista_menu.get() == "Nombre"):
                    par_busqueda = 1
                    pal_buscar = no_tarea.get()

                coincidencias = ResultBusqueda(clientes, pal_buscar, par_busqueda)

                for i in tree.get_children():
                    tree.delete(i)

                for cliente in coincidencias:
                    tree.insert("", tk.END, values=cliente)

    # FUNCION PARA EDITAR
    def editar_cliente():
        selected_items = tree.selection()
        if len(selected_items) == 0:
            messagebox.showwarning("Editar cliente", "Por favor seleccione un cliente para editar")
            return

        item = tree.item(selected_items[0], 'values')
        id, nombre, direccion, telefono, email = item

        ventana_edicion = tk.Toplevel(root)
        ventana_edicion.title("Editar cliente")
        ventana_edicion.geometry("400x300")
        ventana_edicion.configure(bg="#2E2E2E")

        lbl_nombre = tk.Label(ventana_edicion, text="Nombre del cliente: ", fg="white", bg="#2E2E2E")
        lbl_nombre.pack(anchor="w", padx=10, pady=5)
        entry_nombre = tk.Entry(ventana_edicion)
        entry_nombre.insert(0, nombre)
        entry_nombre.pack(anchor="w", padx=10, pady=5)

        lbl_direccion = tk.Label(ventana_edicion, text="Dirección del cliente: ", fg="white", bg="#2E2E2E")
        lbl_direccion.pack(anchor="w", padx=10, pady=5)
        entry_direccion = tk.Entry(ventana_edicion)
        entry_direccion.insert(0, direccion)
        entry_direccion.pack(anchor="w", padx=10, pady=5)

        lbl_telefono = tk.Label(ventana_edicion, text="Télefono del cliente: ", fg="white", bg="#2E2E2E")
        lbl_telefono.pack(anchor="w", padx=10, pady=5)
        entry_telefono = tk.Entry(ventana_edicion)
        entry_telefono.insert(0, telefono)
        entry_telefono.pack(anchor="w", padx=10, pady=5)

        lbl_email = tk.Label(ventana_edicion, text="E-mail del cliente: ", fg="white", bg="#2E2E2E")
        lbl_email.pack(anchor="w", padx=10, pady=5)
        entry_email = tk.Entry(ventana_edicion)
        entry_email.insert(0, email)
        entry_email.pack(anchor="w", padx=10, pady=5)

        def actualizar_cliente():
            nuevo_nombre = entry_nombre.get()
            nuevo_direccion = entry_direccion.get()
            nuevo_telefono = entry_telefono.get()
            nuevo_email = entry_email.get()

            if not nuevo_nombre or not nuevo_direccion or not nuevo_telefono or not nuevo_email:
                messagebox.showerror("Error", "Por favor llenar todos los campos")
                return

            if not nuevo_telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe ser un número válido.")
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
                messagebox.showerror("Error", "El e-mail debe tener un formato válido.")
                return

            clientes = leer_clientes()
            for cliente in clientes:
                if cliente[3] == nuevo_email and str(cliente[0]) != str(id):
                    messagebox.showerror("Error", "El correo electrónico ya está registrado.")
                    return

            clientes_actualizados = []
            for cliente in clientes:
                if str(cliente[0]) == str(id):
                    clientes_actualizados.append((id, nuevo_nombre, nuevo_direccion, nuevo_telefono, nuevo_email))
                else:
                    clientes_actualizados.append(cliente)

            guardar_clientes(clientes_actualizados)

            messagebox.showinfo("cliente Actualizado", "Los datos del cliente se actualizaron correctamente.")
            ventana_edicion.destroy()
            load_list()

        btn_actualizar = tk.Button(ventana_edicion, text="Actualizar", command=actualizar_cliente)
        btn_actualizar.pack(side='left', padx=20, pady=10)

        btn_cancelar = tk.Button(ventana_edicion, text="Cancelar", command=ventana_edicion.destroy)
        btn_cancelar.pack(side='right', padx=20, pady=10)

    def eliminar():
        selected_items = tree.selection()

        if len(selected_items) == 0:
            messagebox.showwarning("Eliminar cliente", "Por favor seleccione un cliente para eliminarlo")
            return

        item_id = tree.item(selected_items[0], 'values')[0]

        ventana_confirmacion_eliminar(item_id)

    def ventana_confirmacion_eliminar(item_id):
        ventana_confirmacion = tk.Toplevel(root)
        ventana_confirmacion.title("Confirmar eliminación")
        ventana_confirmacion.geometry("300x150")
        ventana_confirmacion.configure(bg="#2E2E2E")

        mensaje = f"¿Desea eliminar el cliente con ID: {item_id}?"
        label_mensaje = tk.Label(ventana_confirmacion, text=mensaje, fg="white", bg="#2E2E2E")
        label_mensaje.pack(pady=20)

        btn_confirmar = tk.Button(ventana_confirmacion, text="Eliminar", command=lambda: confirmar_eliminacion(item_id, ventana_confirmacion))
        btn_confirmar.pack(side=tk.LEFT, padx=20)

        btn_cancelar = tk.Button(ventana_confirmacion, text="Cancelar", command=ventana_confirmacion.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=20)

    def confirmar_eliminacion(item_id, ventana_confirmacion):
        clientes = leer_clientes()

        clientes_filtrados = [cliente for cliente in clientes if str(cliente[0]) != str(item_id)]

        guardar_clientes(clientes_filtrados)

        load_list()

        ventana_confirmacion.destroy()

        messagebox.showinfo("Eliminar", f"cliente con ID {item_id} eliminado con éxito.")

    def load_list():
        for i in tree.get_children():
            tree.delete(i)
        for cliente in leer_clientes():
            tree.insert("", tk.END, values=cliente)

    con_gestion_clientes = tk.Frame(window_gestion_clientes, background='#2E2E2E')
    con_gestion_clientes.place(x=0, y=40, width=850, height=320)
    clientes = leer_clientes()

    label1 = tk.Label(con_gestion_clientes, text="Buscar Cliente: ", background="#2E2E2E", fg="white")
    label1.grid(row=0, column=0, padx=25, pady=5)
    no_tarea = tk.Entry(con_gestion_clientes)
    no_tarea.grid(row=0, column=1, padx=0, pady=5)
    lista_opciones = ["ID", "Nombre"]
    lista_menu = tk.StringVar(con_gestion_clientes)
    lista_menu.set("Buscar por:")
    checklist = tk.OptionMenu(con_gestion_clientes, lista_menu, *lista_opciones)
    checklist.grid(row=0, column=2, padx=25, pady=5)
    button2 = tk.Button(con_gestion_clientes, text="Buscar", command=buscar)
    button2.grid(row=0, column=3, pady=5, padx=25)

    columnas = ('Id', 'Nombre', 'Dirección', 'Télefono', 'E-mail')
    tree = ttk.Treeview(con_gestion_clientes, columns=columnas, show='headings')
    tree.heading('Id', text='Id')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Dirección', text='Dirección')
    tree.heading('Télefono', text='Télefono')
    tree.heading('E-mail', text='E-mail')
    tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
    srollbar = ttk.Scrollbar(con_gestion_clientes, orient='vertical', command=tree.yview)
    tree.config(yscrollcommand=srollbar.set)
    srollbar.grid(row=1, column=4, sticky='ns')

    con_gestion_clientes.grid_rowconfigure(1, weight=0)
    con_gestion_clientes.grid_columnconfigure(1, weight=1)

    btn_editar = tk.Button(con_gestion_clientes, text="Editar", command=editar_cliente)
    btn_editar.grid(row=2, column=0, padx=5, pady=5)

    btn_eliminar = tk.Button(con_gestion_clientes, text="Eliminar", command=eliminar)
    btn_eliminar.grid(row=2, column=1, padx=5, pady=5)
    load_list()
    con_add_client.tkraise()


def agregar_cliente(id_var: any = None ,nombre: any = None, direccion: any = None, telefono: any = None, email: any = None, ventana: any = None):

    try:
        if not nombre or not direccion or not telefono or not email:
            raise ValueError("Todos los campos son obligatorios.")

        # Validar que el nombre no se repita
        if any(cliente[1].lower() == nombre.lower() for cliente in leer_clientes()):
            raise ValueError("El nombre ya existe. Ingrese otro nombre.")

        #Validar teléfono: debe ser numérico y tener exactamente 8 dígitos
        #if not telefono.isdigit() or len(telefono) != 8:
        #    raise ValueError("El teléfono debe contener exactamente 8 dígitos numéricos.")

        # Validar email usando una expresión regular básica
        #patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        #if not re.match(patron_email, email):
        #    raise ValueError("El email debe tener un formato y dominio válido.")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    try:
        with open(DATA_FILE_CLIENTES, "a") as file:
            file.write(f"{id_var.get()},{nombre.get()},{direccion.get()},{telefono.get()},{email.get()}\n")
        messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        # Limpiar campos (excepto ID que se actualiza)
        nombre.delete(0, tk.END)
        direccion.delete(0, tk.END)
        telefono.delete(0, tk.END)
        email.delete(0, tk.END)
        id_var.set(str(obtener_siguiente_id()))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")


# Crear botones
buttons = [
    ("Gestión de Clientes", show_gestion_clientes, button_add_bg),
    ("Gestión de Vendedores", ver_tareas, "#007BFF"),  # Azul genérico
    ("Gestión de Clientes", show_gestion_clientes, button_delete_bg),
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
