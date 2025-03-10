import tkinter as tk
from tkinter import messagebox

# Diccionario global para almacenar los usuarios
usuarios = {}

# Función para registrar un usuario
def registrar_usuario():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    telefono = entry_telefono.get()
    fecha = entry_fecha.get()
    id_usuario = entry_id.get()

    # Verificamos si el id_usuario ya existe
    if id_usuario in usuarios:
        messagebox.showerror("Error", f"El usuario con ID {id_usuario} ya existe.")
        return

    # Registramos el usuario
    usuarios[id_usuario] = {
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'fecha': fecha
    }
    messagebox.showinfo("Éxito", f"Usuario {nombre} {apellido} registrado con éxito.")

# Función para eliminar un usuario
def eliminar_usuario():
    id_usuario = entry_id.get()

    # Verificamos si el usuario existe
    if id_usuario in usuarios:
        del usuarios[id_usuario]
        messagebox.showinfo("Éxito", f"Usuario con ID {id_usuario} eliminado con éxito.")
    else:
        messagebox.showerror("Error", f"Usuario con ID {id_usuario} no encontrado.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Usuarios")

# Crear y colocar etiquetas y campos de texto en la ventana
label_nombre = tk.Label(ventana, text="Nombre:")
label_nombre.grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

label_apellido = tk.Label(ventana, text="Apellido:")
label_apellido.grid(row=1, column=0, padx=10, pady=5)
entry_apellido = tk.Entry(ventana)
entry_apellido.grid(row=1, column=1, padx=10, pady=5)

label_telefono = tk.Label(ventana, text="Teléfono:")
label_telefono.grid(row=2, column=0, padx=10, pady=5)
entry_telefono = tk.Entry(ventana)
entry_telefono.grid(row=2, column=1, padx=10, pady=5)

label_fecha = tk.Label(ventana, text="Fecha:")
label_fecha.grid(row=3, column=0, padx=10, pady=5)
entry_fecha = tk.Entry(ventana)
entry_fecha.grid(row=3, column=1, padx=10, pady=5)

label_id = tk.Label(ventana, text="ID del Usuario:")
label_id.grid(row=4, column=0, padx=10, pady=5)
entry_id = tk.Entry(ventana)
entry_id.grid(row=4, column=1, padx=10, pady=5)

# Crear los botones
btn_registrar = tk.Button(ventana, text="Registrar Usuario", command=registrar_usuario)
btn_registrar.grid(row=5, column=0, columnspan=2, pady=10)

btn_eliminar = tk.Button(ventana, text="Eliminar Usuario", command=eliminar_usuario)
btn_eliminar.grid(row=6, column=0, columnspan=2, pady=10)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()