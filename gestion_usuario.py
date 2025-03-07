import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk, filedialog

# ---------------------------Ventana Principal para gestion de USUARIOS

def show_gestion_usuarios():
    def encriptar_contraseña(contraseña):
        return contraseña

    # Función para cargar usuarios desde el archivo
    def cargar_usuarios():
        usuarios = {}
        try:
            with open("usuarios.txt", "r") as file:
                for line in file:
                    id_usuario, nombre_usuario, contraseña, rol = line.strip().split(", ")
                    usuarios[id_usuario] = {
                        "nombre_usuario": nombre_usuario,
                        "contraseña": contraseña,
                        "rol": rol
                    }
        except FileNotFoundError:
            pass  # Si el archivo no existe aún, se maneja sin errores
        return usuarios

    # Función para guardar usuarios en el archivo
    def guardar_usuarios(usuarios):
        with open("usuarios.txt", "w") as file:
            for id_usuario, datos in usuarios.items():
                file.write(f"{id_usuario}, {datos['nombre_usuario']}, {datos['contraseña']}, {datos['rol']}\n")

    # Función para registrar un nuevo usuario
    def registrar_usuario():
        id_usuario = entry_id.get()
        nombre_usuario = entry_nombre.get()
        contrasena = entry_contrasena.get()
        rol = combo_rol.get()

        if not id_usuario or not nombre_usuario or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuarios = cargar_usuarios()

        # Verificar si el ID de usuario ya existe
        if id_usuario in usuarios:
            messagebox.showerror("Error", "El ID de usuario ya existe.")
            return

        # Encriptar la contraseña
        contrasena_encriptada = encriptar_contraseña(contrasena)

        # Registrar el nuevo usuario
        usuarios[id_usuario] = {
            "nombre_usuario": nombre_usuario,
            "contraseña": contrasena_encriptada,
            "rol": rol
        }

        # Guardar los usuarios en el archivo
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Usuario registrado con éxito")

    # Función para modificar un usuario existente
    def modificar_usuario():
        id_usuario = entry_id.get()
        nombre_usuario = entry_nombre.get()
        contrasena = entry_contrasena.get()
        rol = combo_rol.get()

        if not id_usuario or not nombre_usuario or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuarios = cargar_usuarios()

        # Verificar si el ID de usuario existe
        if id_usuario not in usuarios:
            messagebox.showerror("Error", "El ID de usuario no existe.")
            return

        # Encriptar la nueva contraseña
        contrasena_encriptada = encriptar_contraseña(contrasena)

        # Modificar la información del usuario
        usuarios[id_usuario] = {
            "nombre_usuario": nombre_usuario,
            "contraseña": contrasena_encriptada,
            "rol": rol
        }

        # Guardar los usuarios modificados en el archivo
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Usuario modificado con éxito.")

    # Función para eliminar un usuario
    def eliminar_usuario():
        id_usuario = entry_id.get()

        if not id_usuario:
            messagebox.showerror("Error", "El ID de usuario es obligatorio.")
            return

        usuarios = cargar_usuarios()

        # Verificar si el ID de usuario existe
        if id_usuario not in usuarios:
            messagebox.showerror("Error", "El ID de usuario no existe.")
            return

        # Eliminar el usuario
        del usuarios[id_usuario]

        # Guardar los usuarios restantes en el archivo
        guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")

    # Función para autenticar a un usuario
    def autenticar_usuario():
        id_usuario = entry_id.get()
        contrasena = entry_contrasena.get()

        if not id_usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuarios = cargar_usuarios()

        # Verificar si el ID de usuario existe
        if id_usuario not in usuarios:
            messagebox.showerror("Error", "El ID de usuario no existe.")
            return

        # Verificar la contraseña
        if usuarios[id_usuario]["contraseña"] != encriptar_contraseña(contrasena):
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return

        messagebox.showinfo("Éxito", f"Bienvenido, {usuarios[id_usuario]['nombre_usuario']}.")

  # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("300x300")
    ventana.configure(bg="#2E2E2E")

    # Definir elementos de la interfaz
    tk.Label(ventana, text="ID de Usuario:", fg="white", background="#2E2E2E").grid(row=0, column=0)
    entry_id = tk.Entry(ventana)
    entry_id.grid(row=0, column=1)

    tk.Label(ventana, text="Nombre de Usuario:", fg="white", background="#2E2E2E").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana, text="Contraseña:", fg="white", background="#2E2E2E").grid(row=2, column=0)
    entry_contrasena = tk.Entry(ventana, show="*")
    entry_contrasena.grid(row=2, column=1)

    tk.Label(ventana, text="Rol:", fg="white", background="#2E2E2E").grid(row=3, column=0)
    combo_rol = ttk.Combobox(ventana, values=["administrador", "usuario regular"])
    combo_rol.grid(row=3, column=1)

    # Botones para registrar, modificar, eliminar, autenticar
    tk.Button(ventana, text="Registrar Usuario", command=registrar_usuario).grid(row=4, column=0)
    tk.Button(ventana, text="Modificar Usuario", command=modificar_usuario).grid(row=4, column=1)
    tk.Button(ventana, text="Eliminar Usuario", command=eliminar_usuario).grid(row=5, column=0)
    tk.Button(ventana, text="Iniciar Sesión", command=autenticar_usuario).grid(row=5, column=1)


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
        ("Registro de Facturas",show_gestion_usuarios ,button_edit_bg),
        ("Salir", user_window.quit, "#007BFF")
    ]
    for (text, command, bg_color) in buttons:
        button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=button_fg, width=25, height=2)
        button.pack(pady=5)

        button.bind("<Enter>", on_enter)

        button.bind("<Leave>", on_leave)