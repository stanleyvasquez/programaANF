import tkinter as tk
from tkinter import messagebox, ttk

class IngresoFinanciero:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.entries = {}  # Diccionario para almacenar todos los campos de entrada
        
    def abrir_ventana(self):
        """Abre la ventana de ingreso de datos financieros"""
        ventana_ingreso = tk.Toplevel(self.parent_app.root)
        ventana_ingreso.title("Ingresar Datos Financieros")
        ventana_ingreso.geometry("900x750")
        ventana_ingreso.config(bg=self.parent_app.bg_principal)
        ventana_ingreso.resizable(False, False)
        
        # Centrar ventana
        ventana_ingreso.update_idletasks()
        x = (ventana_ingreso.winfo_screenwidth() // 2) - (450)
        y = (ventana_ingreso.winfo_screenheight() // 2) - (375)
        ventana_ingreso.geometry(f'900x750+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_ingreso, bg=self.parent_app.bg_secundario, height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="📝 Ingreso de Datos Financieros",
            font=("Segoe UI", 18, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=25)
        
        # Frame principal con scroll
        canvas = tk.Canvas(ventana_ingreso, bg=self.parent_app.bg_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_ingreso, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.parent_app.bg_principal)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            try:
                # Verificar que el canvas todavía existe antes de hacer scroll
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                # Ignorar el error si el canvas ya fue destruido
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Limpiar binding cuando se cierre la ventana
        def on_closing():
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass
            ventana_ingreso.destroy()
        
        ventana_ingreso.protocol("WM_DELETE_WINDOW", on_closing)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        self.crear_seccion_informacion_general(frame_scroll, 0)
        
        # ===== SECCIÓN: ACTIVOS =====
        self.crear_seccion_datos(frame_scroll, "ACTIVOS", [
            "Efectivo y Equivalentes",
            "Cuentas por Cobrar",
            "Inventarios",
            "Activos Fijos",
            "Otros Activos"
        ], 1)
        
        # ===== SECCIÓN: PASIVOS =====
        self.crear_seccion_datos(frame_scroll, "PASIVOS", [
            "Cuentas por Pagar",
            "Préstamos Bancarios",
            "Obligaciones Financieras",
            "Otros Pasivos"
        ], 2)
        
        # ===== SECCIÓN: PATRIMONIO =====
        self.crear_seccion_datos(frame_scroll, "PATRIMONIO", [
            "Capital Social",
            "Reservas",
            "Utilidades Retenidas"
        ], 3)
        
        # ===== SECCIÓN: INGRESOS =====
        self.crear_seccion_datos(frame_scroll, "INGRESOS", [
            "Ventas",
            "Ingresos por Servicios",
            "Otros Ingresos"
        ], 4)
        
        # ===== SECCIÓN: GASTOS =====
        self.crear_seccion_datos(frame_scroll, "GASTOS", [
            "Costo de Ventas",
            "Gastos Administrativos",
            "Gastos de Ventas",
            "Gastos Financieros",
            "Otros Gastos"
        ], 5)
        
        # Botones de acción
        frame_botones = tk.Frame(frame_scroll, bg=self.parent_app.bg_principal)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=30, sticky="ew")
        
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar Datos",
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_exito,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=12,
            activebackground="#2d8f5a",
            command=lambda: self.guardar_datos(ventana_ingreso)
        )
        btn_guardar.pack(side="left", padx=10, expand=True)
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="❌ Cancelar",
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_peligro,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=12,
            activebackground="#c23850",
            command=on_closing
        )
        btn_cancelar.pack(side="right", padx=10, expand=True)
    
    def crear_seccion_informacion_general(self, parent, fila):
        """Crea la sección de información general con nombre de empresa, año y moneda"""
        # Frame de la sección
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        
        # Título de la sección
        label_titulo = tk.Label(
            frame_seccion,
            text="INFORMACIÓN GENERAL",
            font=("Segoe UI", 14, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=10
        )
        label_titulo.pack(fill="x")
        
        # Frame para los campos
        frame_campos = tk.Frame(frame_seccion, bg=self.parent_app.bg_secundario)
        frame_campos.pack(fill="both", padx=20, pady=15)
        
        # Campo: Nombre de la Empresa
        frame_empresa = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_empresa.pack(fill="x", pady=8)
        
        label_empresa = tk.Label(
            frame_empresa,
            text="Nombre de la Empresa:",
            font=("Segoe UI", 10),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            width=25,
            anchor="w"
        )
        label_empresa.pack(side="left", padx=(0, 10))
        
        entry_empresa = tk.Entry(
            frame_empresa,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=40
        )
        entry_empresa.pack(side="left", ipady=5)
        self.entries["nombre_empresa"] = entry_empresa
        
        # Campo: Año del Análisis
        frame_anio = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_anio.pack(fill="x", pady=8)
        
        label_anio = tk.Label(
            frame_anio,
            text="Año del Análisis:",
            font=("Segoe UI", 10),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            width=25,
            anchor="w"
        )
        label_anio.pack(side="left", padx=(0, 10))
        
        entry_anio = tk.Entry(
            frame_anio,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=40
        )
        entry_anio.pack(side="left", ipady=5)
        self.entries["anio"] = entry_anio
        
        # Campo: Tipo de Moneda
        frame_moneda = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_moneda.pack(fill="x", pady=8)
        
        label_moneda = tk.Label(
            frame_moneda,
            text="Tipo de Moneda:",
            font=("Segoe UI", 10),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            width=25,
            anchor="w"
        )
        label_moneda.pack(side="left", padx=(0, 10))
        
        # Combobox para tipo de moneda
        monedas = [
            "USD - Dólar Estadounidense",
            "EUR - Euro",
            "MXN - Peso Mexicano",
            "COP - Peso Colombiano",
            "ARS - Peso Argentino",
            "CLP - Peso Chileno",
            "PEN - Sol Peruano",
            "BRL - Real Brasileño",
            "GBP - Libra Esterlina",
            "JPY - Yen Japonés"
        ]
        
        combo_moneda = ttk.Combobox(
            frame_moneda,
            values=monedas,
            font=("Segoe UI", 10),
            state="readonly",
            width=38
        )
        combo_moneda.set("USD - Dólar Estadounidense")  # Valor por defecto
        combo_moneda.pack(side="left", ipady=3)
        self.entries["tipo_moneda"] = combo_moneda
        
        # Estilo del combobox
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                       fieldbackground="#2c3e50",
                       background="#2c3e50",
                       foreground="white",
                       arrowcolor="white",
                       borderwidth=0)
    
    def crear_seccion_datos(self, parent, titulo, campos, fila):
        """Crea una sección de ingreso de datos con múltiples campos"""
        # Frame de la sección
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        
        # Título de la sección
        label_titulo = tk.Label(
            frame_seccion,
            text=titulo,
            font=("Segoe UI", 14, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=10
        )
        label_titulo.pack(fill="x")
        
        # Frame para los campos
        frame_campos = tk.Frame(frame_seccion, bg=self.parent_app.bg_secundario)
        frame_campos.pack(fill="both", padx=20, pady=15)
        
        # Crear campos de entrada
        for i, campo in enumerate(campos):
            frame_campo = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
            frame_campo.pack(fill="x", pady=8)
            
            label = tk.Label(
                frame_campo,
                text=campo + ":",
                font=("Segoe UI", 10),
                bg=self.parent_app.bg_secundario,
                fg=self.parent_app.color_texto,
                width=25,
                anchor="w"
            )
            label.pack(side="left", padx=(0, 10))
            
            entry = tk.Entry(
                frame_campo,
                font=("Segoe UI", 10),
                bg="#2c3e50",
                fg="white",
                insertbackground="white",
                relief="flat",
                width=30
            )
            entry.pack(side="left", ipady=5)
            
            # Guardar referencia del entry
            key = f"{titulo}_{campo}"
            self.entries[key] = entry
            
            label_moneda = tk.Label(
                frame_campo,
                text="$",
                font=("Segoe UI", 10, "bold"),
                bg=self.parent_app.bg_secundario,
                fg="#3bb273"
            )
            label_moneda.pack(side="left", padx=(5, 0))
    
    def guardar_datos(self, ventana):
        """Guarda los datos ingresados"""
        # Validar campos obligatorios
        nombre_empresa = self.entries["nombre_empresa"].get().strip()
        anio = self.entries["anio"].get().strip()
        tipo_moneda = self.entries["tipo_moneda"].get()
        
        if not nombre_empresa:
            messagebox.showwarning("Campo Requerido", "Por favor ingresa el nombre de la empresa")
            return
        
        if not anio:
            messagebox.showwarning("Campo Requerido", "Por favor ingresa el año del análisis")
            return
        
        # Validar que el año sea un número
        try:
            anio_num = int(anio)
            if anio_num < 1900 or anio_num > 2100:
                messagebox.showwarning("Año Inválido", "Por favor ingresa un año válido (1900-2100)")
                return
        except ValueError:
            messagebox.showwarning("Año Inválido", "El año debe ser un número válido")
            return
        
        nuevo_registro = {
            "nombre_empresa": nombre_empresa,
            "anio": anio_num,
            "tipo_moneda": tipo_moneda
        }
        
        # Recopilar todos los valores de los campos
        for key, entry in self.entries.items():
            if key not in ["nombre_empresa", "anio", "tipo_moneda"]:
                valor = entry.get().strip()
                try:
                    nuevo_registro[key] = float(valor) if valor else 0
                except ValueError:
                    nuevo_registro[key] = 0
        
        # Agregar el nuevo registro a la lista
        self.parent_app.registros_financieros.append(nuevo_registro)
        
        messagebox.showinfo(
            "Datos Guardados",
            f"Los datos financieros han sido guardados exitosamente.\n\n"
            f"Empresa: {nombre_empresa}\n"
            f"Año: {anio}\n"
            f"Moneda: {tipo_moneda}\n\n"
            "Ahora puedes:\n"
            "• Modificar los datos ingresados\n"
            "• Generar reportes financieros"
        )
        ventana.destroy()
