import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AnalisisVerticalEstadoResultados:
    def __init__(self, parent, datos_financieros):
        self.parent = parent
        self.datos = datos_financieros
        
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        
        window_width = max(900, int(screen_width * 0.85))
        window_height = max(700, int(screen_height * 0.85))
        
        window_width = min(1400, window_width)
        window_height = min(900, window_height)
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Análisis Vertical - Estado de Resultados")
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
            text="📊 Análisis Vertical - Estado de Resultados",
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
        
        # Frame para el análisis vertical
        frame_analisis = tk.Frame(frame_scroll, bg="#1e293b")
        frame_analisis.pack(fill="both", expand=True, padx=padding)
        
        self.crear_analisis_vertical_resultados(frame_analisis)
        
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
    
    def crear_seccion_titulo(self, parent, texto, row):
        frame = tk.Frame(parent, bg="#0f172a", relief="flat")
        frame.grid(row=row, column=0, sticky="ew", pady=(10, 5), padx=5)
        
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
    
    def crear_fila_vertical(self, parent, nombre, valor, porcentaje, row, es_total=False, indent=False):
        frame = tk.Frame(parent, bg="#334155" if not es_total else "#1e40af")
        frame.grid(row=row, column=0, sticky="ew", pady=2, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=0)
        
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
        
        valor_formateado = f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else valor
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 10, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="e",
            padx=8,
            pady=6
        )
        label_valor.grid(row=0, column=1, sticky="e")
        
        porcentaje_formateado = f"{porcentaje:.2f}%" if isinstance(porcentaje, (int, float)) else porcentaje
        label_porcentaje = tk.Label(
            frame,
            text=porcentaje_formateado,
            font=("Segoe UI", 10, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="#fbbf24",
            anchor="e",
            padx=15,
            pady=6
        )
        label_porcentaje.grid(row=0, column=2, sticky="e")
    
    def crear_analisis_vertical_resultados(self, parent):
        row = 0
        
        ventas = float(self.datos.get('INGRESOS_Ventas', 0))
        ingresos_servicios = float(self.datos.get('INGRESOS_Ingresos_por_Servicios', 0))
        otros_ingresos = float(self.datos.get('INGRESOS_Otros_Ingresos', 0))
        costo_ventas = float(self.datos.get('GASTOS_Costo_de_Ventas', 0))
        gastos_admin = float(self.datos.get('GASTOS_Gastos_Administrativos', 0))
        gastos_ventas = float(self.datos.get('GASTOS_Gastos_de_Ventas', 0))
        gastos_financieros = float(self.datos.get('GASTOS_Gastos_Financieros', 0))
        otros_gastos = float(self.datos.get('GASTOS_Otros_Gastos', 0))
        ingresos_financieros = float(self.datos.get('INGRESOS_Ingresos_Financieros', 0))
        
        total_ingresos = ventas + ingresos_servicios + otros_ingresos
        if total_ingresos == 0:
            total_ingresos = 1
        
        self.crear_seccion_titulo(parent, "ANÁLISIS VERTICAL - ESTADO DE RESULTADOS", row)
        row += 1
        
        self.crear_seccion_titulo(parent, "INGRESOS OPERACIONALES", row)
        row += 1
        
        self.crear_fila_vertical(parent, "Ventas", ventas, (ventas/total_ingresos)*100, row, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Ingresos por Servicios", ingresos_servicios, (ingresos_servicios/total_ingresos)*100, row, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Otros Ingresos", otros_ingresos, (otros_ingresos/total_ingresos)*100, row, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL INGRESOS", total_ingresos, 100.0, row, es_total=True)
        row += 2
        
        self.crear_fila_vertical(parent, "(-) Costo de Ventas", abs(costo_ventas), (abs(costo_ventas)/total_ingresos)*100, row, indent=True)
        row += 1
        
        utilidad_bruta = total_ingresos - abs(costo_ventas)
        self.crear_fila_vertical(parent, "UTILIDAD BRUTA", utilidad_bruta, (utilidad_bruta/total_ingresos)*100, row, es_total=True)
        row += 2
        
        self.crear_seccion_titulo(parent, "GASTOS OPERACIONALES", row)
        row += 1
        
        self.crear_fila_vertical(parent, "Gastos Administrativos", abs(gastos_admin), (abs(gastos_admin)/total_ingresos)*100, row, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Gastos de Ventas", abs(gastos_ventas), (abs(gastos_ventas)/total_ingresos)*100, row, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Otros Gastos", abs(otros_gastos), (abs(otros_gastos)/total_ingresos)*100, row, indent=True)
        row += 1
        
        total_gastos_operacionales = abs(gastos_admin) + abs(gastos_ventas) + abs(otros_gastos)
        self.crear_fila_vertical(parent, "TOTAL GASTOS OPERACIONALES", total_gastos_operacionales, (total_gastos_operacionales/total_ingresos)*100, row, es_total=True)
        row += 2
        
        utilidad_operativa = utilidad_bruta - total_gastos_operacionales
        self.crear_fila_vertical(parent, "UTILIDAD (PÉRDIDA) OPERATIVA", utilidad_operativa, (utilidad_operativa/total_ingresos)*100, row, es_total=True)
        row += 2
        
        self.crear_seccion_titulo(parent, "INGRESOS Y GASTOS FINANCIEROS", row)
        row += 1
        
        self.crear_fila_vertical(parent, "Ingresos Financieros", ingresos_financieros, (ingresos_financieros/total_ingresos)*100, row, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Gastos Financieros", abs(gastos_financieros), (abs(gastos_financieros)/total_ingresos)*100, row, indent=True)
        row += 1
        
        resultado_financiero = ingresos_financieros - abs(gastos_financieros)
        self.crear_fila_vertical(parent, "Resultado Financiero Neto", resultado_financiero, (resultado_financiero/total_ingresos)*100, row, es_total=True)
        row += 2
        
        utilidad_antes_impuestos = utilidad_operativa + resultado_financiero
        self.crear_fila_vertical(parent, "UTILIDAD (PÉRDIDA) ANTES DE IMPUESTOS", utilidad_antes_impuestos, (utilidad_antes_impuestos/total_ingresos)*100, row, es_total=True)
        row += 2
        
        impuestos_tasa = 0.30
        impuestos = utilidad_antes_impuestos * impuestos_tasa if utilidad_antes_impuestos > 0 else 0
        self.crear_fila_vertical(parent, "(-) Impuesto sobre la Renta (30%)", impuestos, (impuestos/total_ingresos)*100, row)
        row += 1
        
        utilidad_neta = utilidad_antes_impuestos - impuestos
        self.crear_fila_vertical(parent, "UTILIDAD NETA DEL EJERCICIO", utilidad_neta, (utilidad_neta/total_ingresos)*100, row, es_total=True)
    
    def exportar_pdf(self):
        messagebox.showinfo(
            "Exportar PDF",
            "Funcionalidad de exportación a PDF en desarrollo.\n\n"
            "Próximamente podrás exportar este reporte."
        )

def generar_analisis_vertical_estado_resultados(parent, datos_financieros):
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el Análisis Vertical.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    AnalisisVerticalEstadoResultados(parent, datos_financieros)
