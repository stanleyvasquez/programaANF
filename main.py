import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from ingreso_datos import IngresoFinanciero
from editar_datos import EdicionFinanciero

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
        ventana_reportes.geometry("900x650")
        ventana_reportes.config(bg=self.bg_principal)
        ventana_reportes.resizable(False, False)
        
        # Centrar ventana
        ventana_reportes.update_idletasks()
        x = (ventana_reportes.winfo_screenwidth() // 2) - (450)
        y = (ventana_reportes.winfo_screenheight() // 2) - (325)
        ventana_reportes.geometry(f'900x650+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_reportes, bg=self.bg_secundario, height=80)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="📈 Generación de Reportes Financieros",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_secundario,
            fg=self.color_texto
        )
        titulo.pack(pady=25)
        
        # Frame principal
        frame_principal = tk.Frame(ventana_reportes, bg=self.bg_principal)
        frame_principal.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Instrucciones
        label_instrucciones = tk.Label(
            frame_principal,
            text="Selecciona el tipo de reporte que deseas generar",
            font=("Segoe UI", 12),
            bg=self.bg_principal,
            fg="#a8b2d1"
        )
        label_instrucciones.pack(pady=(0, 25))
        
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
                "descripcion": "ROE descompuesto en margen, rotación y apalancamiento",
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
        
        btn_cerrar = tk.Button(
            frame_principal,
            text="❌ Cerrar",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_peligro,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=40,
            pady=12,
            borderwidth=0,
            activebackground=self.ajustar_color(self.color_peligro, 1.2),
            activeforeground="white",
            command=ventana_reportes.destroy
        )
        btn_cerrar.pack(pady=(20, 0))
    
    def crear_boton_reporte(self, parent, titulo, descripcion, comando):
        """Crea un botón estilizado para cada tipo de reporte"""
        frame_boton = tk.Frame(parent, bg=self.color_acento, cursor="hand2", highlightthickness=0)
        frame_boton.pack(fill="x", pady=8)
        
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
            font=("Segoe UI", 13, "bold"),
            bg=self.color_acento,
            fg="white",
            cursor="hand2",
            anchor="w"
        )
        label_titulo.pack(fill="x", pady=(12, 5), padx=20)
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
            anchor="w"
        )
        label_desc.pack(fill="x", pady=(0, 12), padx=20)
        label_desc.bind("<Enter>", on_enter)
        label_desc.bind("<Leave>", on_leave)
        label_desc.bind("<Button-1>", lambda e: comando())
    
    def generar_balance_general(self):
        messagebox.showinfo(
            "Balance General",
            "Generando Balance General...\n\n"
            "Este reporte mostrará:\n"
            "• Activos Corrientes y No Corrientes\n"
            "• Pasivos Corrientes y No Corrientes\n"
            "• Patrimonio\n"
            "• Ecuación Contable: Activos = Pasivos + Patrimonio"
        )
    
    def generar_estado_resultados(self):
        messagebox.showinfo(
            "Estado de Resultados",
            "Generando Estado de Resultados...\n\n"
            "Este reporte mostrará:\n"
            "• Ingresos Totales\n"
            "• Costos y Gastos\n"
            "• Utilidad Bruta\n"
            "• Utilidad Operacional\n"
            "• Utilidad Neta"
        )
    
    def generar_analisis_vertical_balance(self):
        messagebox.showinfo(
            "Análisis Vertical - Balance",
            "Generando Análisis Vertical del Balance...\n\n"
            "Este reporte mostrará:\n"
            "• Porcentaje de cada cuenta respecto al total de activos\n"
            "• Composición porcentual de activos\n"
            "• Composición porcentual de pasivos y patrimonio\n"
            "• Interpretación de la estructura financiera"
        )
    
    def generar_analisis_vertical_resultados(self):
        messagebox.showinfo(
            "Análisis Vertical - Estado de Resultados",
            "Generando Análisis Vertical del Estado de Resultados...\n\n"
            "Este reporte mostrará:\n"
            "• Porcentaje de cada cuenta respecto a las ventas\n"
            "• Margen bruto (%)\n"
            "• Margen operacional (%)\n"
            "• Margen neto (%)"
        )
    
    def generar_analisis_dupont(self):
        messagebox.showinfo(
            "Análisis DuPont",
            "Generando Análisis de Rentabilidad DuPont...\n\n"
            "Este reporte mostrará:\n"
            "• ROE (Retorno sobre Patrimonio)\n"
            "• Margen de Utilidad Neta\n"
            "• Rotación de Activos\n"
            "• Multiplicador de Apalancamiento\n"
            "• Fórmula: ROE = Margen × Rotación × Apalancamiento"
        )
    
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
