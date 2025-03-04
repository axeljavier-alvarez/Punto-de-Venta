import os
import re
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
# instalar calendario pip install tkcalendar view/toolwindows/terminal
tree = ttk.Treeview
# donde se guardara
DATA_FILE = "clientes.txt"
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


# FUNCION PARA ELIMINAR TAREAS
def eliminar_tareas():
    pass


def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as file:
        for contacto in tareas:
            file.write(",".join(contacto) + "\n")


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

#AGREGANDO EL TITULO
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


# FUNCION PARA LEER CLIENTES
def leer_clientes():
    """Lee los clientes desde el archivo."""
    if not os.path.exists(DATA_FILE):
        return []
    clientes = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            datos = line.strip().split(",")
            if len(datos) >= 5:
                clientes.append(datos[:5])
    return clientes


#AUTOINCREMENTO ID
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


#MENU
def abrir_gestion_clientes():
    ventana_clientes = tk.Toplevel(root)
    ventana_clientes.title("Gestión de Clientes")
    ventana_clientes.geometry("1000x400")

    frames = {}

    def mostrar_frame(nombre):
        for frame in frames.values():
            frame.pack_forget()
        frames[nombre].pack(fill="both", expand=True)

    #INGRESAR CLIENTE
    def ingresar_cliente():
        frame = tk.Frame(ventana_clientes)
        frames["ingresar"] = frame

        tk.Label(frame, text="Ingresar Cliente", font=("Arial", 16, "bold")).pack(pady=10)

        # AUTOINCREMENTEO DEL ID
        tk.Label(frame, text="ID:").pack()
        id_var = tk.StringVar(value=str(obtener_siguiente_id()))
        id_entry = tk.Entry(frame, textvariable=id_var, state="readonly")#SOLO VISTA
        id_entry.pack()

        tk.Label(frame, text="Nombre:").pack()
        nombre_entry = tk.Entry(frame)
        nombre_entry.pack()

        tk.Label(frame, text="Dirección:").pack()
        direccion_entry = tk.Entry(frame)
        direccion_entry.pack()

        tk.Label(frame, text="Teléfono:").pack()
        telefono_entry = tk.Entry(frame)
        telefono_entry.pack()

        tk.Label(frame, text="Email:").pack()
        email_entry = tk.Entry(frame)
        email_entry.pack()

        def agregar_cliente():
            nid = id_var.get()
            nnombre = nombre_entry.get().strip()
            ndireccion = direccion_entry.get().strip()
            ntelefono = telefono_entry.get().strip()
            nemail = email_entry.get().strip()

            try:
                if not nnombre or not ndireccion or not ntelefono or not nemail:
                    raise ValueError("Todos los campos son obligatorios.")

                # Validar que el nombre no se repita
                if any(cliente[1].lower() == nnombre.lower() for cliente in leer_clientes()):
                    raise ValueError("El nombre ya existe. Ingrese otro nombre.")

                # Validar teléfono: debe ser numérico y tener exactamente 8 dígitos
                if not ntelefono.isdigit() or len(ntelefono) != 8:
                    raise ValueError("El teléfono debe contener exactamente 8 dígitos numéricos.")

                # Validar email usando una expresión regular básica
                patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(patron_email, nemail):
                    raise ValueError("El email debe tener un formato y dominio válido.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return


            try:
                with open(DATA_FILE, "a") as file:
                    file.write(f"{nid},{nnombre},{ndireccion},{ntelefono},{nemail}\n")
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                # Limpiar campos (excepto ID que se actualiza)
                nombre_entry.delete(0, tk.END)
                direccion_entry.delete(0, tk.END)
                telefono_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                id_var.set(str(obtener_siguiente_id()))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")

        btn_agregar = tk.Button(frame, text="Agregar Cliente", command=agregar_cliente)
        btn_agregar.pack(pady=10)

    #MOSTRAR CLIENTES
    def mostrar_cliente():
        frame = tk.Frame(ventana_clientes)
        frames["mostrar"] = frame

        tk.Label(frame, text="Lista de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("ID", "Nombre", "Dirección", "Teléfono", "Email")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_datos():
            for row in tree.get_children():
                tree.delete(row)
            for cliente in leer_clientes():
                tree.insert("", "end", values=cliente)

        cargar_datos()
        btn_actualizar = tk.Button(frame, text="Actualizar", command=cargar_datos)
        btn_actualizar.pack(pady=10)

    #MODIFICAR CLIENTE
    def modificar_cliente():
        frame = tk.Frame(ventana_clientes)
        frames["modificar"] = frame

        tk.Label(frame, text="Modificar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="ID del Cliente:").pack()
        id_entry = tk.Entry(frame)
        id_entry.pack()

        tk.Label(frame, text="Nuevo Nombre (opcional):").pack()
        nombre_entry = tk.Entry(frame)
        nombre_entry.pack()

        tk.Label(frame, text="Nueva Dirección (opcional):").pack()
        direccion_entry = tk.Entry(frame)
        direccion_entry.pack()

        tk.Label(frame, text="Nuevo Teléfono (opcional):").pack()
        telefono_entry = tk.Entry(frame)
        telefono_entry.pack()

        tk.Label(frame, text="Nuevo Email (opcional):").pack()
        email_entry = tk.Entry(frame)
        email_entry.pack()

        def actualizar_cliente():
            clientes = leer_clientes()
            nid = id_entry.get().strip()
            nuevo_nombre = nombre_entry.get().strip()
            nueva_direccion = direccion_entry.get().strip()
            nuevo_telefono = telefono_entry.get().strip()
            nuevo_email = email_entry.get().strip()

            try:
                if nuevo_nombre:
                    # Verificar que el nuevo nombre no se repita en otro cliente
                    if any(cliente[0] != nid and cliente[1].lower() == nuevo_nombre.lower() for cliente in clientes):
                        raise ValueError("El nombre ya existe en otro registro.")

                if nuevo_telefono:
                    if not nuevo_telefono.isdigit() or len(nuevo_telefono) != 8:
                        raise ValueError("El teléfono debe contener exactamente 8 dígitos numéricos.")

                if nuevo_email:
                    patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                    if not re.match(patron_email, nuevo_email):
                        raise ValueError("El email debe tener un formato y dominio válido.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

            encontrado = False
            try:
                with open(DATA_FILE, "w") as file:
                    for cliente in clientes:
                        if cliente[0] == nid:
                            cliente[1] = nuevo_nombre if nuevo_nombre else cliente[1]
                            cliente[2] = nueva_direccion if nueva_direccion else cliente[2]
                            cliente[3] = nuevo_telefono if nuevo_telefono else cliente[3]
                            cliente[4] = nuevo_email if nuevo_email else cliente[4]
                            encontrado = True
                        file.write(",".join(cliente) + "\n")
                if encontrado:
                    messagebox.showinfo("Éxito", "Cliente actualizado.")
                else:
                    messagebox.showwarning("Error", "ID no encontrado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")

        btn_actualizar = tk.Button(frame, text="Actualizar", command=actualizar_cliente)
        btn_actualizar.pack(pady=10)

    #ELIMINAR CLIENTE
    def eliminar_cliente():
        frame = tk.Frame(ventana_clientes)
        frames["eliminar"] = frame

        tk.Label(frame, text="Eliminar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="ID del Cliente:").pack()
        id_entry = tk.Entry(frame)
        id_entry.pack()

        def eliminar():
            clientes = leer_clientes()
            clientes_filtrados = [c for c in clientes if c[0] != id_entry.get().strip()]

            try:
                with open(DATA_FILE, "w") as file:
                    for cliente in clientes_filtrados:
                        file.write(",".join(cliente) + "\n")
                messagebox.showinfo("Éxito", "Cliente eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

        btn_eliminar = tk.Button(frame, text="Eliminar", command=eliminar)
        btn_eliminar.pack(pady=10)

    #BUSCAR CLIENTE
    def buscar_cliente():
        frame = tk.Frame(ventana_clientes)
        frames["buscar"] = frame

        tk.Label(frame, text="Buscar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="Buscar por ID o Nombre:").pack()
        busqueda_entry = tk.Entry(frame)
        busqueda_entry.pack()

        resultado_text = tk.Text(frame, height=10, width=50)
        resultado_text.pack(pady=10)

        def buscar():
            busqueda = busqueda_entry.get().lower().strip()
            resultados = []
            for cliente in leer_clientes():
                if busqueda in cliente[0].lower() or busqueda in cliente[1].lower():
                    resultados.append(cliente)
            resultado_text.delete(1.0, tk.END)
            if resultados:
                for cliente in resultados:
                    resultado_text.insert(tk.END, ", ".join(cliente) + "\n")
            else:
                resultado_text.insert(tk.END, "No se encontraron clientes.")

        btn_buscar = tk.Button(frame, text="Buscar", command=buscar)
        btn_buscar.pack(pady=10)

    ingresar_cliente()
    mostrar_cliente()
    modificar_cliente()
    eliminar_cliente()
    buscar_cliente()
    mostrar_frame("ingresar")

    menubar = Menu(ventana_clientes)
    ventana_clientes.config(menu=menubar)
    menubar.add_command(label="Ingresar", command=lambda: mostrar_frame("ingresar"))
    menubar.add_command(label="Modificar", command=lambda: mostrar_frame("modificar"))
    menubar.add_command(label="Eliminar", command=lambda: mostrar_frame("eliminar"))
    menubar.add_command(label="Buscar", command=lambda: mostrar_frame("buscar"))
    menubar.add_command(label="Mostrar", command=lambda: mostrar_frame("mostrar"))




# Crear botones
buttons = [
    ("Gestión de Clientes", abrir_gestion_clientes, button_add_bg),
    ("Gestión de vendedores", ver_tareas, "#007BFF"),  # Azul genérico
    ("Gestión de Productos", eliminar_tareas, button_delete_bg),
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
