import tkinter as tk
from tkinter import scrolledtext, messagebox

# Intentar importar reportlab para generar PDF
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False


def generar_ratios_financieros(root, datos, app):
    """
    Genera la ventana de Ratios Financieros y permite exportar a PDF.
    root: ventana raíz de Tkinter
    datos: diccionario con el registro financiero seleccionado
    app: instancia de AnalisisFinancieroApp (para colores, etc.)
    """

    # =========================
    # CÁLCULO DE RATIOS
    # =========================
    activo_corriente = (
        datos.get("ACTIVOS_Efectivo", 0) +
        datos.get("ACTIVOS_Cuentas_por_cobrar_comerciales", 0) +
        datos.get("ACTIVOS_Prestamos_por_cobrar_a_partes_relacionadas", 0) +
        datos.get("ACTIVOS_Inventarios", 0) +
        datos.get("ACTIVOS_Gastos_pagados_por_anticipado", 0)
    )

    pasivo_corriente = (
        datos.get("PASIVOS_Prestamos_por_pagar_a_corto_plazo", 0) +
        datos.get("PASIVOS_Prestamos_a_partes_relacionadas_corto_plazo", 0) +
        datos.get("PASIVOS_Prestamos_a_partes_relacionadas_porcion_corriente", 0) +
        datos.get("PASIVOS_Cuentas_por_pagar_comerciales", 0) +
        datos.get("PASIVOS_Ingresos_diferidos", 0) +
        datos.get("PASIVOS_Otras_cuentas_por_pagar", 0) +
        datos.get("PASIVOS_Dividendos_por_pagar", 0)
    )

    liquidez_corriente = activo_corriente / pasivo_corriente if pasivo_corriente else 0

    prueba_acida = (
        (activo_corriente - datos.get("ACTIVOS_Inventarios", 0)) / pasivo_corriente
        if pasivo_corriente else 0
    )

    capital_trabajo = activo_corriente - pasivo_corriente

    inventarios = datos.get("ACTIVOS_Inventarios", 0)
    costo_ventas = abs(datos.get("GASTOS_Costo_de_Ventas", 0))

    rotacion_inventarios = costo_ventas / inventarios if inventarios else 0

    cuentas_por_cobrar = datos.get("ACTIVOS_Cuentas_por_cobrar_comerciales", 0)
    ventas = datos.get("INGRESOS_Ventas", 0)

    periodo_cobro = (cuentas_por_cobrar / ventas) * 365 if ventas else 0

    cuentas_por_pagar = datos.get("PASIVOS_Cuentas_por_pagar_comerciales", 0)

    periodo_pago = (cuentas_por_pagar / costo_ventas) * 365 if costo_ventas else 0

    ratios = {
        "liquidez_corriente": round(liquidez_corriente, 2),
        "prueba_acida": round(prueba_acida, 2),
        "capital_trabajo": round(capital_trabajo, 2),
        "rotacion_inventarios": round(rotacion_inventarios, 2),
        "periodo_cobro": round(periodo_cobro, 1),
        "periodo_pago": round(periodo_pago, 1),
    }

    # =========================
    # VENTANA DE RATIOS
    # =========================
    ventana = tk.Toplevel(root)
    ventana.title("📊 Indicadores Financieros – Ratios Financieros")
    ventana.geometry("900x700")  # un poco más ancho para que se vea mejor
    ventana.config(bg="#1e293b")  # mismo fondo que el Balance General
    ventana.resizable(False, False)

    # HEADER similar al balance_general
    frame_header = tk.Frame(ventana, bg="#0f172a")
    frame_header.pack(fill="x", pady=(0, 20))

    tk.Label(
        frame_header,
        text="📊 Ratios Financieros",
        font=("Segoe UI", 24, "bold"),
        bg="#0f172a",
        fg="white"
    ).pack(pady=10)

    nombre_empresa = datos.get("nombre_empresa", "Empresa no definida")
    anio = datos.get("anio", "Año no definido")
    tipo_moneda = datos.get("tipo_moneda", "")

    info_frame = tk.Frame(frame_header, bg="#0f172a")
    info_frame.pack(pady=(0, 10))

    tk.Label(
        info_frame,
        text=f"{nombre_empresa}",
        font=("Segoe UI", 14, "bold"),
        bg="#0f172a",
        fg="#94a3b8"
    ).pack()

    tk.Label(
        info_frame,
        text=f"Año: {anio} | Moneda: {tipo_moneda}",
        font=("Segoe UI", 11),
        bg="#0f172a",
        fg="#64748b"
    ).pack()

    # CUERPO PRINCIPAL
    frame_contenedor = tk.Frame(ventana, bg="#1e293b")
    frame_contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    caja = scrolledtext.ScrolledText(
        frame_contenedor,
        width=95,
        height=25,
        bg="#111827",
        fg="white",
        font=("Segoe UI", 10)
    )
    caja.pack(fill="both", expand=True)

    # ===== CONTENIDO DEL TEXTO =====
    caja.insert(tk.END, "RESULTADOS DE RATIOS FINANCIEROS\n")
    caja.insert(tk.END, "---------------------------------\n\n")

    caja.insert(tk.END, f"Liquidez Corriente: {ratios['liquidez_corriente']:.2f}\n")
    caja.insert(
        tk.END,
        "   • Mide cuántas veces los activos corrientes cubren los pasivos corrientes.\n"
        "   • Una razón mayor a 1 indica, en general, capacidad para cubrir obligaciones de corto plazo.\n\n"
    )

    caja.insert(tk.END, f"Prueba Ácida: {ratios['prueba_acida']:.2f}\n")
    caja.insert(
        tk.END,
        "   • Similar a la liquidez corriente, pero excluye inventarios.\n"
        "   • Evalúa la capacidad de pago inmediato, sin depender de vender existencias.\n\n"
    )

    caja.insert(tk.END, f"Capital de Trabajo: ${ratios['capital_trabajo']:,.2f}\n")
    caja.insert(
        tk.END,
        "   • Diferencia entre activos corrientes y pasivos corrientes.\n"
        "   • Representa el margen de maniobra para operar en el corto plazo.\n\n"
    )

    caja.insert(
        tk.END,
        f"Rotación de Inventarios: {ratios['rotacion_inventarios']:.2f} veces\n"
    )
    caja.insert(
        tk.END,
        "   • Indica cuántas veces en el año se vende y renueva el inventario.\n"
        "   • Un valor bajo puede señalar inventario ocioso; uno muy alto, riesgo de desabastecimiento.\n\n"
    )

    caja.insert(
        tk.END,
        f"Período Promedio de Cobro: {ratios['periodo_cobro']:.1f} días\n"
    )
    caja.insert(
        tk.END,
        "   • Días promedio que tarda la empresa en cobrar sus cuentas por cobrar.\n"
        "   • Se compara con la política de crédito (30 días, 60 días, etc.).\n\n"
    )

    caja.insert(
        tk.END,
        f"Período Promedio de Pago: {ratios['periodo_pago']:.1f} días\n"
    )
    caja.insert(
        tk.END,
        "   • Días promedio que tarda la empresa en pagar a sus proveedores.\n"
        "   • Un plazo mayor mejora liquidez, pero puede afectar la relación con proveedores.\n"
    )

    caja.config(state="disabled")

    # =========================
    # FUNCIÓN PARA EXPORTAR A PDF
    # =========================
    def exportar_pdf():
        if not REPORTLAB_DISPONIBLE:
            messagebox.showerror(
                "Error al exportar",
                "No se encontró la librería 'reportlab'.\n\n"
                "Instálala con:\n\n"
                "    pip install reportlab"
            )
            return

        nombre_limpio = str(nombre_empresa).replace(" ", "_").replace("/", "_")
        nombre_archivo = f"Ratios_Financieros_{nombre_limpio}_{anio}.pdf"

        try:
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            width, height = letter
            y = height - 60

            # ===== Título centrado =====
            titulo = "Ratios Financieros"
            c.setFont("Helvetica-Bold", 16)
            tw = c.stringWidth(titulo, "Helvetica-Bold", 16)
            c.drawString((width - tw) / 2, y, titulo)
            y -= 30

            # ===== Datos generales centrados =====
            c.setFont("Helvetica-Bold", 10)

            texto = f"Empresa: {nombre_empresa}"
            tw = c.stringWidth(texto, "Helvetica-Bold", 10)
            c.drawString((width - tw) / 2, y, texto)
            y -= 15

            texto = f"Año: {anio}"
            tw = c.stringWidth(texto, "Helvetica-Bold", 10)
            c.drawString((width - tw) / 2, y, texto)
            y -= 15

            texto = f"Moneda: {tipo_moneda}"
            tw = c.stringWidth(texto, "Helvetica-Bold", 10)
            c.drawString((width - tw) / 2, y, texto)
            y -= 30

            # ===== Ratios con significado =====
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, "Resultados e interpretación de los ratios:")
            y -= 20
            c.setFont("Helvetica", 10)

            lineas = [
                f"Liquidez Corriente: {ratios['liquidez_corriente']:.2f}",
                "  Indica cuántas veces los activos corrientes cubren los pasivos corrientes.",
                "",
                f"Prueba Ácida: {ratios['prueba_acida']:.2f}",
                "  Mide la capacidad de pago a corto plazo sin considerar inventarios.",
                "",
                f"Capital de Trabajo: ${ratios['capital_trabajo']:,.2f}",
                "  Diferencia entre activos corrientes y pasivos corrientes; margen operativo de corto plazo.",
                "",
                f"Rotación de Inventarios: {ratios['rotacion_inventarios']:.2f} veces",
                "  Veces que el inventario se vende y se repone a lo largo del año.",
                "",
                f"Período Promedio de Cobro: {ratios['periodo_cobro']:.1f} días",
                "  Días promedio para recuperar las cuentas por cobrar.",
                "",
                f"Período Promedio de Pago: {ratios['periodo_pago']:.1f} días",
                "  Días promedio que tarda la empresa en pagar a sus proveedores.",
            ]

            for linea in lineas:
                if y < 80:
                    c.showPage()
                    y = height - 60
                    c.setFont("Helvetica", 10)
                if linea == "":
                    y -= 5
                else:
                    c.drawString(50, y, linea)
                    y -= 15

            c.showPage()
            c.save()

            messagebox.showinfo(
                "PDF generado",
                f"El archivo se ha guardado como:\n\n{nombre_archivo}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error al generar PDF",
                f"Ocurrió un error al generar el PDF:\n\n{e}"
            )

    # =========================
    # BOTONES IGUALES AL BALANCE GENERAL
    # =========================
    frame_botones = tk.Frame(ventana, bg="#1e293b")
    frame_botones.pack(fill="x", padx=20, pady=(0, 20))

    # Botón Cerrar (a la derecha, igual que en Balance General)
    btn_cerrar = tk.Button(
        frame_botones,
        text="✕ Cerrar",
        command=ventana.destroy,
        font=("Segoe UI", 11, "bold"),
        bg="#ef4444",          # mismo rojo
        fg="white",
        activebackground="#dc2626",
        activeforeground="white",
        cursor="hand2",
        relief="flat",
        padx=30,
        pady=10
    )
    btn_cerrar.pack(side="right")

    # Botón Exportar PDF (a la derecha, pero a la izquierda del Cerrar)
    btn_exportar = tk.Button(
        frame_botones,
        text="📄 Exportar PDF",
        command=exportar_pdf,
        font=("Segoe UI", 11, "bold"),
        bg="#0ea5e9",          # mismo celeste
        fg="white",
        activebackground="#0284c7",
        activeforeground="white",
        cursor="hand2",
        relief="flat",
        padx=30,
        pady=10
    )
    btn_exportar.pack(side="right", padx=(0, 10))
