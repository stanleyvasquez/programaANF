import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
class AnalisisVerticalBalance:
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
        self.ventana.title("Análisis Vertical - Balance General")
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
            text="📊 Análisis Vertical - Balance General",
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
        
        padding = int(window_width * 0.04) if window_width > 1000 else 15
        
        # Frame para el análisis (dos columnas)
        frame_analisis = tk.Frame(frame_scroll, bg="#1e293b")
        frame_analisis.pack(fill="both", expand=True, padx=padding)
        
        # Configurar grid para dos columnas iguales
        frame_analisis.columnconfigure(0, weight=1, uniform="col")
        frame_analisis.columnconfigure(1, weight=1, uniform="col")
        
        # COLUMNA IZQUIERDA - ANÁLISIS VERTICAL ACTIVO
        self.crear_analisis_activo(frame_analisis)
        
        # COLUMNA DERECHA - ANÁLISIS VERTICAL PASIVO Y PATRIMONIO
        self.crear_analisis_pasivo_patrimonio(frame_analisis)
        
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
    
    def crear_fila_vertical(self, parent, nombre, valor, porcentaje, row, column, es_total=False, indent=False):
        """Crea una fila con valor y porcentaje para análisis vertical"""
        frame = tk.Frame(parent, bg="#334155" if not es_total else "#1e40af")
        frame.grid(row=row, column=column, sticky="ew", pady=2, padx=5)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=0)
        
        # Nombre de la cuenta
        padding_left = 30 if indent else 15
        label_nombre = tk.Label(
            frame,
            text=nombre,
            font=("Segoe UI", 9, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="w",
            padx=padding_left,
            pady=6,
            wraplength=200
        )
        label_nombre.grid(row=0, column=0, sticky="w")
        
        # Valor
        valor_formateado = f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else valor
        label_valor = tk.Label(
            frame,
            text=valor_formateado,
            font=("Segoe UI", 9, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="white",
            anchor="e",
            padx=8,
            pady=6
        )
        label_valor.grid(row=0, column=1, sticky="e")
        
        # Porcentaje
        porcentaje_formateado = f"{porcentaje:.2f}%" if isinstance(porcentaje, (int, float)) else porcentaje
        label_porcentaje = tk.Label(
            frame,
            text=porcentaje_formateado,
            font=("Segoe UI", 9, "bold" if es_total else "normal"),
            bg="#334155" if not es_total else "#1e40af",
            fg="#fbbf24" if porcentaje > 0 else "white",
            anchor="e",
            padx=15,
            pady=6
        )
        label_porcentaje.grid(row=0, column=2, sticky="e")
    
    def crear_analisis_activo(self, parent):
        """Crea el análisis vertical del ACTIVO"""
        row = 0
        
        self.crear_seccion_titulo(parent, "ANÁLISIS VERTICAL - ACTIVO", row, 0)
        row += 1
        
        # ACTIVO CORRIENTE
        self.crear_seccion_titulo(parent, "ACTIVO CORRIENTE", row, 0)
        row += 1
        
        efectivo = float(self.datos.get('ACTIVOS_Efectivo', 0))
        cuentas_cobrar_com = float(self.datos.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0))
        prestamos_cobrar = float(self.datos.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0))
        inventarios = float(self.datos.get('ACTIVOS_Inventarios', 0))
        gastos_anticipados = float(self.datos.get('ACTIVOS_Gastos_pagados_por_anticipado', 0))
        
        total_corriente = efectivo + cuentas_cobrar_com + prestamos_cobrar + inventarios + gastos_anticipados
        
        # ACTIVO NO CORRIENTE
        propiedades = float(self.datos.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0))
        intangibles = float(self.datos.get('ACTIVOS_Activos_intangibles', 0))
        impuesto_diferido = float(self.datos.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0))
        otros_activos = float(self.datos.get('ACTIVOS_Otros_activos', 0))
        
        total_no_corriente = propiedades + intangibles + impuesto_diferido + otros_activos
        total_activo = total_corriente + total_no_corriente
        
        # Evitar división por cero
        if total_activo == 0:
            total_activo = 1
        
        # Mostrar cuentas de activo corriente
        self.crear_fila_vertical(parent, "Efectivo", efectivo, (efectivo/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Cuentas por cobrar", cuentas_cobrar_com, (cuentas_cobrar_com/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Préstamos por cobrar", prestamos_cobrar, (prestamos_cobrar/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Inventarios", inventarios, (inventarios/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Gastos anticipados", gastos_anticipados, (gastos_anticipados/total_activo)*100, row, 0, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL ACTIVO CORRIENTE", total_corriente, (total_corriente/total_activo)*100, row, 0, es_total=True)
        row += 2
        
        # ACTIVO NO CORRIENTE
        self.crear_seccion_titulo(parent, "ACTIVO NO CORRIENTE", row, 0)
        row += 1
        
        self.crear_fila_vertical(parent, "Propiedades, plantas y equipos", propiedades, (propiedades/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Activos intangibles", intangibles, (intangibles/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Impuesto diferido", impuesto_diferido, (impuesto_diferido/total_activo)*100, row, 0, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Otros activos", otros_activos, (otros_activos/total_activo)*100, row, 0, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL ACTIVO NO CORRIENTE", total_no_corriente, (total_no_corriente/total_activo)*100, row, 0, es_total=True)
        row += 2
        
        self.crear_fila_vertical(parent, "TOTAL ACTIVO", total_activo, 100.0, row, 0, es_total=True)
    
    def crear_analisis_pasivo_patrimonio(self, parent):
        """Crea el análisis vertical de PASIVO Y PATRIMONIO"""
        row = 0
        
        self.crear_seccion_titulo(parent, "ANÁLISIS VERTICAL - PASIVO Y PATRIMONIO", row, 1)
        row += 1
        
        # Calcular totales para obtener el denominador
        prest_corto = float(self.datos.get('PASIVOS_Prestamos_por_pagar_a_corto_plazo', 0))
        prest_partes_corto = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_corto_plazo', 0))
        prest_partes_porcion = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_porcion_corriente', 0))
        cuentas_pagar = float(self.datos.get('PASIVOS_Cuentas_por_pagar_comerciales', 0))
        ingresos_diferidos = float(self.datos.get('PASIVOS_Ingresos_diferidos', 0))
        otras_cuentas = float(self.datos.get('PASIVOS_Otras_cuentas_por_pagar', 0))
        dividendos = float(self.datos.get('PASIVOS_Dividendos_por_pagar', 0))
        
        total_pasivo_corriente = prest_corto + prest_partes_corto + prest_partes_porcion + cuentas_pagar + ingresos_diferidos + otras_cuentas + dividendos
        
        prest_largo = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_largo_plazo', 0))
        total_pasivo = total_pasivo_corriente + prest_largo
        
        capital_social = float(self.datos.get('PATRIMONIO_Capital_social', 0))
        capital_minimo = float(self.datos.get('PATRIMONIO_Capital_social_minimo', 0))
        reserva_legal = float(self.datos.get('PATRIMONIO_Reserva_legal', 0))
        deficit = float(self.datos.get('PATRIMONIO_Deficit_acumulado', 0))
        
        total_patrimonio = capital_social + reserva_legal - deficit
        total_pasivo_patrimonio = total_pasivo + total_patrimonio
        
        # Evitar división por cero
        if total_pasivo_patrimonio == 0:
            total_pasivo_patrimonio = 1
        
        # PASIVO CORRIENTE
        self.crear_seccion_titulo(parent, "PASIVO CORRIENTE", row, 1)
        row += 1
        
        self.crear_fila_vertical(parent, "Préstamos corto plazo", prest_corto, (prest_corto/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Préstamos partes corto plazo", prest_partes_corto, (prest_partes_corto/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Préstamos porción corriente", prest_partes_porcion, (prest_partes_porcion/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Cuentas por pagar", cuentas_pagar, (cuentas_pagar/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Ingresos diferidos", ingresos_diferidos, (ingresos_diferidos/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Otras cuentas por pagar", otras_cuentas, (otras_cuentas/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Dividendos por pagar", dividendos, (dividendos/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL PASIVO CORRIENTE", total_pasivo_corriente, (total_pasivo_corriente/total_pasivo_patrimonio)*100, row, 1, es_total=True)
        row += 2
        
        # PASIVO NO CORRIENTE
        self.crear_seccion_titulo(parent, "PASIVO NO CORRIENTE", row, 1)
        row += 1
        
        self.crear_fila_vertical(parent, "Préstamos largo plazo", prest_largo, (prest_largo/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL PASIVO NO CORRIENTE", prest_largo, (prest_largo/total_pasivo_patrimonio)*100, row, 1, es_total=True)
        row += 2
        
        self.crear_fila_vertical(parent, "TOTAL PASIVO", total_pasivo, (total_pasivo/total_pasivo_patrimonio)*100, row, 1, es_total=True)
        row += 2
        
        # PATRIMONIO
        self.crear_seccion_titulo(parent, "PATRIMONIO", row, 1)
        row += 1
        
        self.crear_fila_vertical(parent, "Capital social", capital_social, (capital_social/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Capital social mínimo", capital_minimo, (capital_minimo/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        self.crear_fila_vertical(parent, "Reserva legal", reserva_legal, (reserva_legal/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        
        deficit_display = -deficit if deficit > 0 else deficit
        self.crear_fila_vertical(parent, "Déficit acumulado", deficit_display, (deficit_display/total_pasivo_patrimonio)*100, row, 1, indent=True)
        row += 1
        
        self.crear_fila_vertical(parent, "TOTAL PATRIMONIO", total_patrimonio, (total_patrimonio/total_pasivo_patrimonio)*100, row, 1, es_total=True)
        row += 2
        
        self.crear_fila_vertical(parent, "TOTAL PASIVO Y PATRIMONIO", total_pasivo_patrimonio, 100.0, row, 1, es_total=True)
    
    def exportar_pdf(self):
        
        nombre_empresa = self.datos.get("nombre_empresa", "N/A")
        anio = self.datos.get("anio", "N/A")
        moneda = self.datos.get("tipo_moneda", "N/A")

        archivo_pdf = f"Analisis_Vertical_Balance_{nombre_empresa}_{anio}.pdf"

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

        estilo_tabla = ParagraphStyle(
            name='TablaTexto',
            parent=estilos['Normal'],
            fontSize=9,
            leading=12
        )

        contenido = []

        # TÍTULO CENTRAL
        contenido.append(Paragraph("Análisis Vertical - Balance General", estilo_titulo))

        # Empresa y año centrados
        contenido.append(Paragraph(f"<b>{nombre_empresa}</b>", estilo_subtitulo))
        contenido.append(Paragraph(f"Año: {anio} &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Moneda: {moneda}", estilo_subtitulo))
        contenido.append(Spacer(1, 12))

        # ------------ TABLAS / DATOS --------------

        def agregar_seccion(titulo):
            contenido.append(Spacer(1, 8))
            contenido.append(Paragraph(f"<b>{titulo}</b>", estilo_seccion))
            contenido.append(Spacer(1, 4))

        def agregar_tabla(lista_tuplas):
            tabla_data = [["Cuenta", "Valor", "%"]]
            tabla_data += lista_tuplas

            tabla = Table(tabla_data, colWidths=[220, 100, 60])

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

        # ------------------ ACTIVOS ----------------------

        # Extraer datos (usamos los mismos nombres que tu clase)
        eff = float(self.datos.get('ACTIVOS_Efectivo', 0))
        cc = float(self.datos.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0))
        pr = float(self.datos.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0))
        inv = float(self.datos.get('ACTIVOS_Inventarios', 0))
        ga = float(self.datos.get('ACTIVOS_Gastos_pagados_por_anticipado', 0))

        propiedades = float(self.datos.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0))
        intang = float(self.datos.get('ACTIVOS_Activos_intangibles', 0))
        imp_diff = float(self.datos.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0))
        otros_act = float(self.datos.get('ACTIVOS_Otros_activos', 0))

        total_corriente = eff + cc + pr + inv + ga
        total_no_corr = propiedades + intang + imp_diff + otros_act
        total_activo = total_corriente + total_no_corr if (total_corriente + total_no_corr) != 0 else 1

        # ------- ACTIVO CORRIENTE ---------
        agregar_seccion("ACTIVO CORRIENTE")

        tabla_activo_corriente = [
            ("Efectivo", f"$ {eff:,.2f}", f"{(eff/total_activo)*100:.2f}%"),
            ("Cuentas por cobrar", f"$ {cc:,.2f}", f"{(cc/total_activo)*100:.2f}%"),
            ("Préstamos por cobrar", f"$ {pr:,.2f}", f"{(pr/total_activo)*100:.2f}%"),
            ("Inventarios", f"$ {inv:,.2f}", f"{(inv/total_activo)*100:.2f}%"),
            ("Gastos anticipados", f"$ {ga:,.2f}", f"{(ga/total_activo)*100:.2f}%"),
            ("TOTAL ACTIVO CORRIENTE", f"$ {total_corriente:,.2f}", f"{(total_corriente/total_activo)*100:.2f}%"),
        ]
        agregar_tabla(tabla_activo_corriente)

        # ------- ACTIVO NO CORRIENTE ---------
        agregar_seccion("ACTIVO NO CORRIENTE")

        tabla_activo_no_corr = [
            ("Propiedades, plantas y equipos", f"$ {propiedades:,.2f}", f"{(propiedades/total_activo)*100:.2f}%"),
            ("Activos intangibles", f"$ {intang:,.2f}", f"{(intang/total_activo)*100:.2f}%"),
            ("Impuesto diferido", f"$ {imp_diff:,.2f}", f"{(imp_diff/total_activo)*100:.2f}%"),
            ("Otros activos", f"$ {otros_act:,.2f}", f"{(otros_act/total_activo)*100:.2f}%"),
            ("TOTAL ACTIVO NO CORRIENTE", f"$ {total_no_corr:,.2f}", f"{(total_no_corr/total_activo)*100:.2f}%"),
            ("TOTAL ACTIVO", f"$ {total_activo:,.2f}", "100%"),
        ]
        agregar_tabla(tabla_activo_no_corr)

        # ------------------ PASIVO Y PATRIMONIO ----------------------

        agregar_seccion("PASIVO Y PATRIMONIO")

        prest_c = float(self.datos.get('PASIVOS_Prestamos_por_pagar_a_corto_plazo', 0))
        prest_pc = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_corto_plazo', 0))
        prest_pcorr = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_porcion_corriente', 0))
        cxp = float(self.datos.get('PASIVOS_Cuentas_por_pagar_comerciales', 0))
        ing_dif = float(self.datos.get('PASIVOS_Ingresos_diferidos', 0))
        otras_cxp = float(self.datos.get('PASIVOS_Otras_cuentas_por_pagar', 0))
        div = float(self.datos.get('PASIVOS_Dividendos_por_pagar', 0))
        prest_lp = float(self.datos.get('PASIVOS_Prestamos_a_partes_relacionadas_largo_plazo', 0))

        total_pasivo_corr = prest_c + prest_pc + prest_pcorr + cxp + ing_dif + otras_cxp + div
        total_pasivo = total_pasivo_corr + prest_lp

        cap_soc = float(self.datos.get('PATRIMONIO_Capital_social', 0))
        cap_min = float(self.datos.get('PATRIMONIO_Capital_social_minimo', 0))
        res_leg = float(self.datos.get('PATRIMONIO_Reserva_legal', 0))
        deficit = float(self.datos.get('PATRIMONIO_Deficit_acumulado', 0))

        total_patrimonio = cap_soc + res_leg - deficit
        total_pasivo_patr = total_pasivo + total_patrimonio if (total_pasivo + total_patrimonio) != 0 else 1

        tabla_pasivo_corr = [
            ("Préstamos corto plazo", f"$ {prest_c:,.2f}", f"{(prest_c/total_pasivo_patr)*100:.2f}%"),
            ("Préstamos partes corto plazo", f"$ {prest_pc:,.2f}", f"{(prest_pc/total_pasivo_patr)*100:.2f}%"),
            ("Préstamos porción corriente", f"$ {prest_pcorr:,.2f}", f"{(prest_pcorr/total_pasivo_patr)*100:.2f}%"),
            ("Cuentas por pagar", f"$ {cxp:,.2f}", f"{(cxp/total_pasivo_patr)*100:.2f}%"),
            ("Ingresos diferidos", f"$ {ing_dif:,.2f}", f"{(ing_dif/total_pasivo_patr)*100:.2f}%"),
            ("Otras cuentas por pagar", f"$ {otras_cxp:,.2f}", f"{(otras_cxp/total_pasivo_patr)*100:.2f}%"),
            ("Dividendos por pagar", f"$ {div:,.2f}", f"{(div/total_pasivo_patr)*100:.2f}%"),
            ("TOTAL PASIVO CORRIENTE", f"$ {total_pasivo_corr:,.2f}", f"{(total_pasivo_corr/total_pasivo_patr)*100:.2f}%"),
        ]
        agregar_tabla(tabla_pasivo_corr)

        tabla_pasivo_pat = [
            ("Préstamos largo plazo", f"$ {prest_lp:,.2f}", f"{(prest_lp/total_pasivo_patr)*100:.2f}%"),
            ("TOTAL PASIVO NO CORRIENTE", f"$ {prest_lp:,.2f}", f"{(prest_lp/total_pasivo_patr)*100:.2f}%"),
            ("TOTAL PASIVO", f"$ {total_pasivo:,.2f}", f"{(total_pasivo/total_pasivo_patr)*100:.2f}%"),
            ("Capital social", f"$ {cap_soc:,.2f}", f"{(cap_soc/total_pasivo_patr)*100:.2f}%"),
            ("Capital social mínimo", f"$ {cap_min:,.2f}", f"{(cap_min/total_pasivo_patr)*100:.2f}%"),
            ("Reserva legal", f"$ {res_leg:,.2f}", f"{(res_leg/total_pasivo_patr)*100:.2f}%"),
            ("Déficit acumulado", f"$ {-deficit:,.2f}", f"{(-deficit/total_pasivo_patr)*100:.2f}%"),
            ("TOTAL PATRIMONIO", f"$ {total_patrimonio:,.2f}", f"{(total_patrimonio/total_pasivo_patr)*100:.2f}%"),
            ("TOTAL PASIVO Y PATRIMONIO", f"$ {total_pasivo_patr:,.2f}", "100%"),
        ]
        agregar_tabla(tabla_pasivo_pat)

        doc.build(contenido)

        messagebox.showinfo(
            "PDF generado",
            f"El archivo PDF fue creado exitosamente:\n\n{archivo_pdf}"
        )

def generar_analisis_vertical_balance(parent, datos_financieros):
    """Función principal para generar el análisis vertical del balance"""
    if not datos_financieros:
        messagebox.showwarning(
            "Sin datos",
            "No hay datos financieros para generar el Análisis Vertical.\n\n"
            "Por favor, ingresa datos primero."
        )
        return
    
    AnalisisVerticalBalance(parent, datos_financieros)
