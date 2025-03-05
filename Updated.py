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

# ---------------------------Agregado
def leer_clientes():
    if not os.path.exists(DATA_FILE_CLIENTES):
        return []
    clientes = []
    with open(DATA_FILE_CLIENTES, "r") as file:
        for line in file:
            id, nombre, direccion, telefono, email = line.strip().split(",")
            clientes.append((id, nombre, direccion, telefono, email))
    return clientes

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
            file.write(",".join(cliente) + "\n")

# -------------------------------Agregado
def ResultBusqueda(clientes=[], pal_buscar="", par_busqueda=0, ):
    resutl = [cliente for cliente in clientes if re.match(f".*{pal_buscar}", cliente[par_busqueda], re.IGNORECASE)]
    return resutl

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

    window_gestion_clientes = tk.Toplevel(root)
    window_gestion_clientes.title("Gestión de Clientes")
    window_gestion_clientes.geometry("850x360")
    window_gestion_clientes.configure(bg="#2E2E2E")

    con_menu = tk.Frame(window_gestion_clientes, background="#0477BF")
    con_menu.pack(fill=tk.X)
    con_menu.pack_propagate(False)
    con_menu.configure(height=40)

    btn_ingresar = tk.Button(con_menu, text="Ingresar", font=('Bold', 10), bd=0, background="#0477BF", command=lambda: mostrar_indicador(ingresar_indicador, con_add_client))
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
    lbl_nombre = tk.Label(con_add_client, text="Código del Cliente: ", fg="white", background="#2E2E2E")
    lbl_nombre.pack(anchor="w", padx=margin_x)
    id_cliente = tk.Entry(con_add_client)
    id_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_id = tk.Label(con_add_client, text="Nombre del Cliente: ", fg="white", background="#2E2E2E")
    lbl_id.pack(anchor="w", padx=margin_x)
    nombre_cliente = tk.Entry(con_add_client)
    nombre_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_direccion_u = tk.Label(con_add_client, text="Dirección del Cliente: ", fg="white", background="#2E2E2E")
    lbl_direccion_u.pack(anchor="w", padx=margin_x)
    direccion_cliente = tk.Entry(con_add_client)
    direccion_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_telefono = tk.Label(con_add_client, text="Teléfono: ", fg="white", background="#2E2E2E")
    lbl_telefono.pack(anchor="w", padx=margin_x)
    telefono_cliente = tk.Entry(con_add_client)
    telefono_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_email = tk.Label(con_add_client, text="Email: ", fg="white", background="#2E2E2E")
    lbl_email.pack(anchor="w", padx=margin_x)
    email_cliente = tk.Entry(con_add_client)
    email_cliente.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    btn_agregar = tk.Button(con_add_client, text="Agregar Cliente", command=lambda: agregar_cliente(id_cliente, nombre_cliente, direccion_cliente, telefono_cliente, email_cliente, window_gestion_clientes))
    btn_agregar.pack(side='left', padx=margin_x)

    btn_cancelar = tk.Button(con_add_client, text="Cancelar")
    btn_cancelar.pack(side='right', padx=margin_x)

    # Panel para Gestionar Clientes
    def buscar():
        if (no_tarea.get() == ""):
            load_list()
        else:
            if (lista_menu.get() == "Buscar por:"):
                messagebox.showerror("Error", "Por favor seleccione un parametro de busqueda")
            else:
                par_busqueda = -1
                if (lista_menu.get() == "ID"):
                    par_busqueda = 0
                elif (lista_menu.get() == "Nombre"):
                    par_busqueda = 1

                coincidencias = ResultBusqueda(clientes, no_tarea.get(), par_busqueda)

                for i in tree.get_children():
                    tree.delete(i)
                for cliente in coincidencias:
                    tree.insert("", tk.END, values=cliente)

    def eliminar():
        lista_items_selec = []
        all_selected = tree.selection()
        for item in all_selected:
            item_values = tree.item(item, 'values')
            lista_items_selec.append(item_values[0])

        if len(lista_items_selec) == 0:
            messagebox.showwarning("Eliminar Cliente", "Por favor seleccione cliente uno para eliminar")
        else:
            confirmacion = messagebox.askyesno("Eliminar", f"¿Estas seguro de eliminar?")
            if confirmacion:
                indices_eliminar = [i for i, cliente in enumerate(clientes, start=0) if
                                    cliente[0] in lista_items_selec]
                for e_cliente in indices_eliminar:
                    clientes.pop(e_cliente)
                guardar_clientes(clientes)
                messagebox.showinfo("Eliminar", "Clientes eliminados con exito.")
                load_list()

    def editar(n_id="", n_nombre="", n_direccion="", n_telefono="", n_email="", ventana: any = None):
        if n_id == "" or n_nombre == "" or n_direccion == "" or n_telefono == "" or n_email == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
        else:
            indice = -1
            for i, cliente in enumerate(clientes, start=0):
                if n_id == cliente[0]:
                    indice = i
                    break

            l_cliente = list(clientes[indice])
            l_cliente[0] = n_id
            l_cliente[1] = n_nombre
            l_cliente[2] = n_direccion
            l_cliente[3] = n_telefono
            l_cliente[4] = n_email
            clientes[indice] = tuple(l_cliente)
            guardar_clientes(clientes)
            messagebox.showinfo("Editar tarea", "Cliente Editado con exito")
            ventana.destroy()
            load_list()

    def editar_cliente():
        lista_items_selec = []
        all_selected = tree.selection()
        for item in all_selected:
            item_values = tree.item(item, 'values')
            lista_items_selec.append(item_values)

        # print(lista_items_selec)

        if len(lista_items_selec) >= 2:
            messagebox.showwarning("Editar Cliente", "Seleccione solo uno para editar")
        elif len(lista_items_selec) == 0:
            messagebox.showwarning("Editar Cliente", "Por favor seleccione cliente uno para editar")
        else:
            window_ingresar_clientes = tk.Toplevel(root)
            window_ingresar_clientes.title("Editar Clientes")
            window_ingresar_clientes.geometry("350x250")
            window_ingresar_clientes.configure(bg="#2E2E2E")

            lbl_id = tk.Label(window_ingresar_clientes, text="Código del Cliente: ", fg="white",background="#2E2E2E")
            lbl_id.pack(anchor="w", padx=30)
            id_cliente = tk.Entry(window_ingresar_clientes)
            id_cliente.delete(0, tk.END)
            id_cliente.insert(0, lista_items_selec[0][0])
            id_cliente.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_nombre = tk.Label(window_ingresar_clientes, text="Nombre del Cliente: ", fg="white", background="#2E2E2E")
            lbl_nombre.pack(anchor="w", padx=30)
            nombre_cliente = tk.Entry(window_ingresar_clientes)
            nombre_cliente.delete(0, tk.END)
            nombre_cliente.insert(0, lista_items_selec[0][1])
            nombre_cliente.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_direccion_u = tk.Label(window_ingresar_clientes, text="Dirección del Cliente: ", fg="white", background="#2E2E2E")
            lbl_direccion_u.pack(anchor="w", padx=30)
            direccion_cliente = tk.Entry(window_ingresar_clientes)
            direccion_cliente.delete(0, tk.END)
            direccion_cliente.insert(0, lista_items_selec[0][2])
            direccion_cliente.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_telefono = tk.Label(window_ingresar_clientes, text="Teléfono del Cliente: ", fg="white", background="#2E2E2E")
            lbl_telefono.pack(anchor="w", padx=30)
            telefono_cliente = tk.Entry(window_ingresar_clientes)
            telefono_cliente.delete(0, tk.END)
            telefono_cliente.insert(0, lista_items_selec[0][3])
            telefono_cliente.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_email = tk.Label(window_ingresar_clientes, text="Email del Cliente: ", fg="white", background="#2E2E2E")
            lbl_email.pack(anchor="w", padx=30)
            email_cliente = tk.Entry(window_ingresar_clientes)
            email_cliente.delete(0, tk.END)
            email_cliente.insert(0, lista_items_selec[0][4])
            email_cliente.pack(anchor="w", padx=30, pady=5, fill="x")


            btn_agregar = tk.Button(window_ingresar_clientes, text="Editar Cliente", command=lambda: editar(
                id_cliente.get(),
                nombre_cliente.get(),
                direccion_cliente.get(),
                telefono_cliente.get(),
                email_cliente.get(),
                window_ingresar_clientes
            ))
            btn_agregar.pack(side='left', padx=40)

            btn_cancelar = tk.Button(window_ingresar_clientes, text="Cancelar", command=window_ingresar_clientes.destroy)
            btn_cancelar.pack(side='right', padx=40)

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

    columnas = ('Codigo', 'Nombre', 'Direccion', 'Telefono', 'Email')
    tree = ttk.Treeview(con_gestion_clientes, columns=columnas, show='headings')
    tree.heading('Codigo', text='Codigo')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Direccion', text='Direccion')
    tree.heading('Telefono', text='Telefono')
    tree.heading('Email', text='Email')
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


def agregar_cliente(id: any = None, nombre: any = None, direccion: any = None, telefono: any = None, email: any = None, ventana: any = None):
    if (id.get() == "" and nombre.get() == "" and direccion.get() == "" and telefono.get() == "" and email.get() == ""):
        messagebox.showerror("Error", "Todos los campos son requeridos")
        return

    try:
        with open(DATA_FILE_CLIENTES, "a") as file:
            file.write(f"{int(id.get())},{nombre.get()},{(direccion.get())},{int(telefono.get())},{(email.get())}\n")
            messagebox.showinfo("Cliente Agregado", "Cliente agregado correctamente")

            id.delete(0, tk.END)
            nombre.delete(0, tk.END)
            direccion.delete(0, tk.END)
            telefono.delete(0, tk.END)
            email.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Verifique los campos ingresados.")


# Crear botones
buttons = [
    ("Gestión de Clientes", show_gestion_clientes, button_add_bg),
    ("Gestión de vendedores", ver_tareas, "#007BFF"),  # Azul genérico
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