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

    # Lo guardamos en un dict para reutilizarlo en el PDF
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
    ventana.geometry("750x700")
    ventana.config(bg=app.bg_principal)
    ventana.resizable(False, False)

    tk.Label(
        ventana,
        text="📊 Ratios Financieros",
        font=("Segoe UI", 20, "bold"),
        bg=app.bg_secundario,
        fg="white",
        anchor="center",
        justify="center"
        
    ).pack(fill="x", pady=10)

    caja = scrolledtext.ScrolledText(
        ventana,
        width=95,
        height=35,
        bg=app.bg_secundario,
        fg="white",
        font=("Segoe UI", 10)
    )
    caja.pack(padx=20, pady=(10, 5))

    # Encabezado
    nombre_empresa = datos.get("nombre_empresa", "Empresa no definida")
    anio = datos.get("anio", "Año no definido")
    tipo_moneda = datos.get("tipo_moneda", "")

    caja.insert(tk.END, f"Empresa: {nombre_empresa}\n")
    caja.insert(tk.END, f"Año: {anio}\n")
    caja.insert(tk.END, f"Moneda: {tipo_moneda}\n\n")

    caja.insert(tk.END, "RESULTADOS DE RATIOS FINANCIEROS\n")
    caja.insert(tk.END, "---------------------------------\n\n")

    caja.insert(tk.END, f"Liquidez Corriente: {ratios['liquidez_corriente']:.2f}\n")
    caja.insert(tk.END, f"Prueba Ácida: {ratios['prueba_acida']:.2f}\n")
    caja.insert(tk.END, f"Capital de Trabajo: ${ratios['capital_trabajo']:,.2f}\n\n")

    caja.insert(tk.END, f"Rotación de Inventarios: {ratios['rotacion_inventarios']:.2f} veces\n")
    caja.insert(tk.END, f"Período Promedio de Cobro: {ratios['periodo_cobro']:.1f} días\n")
    caja.insert(tk.END, f"Período Promedio de Pago: {ratios['periodo_pago']:.1f} días\n\n")

    # =========================
    # INTERPRETACIÓN DE RATIOS (VENTANA)
    # =========================
    caja.insert(tk.END, "INTERPRETACIÓN DE LOS RATIOS\n")
    caja.insert(tk.END, "----------------------------\n\n")

    caja.insert(
        tk.END,
        f"- Liquidez Corriente: indica cuántos {tipo_moneda.split('-')[0].strip() if tipo_moneda else 'unidades monetarias'} "
        f"de activos corrientes tiene la empresa por cada 1 de deuda a corto plazo. "
        f"Un valor de {ratios['liquidez_corriente']:.2f} significa que por cada 1 en pasivos corrientes, "
        f"la empresa dispone de {ratios['liquidez_corriente']:.2f} en activos corrientes.\n\n"
    )

    caja.insert(
        tk.END,
        f"- Prueba Ácida: mide la capacidad de la empresa para cubrir sus deudas a corto plazo sin depender "
        f"de los inventarios. Un valor de {ratios['prueba_acida']:.2f} indica cuántas unidades monetarias "
        f"líquidas (sin inventarios) tiene por cada 1 de pasivo corriente.\n\n"
    )

    caja.insert(
        tk.END,
        f"- Capital de Trabajo: representa el excedente de activos corrientes sobre pasivos corrientes. "
        f"Un capital de trabajo de {ratios['capital_trabajo']:,.2f} significa que, después de cubrir las "
        f"deudas a corto plazo, la empresa aún dispone de ese monto para operar.\n\n"
    )

    caja.insert(
        tk.END,
        f"- Rotación de Inventarios: muestra cuántas veces, aproximadamente, la empresa renueva sus inventarios "
        f"en el año. Un valor de {ratios['rotacion_inventarios']:.2f} veces indica la frecuencia con la que "
        f"el inventario se convierte en ventas.\n\n"
    )

    caja.insert(
        tk.END,
        f"- Período Promedio de Cobro: indica el número de días que, en promedio, tarda la empresa en cobrar "
        f"sus cuentas por cobrar. Un valor de {ratios['periodo_cobro']:.1f} días sugiere el tiempo estimado "
        f"que el efectivo tarda en entrar a la empresa después de una venta a crédito.\n\n"
    )

    caja.insert(
        tk.END,
        f"- Período Promedio de Pago: indica el número de días que, en promedio, la empresa tarda en pagar "
        f"a sus proveedores. Un valor de {ratios['periodo_pago']:.1f} días refleja el plazo habitual de pago "
        f"de las obligaciones con terceros.\n\n"
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

        # Nombre de archivo
        nombre_limpio = str(nombre_empresa).replace(" ", "_").replace("/", "_")
        nombre_archivo = f"Ratios_Financieros_{nombre_limpio}_{anio}.pdf"

        try:
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            width, height = letter
            y = height - 50

            # Título
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width / 2, y, "Ratios Financieros")
            y -= 30

            # Datos generales
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(width / 2, y, f"Empresa: {nombre_empresa}")
            y -= 15
            c.drawCentredString(width / 2, y, f"Año: {anio}")
            y -= 15
            c.drawCentredString(width / 2, y, f"Moneda: {tipo_moneda}")
            y -= 30

            # Ratios
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, "Resultados de Ratios:")
            y -= 20
            c.setFont("Helvetica", 10)

            lineas = [
                f"Liquidez Corriente: {ratios['liquidez_corriente']:.2f}",
                f"Prueba Ácida: {ratios['prueba_acida']:.2f}",
                f"Capital de Trabajo: ${ratios['capital_trabajo']:,.2f}",
                f"Rotación de Inventarios: {ratios['rotacion_inventarios']:.2f} veces",
                f"Período Promedio de Cobro: {ratios['periodo_cobro']:.1f} días",
                f"Período Promedio de Pago: {ratios['periodo_pago']:.1f} días",
            ]

            for linea in lineas:
                if y < 80:  # si ya no hay espacio en la página, crear otra
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(50, y, linea)
                y -= 18

            # Interpretación en el PDF
            if y < 120:
                c.showPage()
                y = height - 50

            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, "Interpretación de los Ratios:")
            y -= 25
            c.setFont("Helvetica", 10)

            interpretaciones = [
                f"• Liquidez Corriente: indica cuántas unidades monetarias de activos corrientes hay por cada 1 de deuda a corto plazo.",
                f"• Prueba Ácida: mide la capacidad de pagar deudas de corto plazo sin depender de los inventarios.",
                f"• Capital de Trabajo: muestra el excedente de activos corrientes sobre pasivos corrientes para operar.",
                f"• Rotación de Inventarios: refleja cuántas veces, aproximadamente, se renueva el inventario en el año.",
                f"• Período Promedio de Cobro: días promedio que tarda la empresa en cobrar sus ventas a crédito.",
                f"• Período Promedio de Pago: días promedio que tarda la empresa en pagar a sus proveedores.",
            ]

            for interp in interpretaciones:
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(50, y, interp)
                y -= 18

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
    # BOTÓN EXPORTAR PDF
    # =========================
    frame_botones = tk.Frame(ventana, bg=app.bg_principal)
    frame_botones.pack(fill="x", pady=(0, 15))

    btn_exportar = tk.Button(
        frame_botones,
        text="📄 Exportar a PDF",
        font=("Segoe UI", 11, "bold"),
        bg=app.color_exito,
        fg="white",
        cursor="hand2",
        relief="flat",
        padx=30,
        pady=8,
        activebackground=app.ajustar_color(app.color_exito, 1.2),
        activeforeground="white",
        command=exportar_pdf
    )
    btn_exportar.pack(side="right", padx=20)
