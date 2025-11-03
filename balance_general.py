import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class BalanceGeneral:
    def __init__(self, parent, datos_financieros):
        self.parent = parent
        self.datos = datos_financieros
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Balance General")
        self.ventana.geometry("1100x800")
        self.ventana.configure(bg="#1e293b")
        
        # Header
        frame_header = tk.Frame(self.ventana, bg="#0f172a", height=100)
        frame_header.pack(fill="x", pady=(0, 20))
        frame_header.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_header,
            text="📊 Balance General",
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
            text=f"Año: {self.datos.get('año', 'N/A')} | Moneda: {self.datos.get('moneda', 'N/A')}",
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
        
        # Frame para el balance (dos columnas)
        frame_balance = tk.Frame(frame_scroll, bg="#1e293b")
        frame_balance.pack(fill="both", expand=True, padx=40)
        
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
    
    def crear_fila_cuenta(self, parent, nombre, valor, row, column, es_total=False):
        """Crea una fila de cuenta"""
        frame = tk.Frame(parent, bg="#334155" if not es_total else "#1e40af")
        frame.grid(row=row, column=column, sticky="ew", pady=2, padx=5)
        
        # Configurar grid interno
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        
        # Nombre de la cuenta
        label_nombre = tk.Label(
            frame,
            text=nombre,
            font=("Segoe UI", 11, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="w",
            padx=15,
            pady=6
        )
        label_nombre.grid(row=0, column=0, sticky="w")
        
        # Valor
        valor_formateado = f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else valor
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 11, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="e",
            padx=15,
            pady=6
        )
        label_valor.grid(row=0, column=1, sticky="e")
    
    def crear_columna_activo(self, parent):
        """Crea la columna de ACTIVO"""
        row = 0
        
        # Título principal ACTIVO
        self.crear_seccion_titulo(parent, "ACTIVO", row, 0)
        row += 1
        
        # Activo Corriente o Circulante
        self.crear_seccion_titulo(parent, "Activo corriente o circulante", row, 0)
        row += 1
        
        efectivo = float(self.datos.get('efectivo_equivalentes', 0))
        cuentas_cobrar = float(self.datos.get('cuentas_cobrar', 0))
        inventarios = float(self.datos.get('inventarios', 0))
        activos_fijos = float(self.datos.get('activos_fijos', 0))
        otros_activos = float(self.datos.get('otros_activos', 0))
        
        self.crear_fila_cuenta(parent, "Efectivo y Equivalentes", efectivo, row, 0)
        row += 1
        self.crear_fila_cuenta(parent, "Cuentas por Cobrar", cuentas_cobrar, row, 0)
        row += 1
        self.crear_fila_cuenta(parent, "Inventarios", inventarios, row, 0)
        row += 1
        
        total_activo_corriente = efectivo + cuentas_cobrar + inventarios
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO CORRIENTE", total_activo_corriente, row, 0, es_total=True)
        row += 1
        
        # Activo No Corriente o Fijo
        self.crear_seccion_titulo(parent, "Activo no corriente o fijo", row, 0)
        row += 1
        
        self.crear_fila_cuenta(parent, "Activos Fijos", activos_fijos, row, 0)
        row += 1
        self.crear_fila_cuenta(parent, "Otros Activos", otros_activos, row, 0)
        row += 1
        
        total_activo_no_corriente = activos_fijos + otros_activos
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO NO CORRIENTE", total_activo_no_corriente, row, 0, es_total=True)
        row += 1
        
        # Espacio
        tk.Frame(parent, bg="#1e293b", height=10).grid(row=row, column=0)
        row += 1
        
        # TOTAL ACTIVO
        total_activo = total_activo_corriente + total_activo_no_corriente
        self.crear_fila_cuenta(parent, "TOTAL ACTIVO", total_activo, row, 0, es_total=True)
    
    def crear_columna_pasivo_patrimonio(self, parent):
        """Crea la columna de PASIVO Y PATRIMONIO"""
        row = 0
        
        # Título principal PASIVO
        self.crear_seccion_titulo(parent, "PASIVO", row, 1)
        row += 1
        
        # Pasivo Corriente o Circulante
        self.crear_seccion_titulo(parent, "Pasivo corriente o circulante", row, 1)
        row += 1
        
        cuentas_pagar = float(self.datos.get('cuentas_pagar', 0))
        prestamos = float(self.datos.get('prestamos_bancarios', 0))
        obligaciones = float(self.datos.get('obligaciones_financieras', 0))
        otros_pasivos = float(self.datos.get('otros_pasivos', 0))
        
        self.crear_fila_cuenta(parent, "Cuentas por Pagar", cuentas_pagar, row, 1)
        row += 1
        self.crear_fila_cuenta(parent, "Préstamos Bancarios", prestamos, row, 1)
        row += 1
        self.crear_fila_cuenta(parent, "Obligaciones Financieras", obligaciones, row, 1)
        row += 1
        self.crear_fila_cuenta(parent, "Otros Pasivos", otros_pasivos, row, 1)
        row += 1
        
        total_pasivo_corriente = cuentas_pagar + prestamos + obligaciones + otros_pasivos
        self.crear_fila_cuenta(parent, "TOTAL PASIVO CORRIENTE", total_pasivo_corriente, row, 1, es_total=True)
        row += 1
        
        # Pasivo No Corriente (si existe)
        # Por ahora no tenemos datos específicos, pero dejamos la estructura
        self.crear_seccion_titulo(parent, "Pasivo no corriente o fijo", row, 1)
        row += 1
        
        # Aquí podrías agregar pasivos a largo plazo si los tienes en los datos
        pasivo_no_corriente = 0
        self.crear_fila_cuenta(parent, "TOTAL PASIVO NO CORRIENTE", pasivo_no_corriente, row, 1, es_total=True)
        row += 1
        
        # PATRIMONIO O CAPITAL CONTABLE
        self.crear_seccion_titulo(parent, "PATRIMONIO O CAPITAL CONTABLE", row, 1)
        row += 1
        
        capital_social = float(self.datos.get('capital_social', 0))
        reservas = float(self.datos.get('reservas', 0))
        utilidades_retenidas = float(self.datos.get('utilidades_retenidas', 0))
        
        self.crear_fila_cuenta(parent, "Capital Social", capital_social, row, 1)
        row += 1
        self.crear_fila_cuenta(parent, "Reservas", reservas, row, 1)
        row += 1
        self.crear_fila_cuenta(parent, "Utilidades Retenidas", utilidades_retenidas, row, 1)
        row += 1
        
        total_patrimonio = capital_social + reservas + utilidades_retenidas
        self.crear_fila_cuenta(parent, "TOTAL PATRIMONIO", total_patrimonio, row, 1, es_total=True)
        row += 1
        
        # Espacio
        tk.Frame(parent, bg="#1e293b", height=10).grid(row=row, column=1)
        row += 1
        
        # TOTAL PASIVO Y PATRIMONIO
        total_pasivo_patrimonio = total_pasivo_corriente + pasivo_no_corriente + total_patrimonio
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
