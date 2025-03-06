import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog

# instalar calendario pip install tkcalendar view/toolwindows/terminal
tree = ttk.Treeview
# donde se guardara
DATA_FILE = "tareas.txt"
DATA_FILE_PRODDUCTOS = "productos.txt"
DATE_FILE_VENDEDORES = "vendedores.txt"
import re


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

#LEER, GUARDAR Y BUSCAR PRODUCTOS
def leer_productos():
    if not os.path.exists(DATA_FILE_PRODDUCTOS):
        return []
    productos = []
    with open(DATA_FILE_PRODDUCTOS, "r") as file:
        for line in file:
            codigo, nombre, precio, stock = line.strip().split(",")
            productos.append((codigo, nombre, precio, stock))
    return productos

def guardar_productos(productos):
    with open(DATA_FILE_PRODDUCTOS, "w") as file:
        for producto in productos:
            file.write(",".join(producto) + "\n")

def ResultBusqueda(productos=[], pal_buscar="", par_busqueda=0, ):
    resutl = [producto for producto in productos if re.match(f".*{pal_buscar}", producto[par_busqueda], re.IGNORECASE)]
    return resutl

#LEER, GUARDAR Y BUSCAR VENDEDORES
def leer_vendedores():
    if not os.path.exists(DATE_FILE_VENDEDORES):
        return []
    vendedores = []
    with open(DATE_FILE_VENDEDORES, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 4:
                id_vendedor, nombre, telefono, email = parts
                vendedores.append((int(id_vendedor), nombre, telefono, email))
    return vendedores


def guardar_vendedores(vendedores):
    with open(DATE_FILE_VENDEDORES, "w") as file:
        for vendedor in vendedores:
            file.write(f"{vendedor[0]},{vendedor[1]},{vendedor[2]},{vendedor[3]}\n")

def generar_id():
    vendedores = leer_vendedores()
    if len(vendedores) == 0:
        return 1
    else:
        return len(vendedores) + 1


def BuscarVendedores(vendedores, pal_buscar, par_busqueda):
    resultado = []

    print(f"Buscando: {pal_buscar} en campo {par_busqueda}")

    for vendedor in vendedores:
        if par_busqueda == 0:
            if str(vendedor[0]) == pal_buscar:
                resultado.append(vendedor)
        elif par_busqueda == 1:
            if re.search(f".*{pal_buscar}.*", vendedor[1], re.IGNORECASE):
                resultado.append(vendedor)
        else:
            pass

    return resultado

# ---------------------------Ventana Principal para gestion de vendedores
def show_gestion_vendedores():
    def ocultar_indicador():
        ingresar_indicador.config(bg="#0477BF")
        gestionar_indicador.config(bg="#0477BF")

    def mostrar_indicador(indicador, frame):
        ocultar_indicador()
        indicador.config(bg="#D97A07")
        frame.tkraise()

    # Ajustar ventana
    window_gestion_vendedores = tk.Toplevel(root)
    window_gestion_vendedores.title("Gestión de Vendedores")
    window_gestion_vendedores.geometry("850x360")
    window_gestion_vendedores.configure(bg="#2E2E2E")

    con_menu = tk.Frame(window_gestion_vendedores, background="#0477BF")
    con_menu.pack(fill=tk.X)
    con_menu.pack_propagate(False)
    con_menu.configure(height=40)

    # Pestaña 1
    btn_ingresar = tk.Button(con_menu, text="Ingresar", font=('Bold', 10), bd=0, background="#0477BF",
                             command=lambda: mostrar_indicador(ingresar_indicador, con_add_vendedor))
    btn_ingresar.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ingresar_indicador = tk.Label(con_menu, text=' ', bg='#D97A07')
    ingresar_indicador.place(x=10, y=35, width=55, height=10)

    # Pestaña 2
    btn_gestionar = tk.Button(con_menu, text="Gestionar Vendedores", font=('Bold', 10), bd=0, background="#0477BF",
                              command=lambda: mostrar_indicador(gestionar_indicador, con_gestion_vendedor))
    btn_gestionar.pack(side=tk.LEFT, fill=tk.Y)
    gestionar_indicador = tk.Label(con_menu, text=' ', bg='#0477BF')
    gestionar_indicador.place(x=73.25, y=35, width=128, height=10)

    margin_x = 100
    con_add_vendedor = tk.Frame(window_gestion_vendedores, background="#2E2E2E")
    con_add_vendedor.place(x=0, y=40, width=850, height=320)

    lbl_margin_y = tk.Label(con_add_vendedor, text="", bg="#2E2E2E")
    lbl_margin_y.pack(anchor="w", pady=4)

    lbl_nombre = tk.Label(con_add_vendedor, text="Nombre del Vendedor: ", fg="white", background="#2E2E2E")
    lbl_nombre.pack(anchor="w", padx=margin_x)
    nombre_vendedor = tk.Entry(con_add_vendedor)
    nombre_vendedor.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_telefono = tk.Label(con_add_vendedor, text="Télefono del Vendedor: ", fg="white", background="#2E2E2E")
    lbl_telefono.pack(anchor="w", padx=margin_x)
    telefono_vendedor = tk.Entry(con_add_vendedor)
    telefono_vendedor.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_email = tk.Label(con_add_vendedor, text="Email del Vendedor: ", fg="white", background="#2E2E2E")
    lbl_email.pack(anchor="w", padx=margin_x)
    email_vendedor = tk.Entry(con_add_vendedor)
    email_vendedor.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    btn_agregar = tk.Button(con_add_vendedor, text="Agregar Vendedor",
                            command=lambda: agregar_vendedor(nombre_vendedor, telefono_vendedor,
                                                             email_vendedor, window_gestion_vendedores))
    btn_agregar.pack(side='left', padx=margin_x)

    btn_cancelar = tk.Button(con_add_vendedor, text="Cancelar")
    btn_cancelar.pack(side='right', padx=margin_x)

    def buscar():
        if (no_vendedor.get() == ""):
            load_list()
        else:
            if (lista_menu.get() == "Buscar por:"):
                messagebox.showerror("Error", "Por favor seleccione un parámetro de búsqueda")
            else:
                par_busqueda = -1
                if (lista_menu.get() == "ID"):
                    par_busqueda = 0
                    pal_buscar = str(no_vendedor.get())
                elif (lista_menu.get() == "Nombre"):
                    par_busqueda = 1
                    pal_buscar = no_vendedor.get()

                coincidencias = BuscarVendedores(vendedores, pal_buscar, par_busqueda)

                for i in tree.get_children():
                    tree.delete(i)

                for vendedor in coincidencias:
                    tree.insert("", tk.END, values=vendedor)
    #FUNCION PARA EDITAR
    def editar_vendedor():
        selected_items = tree.selection()
        if len(selected_items) == 0:
            messagebox.showwarning("Editar Vendedor", "Por favor seleccione un vendedor para editar")
            return

        item = tree.item(selected_items[0], 'values')
        id_vendedor, nombre, telefono, email = item

        ventana_edicion = tk.Toplevel(root)
        ventana_edicion.title("Editar Vendedor")
        ventana_edicion.geometry("400x250")
        ventana_edicion.configure(bg="#2E2E2E")

        lbl_nombre = tk.Label(ventana_edicion, text="Nombre del Vendedor: ", fg="white", bg="#2E2E2E")
        lbl_nombre.pack(anchor="w", padx=10, pady=5)
        entry_nombre = tk.Entry(ventana_edicion)
        entry_nombre.insert(0, nombre)
        entry_nombre.pack(anchor="w", padx=10, pady=5)

        lbl_telefono = tk.Label(ventana_edicion, text="Télefono del Vendedor: ", fg="white", bg="#2E2E2E")
        lbl_telefono.pack(anchor="w", padx=10, pady=5)
        entry_telefono = tk.Entry(ventana_edicion)
        entry_telefono.insert(0, telefono)
        entry_telefono.pack(anchor="w", padx=10, pady=5)

        lbl_email = tk.Label(ventana_edicion, text="Email del Vendedor: ", fg="white", bg="#2E2E2E")
        lbl_email.pack(anchor="w", padx=10, pady=5)
        entry_email = tk.Entry(ventana_edicion)
        entry_email.insert(0, email)
        entry_email.pack(anchor="w", padx=10, pady=5)

        def actualizar_vendedor():
            nuevo_nombre = entry_nombre.get()
            nuevo_telefono = entry_telefono.get()
            nuevo_email = entry_email.get()

            if not nuevo_nombre or not nuevo_telefono or not nuevo_email:
                messagebox.showerror("Error", "Por favor llenar todos los campos")
                return

            if not nuevo_telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe ser un número válido.")
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
                messagebox.showerror("Error", "El email debe tener un formato válido.")
                return

            vendedores = leer_vendedores()
            for vendedor in vendedores:
                if vendedor[3] == nuevo_email and str(vendedor[0]) != str(id_vendedor):
                    messagebox.showerror("Error", "El correo electrónico ya está registrado.")
                    return

            vendedores_actualizados = []
            for vendedor in vendedores:
                if str(vendedor[0]) == str(id_vendedor):
                    vendedores_actualizados.append((id_vendedor, nuevo_nombre, nuevo_telefono, nuevo_email))
                else:
                    vendedores_actualizados.append(vendedor)

            guardar_vendedores(vendedores_actualizados)

            messagebox.showinfo("Vendedor Actualizado", "Los datos del vendedor se actualizaron correctamente.")
            ventana_edicion.destroy()
            load_list()

        btn_actualizar = tk.Button(ventana_edicion, text="Actualizar", command=actualizar_vendedor)
        btn_actualizar.pack(side='left', padx=20, pady=10)

        btn_cancelar = tk.Button(ventana_edicion, text="Cancelar", command=ventana_edicion.destroy)
        btn_cancelar.pack(side='right', padx=20, pady=10)

    def eliminar():
        selected_items = tree.selection()

        if len(selected_items) == 0:
            messagebox.showwarning("Eliminar Vendedor", "Por favor seleccione un vendedor para eliminarlo")
            return

        item_id = tree.item(selected_items[0], 'values')[0]

        ventana_confirmacion_eliminar(item_id)

    def ventana_confirmacion_eliminar(item_id):
        ventana_confirmacion = tk.Toplevel(root)
        ventana_confirmacion.title("Confirmar eliminación")
        ventana_confirmacion.geometry("300x150")
        ventana_confirmacion.configure(bg="#2E2E2E")

        mensaje = f"¿Desea eliminar el vendedor con ID: {item_id}?"
        label_mensaje = tk.Label(ventana_confirmacion, text=mensaje, fg="white", bg="#2E2E2E")
        label_mensaje.pack(pady=20)

        btn_confirmar = tk.Button(ventana_confirmacion, text="Eliminar",
                                  command=lambda: confirmar_eliminacion(item_id, ventana_confirmacion))
        btn_confirmar.pack(side=tk.LEFT, padx=20)

        btn_cancelar = tk.Button(ventana_confirmacion, text="Cancelar", command=ventana_confirmacion.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=20)

    def confirmar_eliminacion(item_id, ventana_confirmacion):
        vendedores = leer_vendedores()

        vendedores_filtrados = [vendedor for vendedor in vendedores if str(vendedor[0]) != str(item_id)]

        guardar_vendedores(vendedores_filtrados)

        load_list()

        ventana_confirmacion.destroy()

        messagebox.showinfo("Eliminar", f"Vendedor con ID {item_id} eliminado con éxito.")


    def load_list():
        for i in tree.get_children():
            tree.delete(i)
        for vendedor in leer_vendedores():
            tree.insert("", tk.END, values=vendedor)
    con_gestion_vendedor = tk.Frame(window_gestion_vendedores, background='#2E2E2E')
    con_gestion_vendedor.place(x=0, y=40, width=850, height=320)
    vendedores = leer_vendedores()

    label1 = tk.Label(con_gestion_vendedor, text="Buscar Vendedor: ", background="#2E2E2E", fg="white")
    label1.grid(row=0, column=0, padx=25, pady=5)
    no_vendedor = tk.Entry(con_gestion_vendedor)
    no_vendedor.grid(row=0, column=1, padx=0, pady=5)
    lista_opciones = ["ID", "Nombre"]
    lista_menu = tk.StringVar(con_gestion_vendedor)
    lista_menu.set("Buscar por:")
    checklist = tk.OptionMenu(con_gestion_vendedor, lista_menu, *lista_opciones)
    checklist.grid(row=0, column=2, padx=25, pady=5)
    button2 = tk.Button(con_gestion_vendedor, text="Buscar", command=buscar)
    button2.grid(row=0, column=3, pady=5, padx=25)

    columnas = ('Id', 'Nombre', 'Télefono', 'Email')
    tree = ttk.Treeview(con_gestion_vendedor, columns=columnas, show='headings')
    tree.heading('Id', text='Id')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Télefono', text='Télefono')
    tree.heading('Email', text='Email')
    tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
    srollbar = ttk.Scrollbar(con_gestion_vendedor, orient='vertical', command=tree.yview)
    tree.config(yscrollcommand=srollbar.set)
    srollbar.grid(row=1, column=4, sticky='ns')

    con_gestion_vendedor.grid_rowconfigure(1, weight=0)
    con_gestion_vendedor.grid_columnconfigure(1, weight=1)

    btn_editar = tk.Button(con_gestion_vendedor, text="Editar", command=editar_vendedor)
    btn_editar.grid(row=2, column=0, padx=5, pady=5)

    btn_eliminar = tk.Button(con_gestion_vendedor, text="Eliminar", command=eliminar)
    btn_eliminar.grid(row=2, column=1, padx=5, pady=5)
    load_list()

    con_gestion_vendedores = tk.Frame(window_gestion_vendedores, background='#2E2E2E')
    con_gestion_vendedores.place(x=0, y=40, width=850, height=320)
    con_add_vendedor.tkraise()


def agregar_vendedor(nombre: any = None, telefono: any = None, email: any = None, ventana: any = None):
    if nombre.get() == "" or telefono.get() == "" or email.get() == "":
        messagebox.showerror("Error", "Por favor llenar todos los campos")
        return

    if not telefono.get().isdigit():
        messagebox.showerror("Error", "El teléfono debe ser un número válido.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email.get()):
        messagebox.showerror("Error", "El email debe tener un formato válido.")
        return

    vendedores = leer_vendedores()

    email_normalizado = email.get().strip().lower()
    for vendedor in vendedores:
        if vendedor[3].strip().lower() == email_normalizado:
            messagebox.showerror("Error", "El correo electrónico ya está registrado.")
            return

    try:
        id_vendedor = generar_id()

        with open(DATE_FILE_VENDEDORES, "a") as file:
            file.write(f"{id_vendedor},{nombre.get()},{telefono.get()},{email.get()}\n")

        messagebox.showinfo("Vendedor Agregado", f"Vendedor agregado correctamente")

        # Limpiar los campos
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)
        email.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Verifique los campos ingresados. Detalle del error: {e}")


# ---------------------------Ventana Principal para gestion de productos
def show_gestion_productos():
    def ocultar_indicador():
        ingresar_indicador.config(bg="#0477BF")
        gestionar_indicador.config(bg="#0477BF")

    def mostrar_indicador(indicador, frame):
        ocultar_indicador()
        indicador.config(bg="#D97A07")
        frame.tkraise()

    window_gestion_productos = tk.Toplevel(root)
    window_gestion_productos.title("Gestión de Productos")
    window_gestion_productos.geometry("850x360")
    window_gestion_productos.configure(bg="#2E2E2E")

    con_menu = tk.Frame(window_gestion_productos, background="#0477BF")
    con_menu.pack(fill=tk.X)
    con_menu.pack_propagate(False)
    con_menu.configure(height=40)

    btn_ingresar = tk.Button(con_menu, text="Ingresar", font=('Bold', 10), bd=0, background="#0477BF",
                             command=lambda: mostrar_indicador(ingresar_indicador, con_add_product))
    btn_ingresar.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ingresar_indicador = tk.Label(con_menu, text='', bg='#D97A07')
    ingresar_indicador.place(x=10, y=35, width=55, height=10)

    btn_gestionar = tk.Button(con_menu, text="Gestionar Productos", font=('Bold', 10), bd=0, background="#0477BF",
                              command=lambda: mostrar_indicador(gestionar_indicador, con_gestion_productos))
    btn_gestionar.pack(side=tk.LEFT, fill=tk.Y)
    gestionar_indicador = tk.Label(con_menu, text='', bg='#0477BF')
    gestionar_indicador.place(x=73.25, y=35, width=128, height=10)

    # Panel para Registrar productos
    margin_x = 100
    con_add_product = tk.Frame(window_gestion_productos, background="#2E2E2E")
    con_add_product.place(x=0, y=40, width=850, height=320)
    lbl_margin_y = tk.Label(con_add_product, text="", bg="#2E2E2E")
    lbl_margin_y.pack(anchor="w", pady=4)
    lbl_nombre = tk.Label(con_add_product, text="Codigo del Producto: ", fg="white", background="#2E2E2E")
    lbl_nombre.pack(anchor="w", padx=margin_x)
    codigo_producto = tk.Entry(con_add_product)
    codigo_producto.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_codigo = tk.Label(con_add_product, text="Nombre del Producto: ", fg="white", background="#2E2E2E")
    lbl_codigo.pack(anchor="w", padx=margin_x)
    nombre_producto = tk.Entry(con_add_product)
    nombre_producto.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_precio_u = tk.Label(con_add_product, text="Precio del Producto: ", fg="white", background="#2E2E2E")
    lbl_precio_u.pack(anchor="w", padx=margin_x)
    precio_producto = tk.Entry(con_add_product)
    precio_producto.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_stock = tk.Label(con_add_product, text="Stock del Producto: ", fg="white", background="#2E2E2E")
    lbl_stock.pack(anchor="w", padx=margin_x)
    stock_producto = tk.Entry(con_add_product)
    stock_producto.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    btn_agregar = tk.Button(con_add_product, text="Agregar Producto",
                            command=lambda: agregar_producto(codigo_producto, nombre_producto, precio_producto,
                                                             stock_producto, window_gestion_productos))
    btn_agregar.pack(side='left', padx=margin_x)

    btn_cancelar = tk.Button(con_add_product, text="Cancelar")
    btn_cancelar.pack(side='right', padx=margin_x)

    # Panel para Gestionar Productos
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

                coincidencias = ResultBusqueda(productos, no_tarea.get(), par_busqueda)

                for i in tree.get_children():
                    tree.delete(i)
                for producto in coincidencias:
                    tree.insert("", tk.END, values=producto)

    def eliminar():
        lista_items_selec = []
        all_selected = tree.selection()
        for item in all_selected:
            item_values = tree.item(item, 'values')
            lista_items_selec.append(item_values[0])

        if len(lista_items_selec) == 0:
            messagebox.showwarning("Eliminar Producto", "Por favor seleccione producto uno para eliminar")
        else:
            confirmacion = messagebox.askyesno("Eliminar", f"¿Estas seguro de eliminar?")
            if confirmacion:
                indices_eliminar = [i for i, producto in enumerate(productos, start=0) if
                                    producto[0] in lista_items_selec]
                for e_producto in indices_eliminar:
                    productos.pop(e_producto)
                guardar_productos(productos)
                messagebox.showinfo("Eliminar", "Productos eliminados con exito.")
                load_list()

    def editar(n_codigo="", n_nombre="", n_precio="", n_stock="", ventana: any = None):
        if n_codigo == "" or n_nombre == "" or n_precio == "" or n_stock == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
        else:
            indice = -1
            for i, producto in enumerate(productos, start=0):
                if n_codigo == producto[0]:
                    indice = i
                    break

            l_producto = list(productos[indice])
            l_producto[0] = n_codigo
            l_producto[1] = n_nombre
            l_producto[2] = n_precio
            l_producto[3] = n_stock
            productos[indice] = tuple(l_producto)
            guardar_productos(productos)
            messagebox.showinfo("Editar tarea", "Producto Editado con exito")
            ventana.destroy()
            load_list()

    def editar_producto():
        lista_items_selec = []
        all_selected = tree.selection()
        for item in all_selected:
            item_values = tree.item(item, 'values')
            lista_items_selec.append(item_values)

        # print(lista_items_selec)

        if len(lista_items_selec) >= 2:
            messagebox.showwarning("Editar Producto", "Seleccione solo uno para editar")
        elif len(lista_items_selec) == 0:
            messagebox.showwarning("Editar Producto", "Por favor seleccione producto uno para editar")
        else:
            window_ingresar_productos = tk.Toplevel(root)
            window_ingresar_productos.title("Editar Productos")
            window_ingresar_productos.geometry("350x250")
            window_ingresar_productos.configure(bg="#2E2E2E")

            lbl_nombre = tk.Label(window_ingresar_productos, text="Codigo del Producto: ", fg="white",
                                  background="#2E2E2E")
            lbl_nombre.pack(anchor="w", padx=30)
            codigo_producto = tk.Entry(window_ingresar_productos)
            codigo_producto.delete(0, tk.END)
            codigo_producto.insert(0, lista_items_selec[0][0])
            codigo_producto.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_codigo = tk.Label(window_ingresar_productos, text="Nombre del Producto: ", fg="white",
                                  background="#2E2E2E")
            lbl_codigo.pack(anchor="w", padx=30)
            nombre_producto = tk.Entry(window_ingresar_productos)
            nombre_producto.delete(0, tk.END)
            nombre_producto.insert(0, lista_items_selec[0][1])
            nombre_producto.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_precio_u = tk.Label(window_ingresar_productos, text="Precio del Producto: ", fg="white",
                                    background="#2E2E2E")
            lbl_precio_u.pack(anchor="w", padx=30)
            precio_producto = tk.Entry(window_ingresar_productos)
            precio_producto.delete(0, tk.END)
            precio_producto.insert(0, lista_items_selec[0][2])
            precio_producto.pack(anchor="w", padx=30, pady=5, fill="x")

            lbl_stock = tk.Label(window_ingresar_productos, text="Nombre del Producto: ", fg="white",
                                 background="#2E2E2E")
            lbl_stock.pack(anchor="w", padx=30)
            stock_producto = tk.Entry(window_ingresar_productos)
            stock_producto.delete(0, tk.END)
            stock_producto.insert(0, lista_items_selec[0][3])
            stock_producto.pack(anchor="w", padx=30, pady=5, fill="x")

            btn_agregar = tk.Button(window_ingresar_productos, text="Editar Producto", command=lambda: editar(
                codigo_producto.get(),
                nombre_producto.get(),
                precio_producto.get(),
                stock_producto.get(),
                window_ingresar_productos
            ))
            btn_agregar.pack(side='left', padx=40)

            btn_cancelar = tk.Button(window_ingresar_productos, text="Cancelar",
                                     command=window_ingresar_productos.destroy)
            btn_cancelar.pack(side='right', padx=40)

    def load_list():
        for i in tree.get_children():
            tree.delete(i)
        for producto in leer_productos():
            tree.insert("", tk.END, values=producto)

    con_gestion_productos = tk.Frame(window_gestion_productos, background='#2E2E2E')
    con_gestion_productos.place(x=0, y=40, width=850, height=320)
    productos = leer_productos()

    label1 = tk.Label(con_gestion_productos, text="Buscar Tarea: ", background="#2E2E2E", fg="white")
    label1.grid(row=0, column=0, padx=25, pady=5)
    no_tarea = tk.Entry(con_gestion_productos)
    no_tarea.grid(row=0, column=1, padx=0, pady=5)
    lista_opciones = ["ID", "Nombre"]
    lista_menu = tk.StringVar(con_gestion_productos)
    lista_menu.set("Buscar por:")
    checklist = tk.OptionMenu(con_gestion_productos, lista_menu, *lista_opciones)
    checklist.grid(row=0, column=2, padx=25, pady=5)
    button2 = tk.Button(con_gestion_productos, text="Buscar", command=buscar)
    button2.grid(row=0, column=3, pady=5, padx=25)

    columnas = ('Codigo', 'Nombre', 'Precio', 'Stock')
    tree = ttk.Treeview(con_gestion_productos, columns=columnas, show='headings')
    tree.heading('Codigo', text='Codigo')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Precio', text='Precio')
    tree.heading('Stock', text='Stock')
    tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
    srollbar = ttk.Scrollbar(con_gestion_productos, orient='vertical', command=tree.yview)
    tree.config(yscrollcommand=srollbar.set)
    srollbar.grid(row=1, column=4, sticky='ns')

    con_gestion_productos.grid_rowconfigure(1, weight=0)
    con_gestion_productos.grid_columnconfigure(1, weight=1)

    btn_editar = tk.Button(con_gestion_productos, text="Editar", command=editar_producto)
    btn_editar.grid(row=2, column=0, padx=5, pady=5)

    btn_eliminar = tk.Button(con_gestion_productos, text="Eliminar", command=eliminar)
    btn_eliminar.grid(row=2, column=1, padx=5, pady=5)
    load_list()
    con_add_product.tkraise()


def agregar_producto(codigo: any = None, nombre: any = None, precio: any = None, stock: any = None,
                     ventana: any = None):
    if (codigo.get() == "" and nombre.get() == "" and precio.get() == "" and stock.get() == ""):
        messagebox.showerror("Error", "Todos los campos son requeridos")
        return

    try:
        with open(DATA_FILE_PRODDUCTOS, "a") as file:
            file.write(f"{codigo.get()},{nombre.get()},{float(precio.get())},{int(stock.get())}\n")
            messagebox.showinfo("Producto Agregado", "Producto agregado correctamente")

            codigo.delete(0, tk.END)
            nombre.delete(0, tk.END)
            precio.delete(0, tk.END)
            stock.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Verifique los campos ingresados.")

#HACIENDO EL MENU PRINCIPAL

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
    #("Gestión de Clientes", button_add_bg),
    ("Gestión de vendedores", show_gestion_vendedores, "#007BFF"),  # Azul genérico
    ("Gestión de Productos", show_gestion_productos, button_delete_bg),
   # ("Registro de Facturas", "#007BFF"),
    #("Gestión de Usuarios", button_edit_bg),
    ("Salir", root.quit, "#007BFF")
]
for (text, command, bg_color) in buttons:
    button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
    button.pack(pady=5)

    button.bind("<Enter>", on_enter)

    button.bind("<Leave>", on_leave)

root.mainloop()