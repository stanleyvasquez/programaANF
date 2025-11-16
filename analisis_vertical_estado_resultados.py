import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

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
        
        custom_accounts = self.datos.get("_cuentas_personalizadas", {})
        custom_ingresos_operacionales = [k for k, v in custom_accounts.items() if v.get("tipo") == "INGRESOS" and v.get("subrubro") == "Ingresos Operacionales"]
        custom_ingresos_financieros = [k for k, v in custom_accounts.items() if v.get("tipo") == "INGRESOS" and v.get("subrubro") == "Ingresos Financieros"]
        custom_gastos_operacionales = [k for k, v in custom_accounts.items() if v.get("tipo") == "GASTOS" and v.get("subrubro") == "Gastos Operacionales"]
        custom_gastos_financieros = [k for k, v in custom_accounts.items() if v.get("tipo") == "GASTOS" and v.get("subrubro") == "Gastos Financieros"]
        
        for clave in custom_ingresos_operacionales:
            ventas += float(self.datos.get(clave, 0))
        for clave in custom_ingresos_financieros:
            ingresos_financieros += float(self.datos.get(clave, 0))
        for clave in custom_gastos_operacionales:
            gastos_admin += float(self.datos.get(clave, 0))
        for clave in custom_gastos_financieros:
            gastos_financieros += float(self.datos.get(clave, 0))
        
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
        
        total_gastos_operacionales = (gastos_admin) + (gastos_ventas) + (otros_gastos)
        self.crear_fila_vertical(parent, "TOTAL GASTOS OPERACIONALES", total_gastos_operacionales, (total_gastos_operacionales/total_ingresos)*100, row, es_total=True)
        row += 2
        
        utilidad_operativa = utilidad_bruta - abs(total_gastos_operacionales)
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
        
        impuestos = float(self.datos.get('GASTOS_Impuesto_sobre_la_Renta', 0))
        self.crear_fila_vertical(parent, "(-) Impuesto sobre la Renta (30%)", impuestos, (impuestos/total_ingresos)*100, row)
        row += 1
        
        utilidad_neta = utilidad_antes_impuestos - abs(impuestos)
        self.crear_fila_vertical(parent, "UTILIDAD NETA DEL EJERCICIO", utilidad_neta, (utilidad_neta/total_ingresos)*100, row, es_total=True)
    
    def exportar_pdf(self):
        nombre_empresa = self.datos.get("nombre_empresa", "N/A")
        anio = self.datos.get("anio", "N/A")
        moneda = self.datos.get("tipo_moneda", "N/A")

        archivo_pdf = f"Analisis_Vertical_Estado_Resultados_{nombre_empresa}_{anio}.pdf"

        doc = SimpleDocTemplate(
            archivo_pdf,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            name='Titulo',
            parent=estilos['Heading1'],
            alignment=1,
            fontSize=18,
            leading=22,
            spaceAfter=10
        )

        estilo_subtitulo = ParagraphStyle(
            name='Subtitulo',
            parent=estilos['Normal'],
            alignment=1,
            fontSize=11,
            leading=14,
            spaceAfter=6
        )

        estilo_seccion = ParagraphStyle(
            name='Seccion',
            parent=estilos['Heading2'],
            fontSize=12,
            leading=14,
            spaceAfter=6,
            spaceBefore=12,
            textColor=colors.black,
            alignment=0,
        )

        contenido = []

        # ---------------- CABECERA ----------------
        contenido.append(Paragraph("Análisis Vertical - Estado de Resultados", estilo_titulo))
        contenido.append(Paragraph(f"<b>{nombre_empresa}</b>", estilo_subtitulo))
        contenido.append(Paragraph(f"Año: {anio} &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Moneda: {moneda}", estilo_subtitulo))
        contenido.append(Spacer(1, 12))

        # ---------------- FUNCIONES AUXILIARES ----------------
        def agregar_seccion(titulo):
            contenido.append(Spacer(1, 8))
            contenido.append(Paragraph(f"<b>{titulo}</b>", estilo_seccion))
            contenido.append(Spacer(1, 4))

        def agregar_tabla(lista_tuplas):
            tabla_data = [["Cuenta", "Valor", "%"]]
            tabla_data += lista_tuplas

            tabla = Table(tabla_data, colWidths=[230, 100, 60])

            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                ('ALIGN', (0,0), (0,-1), 'LEFT'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))

            contenido.append(tabla)
            contenido.append(Spacer(1, 12))

        # =====================================================
        # ===============  CALCULOS IDENTICOS A LA VENTANA  ===
        # =====================================================

        ventas = float(self.datos.get('INGRESOS_Ventas', 0))
        ingresos_servicios = float(self.datos.get('INGRESOS_Ingresos_por_Servicios', 0))
        otros_ingresos = float(self.datos.get('INGRESOS_Otros_Ingresos', 0))
        costo_ventas = float(self.datos.get('GASTOS_Costo_de_Ventas', 0))
        gastos_admin = float(self.datos.get('GASTOS_Gastos_Administrativos', 0))
        gastos_ventas = float(self.datos.get('GASTOS_Gastos_de_Ventas', 0))
        gastos_financieros = float(self.datos.get('GASTOS_Gastos_Financieros', 0))
        otros_gastos = float(self.datos.get('GASTOS_Otros_Gastos', 0))
        ingresos_financieros = float(self.datos.get('INGRESOS_Ingresos_Financieros', 0))

        custom_accounts = self.datos.get("_cuentas_personalizadas", {})
        custom_ingresos_operacionales = [k for k, v in custom_accounts.items() if v.get("tipo") == "INGRESOS" and v.get("subrubro") == "Ingresos Operacionales"]
        custom_ingresos_financieros = [k for k, v in custom_accounts.items() if v.get("tipo") == "INGRESOS" and v.get("subrubro") == "Ingresos Financieros"]
        custom_gastos_operacionales = [k for k, v in custom_accounts.items() if v.get("tipo") == "GASTOS" and v.get("subrubro") == "Gastos Operacionales"]
        custom_gastos_financieros = [k for k, v in custom_accounts.items() if v.get("tipo") == "GASTOS" and v.get("subrubro") == "Gastos Financieros"]

        for clave in custom_ingresos_operacionales:
            ventas += float(self.datos.get(clave, 0))
        for clave in custom_ingresos_financieros:
            ingresos_financieros += float(self.datos.get(clave, 0))
        for clave in custom_gastos_operacionales:
            gastos_admin += float(self.datos.get(clave, 0))
        for clave in custom_gastos_financieros:
            gastos_financieros += float(self.datos.get(clave, 0))

        total_ingresos = ventas + ingresos_servicios + otros_ingresos
        if total_ingresos == 0:
            total_ingresos = 1

        utilidad_bruta = total_ingresos - abs(costo_ventas)
        total_gastos_operacionales = (gastos_admin + gastos_ventas + otros_gastos)
        utilidad_operativa = utilidad_bruta - abs(total_gastos_operacionales)
        resultado_financiero = ingresos_financieros - abs(gastos_financieros)
        utilidad_antes_impuestos = utilidad_operativa + resultado_financiero
        impuestos = float(self.datos.get('GASTOS_Impuesto_sobre_la_Renta', 0))
        utilidad_neta = utilidad_antes_impuestos - abs(impuestos)

        # =====================================================
        # ===============  TABLAS IDENTICAS AL GUI  ===========
        # =====================================================

        agregar_seccion("INGRESOS OPERACIONALES")
        agregar_tabla([
            ("Ventas", f"$ {ventas:,.2f}", f"{(ventas/total_ingresos)*100:.2f}%"),
            ("Ingresos por Servicios", f"$ {ingresos_servicios:,.2f}", f"{(ingresos_servicios/total_ingresos)*100:.2f}%"),
            ("Otros Ingresos", f"$ {otros_ingresos:,.2f}", f"{(otros_ingresos/total_ingresos)*100:.2f}%"),
            ("TOTAL INGRESOS", f"$ {total_ingresos:,.2f}", "100%"),
        ])

        agregar_seccion("COSTO DE VENTAS / UTILIDAD BRUTA")
        agregar_tabla([
            ("Costo de Ventas", f"$ {abs(costo_ventas):,.2f}", f"{(abs(costo_ventas)/total_ingresos)*100:.2f}%"),
            ("UTILIDAD BRUTA", f"$ {utilidad_bruta:,.2f}", f"{(utilidad_bruta/total_ingresos)*100:.2f}%"),
        ])

        agregar_seccion("GASTOS OPERACIONALES")
        agregar_tabla([
            ("Gastos Administrativos", f"$ {abs(gastos_admin):,.2f}", f"{(abs(gastos_admin)/total_ingresos)*100:.2f}%"),
            ("Gastos de Ventas", f"$ {abs(gastos_ventas):,.2f}", f"{(abs(gastos_ventas)/total_ingresos)*100:.2f}%"),
            ("Otros Gastos", f"$ {abs(otros_gastos):,.2f}", f"{(abs(otros_gastos)/total_ingresos)*100:.2f}%"),
            ("TOTAL GASTOS OPERACIONALES", f"$ {total_gastos_operacionales:,.2f}", f"{(total_gastos_operacionales/total_ingresos)*100:.2f}%"),
            ("UTILIDAD OPERATIVA", f"$ {utilidad_operativa:,.2f}", f"{(utilidad_operativa/total_ingresos)*100:.2f}%"),
        ])

        agregar_seccion("INGRESOS Y GASTOS FINANCIEROS")
        agregar_tabla([
            ("Ingresos Financieros", f"$ {ingresos_financieros:,.2f}", f"{(ingresos_financieros/total_ingresos)*100:.2f}%"),
            ("Gastos Financieros", f"$ {abs(gastos_financieros):,.2f}", f"{(abs(gastos_financieros)/total_ingresos)*100:.2f}%"),
            ("Resultado Financiero Neto", f"$ {resultado_financiero:,.2f}", f"{(resultado_financiero/total_ingresos)*100:.2f}%"),
            ("UTILIDAD ANTES DE IMPUESTOS", f"$ {utilidad_antes_impuestos:,.2f}", f"{(utilidad_antes_impuestos/total_ingresos)*100:.2f}%"),
        ])

        agregar_seccion("IMPUESTOS Y UTILIDAD NETA")
        agregar_tabla([
            ("Impuesto sobre la Renta (30%)", f"$ {impuestos:,.2f}", f"{(impuestos/total_ingresos)*100:.2f}%"),
            ("UTILIDAD NETA DEL EJERCICIO", f"$ {utilidad_neta:,.2f}", f"{(utilidad_neta/total_ingresos)*100:.2f}%"),
        ])

        # ---------------- CREAR PDF ----------------
        doc.build(contenido)

        messagebox.showinfo(
            "PDF generado",
            f"El archivo PDF fue creado exitosamente:\n\n{archivo_pdf}"
        )

def generar_analisis_vertical_estado_resultados(parent, datos_financieros, app_instance=None):
    if app_instance:
        app_instance.cargar_desde_archivo()
        if app_instance.registros_financieros:
            datos_financieros = app_instance.registros_financieros[-1]
    
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el Análisis Vertical.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    AnalisisVerticalEstadoResultados(parent, datos_financieros)
