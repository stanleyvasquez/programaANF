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
        ventana_ingreso.geometry("950x700")
        ventana_ingreso.config(bg=self.parent_app.bg_principal)
        ventana_ingreso.resizable(False, False)
        
        # Centrar ventana
        ventana_ingreso.update_idletasks()
        x = (ventana_ingreso.winfo_screenwidth() // 2) - (475)
        y = (ventana_ingreso.winfo_screenheight() // 2) - (350)
        ventana_ingreso.geometry(f'950x700+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_ingreso, bg=self.parent_app.bg_secundario, height=70)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="📝 Ingreso de Datos Financieros",
            font=("Segoe UI", 18, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=20)
        
        # Frame contenedor para centrar el contenido
        frame_contenedor = tk.Frame(ventana_ingreso, bg=self.parent_app.bg_principal)
        frame_contenedor.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Frame principal con scroll
        canvas = tk.Canvas(frame_contenedor, bg=self.parent_app.bg_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.parent_app.bg_principal)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def on_closing():
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass
            ventana_ingreso.destroy()
        
        ventana_ingreso.protocol("WM_DELETE_WINDOW", on_closing)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(60, 0))
        scrollbar.pack(side="right", fill="y")
        
        self.crear_seccion_informacion_general(frame_scroll, 0)
        
        frame_columnas = tk.Frame(frame_scroll, bg=self.parent_app.bg_principal)
        frame_columnas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        frame_columnas.grid_columnconfigure(0, weight=1, uniform="col")
        frame_columnas.grid_columnconfigure(1, weight=1, uniform="col")
        
        frame_col_izq = tk.Frame(frame_columnas, bg=self.parent_app.bg_principal)
        frame_col_izq.grid(row=0, column=0, sticky="nsew", padx=5)
        
        self.crear_seccion_datos_compacta(frame_col_izq, "ACTIVOS", [
            {
                'subrubro': 'Activo Corriente',
                'campos': [
                    'Efectivo',
                    'Cuentas por cobrar comerciales',
                    'Préstamos por cobrar a partes relacionadas',
                    'Inventarios',
                    'Gastos pagados por anticipado'
                ]
            },
            {
                'subrubro': 'Activo No Corriente',
                'campos': [
                    'Propiedades, plantas y equipos',
                    'Activos intangibles',
                    'Impuesto sobre la renta diferido',
                    'Otros activos'
                ]
            }
        ], 0)
        
        self.crear_seccion_datos_compacta(frame_col_izq, "PASIVOS", [
            {
                'subrubro': 'Pasivo Corriente',
                'campos': [
                    'Préstamos por pagar a corto plazo',
                    'Préstamos a partes relacionadas corto plazo',
                    'Préstamos a partes relacionadas porción corriente',
                    'Cuentas por pagar comerciales',
                    'Ingresos diferidos',
                    'Otras cuentas por pagar',
                    'Dividendos por pagar'
                ]
            },
            {
                'subrubro': 'Pasivo No Corriente',
                'campos': [
                    'Préstamos a partes relacionadas largo plazo'
                ]
            }
        ], 1)
        
        frame_col_der = tk.Frame(frame_columnas, bg=self.parent_app.bg_principal)
        frame_col_der.grid(row=0, column=1, sticky="nsew", padx=5)
        
        self.crear_seccion_datos_compacta(frame_col_der, "PATRIMONIO", [
            {
                'subrubro': 'Capital Contable',
                'campos': [
                    'Capital social',
                    'Capital social mínimo',
                    'Reserva legal',
                    'Déficit acumulado'
                ]
            }
        ], 0)
        
           # INGRESOS (operacionales + financieros)
        self.crear_seccion_datos_compacta(frame_col_der, "INGRESOS", [
            "Ventas",
            "Ingresos por Servicios",
            "Otros Ingresos",
            "Ingresos Financieros"
        ], 1)
        
        # GASTOS (operacionales, financieros e impuestos)
        # 👇 IMPORTANTE: aquí se espera que los gastos se ingresen en NEGATIVO
        self.crear_seccion_datos_compacta(frame_col_der, "GASTOS", [
            "Costo de Ventas",
            "Gastos Administrativos",
            "Gastos de Ventas",
            "Gastos Financieros",
            "Otros Gastos",
            "Impuesto sobre la Renta",
            "Contribucion Especial"
        ], 2)

        
        frame_botones = tk.Frame(frame_scroll, bg=self.parent_app.bg_principal)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew", padx=20)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar Datos",
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_exito,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=40,
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
            padx=40,
            pady=12,
            activebackground="#c23850",
            command=on_closing
        )
        btn_cancelar.pack(side="right", padx=10, expand=True)
    
    def crear_seccion_informacion_general(self, parent, fila):
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, columnspan=2, pady=10, padx=15, sticky="ew")
        
        label_titulo = tk.Label(
            frame_seccion,
            text="INFORMACIÓN GENERAL",
            font=("Segoe UI", 13, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=8
        )
        label_titulo.pack(fill="x")
        
        frame_campos = tk.Frame(frame_seccion, bg=self.parent_app.bg_secundario)
        frame_campos.pack(fill="both", padx=15, pady=12)
        
        frame_campos.grid_columnconfigure(0, weight=1)
        frame_campos.grid_columnconfigure(1, weight=1)
        frame_campos.grid_columnconfigure(2, weight=1)
        
        frame_empresa = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_empresa.grid(row=0, column=0, padx=8, sticky="ew")
        
        label_empresa = tk.Label(
            frame_empresa,
            text="Nombre de la Empresa:",
            font=("Segoe UI", 9, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            anchor="w"
        )
        label_empresa.pack(anchor="w", pady=(0, 3))
        
        entry_empresa = tk.Entry(
            frame_empresa,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        entry_empresa.pack(fill="x", ipady=6)
        self.entries["nombre_empresa"] = entry_empresa
        
        frame_anio = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_anio.grid(row=0, column=1, padx=8, sticky="ew")
        
        label_anio = tk.Label(
            frame_anio,
            text="Año del Análisis:",
            font=("Segoe UI", 9, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            anchor="w"
        )
        label_anio.pack(anchor="w", pady=(0, 3))
        
        entry_anio = tk.Entry(
            frame_anio,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        entry_anio.pack(fill="x", ipady=6)
        self.entries["anio"] = entry_anio
        
        frame_moneda = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
        frame_moneda.grid(row=0, column=2, padx=8, sticky="ew")
        
        label_moneda = tk.Label(
            frame_moneda,
            text="Tipo de Moneda:",
            font=("Segoe UI", 9, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto,
            anchor="w"
        )
        label_moneda.pack(anchor="w", pady=(0, 3))
        
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
            font=("Segoe UI", 9),
            state="readonly"
        )
        combo_moneda.set("USD - Dólar Estadounidense")
        combo_moneda.pack(fill="x", ipady=4)
        self.entries["tipo_moneda"] = combo_moneda
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                       fieldbackground="#2c3e50",
                       background="#2c3e50",
                       foreground="white",
                       arrowcolor="white",
                       borderwidth=0)
    
    def crear_seccion_datos_compacta(self, parent, titulo, campos, fila):
        frame_seccion = tk.Frame(parent, bg=self.parent_app.bg_secundario, relief="solid", borderwidth=1)
        frame_seccion.grid(row=fila, column=0, pady=8, sticky="ew")
        
        label_titulo = tk.Label(
            frame_seccion,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=self.parent_app.color_acento,
            fg="white",
            pady=6
        )
        label_titulo.pack(fill="x")
        
        frame_campos = tk.Frame(frame_seccion, bg=self.parent_app.bg_secundario)
        frame_campos.pack(fill="both", padx=12, pady=10)
        
        for item in campos:
            if isinstance(item, dict):
                # Es un subrubro con sus propios campos
                subrubro = item.get('subrubro', '')
                subcampos = item.get('campos', [])
                
                # Etiqueta del subrubro
                label_subrubro = tk.Label(
                    frame_campos,
                    text=subrubro,
                    font=("Segoe UI", 9, "bold"),
                    bg=self.parent_app.bg_secundario,
                    fg="#94a3b8"
                )
                label_subrubro.pack(fill="x", pady=(8, 4), padx=(0, 0))
                
                # Campos del subrubro
                for subcampo in subcampos:
                    frame_campo = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
                    frame_campo.pack(fill="x", pady=2)
                    
                    label = tk.Label(
                        frame_campo,
                        text=subcampo + ":",
                        font=("Segoe UI", 8),
                        bg=self.parent_app.bg_secundario,
                        fg=self.parent_app.color_texto,
                        width=28,
                        anchor="w"
                    )
                    label.pack(side="left", padx=(15, 8))
                    
                    entry = tk.Entry(
                        frame_campo,
                        font=("Segoe UI", 8),
                        bg="#2c3e50",
                        fg="white",
                        insertbackground="white",
                        relief="flat",
                        width=18
                    )
                    entry.pack(side="left", ipady=3, fill="x", expand=True)
                    
                    key = f"{titulo}_{subcampo}".replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                    self.entries[key] = entry
                    
                    label_moneda = tk.Label(
                        frame_campo,
                        text="$",
                        font=("Segoe UI", 9, "bold"),
                        bg=self.parent_app.bg_secundario,
                        fg="#3bb273"
                    )
                    label_moneda.pack(side="left", padx=(4, 0))
            else:
                # Campo simple
                frame_campo = tk.Frame(frame_campos, bg=self.parent_app.bg_secundario)
                frame_campo.pack(fill="x", pady=4)
                
                label = tk.Label(
                    frame_campo,
                    text=item + ":",
                    font=("Segoe UI", 9),
                    bg=self.parent_app.bg_secundario,
                    fg=self.parent_app.color_texto,
                    width=20,
                    anchor="w"
                )
                label.pack(side="left", padx=(0, 8))
                
                entry = tk.Entry(
                    frame_campo,
                    font=("Segoe UI", 9),
                    bg="#2c3e50",
                    fg="white",
                    insertbackground="white",
                    relief="flat",
                    width=20
                )
                entry.pack(side="left", ipady=4, fill="x", expand=True)
                
                key = f"{titulo}_{item}".replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                self.entries[key] = entry
                
                label_moneda = tk.Label(
                    frame_campo,
                    text="$",
                    font=("Segoe UI", 10, "bold"),
                    bg=self.parent_app.bg_secundario,
                    fg="#3bb273"
                )
                label_moneda.pack(side="left", padx=(4, 0))

    def guardar_datos(self, ventana):
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
        
        nuevo_registro = {
            "nombre_empresa": nombre_empresa,
            "anio": anio_num,
            "tipo_moneda": tipo_moneda
        }
        
        for key, entry in self.entries.items():
            if key not in ["nombre_empresa", "anio", "tipo_moneda"]:
                valor = entry.get().strip()
                try:
                    valor_numerico = float(valor) if valor else 0
                except ValueError:
                    valor_numerico = 0
                
                # Guardar con la clave exacta del formato SECCION_CampoNormalizado
                nuevo_registro[key] = valor_numerico
        
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
