import tkinter as tk
from tkinter import scrolledtext
import subprocess
import sys

def open_sqlmap_window():
    try:
        # Crear la ventana de SQLmap
        sqlmap_window = tk.Tk()
        sqlmap_window.title("SQLmap Menu")
        sqlmap_window.geometry("1200x800")
        sqlmap_window.configure(bg="#2e2e2e")

        # Crear un marco para los widgets
        frame = tk.Frame(sqlmap_window, bg="#1e1e1e", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Función para aplicar un tema
        def apply_theme(bg_color, fg_color, button_bg_color, button_fg_color):
            sqlmap_window.configure(bg=bg_color)
            frame.configure(bg=bg_color)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=button_bg_color, fg=button_fg_color)

        # Opciones de temas
        def theme_white():
            apply_theme("#ffffff", "#000000", "#e0e0e0", "#000000")

        def theme_dark():
            apply_theme("#2e2e2e", "#f0f0f0", "#3a3a3a", "#f0f0f0")

        def theme_blue():
            apply_theme("#003366", "#ffffff", "#00509e", "#ffffff")

        def write_to_console(text):
            output_text.configure(state=tk.NORMAL)
            output_text.insert(tk.END, text)
            output_text.see(tk.END)  # Desplazar el texto hasta el final
            output_text.configure(state=tk.DISABLED)

        def execute_sqlmap_command(command):
            url = entry_url.get().strip()
            if not url:
                write_to_console("Error: URL no especificada.\n")
                return

            try:
                cmd = command.format(url)
                write_to_console(f"Ejecutando comando: {cmd}\n")
                sqlmap_window.update()  # Refrescar la interfaz
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                write_to_console(f"Salida:\n{result.stdout}\n")
                write_to_console(f"Errores:\n{result.stderr}\n")
                write_to_console("-" * 50 + "\n")
            except Exception as e:
                write_to_console(f"Error: {e}\n")

        # Etiqueta de URL
        tk.Label(frame, text="Ingrese URL:", font=("Arial", 14), bg="#1e1e1e", fg="#ffffff").pack(pady=5)
        entry_url = tk.Entry(frame, bg="#ffffff", fg="#000000", bd=2, insertbackground='#000000')
        entry_url.pack(pady=5)

        # Botones para ejecutar comandos de SQLmap
        tk.Button(frame, text="SQLmap --dbs (Listar Bases de Datos)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --dbs"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap --tables (Listar Tablas)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --tables"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap --dump (Volcar Datos)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --dump"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap --users (Listar Usuarios)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --users"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap --passwords (Listar Contraseñas)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --passwords"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap --tables --dump (Tablas y Volcado)", command=lambda: execute_sqlmap_command("sqlmap -u {0} --tables --dump"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap -D (Base de Datos)", command=lambda: execute_sqlmap_command("sqlmap -D {0} --tables"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap -T (Tabla)", command=lambda: execute_sqlmap_command("sqlmap -T {0} --columns"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap -C (Columnas)", command=lambda: execute_sqlmap_command("sqlmap -C {0} --dump"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="SQLmap -D (Volcar Datos)", command=lambda: execute_sqlmap_command("sqlmap -D {0} --dump"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)

        output_text = scrolledtext.ScrolledText(frame, width=90, height=20, bg="#1e1e1e", fg="#ffffff", bd=2, font=("Consolas", 10))
        output_text.pack(pady=10)

        # Deshabilitar la edición del área de texto para simular una consola
        output_text.configure(state=tk.DISABLED)

        def back_to_main():
            sqlmap_window.destroy()
            subprocess.Popen([sys.executable, 'code.py'])

        back_button = tk.Button(sqlmap_window, text="Volver", font=("Arial", 18, "bold"), bg="#00509e", fg="#ffffff", relief=tk.FLAT, command=back_to_main)
        back_button.place(relx=0.0, y=10, anchor="nw")

        sqlmap_window.mainloop()

    except Exception as e:
        print(f"Error al iniciar la GUI de SQLmap: {e}")

if __name__ == "__main__":
    open_sqlmap_window()
