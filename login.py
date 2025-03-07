import tkinter as tk
from tkinter import messagebox
from gestion_admin import ventana_admin  # Importamos la ventana del administrador
from gestion_usuario import ventana_usuario  # Importamos la ventana del usuario


# Función para leer el archivo de usuarios
def leer_usuarios():
    usuarios = []
    try:
        with open("usuarios.txt", "r") as file:
            for linea in file:
                datos = linea.strip().split(",")  # Separar los datos por ","
                if len(datos) == 4:
                    usuarios.append(datos)
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo usuarios.txt")
    return usuarios


# Validar usuario y abrir la ventana correspondiente
def validar_usuario(id_usuario, password_usuario):
    user_id = id_usuario.get().strip()  #
    password = password_usuario.get().strip()

    usuarios = leer_usuarios()

    for usuario in usuarios:
        usuario_id = usuario[0].strip()
        usuario_nombre = usuario[1].strip()
        usuario_password = usuario[2].strip()
        usuario_tipo = usuario[3].strip()

        if user_id == usuario_id and password == usuario_password:
            messagebox.showinfo("Acceso", f"Bienvenido {usuario_nombre}")

            root.withdraw()

            if usuario_tipo == "administrador":
                ventana_admin()
            else:
                ventana_usuario(usuario_nombre)
            return

    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Interfaz del Login
root = tk.Tk()
root.title("LOG-IN")
root.geometry("500x500")
root.configure(bg="#2E2E2E")

titulo = tk.Label(root, text="Log In", bg="#2E2E2E", fg="white", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

con_add_login = tk.Frame(root, background="#2E2E2E")
con_add_login.place(x=0, y=120, width=500, height=300)

lbl_usuario = tk.Label(con_add_login, text="ID: ", fg="white", background="#2E2E2E", font=("Arial", 18, "bold"))
lbl_usuario.pack(anchor="w", padx=100)
id_usuario = tk.Entry(con_add_login)
id_usuario.pack(anchor="w", padx=100, pady=5, fill="x")

lbl_password = tk.Label(con_add_login, text="Contraseña: ", fg="white", background="#2E2E2E", font=("Arial", 18, "bold"))
lbl_password.pack(anchor="w", padx=100)
password_usuario = tk.Entry(con_add_login, show="*")  # Ocultar la contraseña
password_usuario.pack(anchor="w", padx=100, pady=5, fill="x")

btn_ingresar = tk.Button(con_add_login, text="Ingresar", command=lambda: validar_usuario(id_usuario, password_usuario), bg="#28A745", fg="#FFFFFF", width=25, height=2)
btn_ingresar.pack(anchor="w", padx=150, pady=30, fill="x")

root.mainloop()
