import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# DONDE SE GUARDARA VENDEDORES
DATA_FILE = "vendedores.txt"


def leer_vendedores():
    if not os.path.exists(DATA_FILE):
        return []
    vendedores = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            nombre, telefono, email = line.strip().split(",")
            vendedores.append((nombre, telefono, email))
    return vendedores


def guardar_tareas(tareas):
    with open(DATA_FILE, "w") as file:
        for contacto in tareas:
            file.write(",".join(contacto) + "\n")


def ver_vendedores():
    def load_list(data=None):
        if data is None:
            data = leer_vendedores()

        for row in tree.get_children():
            tree.delete(row)

        for idx, item in enumerate(data):
            tree.insert("", "end", values=(idx + 1, *item, "Editar", "Eliminar"))

    def buscar():
        query = search_entry.get().lower()
        filtered_data = [v for v in vendedores if str(v[0]).lower() == query or v[0].lower().startswith(query)]
        load_list(filtered_data)

    def editar_vendedor(vendedor):
        def guardar():
            new_nombre = nuevo_nombre.get() or vendedor[0]
            new_telefono = nuevo_telefono.get() or vendedor[1]
            new_email = nuevo_email.get() or vendedor[2]

            # Actualizar el vendedor
            index = vendedores.index(vendedor)
            vendedores[index] = (new_nombre, new_telefono, new_email)
            guardar_tareas(vendedores)
            messagebox.showinfo("Vendedor Editado", "El vendedor ha sido editado correctamente")
            window_editar.destroy()
            load_list()

        window_editar = tk.Toplevel(root)
        window_editar.title("Editar Vendedor")
        window_editar.geometry("400x300")

        tk.Label(window_editar, text="Nombre:").pack()
        nuevo_nombre = tk.Entry(window_editar)
        nuevo_nombre.insert(0, vendedor[0])
        nuevo_nombre.pack()

        tk.Label(window_editar, text="Teléfono:").pack()
        nuevo_telefono = tk.Entry(window_editar)
        nuevo_telefono.insert(0, vendedor[1])
        nuevo_telefono.pack()

        tk.Label(window_editar, text="Email:").pack()
        nuevo_email = tk.Entry(window_editar)
        nuevo_email.insert(0, vendedor[2])
        nuevo_email.pack()

        tk.Button(window_editar, text="Guardar", command=guardar).pack(pady=10)

    def eliminar_vendedor(vendedor):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este vendedor?"):
            index = vendedores.index(vendedor)
            vendedores.pop(index)
            guardar_tareas(vendedores)
            messagebox.showinfo("Vendedor Eliminado", "El vendedor ha sido eliminado correctamente")
            load_list()

    window_ver_vendedores = tk.Toplevel(root)
    window_ver_vendedores.title("Ver Vendedores")
    window_ver_vendedores.geometry("600x400")
    global vendedores
    vendedores = leer_vendedores()

    # Campo de búsqueda
    search_frame = tk.Frame(window_ver_vendedores)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Buscar (ID o Nombre):").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT)
    tk.Button(search_frame, text="Buscar", command=buscar).pack(side=tk.LEFT)

    columns = ("ID", "Nombre", "Teléfono", "Email", "Acciones", "Eliminar")
    tree = ttk.Treeview(window_ver_vendedores, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    tree.pack(fill=tk.BOTH, expand=True)

    for idx, vendedor in enumerate(vendedores):
        tree.insert("", "end", values=(idx + 1, *vendedor, "Editar", "Eliminar"))

    def on_item_click(event):
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            row_id = tree.identify_row(event.y)
            col_id = tree.identify_column(event.x)
            selected_item = tree.item(row_id)["values"]
            if col_id == "#5":  # Columna "Editar"
                editar_vendedor(vendedores[selected_item[0] - 1])
            elif col_id == "#6":  # Columna "Eliminar"
                eliminar_vendedor(vendedores[selected_item[0] - 1])

    tree.bind("<Button-1>", on_item_click)

    load_list()


def agregar_vendedores():
    def agregar():
        vnombre = nombre.get()
        vtelefono = telefono.get()
        vemail = email.get()

        if not vnombre or not vtelefono or not vemail:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        with open(DATA_FILE, "a") as file:
            file.write(f"{vnombre},{vtelefono},{vemail}\n")
            messagebox.showinfo("Tarea Agregada", "El vendedor fue agregado exitosamente")
            window_agregar_vendedor.destroy()

    window_agregar_vendedor = tk.Toplevel(root)
    window_agregar_vendedor.title("Agregar Vendedores")
    window_agregar_vendedor.geometry("450x300")

    tk.Label(window_agregar_vendedor, text="Nombre:").grid(row=0, column=0)
    nombre = tk.Entry(window_agregar_vendedor)
    nombre.grid(row=0, column=1)

    tk.Label(window_agregar_vendedor, text="Teléfono:").grid(row=1, column=0)
    telefono = tk.Entry(window_agregar_vendedor)
    telefono.grid(row=1, column=1)

    tk.Label(window_agregar_vendedor, text="Email:").grid(row=2, column=0)
    email = tk.Entry(window_agregar_vendedor)
    email.grid(row=2, column=1)

    tk.Button(window_agregar_vendedor, text="Agregar", command=agregar).grid(row=3, columnspan=2)


# MENU PRINCIPAL
root = tk.Tk()
root.title("Ventana Principal")
root.geometry("500x500")
root.configure(bg="#2E2E2E")

titulo = tk.Label(root, text="Punto de Venta", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(pady=20)

# Crear botones
buttons = [
    ("Agregar Vendedores", agregar_vendedores),
    ("Ver Vendedores", ver_vendedores),
    ("Salir", root.quit)
]

for (text, command) in buttons:
    button = tk.Button(frame, text=text, command=command, bg="#007BFF", fg="#FFFFFF", width=25, height=2)
    button.pack(pady=5)

root.mainloop()