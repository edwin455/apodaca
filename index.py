import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Holaquehace1",
        database="dissoft",
        port=3307
    )

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("300x200")
        self.configure(bg="#ecf0f1")
        self.resizable(False, False)

        tk.Label(self, text="Email:", bg="#ecf0f1").pack(pady=10)
        self.entry_user = ttk.Entry(self, width=30)
        self.entry_user.pack()

        tk.Label(self, text="Contraseña:", bg="#ecf0f1").pack(pady=10)
        self.entry_pass = ttk.Entry(self, show="*", width=30)
        self.entry_pass.pack()

        ttk.Button(self, text="Ingresar", command=self.verificar).pack(pady=20)

    def verificar(self):
        email = self.entry_user.get()
        contrasena = self.entry_pass.get()

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT usuarios.id, usuarios.nombre, roles.nombre AS rol
                FROM usuarios
                INNER JOIN roles ON usuarios.rol_id = roles.id
                WHERE usuarios.email = %s AND usuarios.contrasena = %s
            """, (email, contrasena))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                self.destroy()
                app = SidebarApp()
                app.mainloop()
            else:
                messagebox.showerror("Acceso denegado", "Credenciales incorrectas.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de conexión", str(e))



class SidebarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PIA DISSOFT")
        self.geometry("1100x650")
        self.configure(bg="#ecf0f1")

        # SIDEBAR
        self.sidebar = tk.Frame(self, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
        self.sidebar, text="Municipio Apodaca", bg="#2c3e50", fg="white",
        font=("Helvetica", 24, "bold")
        ).pack(pady=20)



        menu_items = [
            ("🏠 Inicio", self.show_inicio),
            ("👤 Usuarios", self.show_usuarios),
            ("📅 Actividades", self.show_actividades),
            ("📝 Reportes", self.show_reportes),]
        
        # Botón Cerrar Sesión
        btn_logout = tk.Button(
            self.sidebar, text="🚪 Cerrar Sesión", bg="#e74c3c", fg="white",
            relief="flat", anchor="w", font=("Helvetica", 12),
            activebackground="#c0392b", activeforeground="white",
            padx=10, pady=10, command=self.cerrar_sesion
        )
        btn_logout.pack(fill="x", padx=10, pady=20)


        for text, command in menu_items:
            btn = tk.Button(
                self.sidebar, text=text, bg="#34495e", fg="white",
                relief="flat", anchor="w", font=("Helvetica", 12),
                activebackground="#1abc9c", activeforeground="white",
                padx=10, pady=10, command=command
            )
            btn.pack(fill="x", padx=10, pady=4)

        self.main_content = tk.Frame(self, bg="#ecf0f1")
        self.main_content.pack(side="right", expand=True, fill="both")

        self.show_inicio()
        
    def cerrar_sesion(self):
        self.destroy()  # Cierra ventana principal
        login = LoginWindow()  # Vuelve a abrir login
        login.mainloop()

        
    def show_usuarios(self):
        self.clear_main_content()

        tk.Label(self.main_content, text="👤 Gestión de Usuarios",
                 font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

        # Botones de acción
        action_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="+ Nuevo Usuario", bg="#27ae60", fg="white",
                  font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                  command=self.abrir_ventana_nuevo_usuario).pack(side="left", padx=5)

        tk.Button(action_frame, text="✏️ Modificar Usuario", bg="#f39c12", fg="white",
                  font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                  command=self.modificar_usuario).pack(side="left", padx=5)

        table_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        table_frame.pack(padx=20, fill="both", expand=True)

        cols = ("ID", "Nombre", "Email", "Rol")
        self.usuario_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.usuario_tree.heading(col, text=col)
            self.usuario_tree.column(col, width=150, anchor="center")

        usuarios = [
            (1, "Juan Pérez", "juan@example.com", "Administrador"),
            (2, "Ana López", "ana@example.com", "Usuario"),
            (3, "Carlos Ruiz", "carlos@example.com", "Supervisor")
        ]

        for usuario in usuarios:
            self.usuario_tree.insert("", "end", values=usuario)

        self.usuario_tree.pack(fill="both", expand=True)

    def abrir_ventana_nuevo_usuario(self):
        self._abrir_ventana_usuario(modo="nuevo")

    def modificar_usuario(self):
        selected = self.usuario_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar usuario", "Por favor selecciona un usuario para modificar.")
            return
        valores = self.usuario_tree.item(selected[0], "values")
        self._abrir_ventana_usuario(modo="editar", item_id=selected[0], valores=valores)

    def _abrir_ventana_usuario(self, modo="nuevo", item_id=None, valores=None):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Usuario" if modo == "nuevo" else "Modificar Usuario")
        ventana.geometry("400x300")
        ventana.configure(bg="#ecf0f1")

        tk.Label(ventana, text="Nombre:", bg="#ecf0f1").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.pack()

        tk.Label(ventana, text="Email:", bg="#ecf0f1").pack(pady=5)
        entry_email = ttk.Entry(ventana, width=40)
        entry_email.pack()

        tk.Label(ventana, text="Contraseña:", bg="#ecf0f1").pack(pady=5)
        entry_pass = ttk.Entry(ventana, width=40, show="*")
        entry_pass.pack()

        tk.Label(ventana, text="Rol:", bg="#ecf0f1").pack(pady=5)
        combo_rol = ttk.Combobox(ventana, values=["Administrador", "Usuario", "Supervisor"], state="readonly", width=37)
        combo_rol.set("Usuario")
        combo_rol.pack()

        if modo == "editar" and valores:
            entry_nombre.insert(0, valores[1])
            entry_email.insert(0, valores[2])
            combo_rol.set(valores[3])

        def guardar():
            nombre = entry_nombre.get().strip()
            email = entry_email.get().strip()
            contrasena = entry_pass.get().strip()
            rol = combo_rol.get()

            if not nombre or not email or not contrasena:
                messagebox.showerror("Campos vacíos", "Todos los campos son obligatorios.")
                return

            try:
                conn = conectar_db()
                cursor = conn.cursor()

                if modo == "nuevo":
                    cursor.execute("SELECT id FROM roles WHERE nombre = %s", (rol,))
                    rol_id = cursor.fetchone()
                    if not rol_id:
                        messagebox.showerror("Error", "Rol no válido")
                        return

                    cursor.execute(
                        "INSERT INTO usuarios (nombre, email, contrasena, rol_id) VALUES (%s, %s, %s, %s)",
                        (nombre, email, contrasena, rol_id[0])
                    )
                    conn.commit()
                    nuevo_id = cursor.lastrowid
                    self.usuario_tree.insert("", "end", values=(nuevo_id, nombre, email, rol))

                else:
                    cursor.execute("""
                        UPDATE usuarios 
                        SET nombre=%s, email=%s, rol_id=(SELECT id FROM roles WHERE nombre=%s)
                        WHERE id=%s
                    """, (nombre, email, rol, valores[0]))
                    conn.commit()
                    self.usuario_tree.item(item_id, values=(valores[0], nombre, email, rol))

                conn.close()
                ventana.destroy()

            except Exception as e:
                messagebox.showerror("Error de base de datos", str(e))

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    # En show_usuarios, reemplaza usuarios de prueba por consulta real:
    def show_usuarios(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="👤 Gestión de Usuarios",
                font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

        action_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="+ Nuevo Usuario", bg="#27ae60", fg="white",
                font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                command=self.abrir_ventana_nuevo_usuario).pack(side="left", padx=5)

        tk.Button(action_frame, text="✏️ Modificar Usuario", bg="#f39c12", fg="white",
                font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                command=self.modificar_usuario).pack(side="left", padx=5)

        table_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        table_frame.pack(padx=20, fill="both", expand=True)

        cols = ("ID", "Nombre", "Email", "Rol")
        self.usuario_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.usuario_tree.heading(col, text=col)
            self.usuario_tree.column(col, width=150, anchor="center")

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT usuarios.id, usuarios.nombre, usuarios.email, roles.nombre
                FROM usuarios
                INNER JOIN roles ON usuarios.rol_id = roles.id
            """)
            for row in cursor.fetchall():
                self.usuario_tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.usuario_tree.pack(fill="both", expand=True)

    def show_actividades(self):
        self.clear_main_content()

        tk.Label(self.main_content, text="📅 Actividades Registradas",
                font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

        action_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="+ Agregar Actividad", bg="#27ae60", fg="white",
                font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                command=self.abrir_ventana_nueva_actividad).pack(side="left", padx=5)

        tk.Button(action_frame, text="✏️ Modificar Actividad", bg="#f39c12", fg="white",
                font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5,
                command=self.modificar_actividad).pack(side="left", padx=5)

        table_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        table_frame.pack(padx=20, fill="both", expand=True)

        cols = ("ID", "Nombre", "Fecha y Hora", "Organizador", "Ubicación", "Resultado")
        self.actividades_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.actividades_tree.heading(col, text=col)
            self.actividades_tree.column(col, width=130, anchor="center")

        # Cargar datos reales desde la base
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT actividades.id, actividades.nombre, 
                    CONCAT(actividades.fecha, ' ', DATE_FORMAT(actividades.fecha, '%H:%i')) AS fecha_hora,
                    usuarios.nombre, actividades.ubicacion, actividades.resultado
                FROM actividades
                LEFT JOIN usuarios ON actividades.organizador_id = usuarios.id
            """)
            for row in cursor.fetchall():
                self.actividades_tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.actividades_tree.pack(fill="both", expand=True)


    def abrir_ventana_nueva_actividad(self):
        self._abrir_ventana_actividad(modo="nueva")

    def modificar_actividad(self):
        selected = self.actividades_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar actividad", "Por favor selecciona una actividad para modificar.")
            return
        valores = self.actividades_tree.item(selected[0], "values")
        self._abrir_ventana_actividad(modo="editar", item_id=selected[0], valores=valores)


    def _abrir_ventana_actividad(self, modo="nueva", item_id=None, valores=None):
        from datetime import datetime

        ventana = tk.Toplevel(self)
        ventana.title("Nueva Actividad" if modo == "nueva" else "Modificar Actividad")
        ventana.geometry("400x400")
        ventana.configure(bg="#ecf0f1")

        tk.Label(ventana, text="Nombre:", bg="#ecf0f1").pack(pady=5)
        entry_nombre = ttk.Entry(ventana, width=40)
        entry_nombre.pack()

        tk.Label(ventana, text="Fecha (YYYY-MM-DD):", bg="#ecf0f1").pack(pady=5)
        entry_fecha = ttk.Entry(ventana, width=40)
        entry_fecha.pack()

        tk.Label(ventana, text="Hora (HH:MM):", bg="#ecf0f1").pack(pady=5)
        entry_hora = ttk.Entry(ventana, width=40)
        entry_hora.pack()

        tk.Label(ventana, text="Organizador:", bg="#ecf0f1").pack(pady=5)
        entry_org = ttk.Entry(ventana, width=40)
        entry_org.pack()

        tk.Label(ventana, text="Ubicación:", bg="#ecf0f1").pack(pady=5)
        entry_ubic = ttk.Entry(ventana, width=40)
        entry_ubic.pack()

        tk.Label(ventana, text="Resultado:", bg="#ecf0f1").pack(pady=5)
        entry_res = ttk.Entry(ventana, width=40)
        entry_res.pack()

        if modo == "editar" and valores:
            entry_nombre.insert(0, valores[1])
            if valores[2]:
                fecha_hora = valores[2].split()
                if len(fecha_hora) == 2:
                    entry_fecha.insert(0, fecha_hora[0])
                    entry_hora.insert(0, fecha_hora[1])
            entry_org.insert(0, valores[3])
            entry_ubic.insert(0, valores[4])
            entry_res.insert(0, valores[5])

        def guardar_actividad():
            nombre = entry_nombre.get().strip()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()
            organizador = entry_org.get().strip()
            ubicacion = entry_ubic.get().strip()
            resultado = entry_res.get().strip()

            if not nombre or not fecha or not hora or not organizador or not ubicacion:
                messagebox.showerror("Campos vacíos", "Todos los campos excepto resultado son obligatorios.")
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                datetime.strptime(hora, "%H:%M")
            except ValueError:
                messagebox.showerror("Formato inválido", "Fecha debe ser YYYY-MM-DD y Hora HH:MM")
                return

            try:
                conn = conectar_db()
                cursor = conn.cursor()

                # Buscar id del organizador
                cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (organizador,))
                org_id = cursor.fetchone()
                if not org_id:
                    messagebox.showerror("Error", "Organizador no encontrado en usuarios.")
                    return

                if modo == "nueva":
                    cursor.execute("""
                        INSERT INTO actividades (nombre, fecha, ubicacion, organizador_id, resultado)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (nombre, fecha, ubicacion, org_id[0], resultado))
                    conn.commit()
                    nuevo_id = cursor.lastrowid
                    self.actividades_tree.insert("", "end", values=(nuevo_id, nombre, f"{fecha} {hora}", organizador, ubicacion, resultado))
                else:
                    cursor.execute("""
                        UPDATE actividades
                        SET nombre=%s, fecha=%s, ubicacion=%s, organizador_id=%s, resultado=%s
                        WHERE id=%s
                    """, (nombre, fecha, ubicacion, org_id[0], resultado, valores[0]))
                    conn.commit()
                    self.actividades_tree.item(item_id, values=(valores[0], nombre, f"{fecha} {hora}", organizador, ubicacion, resultado))

                conn.close()
                ventana.destroy()

            except Exception as e:
                messagebox.showerror("Error de base de datos", str(e))

        ttk.Button(ventana, text="Guardar", command=guardar_actividad).pack(pady=20)


    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_inicio(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="🏠 Inicio", font=("Helvetica", 22, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(padx=20, pady=20, anchor="w")

        self.clear_main_content()
        tk.Label(self.main_content, text="🏠 Inicio", font=("Helvetica", 22, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(padx=20, pady=20, anchor="w")

        stats_frame = tk.Frame(self.main_content, bg="#ecf0f1")
        stats_frame.pack(pady=10)
        self._crear_tarjeta(stats_frame, "👷 Trabajadores en activo", "2", "#27ae60")
        self._crear_tarjeta(stats_frame, "🛌 Trabajadores en inactivo", "0", "#c0392b")

    def show_reportes(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="📝 Generar Reporte",
                 font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)

        form = tk.Frame(self.main_content, bg="#ecf0f1")
        form.pack(padx=30, pady=5)

        campos = {
            "Actividad ID": "text",
            "Total Asistentes": "text",
            "Descripción": "multiline"
        }
        self.entries = {}

        for i, (label, tipo) in enumerate(campos.items()):
            tk.Label(form, text=label + ":", bg="#ecf0f1").grid(row=i, column=0, sticky="e", pady=2)

            if tipo == "multiline":
                entry = tk.Text(form, height=4, width=40)
                entry.grid(row=i, column=1, pady=2)
            else:
                entry = ttk.Entry(form, width=40)
                entry.grid(row=i, column=1, pady=2)

            self.entries[label] = entry

        tk.Button(self.main_content, text="📝 Generar Reporte", bg="#2980b9", fg="white",
                  font=("Helvetica", 11, "bold"), padx=10, pady=5,
                  command=self.generar_reporte).pack(pady=10)

    def generar_reporte(self):
        if not hasattr(self, 'entries'):
            messagebox.showerror("Error", "No se encontraron datos para generar el reporte.")
            return

        datos = {}
        for campo, widget in self.entries.items():
            if isinstance(widget, tk.Text):
                valor = widget.get("1.0", tk.END).strip()
            else:
                valor = widget.get().strip()
            datos[campo] = valor

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            title="Guardar Reporte",
            initialfile=f"Reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        if not archivo:
            return

        try:
            c = canvas.Canvas(archivo, pagesize=A4)
            width, height = A4
            y = height - 50

            # ⬇️ LOGOTIPO (ajusta la ruta si está en otro lugar)
            try:
                c.drawImage("logo.png", 50, y - 50, width=100, height=50, preserveAspectRatio=True)
            except Exception as e:
                print("⚠️ No se pudo cargar el logotipo:", e)

            # ⬇️ Encabezado del documento
            c.setFont("Helvetica-Bold", 18)
            c.drawString(170, y, "Municipio de Apodaca")
            y -= 80

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Reporte de Acceso No Autorizado")
            y -= 30

            # Cuerpo del reporte
            c.setFont("Helvetica", 12)
            for campo, valor in datos.items():
                if y < 100:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 12)
                c.drawString(50, y, f"{campo}: {valor}")
                y -= 20

            c.save()
            messagebox.showinfo("Reporte generado", f"✅ El archivo fue guardado en:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Ocurrió un error al generar el PDF:\n{str(e)}")


    def _crear_tarjeta(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg=color, width=200, height=100)
        card.pack(side="left", padx=15, pady=10)
        tk.Label(card, text=titulo, font=("Helvetica", 12), bg=color, fg="white").pack(pady=5)
        tk.Label(card, text=valor, font=("Helvetica", 24, "bold"), bg=color, fg="white").pack()


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
