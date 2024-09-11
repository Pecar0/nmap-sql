import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
import subprocess
import random
import string

# Configuración de estilos
BACKGROUND_COLOR = "#f5f5f5"
BUTTON_COLOR_LOGIN = "#4CAF50"
BUTTON_COLOR_REGISTER = "#008CBA"
TEXT_COLOR = "white"
FONT = ("Helvetica", 12)

class UserManager:
    def __init__(self):
        self.setup_database()

    def setup_database(self):
        """ Configura la base de datos SQLite3. """
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                key TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def verify_credentials(self, username, key):
        """ Verifica las credenciales del usuario. """
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND key = ?', (username, key))
        user = c.fetchone()
        conn.close()
        return user

    def generate_key(self):
        """ Genera una clave aleatoria de 12 caracteres. """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def add_user(self, username, password):
        """ Agrega un nuevo usuario a la base de datos. """
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            key = self.generate_key()
            c.execute('INSERT INTO users (username, password, key) VALUES (?, ?, ?)', (username, password, key))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario registrado con éxito.\nTu clave es: {key}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
        finally:
            conn.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x350")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.user_manager = UserManager()

        # Crear estilos de botones
        self.create_styles()

        self.create_widgets()

    def create_styles(self):
        """ Crea los estilos de los botones. """
        style = ttk.Style()
        style.configure("Login.TButton", background=BUTTON_COLOR_LOGIN, foreground=TEXT_COLOR, padding=6)
        style.configure("Register.TButton", background=BUTTON_COLOR_REGISTER, foreground=TEXT_COLOR, padding=6)
        style.map("Login.TButton", background=[("active", BUTTON_COLOR_LOGIN)])
        style.map("Register.TButton", background=[("active", BUTTON_COLOR_REGISTER)])

    def create_widgets(self):
        """ Crea todos los widgets de la ventana principal. """
        title_label = ttk.Label(self.root, text="Inicio de Sesión", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Nombre de usuario
        self.create_label_entry("Nombre de Usuario:", "username")

        # Clave de acceso
        self.create_label_entry("Clave de Acceso:", "key", show="*")

        # Botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=(10, 20))

        self.create_button(button_frame, "Iniciar Sesión", self.login, "Login")
        self.create_button(button_frame, "Registrar Usuario", self.open_register_window, "Register")

    def create_label_entry(self, text, key, show=""):
        """ Crea una etiqueta y una entrada para el formulario. """
        ttk.Label(self.root, text=text, font=self.custom_font, background=BACKGROUND_COLOR).pack(pady=5)
        entry = ttk.Entry(self.root, font=self.custom_font, show=show)
        entry.pack(pady=5, padx=20, fill='x')
        setattr(self, f'entry_{key}', entry)

    def create_button(self, parent, text, command, style_name):
        """ Crea un botón con el estilo y comando especificados. """
        button = ttk.Button(parent, text=text, command=command, style=f"{style_name}.TButton")
        button.grid(row=0, column=parent.grid_size()[1], padx=5)  # Adjust column dynamically

    def login(self):
        """ Maneja el inicio de sesión del usuario. """
        username = self.entry_username.get().strip()
        key = self.entry_key.get().strip()

        if username and key:
            user = self.user_manager.verify_credentials(username, key)
            if user:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                self.root.destroy()

                try:
                    subprocess.Popen(['python3', 'code.py', username])
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir la GUI de code.py: {e}")
            else:
                messagebox.showerror("Error", "Nombre de usuario o clave incorrectos.")
        else:
            messagebox.showwarning("Advertencia", "Nombre de usuario o clave no proporcionados.")

    def open_register_window(self):
        """ Abre la ventana de registro de usuario. """
        register_window = tk.Toplevel(self.root)
        register_window.title("Registro de Usuario")
        register_window.geometry("400x300")
        register_window.configure(bg=BACKGROUND_COLOR)

        ttk.Label(register_window, text="Nombre de Usuario:", font=self.custom_font, background=BACKGROUND_COLOR).pack(pady=5)
        register_username = ttk.Entry(register_window, font=self.custom_font)
        register_username.pack(pady=5, padx=20, fill='x')

        ttk.Label(register_window, text="Contraseña:", font=self.custom_font, background=BACKGROUND_COLOR).pack(pady=5)
        register_password = ttk.Entry(register_window, show="*", font=self.custom_font)
        register_password.pack(pady=5, padx=20, fill='x')

        ttk.Button(register_window, text="Registrar", command=lambda: self.register_user(register_username, register_password, register_window), style="Register.TButton").pack(pady=20)

    def register_user(self, register_username, register_password, window):
        """ Registra un nuevo usuario desde la ventana de registro. """
        username = register_username.get().strip()
        password = register_password.get().strip()
        if username and password:
            self.user_manager.add_user(username, password)
            window.destroy()
        else:
            messagebox.showwarning("Advertencia", "Nombre de usuario o contraseña no proporcionados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
