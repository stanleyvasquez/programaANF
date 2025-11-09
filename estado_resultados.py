import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class EstadoResultados:
    def __init__(self, parent, datos_financieros):
        self.parent = parent
        self.datos = datos_financieros
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Estado de Resultados")
        self.ventana.geometry("1100x800")
        self.ventana.configure(bg="#1e293b")
        
        # Header
        frame_header = tk.Frame(self.ventana, bg="#0f172a", height=100)
        frame_header.pack(fill="x", pady=(0, 20))
        frame_header.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_header,
            text="💰 Estado de Resultados",
            font=("Segoe UI", 24, "bold"),
            bg="#0f172a",
            fg="white"
        )
        label_titulo.pack(pady=10)
        
        # Información de la empresa
        info_frame = tk.Frame(frame_header, bg="#0f172a")
        info_frame.pack()
        
        label_empresa = tk.Label(
            info_frame,
            text=f"{self.datos.get('nombre_empresa', 'N/A')}",
            font=("Segoe UI", 14, "bold"),
            bg="#0f172a",
            fg="#94a3b8"
        )
        label_empresa.pack()
        
        label_info = tk.Label(
            info_frame,
            text=f"Año: {self.datos.get('anio', 'N/A')} | Moneda: {self.datos.get('tipo_moneda', 'N/A')}",
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#64748b"
        )
        label_info.pack()
        
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
        
        # Frame para el estado de resultados (una sola columna)
        frame_resultados = tk.Frame(frame_scroll, bg="#1e293b")
        frame_resultados.pack(fill="both", expand=True, padx=60)
        
        # Crear estado de resultados
        self.crear_estado_resultados(frame_resultados)
        
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
        """Crea un título de sección"""
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
    
    def crear_fila_cuenta(self, parent, nombre, valor, row, es_total=False, es_subtotal=False, indent=False):
        """Crea una fila de cuenta con indentación opcional"""
        if es_total:
            bg_color = "#1e40af"
        elif es_subtotal:
            bg_color = "#334155"
        else:
            bg_color = "#475569"
        
        frame = tk.Frame(parent, bg=bg_color)
        frame.grid(row=row, column=0, sticky="ew", pady=2, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        
        # Nombre de la cuenta
        padding_left = 30 if indent else 15
        label_nombre = tk.Label(
            frame,
            text=nombre,
            font=("Segoe UI", 10, "bold" if (es_total or es_subtotal) else "normal"),
            bg=bg_color,
            fg="white",
            anchor="w",
            padx=padding_left,
            pady=6
        )
        label_nombre.grid(row=0, column=0, sticky="w")
        
        # Valor
        valor_formateado = f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else valor
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 10, "bold" if (es_total or es_subtotal) else "normal"),
            bg=bg_color,
            fg="white",
            anchor="e",
            padx=15,
            pady=6
        )
        label_valor.grid(row=0, column=1, sticky="e")
    
    def crear_estado_resultados(self, parent):
            """Crea el estado de resultados completo"""
            row = 0
            
            # Obtener datos
            ventas = float(self.datos.get('INGRESOS_Ventas', 0))
            ingresos_servicios = float(self.datos.get('INGRESOS_Ingresos_por_Servicios', 0))
            otros_ingresos = float(self.datos.get('INGRESOS_Otros_Ingresos', 0))
            
            costo_ventas = float(self.datos.get('GASTOS_Costo_de_Ventas', 0))
            gastos_admin = float(self.datos.get('GASTOS_Gastos_Administrativos', 0))
            gastos_ventas = float(self.datos.get('GASTOS_Gastos_de_Ventas', 0))
            gastos_financieros = float(self.datos.get('GASTOS_Gastos_Financieros', 0))
            otros_gastos = float(self.datos.get('GASTOS_Otros_Gastos', 0))
            
            # Títulos y cálculos
            self.crear_seccion_titulo(parent, "ESTADO DE RESULTADOS", row)
            row += 1
            
            # INGRESOS
            self.crear_seccion_titulo(parent, "INGRESOS OPERACIONALES", row)
            row += 1
            
            self.crear_fila_cuenta(parent, "Ventas", ventas, row, indent=True)
            row += 1
            self.crear_fila_cuenta(parent, "Ingresos por Servicios", ingresos_servicios, row, indent=True)
            row += 1
            self.crear_fila_cuenta(parent, "Otros Ingresos", otros_ingresos, row, indent=True)
            row += 1
            
            total_ingresos = ventas + ingresos_servicios + otros_ingresos
            self.crear_fila_cuenta(parent, "TOTAL INGRESOS", total_ingresos, row, es_subtotal=True)
            row += 2
            
            # COSTO DE VENTAS
            self.crear_fila_cuenta(parent, "(-) Costo de Ventas", costo_ventas, row, indent=True)
            row += 1
            
            utilidad_bruta = total_ingresos - costo_ventas
            self.crear_fila_cuenta(parent, "UTILIDAD BRUTA", utilidad_bruta, row, es_subtotal=True)
            row += 2
            
            # GASTOS OPERACIONALES (sin incluir gastos financieros)
            self.crear_seccion_titulo(parent, "GASTOS OPERACIONALES", row)
            row += 1

            self.crear_fila_cuenta(parent, "Gastos Administrativos", gastos_admin, row, indent=True)
            row += 1
            self.crear_fila_cuenta(parent, "Gastos de Ventas", gastos_ventas, row, indent=True)
            row += 1
            self.crear_fila_cuenta(parent, "Otros Gastos", otros_gastos, row, indent=True)
            row += 1

            total_gastos_operacionales = gastos_admin + gastos_ventas + otros_gastos
            self.crear_fila_cuenta(parent, "TOTAL GASTOS OPERACIONALES", total_gastos_operacionales, row, es_subtotal=True)
            row += 2

            # UTILIDAD OPERATIVA
            #utilidad_operativa = utilidad_bruta - total_gastos_operacionales
            if total_gastos_operacionales < 0:
                utilidad_operativa = utilidad_bruta - abs(total_gastos_operacionales)
            else:
                utilidad_operativa = utilidad_bruta - total_gastos_operacionales
            self.crear_fila_cuenta(parent, "UTILIDAD (PÉRDIDA) OPERATIVA", utilidad_operativa, row, es_subtotal=True)
            row += 2

            # INGRESOS Y GASTOS FINANCIEROS
            self.crear_seccion_titulo(parent, "INGRESOS Y GASTOS FINANCIEROS", row)
            row += 1

            ingresos_financieros = float(self.datos.get('INGRESOS_Ingresos_Financieros', 0))
            self.crear_fila_cuenta(parent, "Ingresos Financieros", ingresos_financieros, row, indent=True)
            row += 1

            self.crear_fila_cuenta(parent, "Gastos Financieros", gastos_financieros, row, indent=True)
            row += 1

            resultado_financiero = ingresos_financieros - abs(gastos_financieros)
            self.crear_fila_cuenta(parent, "Resultado Financiero Neto", resultado_financiero, row, es_subtotal=True)
            row += 2

            # UTILIDAD ANTES DE IMPUESTOS
            utilidad_antes_impuestos = utilidad_operativa + resultado_financiero
            self.crear_fila_cuenta(parent, "UTILIDAD (PÉRDIDA) ANTES DE IMPUESTOS", utilidad_antes_impuestos, row, es_subtotal=True)
            row += 2

            # IMPUESTOS
            impuestos_tasa = 0.30
            impuestos = utilidad_antes_impuestos * impuestos_tasa if utilidad_antes_impuestos > 0 else 0
            self.crear_fila_cuenta(parent, "(-) Impuesto sobre la Renta (30%)", impuestos, row)
            row += 1

            # UTILIDAD NETA
            utilidad_neta = utilidad_antes_impuestos - impuestos
            self.crear_fila_cuenta(parent, "UTILIDAD NETA DEL EJERCICIO", utilidad_neta, row, es_total=True)
            row += 2

            
            # MÁRGENES
            self.crear_seccion_titulo(parent, "ANÁLISIS DE MÁRGENES", row)
            row += 1
            
            margen_bruto = (utilidad_bruta / total_ingresos * 100) if total_ingresos > 0 else 0
            margen_operativo = (utilidad_operativa / total_ingresos * 100) if total_ingresos > 0 else 0
            margen_neto = (utilidad_neta / total_ingresos * 100) if total_ingresos > 0 else 0
            
            self.crear_fila_cuenta(parent, "Margen Bruto", f"{margen_bruto:.2f}%", row)
            row += 1
            self.crear_fila_cuenta(parent, "Margen Operativo", f"{margen_operativo:.2f}%", row)
            row += 1
            self.crear_fila_cuenta(parent, "Margen Neto", f"{margen_neto:.2f}%", row)
    
    def exportar_pdf(self):
        """Exporta el estado de resultados a PDF"""
        messagebox.showinfo(
            "Exportar PDF",
            "Funcionalidad de exportación a PDF en desarrollo.\n\n"
            "Próximamente podrás exportar este reporte."
        )

def generar_estado_resultados(parent, datos_financieros):
    """Función principal para generar el estado de resultados"""
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el Estado de Resultados.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    EstadoResultados(parent, datos_financieros)
