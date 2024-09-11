import tkinter as tk
from tkinter import Menu, scrolledtext
import subprocess
import sys

def open_main_window(username):
    try:
        # Crear la ventana principal
        main_window = tk.Tk()
        main_window.title("SPRLOG")
        main_window.configure(bg="#2e2e2e")
        main_window.geometry("1200x800")

        # Crear un marco para los widgets
        frame = tk.Frame(main_window, bg="#1e1e1e", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        def show_options(event):
            options_menu.post(event.x_root, event.y_root)

        def apply_theme(bg_color, fg_color, button_bg_color, button_fg_color):
            main_window.configure(bg=bg_color)
            frame.configure(bg=bg_color)
            username_label.configure(bg=bg_color, fg=fg_color)
            options_menu.configure(bg=bg_color, fg=fg_color)
            for item in options_menu.winfo_children():
                item.configure(bg=bg_color, fg=fg_color)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=button_bg_color, fg=button_fg_color)
            arrow_button.configure(bg=button_bg_color, fg=button_fg_color)

        def theme_white():
            apply_theme("#ffffff", "#000000", "#e0e0e0", "#000000")

        def theme_dark():
            apply_theme("#2e2e2e", "#f0f0f0", "#3a3a3a", "#f0f0f0")

        def theme_blue():
            apply_theme("#003366", "#ffffff", "#00509e", "#ffffff")

        def logout_option():
            main_window.destroy()
            subprocess.Popen([sys.executable, 'main.py'])  # Vuelve a ejecutar main.py

        def quit_option():
            main_window.quit()

        def write_to_console(text):
            output_text.configure(state=tk.NORMAL)
            output_text.insert(tk.END, text)
            output_text.see(tk.END)  # Desplazar el texto hasta el final
            output_text.configure(state=tk.DISABLED)

        def execute_nmap_command(command):
            ip = entry_ip.get().strip()
            if not ip:
                write_to_console("Error: IP no especificada.\n")
                return

            if ip.startswith("http://"):
                ip = ip[7:]
            elif ip.startswith("https://"):
                ip = ip[8:]

            ip = ip.split('/')[0]

            try:
                cmd = command.format(ip)
                write_to_console(f"Ejecutando comando: {cmd}\n")
                main_window.update()  # Refrescar la interfaz
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                write_to_console(f"Salida:\n{result.stdout}\n")
                write_to_console(f"Errores:\n{result.stderr}\n")
                write_to_console("-" * 50 + "\n")
            except Exception as e:
                write_to_console(f"Error: {e}\n")

        username_label = tk.Label(frame, text=f"Usuario: {username}", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="#ffffff")
        username_label.pack(anchor="nw", padx=10, pady=10)

        # Crear un menú desplegable de opciones
        options_menu = Menu(main_window, tearoff=0, bg="#3a3a3a", fg="#ffffff")
        
        # Submenú de temas
        themes_menu = Menu(options_menu, tearoff=0, bg="#3a3a3a", fg="#ffffff")
        themes_menu.add_command(label="Tema Blanco", command=theme_white)
        themes_menu.add_command(label="Tema Oscuro", command=theme_dark)
        themes_menu.add_command(label="Tema Azul", command=theme_blue)

        # Agregar comandos al menú principal
        options_menu.add_cascade(label="Temas", menu=themes_menu)
        options_menu.add_command(label="Cerrar sesión", command=logout_option)
        options_menu.add_command(label="Salir", command=quit_option)

        # Bind del clic en el nombre de usuario para mostrar el menú
        username_label.bind("<Button-1>", show_options)

        # Widgets para el comando nmap
        tk.Label(frame, text="Ingrese IP:", font=("Arial", 14), bg="#1e1e1e", fg="#ffffff").pack(pady=5)
        entry_ip = tk.Entry(frame, bg="#ffffff", fg="#000000", bd=2, insertbackground='#000000')
        entry_ip.pack(pady=5)

        # Botones para ejecutar comandos nmap
        tk.Button(frame, text="Nmap -sV (Versiones de Servicio)", command=lambda: execute_nmap_command("nmap -sV {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -O (Sistema Operativo)", command=lambda: execute_nmap_command("nmap -O {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -A (Detección Completa)", command=lambda: execute_nmap_command("nmap -A {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -T4 (Rápido)", command=lambda: execute_nmap_command("nmap -T4 {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -p (Escaneo de Puertos)", command=lambda: execute_nmap_command("nmap -p {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -sC (Escaneo de Vulnerabilidades)", command=lambda: execute_nmap_command("nmap -sC {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)
        tk.Button(frame, text="Nmap -sP (Escaneo de IPs)", command=lambda: execute_nmap_command("nmap -sP {0}"), font=("Arial", 12), bg="#00509e", fg="#ffffff").pack(pady=5, fill=tk.X)

        output_text = scrolledtext.ScrolledText(frame, width=90, height=20, bg="#1e1e1e", fg="#ffffff", bd=2, font=("Consolas", 10))
        output_text.pack(pady=10)

        # Deshabilitar la edición del área de texto para simular una consola
        output_text.configure(state=tk.DISABLED)

        # Función para abrir menu2.py y cerrar la ventana actual
        def open_menu2():
            main_window.destroy()
            subprocess.Popen([sys.executable, 'menu2.py'])

        arrow_button = tk.Button(main_window, text="≥", font=("Arial", 18, "bold"), bg="#00509e", fg="#ffffff", relief=tk.FLAT, command=open_menu2)
        arrow_button.place(relx=1.0, y=10, anchor="ne")  # Ajustar posición en la esquina superior derecha

        main_window.mainloop()

    except Exception as e:
        print(f"Error al iniciar la GUI: {e}")

if __name__ == "__main__":
    # Usar un nombre de usuario predeterminado si no se proporciona uno como argumento
    username = sys.argv[1] if len(sys.argv) > 1 else "Usuario Desconocido"
    open_main_window(username)
