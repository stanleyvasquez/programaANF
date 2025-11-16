import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

class AnalisisDuPont:
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
        self.ventana.title("Análisis DuPont - Rentabilidad")
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
            text="📈 Análisis DuPont - Rentabilidad",
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
        
        # Frame para el análisis DuPont
        frame_analisis = tk.Frame(frame_scroll, bg="#1e293b")
        frame_analisis.pack(fill="both", expand=True, padx=padding, pady=20)
        
        self.crear_analisis_dupont(frame_analisis)
        
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
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(15, 8), padx=5)
        
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
    
    def crear_fila_indicador(self, parent, nombre, valor, fila, es_total=False, es_formula=False):
        """Crea una fila con un indicador de rentabilidad"""
        if es_total:
            bg_color = "#1e40af"
            fg_color = "white"
        elif es_formula:
            bg_color = "#334155"
            fg_color = "#fbbf24"
        else:
            bg_color = "#334155"
            fg_color = "white"
        
        frame = tk.Frame(parent, bg=bg_color)
        frame.grid(row=fila, column=0, columnspan=2, sticky="ew", pady=3, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        
        label_nombre = tk.Label(
            frame,
            text=nombre,
            font=("Segoe UI", 11, "bold" if es_total else "normal"),
            bg=bg_color,
            fg=fg_color,
            anchor="w",
            padx=15,
            pady=8,
            wraplength=400
        )
        label_nombre.grid(row=0, column=0, sticky="w")
        
        # Formatear valor
        if isinstance(valor, str):
            valor_formateado = valor
        elif isinstance(valor, float) or isinstance(valor, int):
            if "%" in nombre or "porcentaje" in nombre.lower() or "margen" in nombre.lower():
                valor_formateado = f"{valor:.2f}%"
            else:
                valor_formateado = f"{valor:.4f} veces"
        else:
            valor_formateado = str(valor)
        
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 11, "bold" if es_total else "normal"),
            bg=bg_color,
            fg=fg_color,
            anchor="e",
            padx=15,
            pady=8
        )
        label_valor.grid(row=0, column=1, sticky="e")
    
    def crear_formula_visual(self, parent, formula_texto, row):
        """Crea una representación visual de la fórmula"""
        frame = tk.Frame(parent, bg="#1e293b", relief="solid", borderwidth=1)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        
        label = tk.Label(
            frame,
            text=formula_texto,
            font=("Segoe UI", 8, "italic"),
            bg="#1e293b",
            fg="#94a3b8",
            anchor="w",
            padx=12,
            pady=8,
            wraplength=400,
            justify="left"
        )
        label.pack(fill="x")
    
    def crear_analisis_dupont(self, parent):
        """Crea el análisis DuPont completo"""
        
        # Datos del Estado de Resultados
        ventas = float(self.datos.get('INGRESOS_Ventas', 0))
        ingresos_servicios = float(self.datos.get('INGRESOS_Ingresos_por_Servicios', 0))
        otros_ingresos = float(self.datos.get('INGRESOS_Otros_Ingresos', 0))
        ingresos_financieros = float(self.datos.get('INGRESOS_Ingresos_Financieros', 0))
        
        costo_ventas = float(self.datos.get('GASTOS_Costo_de_Ventas', 0))
        gastos_admin = float(self.datos.get('GASTOS_Gastos_Administrativos', 0))
        gastos_ventas = float(self.datos.get('GASTOS_Gastos_de_Ventas', 0))
        gastos_financieros = float(self.datos.get('GASTOS_Gastos_Financieros', 0))
        otros_gastos = float(self.datos.get('GASTOS_Otros_Gastos', 0))
        impuestos = float(self.datos.get('GASTOS_Impuesto_sobre_la_Renta', 0))
        
        # Datos del Balance General
        efectivo = float(self.datos.get('ACTIVOS_Efectivo', 0))
        cuentas_cobrar = float(self.datos.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0))
        prestamos_cobrar = float(self.datos.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0))
        inventarios = float(self.datos.get('ACTIVOS_Inventarios', 0))
        gastos_anticipados = float(self.datos.get('ACTIVOS_Gastos_pagados_por_anticipado', 0))
        
        propiedades = float(self.datos.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0))
        intangibles = float(self.datos.get('ACTIVOS_Activos_intangibles', 0))
        impuesto_diferido = float(self.datos.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0))
        otros_activos = float(self.datos.get('ACTIVOS_Otros_activos', 0))
        
        capital_social = float(self.datos.get('PATRIMONIO_Capital_social', 0))
        capital_minimo = float(self.datos.get('PATRIMONIO_Capital_social_minimo', 0))
        reserva_legal = float(self.datos.get('PATRIMONIO_Reserva_legal', 0))
        deficit = float(self.datos.get('PATRIMONIO_Deficit_acumulado', 0))
        
        # Cálculos de totales
        total_ingresos = ventas + ingresos_servicios + otros_ingresos
        total_gastos_operacionales = abs(costo_ventas) + abs(gastos_admin) + abs(gastos_ventas) + abs(otros_gastos)
        utilidad_operativa = total_ingresos - total_gastos_operacionales
        resultado_financiero = ingresos_financieros - abs(gastos_financieros)
        utilidad_antes_impuestos = utilidad_operativa + resultado_financiero
        utilidad_neta = utilidad_antes_impuestos - abs(impuestos)
        
        total_activo_corriente = efectivo + cuentas_cobrar + prestamos_cobrar + inventarios + gastos_anticipados
        total_activo_no_corriente = propiedades + intangibles + impuesto_diferido + otros_activos
        activos_totales = total_activo_corriente + total_activo_no_corriente
        
        patrimonio = capital_social + reserva_legal - deficit
        
        # Validaciones para evitar divisiones por cero
        if ventas == 0:
            ventas = 1
        if activos_totales == 0:
            activos_totales = 1
        if patrimonio == 0:
            patrimonio = 1
        
        margen_utilidad_neta = (utilidad_neta / ventas) * 100 if ventas != 0 else 0
        rotacion_activos = ventas / activos_totales if activos_totales != 0 else 0
        rsa = (margen_utilidad_neta / 100) * rotacion_activos
        multiplicador_capital = activos_totales / patrimonio if patrimonio != 0 else 0
        rsp = rsa * multiplicador_capital  # ROE
        
        row = 0
        
        # Título principal
        self.crear_seccion_titulo(parent, "ANÁLISIS DE RENTABILIDAD - SISTEMA DUPONT", row)
        row += 2
        
        # Datos base
        self.crear_seccion_titulo(parent, "DATOS BASE", row)
        row += 1
        
        self.crear_fila_indicador(parent, "Ventas Netas", f"$ {ventas:,.2f}", row)
        row += 1
        self.crear_fila_indicador(parent, "Utilidad Neta", f"$ {utilidad_neta:,.2f}", row)
        row += 1
        self.crear_fila_indicador(parent, "Activos Totales", f"$ {activos_totales:,.2f}", row)
        row += 1
        self.crear_fila_indicador(parent, "Patrimonio (Capital Contable)", f"$ {patrimonio:,.2f}", row)
        row += 2
        
        # Componentes del DuPont
        self.crear_seccion_titulo(parent, "COMPONENTES DEL ANÁLISIS DUPONT", row)
        row += 1
        
        # 1. Margen de Utilidad Neta
        self.crear_fila_indicador(parent, "1️⃣ Margen de Utilidad Neta", margen_utilidad_neta, row, es_formula=True)
        row += 1
        self.crear_formula_visual(parent, "Margen Neto = (Utilidad Neta / Ventas) × 100", row)
        row += 1
        self.crear_fila_indicador(parent, f"   → {margen_utilidad_neta:.2f}% por cada $ de ventas", "N/A", row)
        row += 2
        
        # 2. Rotación de Activos
        self.crear_fila_indicador(parent, "2️⃣ Rotación de Activos", rotacion_activos, row, es_formula=True)
        row += 1
        self.crear_formula_visual(parent, "Rotación = Ventas / Activos Totales", row)
        row += 1
        self.crear_fila_indicador(parent, f"   → Genera ${rotacion_activos:.2f} en ventas por $ de activos", "N/A", row)
        row += 2
        
        # 3. Rendimiento sobre Activos (RSA)
        self.crear_fila_indicador(parent, "3️⃣ Rendimiento sobre Activos (RSA)", rsa * 100, row, es_total=True)
        row += 1
        self.crear_formula_visual(parent, "RSA = Margen Neto × Rotación de Activos", row)
        row += 1
        self.crear_fila_indicador(parent, f"   → {rsa*100:.2f}% de retorno sobre el total de activos", "N/A", row)
        row += 2
        
        # 4. Multiplicador del Capital
        self.crear_fila_indicador(parent, "4️⃣ Multiplicador del Capital", multiplicador_capital, row, es_formula=True)
        row += 1
        self.crear_formula_visual(parent, "Multiplicador = Activos Totales / Patrimonio (Apalancamiento)", row)
        row += 1
        self.crear_fila_indicador(parent, f"   → Por cada $ de patrimonio, hay ${multiplicador_capital:.2f} en activos", "N/A", row)
        row += 2
        
        # 5. Rendimiento sobre Patrimonio (RSP o ROE)
        self.crear_fila_indicador(parent, "5️⃣ Rendimiento sobre Patrimonio (ROE)", rsp * 100, row, es_total=True)
        row += 1
        self.crear_formula_visual(parent, "ROE = RSA × Multiplicador del Capital", row)
        row += 1
        self.crear_fila_indicador(parent, f"   → {rsp*100:.2f}% de retorno para los accionistas", "N/A", row)
    
    def exportar_pdf(self):
        nombre_empresa = self.datos.get("nombre_empresa", "N/A")
        anio = self.datos.get("anio", "N/A")
        moneda = self.datos.get("tipo_moneda", "N/A")

        archivo_pdf = f"Analisis_DuPont_{nombre_empresa}_{anio}.pdf"

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
            spaceAfter=8,
            spaceBefore=10,
            textColor=colors.black,
            alignment=0,
        )

        estilo_formula = ParagraphStyle(
            name='Formula',
            parent=estilos['Normal'],
            fontSize=9,
            textColor=colors.grey,
            leading=10,
            spaceAfter=4,
        )

        contenido = []

        # ------------ TITULO CENTRADO ------------
        contenido.append(Paragraph("Análisis de Rentabilidad – Sistema DuPont", estilo_titulo))
        contenido.append(Paragraph(f"<b>{nombre_empresa}</b>", estilo_subtitulo))
        contenido.append(Paragraph(f"Año: {anio} &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Moneda: {moneda}", estilo_subtitulo))
        contenido.append(Spacer(1, 15))

        # ------------ FUNCIONES AUXILIARES ------------
        def agregar_seccion(titulo):
            contenido.append(Paragraph(f"<b>{titulo}</b>", estilo_seccion))
            contenido.append(Spacer(1, 6))

        def agregar_tabla(data):
            tabla = Table(data, colWidths=[240, 120])

            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                ('ALIGN', (0,0), (0,-1), 'LEFT'),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('FONTSIZE', (0,0), (-1,-1), 9)
            ]))

            contenido.append(tabla)
            contenido.append(Spacer(1, 12))

        def agregar_formula(texto):
            contenido.append(Paragraph(texto, estilo_formula))
            contenido.append(Spacer(1, 4))

        # ------------ OBTENER DATOS (igual que en tu clase) ------------
        ventas = float(self.datos.get('INGRESOS_Ventas', 0))
        ingresos_servicios = float(self.datos.get('INGRESOS_Ingresos_por_Servicios', 0))
        otros_ingresos = float(self.datos.get('INGRESOS_Otros_Ingresos', 0))
        ingresos_financieros = float(self.datos.get('INGRESOS_Ingresos_Financieros', 0))

        costo_ventas = float(self.datos.get('GASTOS_Costo_de_Ventas', 0))
        gastos_admin = float(self.datos.get('GASTOS_Gastos_Administrativos', 0))
        gastos_ventas = float(self.datos.get('GASTOS_Gastos_de_Ventas', 0))
        gastos_financieros = float(self.datos.get('GASTOS_Gastos_Financieros', 0))
        otros_gastos = float(self.datos.get('GASTOS_Otros_Gastos', 0))
        impuestos = float(self.datos.get('GASTOS_Impuesto_sobre_la_Renta', 0))

        # Balance
        efectivo = float(self.datos.get('ACTIVOS_Efectivo', 0))
        cuentas_cobrar = float(self.datos.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0))
        prestamos_cobrar = float(self.datos.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0))
        inventarios = float(self.datos.get('ACTIVOS_Inventarios', 0))
        gastos_anticipados = float(self.datos.get('ACTIVOS_Gastos_pagados_por_anticipado', 0))

        propiedades = float(self.datos.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0))
        intangibles = float(self.datos.get('ACTIVOS_Activos_intangibles', 0))
        impuesto_diferido = float(self.datos.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0))
        otros_activos = float(self.datos.get('ACTIVOS_Otros_activos', 0))

        capital_social = float(self.datos.get('PATRIMONIO_Capital_social', 0))
        reserva_legal = float(self.datos.get('PATRIMONIO_Reserva_legal', 0))
        deficit = float(self.datos.get('PATRIMONIO_Deficit_acumulado', 0))

        total_ingresos = ventas + ingresos_servicios + otros_ingresos
        total_gastos_oper = abs(costo_ventas) + abs(gastos_admin) + abs(gastos_ventas) + abs(otros_gastos)
        utilidad_operativa = total_ingresos - total_gastos_oper
        resultado_financiero = ingresos_financieros - abs(gastos_financieros)
        utilidad_antes_impuestos = utilidad_operativa + resultado_financiero
        utilidad_neta = utilidad_antes_impuestos - abs(impuestos)

        total_activo_corriente = efectivo + cuentas_cobrar + prestamos_cobrar + inventarios + gastos_anticipados
        total_activo_no_corriente = propiedades + intangibles + impuesto_diferido + otros_activos
        activos_totales = total_activo_corriente + total_activo_no_corriente

        patrimonio = capital_social + reserva_legal - deficit

        if ventas == 0: ventas = 1
        if activos_totales == 0: activos_totales = 1
        if patrimonio == 0: patrimonio = 1

        margen_neto = (utilidad_neta / ventas) * 100
        rotacion_activos = ventas / activos_totales
        rsa = (margen_neto / 100) * rotacion_activos
        multiplicador_capital = activos_totales / patrimonio
        roe = rsa * multiplicador_capital

        # ------------ SECCIÓN: DATOS BASE ------------
        agregar_seccion("DATOS BASE")

        tabla_datos = [
            ["Ventas Netas", f"$ {ventas:,.2f}"],
            ["Utilidad Neta", f"$ {utilidad_neta:,.2f}"],
            ["Activos Totales", f"$ {activos_totales:,.2f}"],
            ["Patrimonio (Capital Contable)", f"$ {patrimonio:,.2f}"]
        ]
        agregar_tabla(tabla_datos)

        # ------------ COMPONENTES DUPONT ------------
        agregar_seccion("COMPONENTES DEL SISTEMA DUPONT")

        tabla_componentes = [
            ["Margen de Utilidad Neta", f"{margen_neto:.2f}%"],
            ["Rotación de Activos", f"{rotacion_activos:.4f} veces"],
            ["Multiplicador del Capital", f"{multiplicador_capital:.4f} veces"],
            ["Rendimiento sobre Activos (RSA)", f"{rsa*100:.2f}%"],
            ["Rendimiento sobre Patrimonio (ROE)", f"{roe*100:.2f}%"],
        ]
        agregar_tabla(tabla_componentes)

        # ------------ FORMULAS ------------
        agregar_seccion("FÓRMULAS UTILIZADAS")

        agregar_formula("Margen Neto = (Utilidad Neta / Ventas) × 100")
        agregar_formula("Rotación de Activos = Ventas / Activos Totales")
        agregar_formula("RSA = Margen Neto × Rotación de Activos")
        agregar_formula("Multiplicador = Activos Totales / Patrimonio")
        agregar_formula("ROE = RSA × Multiplicador del Capital")

        # ------------ GENERAR PDF ------------
        doc.build(contenido)

        messagebox.showinfo(
            "PDF generado",
            f"El archivo PDF fue creado exitosamente:\n\n{archivo_pdf}"
        )

def generar_analisis_dupont(parent, datos_financieros, app_instance=None):
    """Función principal para generar el análisis DuPont"""
    if app_instance:
        app_instance.cargar_desde_archivo()
        if app_instance.registros_financieros:
            datos_financieros = app_instance.registros_financieros[-1]
    
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el Análisis DuPont.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    AnalisisDuPont(parent, datos_financieros)
