import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog
import re

DATA_FILE_FACTURAS = "facturas.txt"
DATA_FILE_PRODDUCTOS = "productos.txt"

# ---------------------------Ventana Principal para gestion de Facturacion

def leer_facturas():
    if not os.path.exists(DATA_FILE_FACTURAS):
        return []
    productos = []
    with open(DATA_FILE_FACTURAS, "r") as file:
        for line in file:
            codigo, nombre, precio, stock = line.strip().split(",")
            productos.append((codigo, nombre, precio, stock))
    return productos

def leer_productos():
    if not os.path.exists(DATA_FILE_PRODDUCTOS):
        return []
    productos = []
    with open(DATA_FILE_PRODDUCTOS, "r") as file:
        for line in file:
            codigo, nombre, precio, stock = line.strip().split(",")
            productos.append((codigo, nombre, precio, stock))
    return productos

def ResultBusqueda(productos=[], pal_buscar="", par_busqueda=0, ):
    resutl = [producto for producto in productos if re.match(f".*{pal_buscar}", producto[par_busqueda], re.IGNORECASE)]
    return resutl

def guardar_productos(productos):
    with open(DATA_FILE_PRODDUCTOS, "w") as file:
        for producto in productos:
            file.write(",".join(producto) + "\n")

# MODULO DE FACTURACION________________________________________________________________________
def facturacion():
    def get_list_for_lisbox(tipo):
        try:
            result = []
            if not os.path.exists(f"{tipo}.txt"):
                return []
            with open(f"{tipo}.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    result.append(data[1])
            return result
        except:
            print("Error al obtener datos para el listbox")

    def ocultar_indicador():
        ingresar_indicador.config(bg="#0477BF")
        gestionar_indicador.config(bg="#0477BF")

    def mostrar_indicador(indicador, frame):
        ocultar_indicador()
        indicador.config(bg="#D97A07")
        frame.tkraise()

    def agregar_item_factura(item=-1, cantidad=-1):
        productos = leer_productos()
        existe = False
        indice = -1
        if cantidad <= 0:
            messagebox.showerror("Error", "Ingrese un numero mayor a cero para la cantidad del producto")
            return

        if len(lista_productos_factura) != 0:
            for i, buscar_item in enumerate(lista_productos_factura, start=0):
                if buscar_item[0] == productos[item][1]:
                    cantidad = int(buscar_item[1]) + cantidad
                    existe = True
                    indice = i
                    break
        if (cantidad <= int(productos[item][3])):
            total = 0
            if existe:
                aux_tuple = list(lista_productos_factura[indice])
                aux_tuple[1] = cantidad
                aux_tuple[3] = float(productos[item][2]) * cantidad
                lista_productos_factura[indice] = tuple(aux_tuple)
            else:
                lista_productos_factura.append(
                    (productos[item][1], cantidad, productos[item][2], float(productos[item][2]) * cantidad, item))

            for i in tree_factura.get_children():
                tree_factura.delete(i)

            for producto in lista_productos_factura:
                tree_factura.insert("", tk.END, values=producto)
                total += float(producto[3])
            lbl_total.config(text=f"Total : Q. {total}")
        else:
            messagebox.showerror("Sin Stock", "No hay suficiente stock")
        stock_producto.delete(0, tk.END)

    def agregar_factura(vendedor="", cliente="", productos=[]):
        if (vendedor == "" or cliente == "" or productos == "" or len(productos) == 0):
            messagebox.showerror("Error", "Falta campo que seleccionar o no hay items en la factura")
            return

        # try:
        total = 0
        string_productos = ""

        total_productos = leer_productos()
        for item_factura in productos:
            string_productos += f"{str(item_factura[1])} {item_factura[0]} | "
            total = total + float(item_factura[3])

            restar_stock = list(total_productos[int(item_factura[4])])
            restar_stock[3] = str(int(restar_stock[3]) - int(item_factura[1]))
            total_productos[int(item_factura[4])] = tuple(restar_stock)
        print(total_productos)
        guardar_productos(total_productos)

        with open(DATA_FILE_FACTURAS, "a") as file:
            file.write(f"{vendedor},{cliente},{string_productos},{total}\n")
            messagebox.showinfo("Facturas", "Factura Guardada con exito")

            lista_productos_factura.clear()
            for i in tree_factura.get_children():
                tree_factura.delete(i)
        # except :
        # messagebox.showerror("Error", "Verifique los campos ingresados.")

    def actualizar_item_factura(nombre_item="", nueva_cantidad=-1, window_edit: any = None):
        if (nombre_item == -1 or nueva_cantidad == -1):
            print("Error al bonter datos par editar item")
            return

        total_productos = leer_productos()
        stock = -1
        for get_stock in total_productos:
            if (get_stock[1] == nombre_item):
                stock = int(get_stock[3])

        for i, item in enumerate(lista_productos_factura, start=0):
            if item[0] == nombre_item:
                if (nueva_cantidad > stock):
                    messagebox.showerror("Error", "No hay suficiente stock")
                    break
                else:
                    if (nueva_cantidad == 0):
                        eliminar_item()
                        window_edit.destroy()
                        break
                    aux = list(item)
                    aux[1] = str(nueva_cantidad)
                    aux[3] = str(nueva_cantidad * float(item[2]))
                    lista_productos_factura[i] = tuple(aux)
                    for i in tree_factura.get_children(): tree_factura.delete(i)

                    total = 0
                    for producto in lista_productos_factura:
                        tree_factura.insert("", tk.END, values=producto)
                        total += float(producto[3])
                    lbl_total.config(text=f"Total : Q. {total}")
                    window_edit.destroy()
                    break

    def eliminar_item(event: any = None):
        nombre_producto = tree_factura.item(tree_factura.focus(), "values")[0]
        for i, item in enumerate(lista_productos_factura, start=0):
            if item[0] == nombre_producto:
                lista_productos_factura.pop(i)
                break
        total = 0

        for i in tree_factura.get_children(): tree_factura.delete(i)
        for producto in lista_productos_factura:
            tree_factura.insert("", tk.END, values=producto)
            total += float(producto[3])
        lbl_total.config(text=f"Total : Q. {total}")

    def ventana_item_factura(event):
        if tree_factura.focus():
            # print( tree_factura.item( tree_factura.focus(), "values" )[0] )
            nombre_producto = tree_factura.item(tree_factura.focus(), "values")[0]
            window_editar_producto_factura = tk.Toplevel(window_gestion_productos, background="#2E2E2E")
            window_editar_producto_factura.title("Editar Producto")
            window_editar_producto_factura.geometry("390x130")

            frame_edit = tk.Frame(window_editar_producto_factura, background="#2E2E2E")
            frame_edit.pack(pady=15)
            label_desc_edit = tk.Label(frame_edit, text="Ingrese la nueva cantidad(0 para eliminar): ",
                                       background="#2E2E2E", fg="white")
            label_desc_edit.pack(anchor=tk.W, pady=5)
            nueva_cantidad = tk.Entry(frame_edit)
            nueva_cantidad.pack(anchor=tk.W, pady=5)
            btn_actualizar_item = tk.Button(frame_edit, text="Actualizar",
                                            command=lambda: actualizar_item_factura(nombre_producto,
                                                                                    int(nueva_cantidad.get()),
                                                                                    window_editar_producto_factura))
            btn_actualizar_item.pack(pady=5)

    def mostrar_stock(value):
        total_productos = leer_productos()
        for producto in total_productos:
            if value == producto[1]:
                indicador_stock.config(text=f"Stock: {producto[3]}")

    window_gestion_productos = tk.Toplevel()
    window_gestion_productos.title("Gestión de Facturas")
    window_gestion_productos.geometry("880x620")
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

    btn_gestionar = tk.Button(con_menu, text="Ver Facturas", font=('Bold', 10), bd=0, background="#0477BF",
                              command=lambda: mostrar_indicador(gestionar_indicador, con_gestion_productos))
    btn_gestionar.pack(side=tk.LEFT, fill=tk.Y)
    gestionar_indicador = tk.Label(con_menu, text='', bg='#0477BF')
    gestionar_indicador.place(x=73.25, y=35, width=84, height=10)

    # Panel para Registrar facturas
    margin_x = 100
    con_add_product = tk.Frame(window_gestion_productos, background="#2E2E2E")
    con_add_product.place(x=0, y=40, width=850, height=580)
    lbl_margin_y = tk.Label(con_add_product, text="", bg="#2E2E2E")
    lbl_margin_y.pack(anchor="w", pady=2)

    lbl_nombre = tk.Label(con_add_product, text="Seleccione un Vendedor: ", fg="white", background="#2E2E2E")
    lbl_nombre.pack(anchor="w", padx=margin_x)
    lista_vendedores = get_list_for_lisbox("vendedores")
    opc_vendedores = tk.StringVar(con_add_product)
    checklist_vendedores = tk.OptionMenu(con_add_product, opc_vendedores, *lista_vendedores)
    checklist_vendedores.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_codigo = tk.Label(con_add_product, text="Seleccione un Cliente: ", fg="white", background="#2E2E2E")
    lbl_codigo.pack(anchor="w", padx=margin_x)
    lista_clientes = get_list_for_lisbox("clientes")
    opc_clientes = tk.StringVar(con_add_product)
    checklist_clientes = tk.OptionMenu(con_add_product, opc_clientes, *lista_clientes)
    checklist_clientes.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_precio_u = tk.Label(con_add_product, text="Seleccione Producto: ", fg="white", background="#2E2E2E")
    lbl_precio_u.pack(anchor="w", padx=margin_x)
    lista_productos = get_list_for_lisbox("productos")
    opc_productos = tk.StringVar(con_add_product)
    checklist_productos = tk.OptionMenu(con_add_product, opc_productos, *lista_productos, command=mostrar_stock)
    checklist_productos.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lbl_stock = tk.Label(con_add_product, text="Cantidad: ", fg="white", background="#2E2E2E")
    lbl_stock.pack(anchor="w", padx=margin_x)
    stock_producto = tk.Entry(con_add_product)
    stock_producto.pack(anchor="w", padx=margin_x, pady=5, fill="x")

    lista_productos_factura = []

    frame_stock = tk.Frame(con_add_product, background="#2E2E2E")
    frame_stock.pack(anchor='w', padx=margin_x, pady=5)
    btn_agregar = tk.Button(frame_stock, text="Agregar",
                            command=lambda: agregar_item_factura(int(lista_productos.index(opc_productos.get())),
                                                                 int(stock_producto.get())))
    # btn_agregar.pack( anchor='w', padx=margin_x , pady=5 )
    btn_agregar.pack(side=tk.LEFT)
    indicador_stock = tk.Label(frame_stock, text="Stock: ", fg="white", background="#2E2E2E", font=('bold', 15))
    indicador_stock.pack(side=tk.LEFT, padx=20)

    frame_f = tk.Frame(con_add_product)
    frame_f.pack(anchor="w", fill="x")

    columnas_factura = ('Producto', 'Cantidad', 'PrecioU', 'Subtotal')
    tree_factura = ttk.Treeview(frame_f, columns=columnas_factura, show='headings')
    tree_factura.heading('Producto', text='Producto')
    tree_factura.heading('Cantidad', text='Cantidad')
    tree_factura.heading('PrecioU', text="Precio Unitario")
    tree_factura.heading('Subtotal', text='Subtotal')
    tree_factura.pack(side=tk.LEFT, fill="x", expand=True)
    srollbar_factura = ttk.Scrollbar(frame_f, orient='vertical', command=tree_factura.yview)
    tree_factura.config(yscrollcommand=srollbar_factura.set)
    srollbar_factura.pack(side=tk.LEFT)
    tree_factura.bind('<Double-Button-1>', ventana_item_factura)
    tree_factura.bind('<Delete>', eliminar_item)

    lbl_total = tk.Label(con_add_product, text="Total : Q. ", fg="white", background="#2E2E2E")
    lbl_total.pack()

    btn_save_factura = tk.Button(con_add_product, text="Guardar", command=lambda: agregar_factura(opc_vendedores.get(),
                                                                                                  opc_clientes.get(),
                                                                                                  lista_productos_factura))
    btn_save_factura.pack(pady=5)

    # Panel para visualizar las facturas
    def buscar():
        if (no_tarea.get() == ""):
            load_list()
        else:
            if (lista_menu.get() == "Buscar por:"):
                messagebox.showerror("Error", "Por favor seleccione un parametro de busqueda")
            else:
                par_busqueda = -1
                if (lista_menu.get() == "Vendedor"):
                    par_busqueda = 0
                elif (lista_menu.get() == "Cliente"):
                    par_busqueda = 1

                coincidencias = ResultBusqueda(facturas, no_tarea.get(), par_busqueda)

                for i in tree.get_children():
                    tree.delete(i)
                for producto in coincidencias:
                    tree.insert("", tk.END, values=producto)

    def load_list():
        for i in tree.get_children():
            tree.delete(i)
        for producto in leer_facturas():
            tree.insert("", tk.END, values=producto)

    con_gestion_productos = tk.Frame(window_gestion_productos, background='#2E2E2E')
    con_gestion_productos.place(x=0, y=40, width=850, height=570)

    label1 = tk.Label(con_gestion_productos, text="Buscar Tarea: ", background="#2E2E2E", fg="white")
    label1.grid(row=0, column=0, padx=25, pady=5)
    no_tarea = tk.Entry(con_gestion_productos)
    no_tarea.grid(row=0, column=1, padx=0, pady=5)
    lista_opciones = ["Vendedor", "Cliente"]
    lista_menu = tk.StringVar(con_gestion_productos)
    lista_menu.set("Buscar por:")
    checklist = tk.OptionMenu(con_gestion_productos, lista_menu, *lista_opciones)
    checklist.grid(row=0, column=2, padx=25, pady=5)
    button2 = tk.Button(con_gestion_productos, text="Buscar", command=buscar)
    button2.grid(row=0, column=3, pady=5, padx=25)

    facturas = leer_facturas()
    columnas = ('Vendedor', 'Cliente', 'Productos', 'Total')
    tree = ttk.Treeview(con_gestion_productos, columns=columnas, show='headings')
    tree.heading('Vendedor', text='Vendedor')
    tree.heading('Cliente', text='Cliente')
    tree.heading('Productos', text='Productos')
    tree.heading('Total', text='Total')
    tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
    srollbar = ttk.Scrollbar(con_gestion_productos, orient='vertical', command=tree.yview)
    tree.config(yscrollcommand=srollbar.set)
    srollbar.grid(row=1, column=4, sticky='ns')

    con_gestion_productos.grid_rowconfigure(1, weight=0)
    con_gestion_productos.grid_columnconfigure(1, weight=1)

    load_list()
    con_add_product.tkraise()


def ventana_usuario(nombre_usuario):
    user_window = tk.Toplevel()
    user_window.title("Panel de Usuario")
    user_window.geometry("500x300")
    user_window.configure(bg="#2E2E2E")

    # AGREGANDO EL TITULO
    titulo = tk.Label(user_window, text=f"Bienvenid@, {nombre_usuario}", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    # Crear un marco para los botones
    frame = tk.Frame(user_window, bg="#2E2E2E")
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
        ("Registro de Facturas",facturacion ,button_edit_bg),
        ("Salir", user_window.quit, "#007BFF")
    ]
    for (text, command, bg_color) in buttons:
        button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
        button.pack(pady=5)

        button.bind("<Enter>", on_enter)

        button.bind("<Leave>", on_leave)