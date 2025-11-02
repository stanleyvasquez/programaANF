import tkinter as tk
from tkinter import messagebox, ttk

class EdicionFinanciero:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.entries = {}  # Diccionario para almacenar todos los campos de entrada
        self.datos_actuales = None  # Almacenará los datos del registro seleccionado
        
    def abrir_ventana(self):
        """Abre la ventana de selección de registro para editar"""
        ventana_seleccion = tk.Toplevel(self.parent_app.root)
        ventana_seleccion.title("Editar Datos Financieros")
        ventana_seleccion.geometry("1000x600")
        ventana_seleccion.config(bg=self.parent_app.bg_principal)
        ventana_seleccion.resizable(False, False)
        
        # Centrar ventana
        ventana_seleccion.update_idletasks()
        x = (ventana_seleccion.winfo_screenwidth() // 2) - (500)
        y = (ventana_seleccion.winfo_screenheight() // 2) - (300)
        ventana_seleccion.geometry(f'1000x600+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_seleccion, bg=self.parent_app.bg_secundario, height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="✏️ Editar Datos Financieros",
            font=("Segoe UI", 18, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=25)
        
        # Frame principal
        frame_principal = tk.Frame(ventana_seleccion, bg=self.parent_app.bg_principal)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instrucciones
        label_instrucciones = tk.Label(
            frame_principal,
            text="Selecciona un registro de la tabla para editar sus datos completos",
            font=("Segoe UI", 11),
            bg=self.parent_app.bg_principal,
            fg="#a8b2d1"
        )
        label_instrucciones.pack(pady=(0, 15))
        
        frame_tabla = tk.Frame(frame_principal, bg=self.parent_app.bg_secundario, 
                              highlightthickness=1, highlightbackground="#34495e")
        frame_tabla.pack(fill="both", expand=True, padx=10)
        
        # Crear Treeview (tabla) con más columnas
        columnas = ("Empresa", "Año", "Moneda", "Total Activos", "Total Pasivos")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        tabla.heading("Empresa", text="Empresa")
        tabla.heading("Año", text="Año")
        tabla.heading("Moneda", text="Moneda")
        tabla.heading("Total Activos", text="Total Activos")
        tabla.heading("Total Pasivos", text="Total Pasivos")
        
        tabla.column("Empresa", width=250, anchor="w")
        tabla.column("Año", width=100, anchor="center")
        tabla.column("Moneda", width=150, anchor="center")
        tabla.column("Total Activos", width=200, anchor="e")
        tabla.column("Total Pasivos", width=200, anchor="e")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2c3e50",
                       foreground="white",
                       fieldbackground="#2c3e50",
                       borderwidth=0,
                       font=("Segoe UI", 10),
                       rowheight=28)
        style.configure("Treeview.Heading",
                       background=self.parent_app.color_acento,
                       foreground="white",
                       borderwidth=0,
                       font=("Segoe UI", 11, "bold"),
                       relief="flat")
        style.map("Treeview", 
                 background=[("selected", self.parent_app.color_exito)],
                 foreground=[("selected", "white")])
        
        # Insertar datos de ejemplo (aquí se cargarían los datos reales guardados)
        for registro in self.parent_app.registros_financieros:
            total_activos = sum([
                registro.get("ACTIVOS_Efectivo y Equivalentes", 0),
                registro.get("ACTIVOS_Cuentas por Cobrar", 0),
                registro.get("ACTIVOS_Inventarios", 0),
                registro.get("ACTIVOS_Activos Fijos", 0),
                registro.get("ACTIVOS_Otros Activos", 0)
            ])
            
            total_pasivos = sum([
                registro.get("PASIVOS_Cuentas por Pagar", 0),
                registro.get("PASIVOS_Préstamos Bancarios", 0),
                registro.get("PASIVOS_Obligaciones Financieras", 0),
                registro.get("PASIVOS_Otros Pasivos", 0)
            ])
            
            tabla.insert("", "end", values=(
                registro.get("nombre_empresa", "N/A"),
                registro.get("anio", "N/A"),
                registro.get("tipo_moneda", "N/A"),
                f"${total_activos:,.2f}",
                f"${total_pasivos:,.2f}"
            ), tags=(str(self.parent_app.registros_financieros.index(registro)),))
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        
        tabla.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=self.parent_app.bg_principal)
        frame_botones.pack(fill="x", pady=(20, 0))
        
        def editar_seleccion():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Por favor selecciona un registro para editar")
                return
            
            # Obtener el índice del registro seleccionado
            item = tabla.item(seleccion[0])
            indice = int(item["tags"][0])
            
            # Obtener los datos completos del registro
            self.datos_actuales = self.parent_app.registros_financieros[indice]
            self.indice_actual = indice
            
            # Cerrar ventana de selección y abrir ventana de edición
            ventana_seleccion.destroy()
            self.abrir_formulario_edicion()
        
        btn_editar = tk.Button(
            frame_botones,
            text="✏️ Editar Seleccionado",
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=12,
            borderwidth=0,
            activebackground=self.parent_app.ajustar_color(self.parent_app.color_acento, 1.2),
            activeforeground="white",
            command=editar_seleccion
        )
        btn_editar.pack(side="left", padx=10, expand=True)
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="❌ Cerrar",
            font=("Segoe UI", 12, "bold"),
            bg="#6c7a89",
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=12,
            borderwidth=0,
            activebackground=self.parent_app.ajustar_color("#6c7a89", 1.2),
            activeforeground="white",
            command=ventana_seleccion.destroy
        )
        btn_cerrar.pack(side="right", padx=10, expand=True)
    
    def abrir_formulario_edicion(self):
        """Abre el formulario de edición con los datos pre-cargados"""
        ventana_edicion = tk.Toplevel(self.parent_app.root)
        ventana_edicion.title("Editar Datos Financieros")
        ventana_edicion.geometry("900x750")
        ventana_edicion.config(bg=self.parent_app.bg_principal)
        ventana_edicion.resizable(False, False)
        
        # Centrar ventana
        ventana_edicion.update_idletasks()
        x = (ventana_edicion.winfo_screenwidth() // 2) - (450)
        y = (ventana_edicion.winfo_screenheight() // 2) - (375)
        ventana_edicion.geometry(f'900x750+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_edicion, bg=self.parent_app.bg_secundario, height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="✏️ Editar Datos Financieros",
            font=("Segoe UI", 18, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=25)
        
        # Frame principal con scroll
        canvas = tk.Canvas(ventana_edicion, bg=self.parent_app.bg_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_edicion, orient="vertical", command=canvas.yview)
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
            ventana_edicion.destroy()
        
        ventana_edicion.protocol("WM_DELETE_WINDOW", on_closing)
        
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
            text="💾 Guardar Cambios",
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_exito,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=12,
            activebackground="#2d8f5a",
            command=lambda: self.guardar_cambios(ventana_edicion)
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
        """Crea la sección de información general con datos pre-cargados"""
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        
        label_titulo = tk.Label(
            frame_seccion,
            text="INFORMACIÓN GENERAL",
            font=("Segoe UI", 14, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=10
        )
        label_titulo.pack(fill="x")
        
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
        entry_empresa.insert(0, self.datos_actuales.get("nombre_empresa", ""))
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
        entry_anio.insert(0, str(self.datos_actuales.get("anio", "")))
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
        combo_moneda.set(self.datos_actuales.get("tipo_moneda", "USD - Dólar Estadounidense"))
        combo_moneda.pack(side="left", ipady=3)
        self.entries["tipo_moneda"] = combo_moneda
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                       fieldbackground="#2c3e50",
                       background="#2c3e50",
                       foreground="white",
                       arrowcolor="white",
                       borderwidth=0)
    
    def crear_seccion_datos(self, parent, titulo, campos, fila):
        """Crea una sección de ingreso de datos con valores pre-cargados"""
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        
        label_titulo = tk.Label(
            frame_seccion,
            text=titulo,
            font=("Segoe UI", 14, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=10
        )
        label_titulo.pack(fill="x")
        
        frame_campos = tk.Frame(frame_seccion, bg=self.parent_app.bg_secundario)
        frame_campos.pack(fill="both", padx=20, pady=15)
        
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
            
            key = f"{titulo}_{campo}"
            valor_existente = self.datos_actuales.get(key, 0)
            if valor_existente != 0:
                entry.insert(0, str(valor_existente))
            
            entry.pack(side="left", ipady=5)
            self.entries[key] = entry
            
            label_moneda = tk.Label(
                frame_campo,
                text="$",
                font=("Segoe UI", 10, "bold"),
                bg=self.parent_app.bg_secundario,
                fg="#3bb273"
            )
            label_moneda.pack(side="left", padx=(5, 0))
    
    def guardar_cambios(self, ventana):
        """Guarda los cambios realizados en el registro"""
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
        
        try:
            anio_num = int(anio)
            if anio_num < 1900 or anio_num > 2100:
                messagebox.showwarning("Año Inválido", "Por favor ingresa un año válido (1900-2100)")
                return
        except ValueError:
            messagebox.showwarning("Año Inválido", "El año debe ser un número válido")
            return
        
        datos_actualizados = {
            "nombre_empresa": nombre_empresa,
            "anio": anio_num,
            "tipo_moneda": tipo_moneda
        }
        
        # Recopilar todos los valores de los campos
        for key, entry in self.entries.items():
            if key not in ["nombre_empresa", "anio", "tipo_moneda"]:
                valor = entry.get().strip()
                try:
                    datos_actualizados[key] = float(valor) if valor else 0
                except ValueError:
                    datos_actualizados[key] = 0
        
        # Actualizar el registro en la lista principal
        self.parent_app.registros_financieros[self.indice_actual] = datos_actualizados
        
        messagebox.showinfo(
            "Cambios Guardados",
            f"Los datos financieros han sido actualizados exitosamente.\n\n"
            f"Empresa: {nombre_empresa}\n"
            f"Año: {anio}\n"
            f"Moneda: {tipo_moneda}"
        )
        ventana.destroy()
