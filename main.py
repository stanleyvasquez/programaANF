import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from ingreso_datos import IngresoFinanciero
from editar_datos import EdicionFinanciero
from balance_general import generar_balance_general
from estado_resultados import generar_estado_resultados
from analisis_vertical_balance import generar_analisis_vertical_balance
from analisis_vertical_estado_resultados import generar_analisis_vertical_estado_resultados
from analisis_dupont import generar_analisis_dupont

# =========================
# Ventana principal mejorada
# =========================
class AnalisisFinancieroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis Financiero")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Centrar ventana en la pantalla
        self.centrar_ventana()
        
        # Configurar colores modernos
        self.bg_principal = "#1a1a2e"
        self.bg_secundario = "#16213e"
        self.color_acento = "#0f4c75"
        self.color_texto = "#ffffff"
        self.color_exito = "#3bb273"
        self.color_peligro = "#e94560"
        
        self.root.config(bg=self.bg_principal)
        
        self.registros_financieros = []
        
        # Crear interfaz
        self.crear_header()
        self.crear_menu_principal()
        self.crear_footer()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        frame_header = tk.Frame(self.root, bg=self.bg_secundario, height=100)
        frame_header.pack(fill="x", pady=(0, 20))
        frame_header.pack_propagate(False)
        
        # Título principal
        titulo = tk.Label(
            frame_header, 
            text="📊 Análisis Financiero Empresarial",
            font=("Segoe UI", 22, "bold"), 
            bg=self.bg_secundario, 
            fg=self.color_texto
        )
        titulo.pack(pady=(15, 5))
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_header, 
            text="Sistema Integral de Gestión y Reportes Financieros",
            font=("Segoe UI", 11), 
            bg=self.bg_secundario, 
            fg="#a8b2d1"
        )
        subtitulo.pack()

    def crear_menu_principal(self):
        """Crea el menú principal con botones mejorados"""
        frame_menu = tk.Frame(self.root, bg=self.bg_principal)
        frame_menu.pack(expand=True, fill="both", padx=80, pady=10)
        
        # Configurar grid
        frame_menu.grid_columnconfigure(0, weight=1)
        
        # Botón Ingresar Datos
        self.crear_boton_menu(
            frame_menu, 
            "📝 Ingresar Datos",
            "Registrar nueva información financiera",
            self.color_acento,
            self.ingresar_datos,
            0
        )
        
        # Botón Modificar Datos
        self.crear_boton_menu(
            frame_menu, 
            "✏️ Modificar Datos",
            "Editar o eliminar registros existentes",
            self.color_acento,
            self.modificar_datos,
            1
        )
        
        # Botón Generar Reportes
        self.crear_boton_menu(
            frame_menu, 
            "📈 Generar Reportes",
            "Balance, Estado de Resultados, Análisis DuPont",
            self.color_exito,
            self.generar_reportes,
            2
        )
        
        # Botón Salir
        self.crear_boton_menu(
            frame_menu, 
            "🚪 Salir",
            "Cerrar la aplicación",
            self.color_peligro,
            self.salir,
            3
        )

    def crear_boton_menu(self, parent, texto, descripcion, color, comando, fila):
        """Crea un botón estilizado para el menú"""
        frame_boton = tk.Frame(parent, bg=color, cursor="hand2", highlightthickness=0)
        frame_boton.grid(row=fila, column=0, pady=12, sticky="ew")
        
        # Efecto hover mejorado
        def on_enter(e):
            color_hover = self.ajustar_color(color, 1.2)
            frame_boton.config(bg=color_hover)
            label_texto.config(bg=color_hover)
            label_desc.config(bg=color_hover)
        
        def on_leave(e):
            frame_boton.config(bg=color)
            label_texto.config(bg=color)
            label_desc.config(bg=color)
        
        frame_boton.bind("<Enter>", on_enter)
        frame_boton.bind("<Leave>", on_leave)
        frame_boton.bind("<Button-1>", lambda e: comando())
        
        # Texto principal del botón
        label_texto = tk.Label(
            frame_boton,
            text=texto,
            font=("Segoe UI", 14, "bold"),
            bg=color,
            fg="white",
            cursor="hand2"
        )
        label_texto.pack(pady=(15, 5), padx=20)
        label_texto.bind("<Enter>", on_enter)
        label_texto.bind("<Leave>", on_leave)
        label_texto.bind("<Button-1>", lambda e: comando())
        
        # Descripción del botón
        label_desc = tk.Label(
            frame_boton,
            text=descripcion,
            font=("Segoe UI", 9),
            bg=color,
            fg="#e0e0e0",
            cursor="hand2"
        )
        label_desc.pack(pady=(0, 15), padx=20)
        label_desc.bind("<Enter>", on_enter)
        label_desc.bind("<Leave>", on_leave)
        label_desc.bind("<Button-1>", lambda e: comando())

    def ajustar_color(self, color_hex, factor):
        """Ajusta el brillo de un color hexadecimal"""
        color_hex = color_hex.lstrip('#')
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def crear_footer(self):
        """Crea el pie de página"""
        frame_footer = tk.Frame(self.root, bg=self.bg_principal)
        frame_footer.pack(side="bottom", fill="x", pady=15)
        
        footer = tk.Label(
            frame_footer, 
            text="© 2025 - Proyecto Universitario de Análisis Financiero",
            font=("Segoe UI", 9), 
            bg=self.bg_principal, 
            fg="#6c7a89"
        )
        footer.pack()

    # =========================
    # Funciones de los botones
    # =========================
    
    def ingresar_datos(self):
        """Abre la ventana de ingreso de datos usando el módulo externo"""
        ingreso = IngresoFinanciero(self)
        ingreso.abrir_ventana()

    def modificar_datos(self):
        """Abre la ventana de edición de datos usando el módulo externo"""
        if not self.registros_financieros:
            messagebox.showinfo(
                "Sin Registros",
                "No hay registros financieros para editar.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        edicion = EdicionFinanciero(self)
        edicion.abrir_ventana()

    def generar_reportes(self):
        ventana_reportes = tk.Toplevel(self.root)
        ventana_reportes.title("Generar Reportes Financieros")
        ventana_reportes.geometry("850x700")
        ventana_reportes.config(bg=self.bg_principal)
        ventana_reportes.resizable(False, False)
        
        # Centrar ventana
        ventana_reportes.update_idletasks()
        x = (ventana_reportes.winfo_screenwidth() // 2) - (425)
        y = (ventana_reportes.winfo_screenheight() // 2) - (350)
        ventana_reportes.geometry(f'850x700+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_reportes, bg=self.bg_secundario, height=90)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="✓ Generación de Reportes Financieros",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_secundario,
            fg=self.color_texto
        )
        titulo.pack(pady=(20, 5))
        
        subtitulo = tk.Label(
            frame_header,
            text="Selecciona el tipo de reporte que deseas generar",
            font=("Segoe UI", 10),
            bg=self.bg_secundario,
            fg="#a8b2d1"
        )
        subtitulo.pack(pady=(0, 15))
        
        frame_container = tk.Frame(ventana_reportes, bg=self.bg_principal)
        frame_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_container, bg=self.bg_principal, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        frame_principal = tk.Frame(canvas, bg=self.bg_principal)
        
        frame_principal.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_principal, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def on_closing():
            canvas.unbind_all("<MouseWheel>")
            ventana_reportes.destroy()
        
        ventana_reportes.protocol("WM_DELETE_WINDOW", on_closing)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(180, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Botones de reportes
        reportes = [
            {
                "titulo": "📊 Balance General",
                "descripcion": "Estado de situación financiera con activos, pasivos y patrimonio",
                "comando": self.generar_balance_general
            },
            {
                "titulo": "💰 Estado de Resultados",
                "descripcion": "Ingresos, gastos y utilidad neta del período",
                "comando": self.generar_estado_resultados
            },
            {
                "titulo": "📈 Análisis Vertical - Balance",
                "descripcion": "Análisis porcentual de cada cuenta respecto al total de activos",
                "comando": self.generar_analisis_vertical_balance
            },
            {
                "titulo": "📉 Análisis Vertical - Estado de Resultados",
                "descripcion": "Análisis porcentual de cada cuenta respecto a las ventas totales",
                "comando": self.generar_analisis_vertical_resultados
            },
            {
                "titulo": "🎯 Análisis de Rentabilidad DuPont",
                "descripcion": "ROE (Retorno sobre Patrimonio) descompuesto en margen, rotación y apalancamiento",
                "comando": self.generar_analisis_dupont
            },
            {
                "titulo": "📋 Resumen Ejecutivo",
                "descripcion": "Resumen completo de todos los análisis y conclusiones",
                "comando": self.generar_resumen_ejecutivo
            }
        ]
        
        for reporte in reportes:
            self.crear_boton_reporte(frame_principal, reporte["titulo"], 
                                    reporte["descripcion"], reporte["comando"])
        
        frame_footer = tk.Frame(ventana_reportes, bg=self.bg_principal)
        frame_footer.pack(fill="x", padx=30, pady=(10, 20))
        
        btn_cerrar = tk.Button(
            frame_footer,
            text="✕ Cerrar",
            font=("Segoe UI", 11, "bold"),
            bg=self.color_peligro,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10,
            borderwidth=0,
            activebackground=self.ajustar_color(self.color_peligro, 1.2),
            activeforeground="white",
            command=on_closing
        )
        btn_cerrar.pack()
    
    def crear_boton_reporte(self, parent, titulo, descripcion, comando):
        """Crea un botón estilizado para cada tipo de reporte"""
        frame_boton = tk.Frame(parent, bg=self.color_acento, cursor="hand2", 
                              highlightthickness=0, relief="flat")
        frame_boton.pack(fill="x", pady=6)
        
        def on_enter(e):
            color_hover = self.ajustar_color(self.color_acento, 1.3)
            frame_boton.config(bg=color_hover)
            label_titulo.config(bg=color_hover)
            label_desc.config(bg=color_hover)
        
        def on_leave(e):
            frame_boton.config(bg=self.color_acento)
            label_titulo.config(bg=self.color_acento)
            label_desc.config(bg=self.color_acento)
        
        frame_boton.bind("<Enter>", on_enter)
        frame_boton.bind("<Leave>", on_leave)
        frame_boton.bind("<Button-1>", lambda e: comando())
        
        label_titulo = tk.Label(
            frame_boton,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=self.color_acento,
            fg="white",
            cursor="hand2",
            anchor="w"
        )
        label_titulo.pack(fill="x", pady=(10, 3), padx=18)
        label_titulo.bind("<Enter>", on_enter)
        label_titulo.bind("<Leave>", on_leave)
        label_titulo.bind("<Button-1>", lambda e: comando())
        
        label_desc = tk.Label(
            frame_boton,
            text=descripcion,
            font=("Segoe UI", 9),
            bg=self.color_acento,
            fg="#e0e0e0",
            cursor="hand2",
            anchor="w",
            wraplength=500
        )
        label_desc.pack(fill="x", pady=(0, 10), padx=18)
        label_desc.bind("<Enter>", on_enter)
        label_desc.bind("<Leave>", on_leave)
        label_desc.bind("<Button-1>", lambda e: comando())
    
    def generar_balance_general(self):
        if not self.registros_financieros:
            messagebox.showwarning(
                "Sin Datos",
                "No hay registros financieros para generar el Balance General.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        # Si hay un solo registro, usarlo directamente
        if len(self.registros_financieros) == 1:
            generar_balance_general(self.root, self.registros_financieros[0])
            return
        
        # Si hay múltiples registros, permitir seleccionar uno
        self.seleccionar_registro_para_reporte("Balance General", generar_balance_general)
    
    def seleccionar_registro_para_reporte(self, nombre_reporte, funcion_reporte):
        """Permite seleccionar un registro cuando hay múltiples registros disponibles"""
        ventana_seleccion = tk.Toplevel(self.root)
        ventana_seleccion.title(f"Seleccionar Registro - {nombre_reporte}")
        ventana_seleccion.geometry("700x500")
        ventana_seleccion.config(bg=self.bg_principal)
        ventana_seleccion.resizable(False, False)
        
        # Centrar ventana
        ventana_seleccion.update_idletasks()
        x = (ventana_seleccion.winfo_screenwidth() // 2) - (350)
        y = (ventana_seleccion.winfo_screenheight() // 2) - (250)
        ventana_seleccion.geometry(f'700x500+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_seleccion, bg=self.bg_secundario, height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text=f"Seleccionar Registro para {nombre_reporte}",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_secundario,
            fg=self.color_texto
        )
        titulo.pack(pady=(20, 5))
        
        subtitulo = tk.Label(
            frame_header,
            text="Selecciona el registro financiero que deseas analizar",
            font=("Segoe UI", 10),
            bg=self.bg_secundario,
            fg="#a8b2d1"
        )
        subtitulo.pack()
        

        # Frame para la tabla
        frame_tabla = tk.Frame(ventana_seleccion, bg=self.bg_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear Treeview
        columnas = ("Empresa", "Año", "Moneda", "Total Activos", "Total Pasivos")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12,)
                # Estilo oscuro para Treeview
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background=self.bg_secundario,
            fieldbackground=self.bg_secundario,
            foreground=self.color_texto,
            rowheight=25,
            font=("Segoe UI", 10)
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", self.color_acento)],
            foreground=[("selected", "white")]
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.color_acento,
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )


        # Aplicar el estilo al Treeview
        tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12,
            style="Custom.Treeview"
        )


        # Configurar columnas
        tree.heading("Empresa", text="Empresa")
        tree.heading("Año", text="Año")
        tree.heading("Moneda", text="Moneda")
        tree.heading("Total Activos", text="Total Activos")
        tree.heading("Total Pasivos", text="Total Pasivos")
        
        tree.column("Empresa", width=200, anchor="w")
        tree.column("Año", width=80, anchor="center")
        tree.column("Moneda", width=150, anchor="center")
        tree.column("Total Activos", width=120, anchor="e")
        tree.column("Total Pasivos", width=120, anchor="e")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insertar datos
        for idx, registro in enumerate(self.registros_financieros):
            total_activos = (
                float(registro.get('ACTIVOS_Efectivo', 0)) +
                float(registro.get('ACTIVOS_Cuentas_por_cobrar_comerciales', 0)) +
                float(registro.get('ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas', 0)) +
                float(registro.get('ACTIVOS_Inventarios', 0)) +
                float(registro.get('ACTIVOS_Gastos_pagados_por_anticipado', 0)) +
                float(registro.get('ACTIVOS_Propiedades,_plantas_y_equipos', 0)) +
                float(registro.get('ACTIVOS_Activos_intangibles', 0)) +
                float(registro.get('ACTIVOS_Impuesto_sobre_la_renta_diferido', 0)) +
                float(registro.get('ACTIVOS_Otros_activos', 0))
            )
            
            total_pasivos = (
                float(registro.get('PASIVOS_Prestamos_por_pagar_a_corto_plazo', 0)) +
                float(registro.get('PASIVOS_Prestamos_a_partes_relacionadas_corto_plazo', 0)) +
                float(registro.get('PASIVOS_Prestamos_a_partes_relacionadas_porcion_corriente', 0)) +
                float(registro.get('PASIVOS_Cuentas_por_pagar_comerciales', 0)) +
                float(registro.get('PASIVOS_Ingresos_diferidos', 0)) +
                float(registro.get('PASIVOS_Otras_cuentas_por_pagar', 0)) +
                float(registro.get('PASIVOS_Dividendos_por_pagar', 0)) +
                float(registro.get('PASIVOS_Prestamos_a_partes_relacionadas_largo_plazo', 0))
            )
            
            tree.insert("", "end", iid=idx, values=(
                registro.get('nombre_empresa', 'N/A'),
                registro.get('anio', 'N/A'),
                registro.get('tipo_moneda', 'N/A'),
                f"${total_activos:,.2f}",
                f"${total_pasivos:,.2f}"
            ))
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame de botones
        frame_botones = tk.Frame(ventana_seleccion, bg=self.bg_principal)
        frame_botones.pack(fill="x", padx=20, pady=(0, 20))
        
        def generar_reporte_seleccionado():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning(
                    "Sin Selección",
                    "Por favor, selecciona un registro de la tabla."
                )
                return
            
            idx = int(seleccion[0])
            registro = self.registros_financieros[idx]
            ventana_seleccion.destroy()
            funcion_reporte(self.root, registro)
        
        btn_generar = tk.Button(
            frame_botones,
            text="✓ Generar Reporte",
            command=generar_reporte_seleccionado,
            font=("Segoe UI", 11, "bold"),
            bg=self.color_exito,
            fg="white",
            activebackground=self.ajustar_color(self.color_exito, 1.2),
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10
        )
        btn_generar.pack(side="right")
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="✕ Cancelar",
            command=ventana_seleccion.destroy,
            font=("Segoe UI", 11, "bold"),
            bg=self.color_peligro,
            fg="white",
            activebackground=self.ajustar_color(self.color_peligro, 1.2),
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10
        )
        btn_cancelar.pack(side="right", padx=(0, 10))
    
    def generar_estado_resultados(self):
        if not self.registros_financieros:
            messagebox.showwarning(
                "Sin Datos",
                "No hay registros financieros para generar el Estado de Resultados.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        # Si hay un solo registro, usarlo directamente
        if len(self.registros_financieros) == 1:
            generar_estado_resultados(self.root, self.registros_financieros[0])
            return
        
        # Si hay múltiples registros, permitir seleccionar uno
        self.seleccionar_registro_para_reporte("Estado de Resultados", generar_estado_resultados)
    
    def generar_analisis_vertical_balance(self):
        if not self.registros_financieros:
            messagebox.showwarning(
                "Sin Datos",
                "No hay registros financieros para generar el Análisis Vertical.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        # Si hay un solo registro, usarlo directamente
        if len(self.registros_financieros) == 1:
            generar_analisis_vertical_balance(self.root, self.registros_financieros[0])
            return
        
        # Si hay múltiples registros, permitir seleccionar uno
        self.seleccionar_registro_para_reporte("Análisis Vertical - Balance", generar_analisis_vertical_balance)
    
    def generar_analisis_vertical_resultados(self):
        if not self.registros_financieros:
            messagebox.showwarning(
                "Sin Datos",
                "No hay registros financieros para generar el Análisis Vertical.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        if len(self.registros_financieros) == 1:
            generar_analisis_vertical_estado_resultados(self.root, self.registros_financieros[0])
            return
        
        self.seleccionar_registro_para_reporte(
            "Análisis Vertical - Estado de Resultados", 
            generar_analisis_vertical_estado_resultados
        )
    
    def generar_analisis_dupont(self):
        if not self.registros_financieros:
            messagebox.showwarning(
                "Sin Datos",
                "No hay registros financieros para generar el Análisis de Rentabilidad DuPont.\n\n"
                "Por favor, ingresa datos primero usando la opción 'Ingresar Datos'."
            )
            return
        
        # Si hay un solo registro, usarlo directamente
        if len(self.registros_financieros) == 1:
            generar_analisis_dupont(self.root, self.registros_financieros[0])
            return
        
        # Si hay múltiples registros, permitir seleccionar uno
        self.seleccionar_registro_para_reporte("Análisis DuPont", generar_analisis_dupont)
    
    def generar_resumen_ejecutivo(self):
        messagebox.showinfo(
            "Resumen Ejecutivo",
            "Generando Resumen Ejecutivo...\n\n"
            "Este reporte incluirá:\n"
            "• Resumen de Balance General\n"
            "• Resumen de Estado de Resultados\n"
            "• Principales indicadores financieros\n"
            "• Análisis de rentabilidad\n"
            "• Conclusiones y recomendaciones"
        )

    def salir(self):
        confirmar = messagebox.askyesno(
            "Confirmar Salida", 
            "¿Estás seguro de que deseas salir del programa?"
        )
        if confirmar:
            self.root.destroy()


# =========================
# Ejecución principal
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisisFinancieroApp(root)
    root.mainloop()
