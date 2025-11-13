import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class BalanceGeneral:
    def __init__(self, parent, datos_financieros):
        self.parent = parent
        self.datos = datos_financieros
        
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        
        # Use 85% of screen space, with minimum of 900x700
        window_width = max(900, int(screen_width * 0.85))
        window_height = max(700, int(screen_height * 0.85))
        
        # Limit to maximum reasonable size
        window_width = min(1400, window_width)
        window_height = min(900, window_height)
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Balance General")
        self.ventana.geometry(f"{window_width}x{window_height}")
        self.ventana.configure(bg="#1e293b")
        
        # Center window on screen
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.ventana.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        frame_header = tk.Frame(self.ventana, bg="#0f172a")
        frame_header.pack(fill="x", pady=(0, 20))
        
        label_titulo = tk.Label(
            frame_header,
            text="📊 Balance General",
            font=("Segoe UI", 24, "bold"),
            bg="#0f172a",
            fg="white",
            wraplength=int(window_width * 0.9)
        )
        label_titulo.pack(pady=10)
        
        # Información de la empresa
        info_frame = tk.Frame(frame_header, bg="#0f172a")
        info_frame.pack(pady=(0, 15))
        
        label_empresa = tk.Label(
            info_frame,
            text=f"{self.datos.get('nombre_empresa', 'N/A')}",
            font=("Segoe UI", 14, "bold"),
            bg="#0f172a",
            fg="#94a3b8",
            wraplength=int(window_width * 0.9)
        )
        label_empresa.pack()
        
        label_info = tk.Label(
            info_frame,
            text=f"Año: {self.datos.get('anio', 'N/A')} | Moneda: {self.datos.get('tipo_moneda', 'N/A')} ",
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#64748b",
            wraplength=int(window_width * 0.9)
        )
        label_info.pack(pady=(0, 5))
        
        # Frame principal con scroll
        frame_contenedor = tk.Frame(self.ventana, bg="#1e293b")
        frame_contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_contenedor, bg="#1e293b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        
        frame_scroll = tk.Frame(canvas, bg="#1e293b")
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def on_closing():
            canvas.unbind_all("<MouseWheel>")
            self.ventana.destroy()
        
        self.ventana.protocol("WM_DELETE_WINDOW", on_closing)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        padding = int(window_width * 0.05) if window_width > 1000 else 20
        
        # Frame para el balance (dos columnas)
        frame_balance = tk.Frame(frame_scroll, bg="#1e293b")
        frame_balance.pack(fill="both", expand=True, padx=padding)
        
        # Configurar grid para dos columnas iguales
        frame_balance.columnconfigure(0, weight=1, uniform="col")
        frame_balance.columnconfigure(1, weight=1, uniform="col")
        
        # COLUMNA IZQUIERDA - ACTIVO
        self.crear_columna_activo(frame_balance)
        
        # COLUMNA DERECHA - PASIVO Y PATRIMONIO
        self.crear_columna_pasivo_patrimonio(frame_balance)
        
        # Frame de botones
        frame_botones = tk.Frame(self.ventana, bg="#1e293b")
        frame_botones.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="✕ Cerrar",
            command=on_closing,
            font=("Segoe UI", 11, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10
        )
        btn_cerrar.pack(side="right")
        
        btn_exportar = tk.Button(
            frame_botones,
            text="📄 Exportar PDF",
            command=self.exportar_pdf,
            font=("Segoe UI", 11, "bold"),
            bg="#0ea5e9",
            fg="white",
            activebackground="#0284c7",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10
        )
        btn_exportar.pack(side="right", padx=(0, 10))
    
    def crear_seccion_titulo(self, parent, texto, row, column):
        """Crea un título de sección"""
        frame = tk.Frame(parent, bg="#0f172a", relief="flat")
        frame.grid(row=row, column=column, sticky="ew", pady=(10, 5), padx=5)
        
        label = tk.Label(
            frame,
            text=texto,
            font=("Segoe UI", 13, "bold"),
            bg="#0f172a",
            fg="white",
            anchor="w",
            padx=15,
            pady=8
        )
        label.pack(fill="x")
    
    def crear_fila_cuenta(self, parent, nombre, valor, row, column, es_total=False, indent=False):
        """Crea una fila de cuenta con indentación opcional"""
        frame = tk.Frame(parent, bg="#334155" if not es_total else "#1e40af")
        frame.grid(row=row, column=column, sticky="ew", pady=2, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        
        # Nombre de la cuenta
        padding_left = 30 if indent else 15
        label_nombre = tk.Label(
            frame,
            text=nombre,
            font=("Segoe UI", 10, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="w",
            padx=padding_left,
            pady=6,
            wraplength=250
        )
        label_nombre.grid(row=0, column=0, sticky="w")
        
        # Valor
        valor_formateado = f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else valor
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 10, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="e",
            padx=15,
            pady=6
        )
        label_valor.grid(row=0, column=1, sticky="e")
    
    def crear_columna_activo(self, parent):
        """Crea la columna de ACTIVO con estructura detallada"""
        row = 0
        
        self.crear_seccion_titulo(parent, "ACTIVO", row, 0)
        row += 1
        
        # ACTIVO CORRIENTE
        self.crear_seccion_titulo(parent, "ACTIVO CORRIENTE", row, 0)
        row += 1
        
        efectivo = float(self.datos.get('ACTIVOS_Efectivo', 0))
        cuentas_cobrar_com = float(self.datos.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0))
        prestamos_cobrar = float(self.datos.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0))
        inventarios = float(self.datos.get('ACTIVOS_Inventarios', 0))
        gastos_anticipados = float(self.datos.get('ACTIVOS_Gastos_pagados_por_anticipado', 0))
        
        self.crear_fila_cuenta(parent, "Efectivo", efectivo, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Cuentas por cobrar comerciales y otras", cuentas_cobrar_com, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Préstamos por cobrar a partes relacionadas", prestamos_cobrar, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Inventarios", inventarios, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Gastos pagados por anticipado", gastos_anticipados, row, 0, indent=True)
        row += 1
        
        total_corriente = efectivo + cuentas_cobrar_com + prestamos_cobrar + inventarios + gastos_anticipados
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO CORRIENTE", total_corriente, row, 0, es_total=True)
        row += 1
        
        # ACTIVO NO CORRIENTE
        row += 1
        self.crear_seccion_titulo(parent, "ACTIVO NO CORRIENTE", row, 0)
        row += 1
        
        propiedades = float(self.datos.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0))
        intangibles = float(self.datos.get('ACTIVOS_Activos_intangibles', 0))
        impuesto_diferido = float(self.datos.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0))
        otros_activos = float(self.datos.get('ACTIVOS_Otros_activos', 0))
        
        self.crear_fila_cuenta(parent, "Propiedades, plantas y equipos", propiedades, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Activos intangibles", intangibles, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Impuesto sobre la renta diferido", impuesto_diferido, row, 0, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Otros activos", otros_activos, row, 0, indent=True)
        row += 1
        
        total_no_corriente = propiedades + intangibles + impuesto_diferido + otros_activos
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO NO CORRIENTE", total_no_corriente, row, 0, es_total=True)
        row += 1
        
        row += 1
        total_activo = total_corriente + total_no_corriente
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO", total_activo, row, 0, es_total=True)
    
    def crear_columna_pasivo_patrimonio(self, parent):
        """Crea la columna de PASIVO Y PATRIMONIO con estructura detallada"""
        row = 0
        
        self.crear_seccion_titulo(parent, "PASIVO", row, 1)
        row += 1
        
        # PASIVO CORRIENTE
        self.crear_seccion_titulo(parent, "PASIVO CORRIENTE", row, 1)
        row += 1
        
        prest_corto = float(self.datos.get('PASIVOS_Prestamos_por_pagar_a_corto_plazo', 0))
        prest_partes_corto = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_corto_plazo', 0))
        prest_partes_porcion = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_porcion_corriente', 0))
        cuentas_pagar = float(self.datos.get('PASIVOS_Cuentas_por_pagar_comerciales', 0))
        ingresos_diferidos = float(self.datos.get('PASIVOS_Ingresos_diferidos', 0))
        otras_cuentas = float(self.datos.get('PASIVOS_Otras_cuentas_por_pagar', 0))
        dividendos = float(self.datos.get('PASIVOS_Dividendos_por_pagar', 0))
        
        self.crear_fila_cuenta(parent, "Préstamos por pagar a corto plazo", prest_corto, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Préstamos a partes relacionadas corto plazo", prest_partes_corto, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Préstamos a partes relacionadas porción corriente", prest_partes_porcion, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Cuentas por pagar comerciales", cuentas_pagar, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Ingresos diferidos", ingresos_diferidos, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Otras cuentas por pagar y acumuladas", otras_cuentas, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Dividendos por pagar", dividendos, row, 1, indent=True)
        row += 1
        
        total_pasivo_corriente = prest_corto + prest_partes_corto + prest_partes_porcion + cuentas_pagar + ingresos_diferidos + otras_cuentas + dividendos
        self.crear_fila_cuenta(parent, "TOTAL PASIVO CORRIENTE", total_pasivo_corriente, row, 1, es_total=True)
        row += 1
        
        # PASIVO NO CORRIENTE
        row += 1
        self.crear_seccion_titulo(parent, "PASIVO NO CORRIENTE", row, 1)
        row += 1
        
        prest_largo = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_largo_plazo', 0))
        
        self.crear_fila_cuenta(parent, "Préstamos a partes relacionadas largo plazo", prest_largo, row, 1, indent=True)
        row += 1
        
        self.crear_fila_cuenta(parent, "TOTAL PASIVO NO CORRIENTE", prest_largo, row, 1, es_total=True)
        row += 1
        
        row += 1
        total_pasivo = total_pasivo_corriente + prest_largo
        self.crear_fila_cuenta(parent, "TOTAL PASIVO", total_pasivo, row, 1, es_total=True)
        row += 1
        
        # PATRIMONIO O CAPITAL CONTABLE
        row += 1
        self.crear_seccion_titulo(parent, "PATRIMONIO O CAPITAL CONTABLE", row, 1)
        row += 1
        
        capital_social = float(self.datos.get('PATRIMONIO_Capital_social', 0))
        capital_minimo = float(self.datos.get('PATRIMONIO_Capital_social_minimo', 0))
        reserva_legal = float(self.datos.get('PATRIMONIO_Reserva_legal', 0))
        deficit = float(self.datos.get('PATRIMONIO_Deficit_acumulado', 0))
        
        self.crear_fila_cuenta(parent, "Capital social", capital_social, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Capital social mínimo", capital_minimo, row, 1, indent=True)
        row += 1
        self.crear_fila_cuenta(parent, "Reserva legal", reserva_legal, row, 1, indent=True)
        row += 1
        deficit_display = -deficit if deficit > 0 else deficit
        self.crear_fila_cuenta(parent, "Déficit acumulado", deficit_display, row, 1, indent=True)
        row += 1
        
        total_patrimonio = capital_social  + reserva_legal - deficit
        self.crear_fila_cuenta(parent, "TOTAL PATRIMONIO", total_patrimonio, row, 1, es_total=True)
        row += 1
        
        row += 1
        total_pasivo_patrimonio = total_pasivo + total_patrimonio
        self.crear_fila_cuenta(parent, "TOTAL PASIVO Y PATRIMONIO", total_pasivo_patrimonio, row, 1, es_total=True)
    
    def exportar_pdf(self):
        """Exporta el balance general a PDF"""
        messagebox.showinfo(
            "Exportar PDF",
            "Funcionalidad de exportación a PDF en desarrollo.\n\n"
            "Próximamente podrás exportar este reporte."
        )

def generar_balance_general(parent, datos_financieros):
    """Función principal para generar el balance general"""
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el balance general.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    BalanceGeneral(parent, datos_financieros)
