import tkinter as tk
from tkinter import messagebox, ttk

class AgregarCuenta:
    def __init__(self, parent_app, callback=None):
        self.parent_app = parent_app
        self.callback = callback
        
    def abrir_ventana(self):
        """Abre el asistente interactivo para agregar cuentas"""
        ventana_asistente = tk.Toplevel(self.parent_app.root)
        ventana_asistente.title("Agregar Cuenta Personalizada")
        ventana_asistente.geometry("600x750")
        ventana_asistente.config(bg=self.parent_app.bg_principal)
        ventana_asistente.resizable(False, False)
        
        # Centrar ventana
        ventana_asistente.update_idletasks()
        x = (ventana_asistente.winfo_screenwidth() // 2) - 300
        y = (ventana_asistente.winfo_screenheight() // 2) - 375
        ventana_asistente.geometry(f'600x750+{x}+{y}')
        
        # HEADER
        frame_header = tk.Frame(ventana_asistente, bg=self.parent_app.bg_secundario, height=60)
        frame_header.pack(side="top", fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="Agregar Cuenta Personalizada",
            font=("Segoe UI", 16, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=10)
        
        # ----- CONTENEDOR CENTRAL (SCROLL) -----
        frame_contenido = tk.Frame(ventana_asistente, bg=self.parent_app.bg_principal)
        frame_contenido.pack(side="top", fill="both", expand=True)
        
        canvas = tk.Canvas(frame_contenido, bg=self.parent_app.bg_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.parent_app.bg_principal)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # ----- PASO 1 -----
        label_paso1 = tk.Label(
            frame_scroll,
            text="Paso 1: Tipo de Cuenta",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.bg_principal,
            fg=self.parent_app.color_acento
        )
        label_paso1.pack(anchor="w", pady=(0, 8))
        
        frame_tipos = tk.Frame(frame_scroll, bg=self.parent_app.bg_principal)
        frame_tipos.pack(fill="x", pady=(0, 15))
        
        tipos_cuenta = [
            {"nombre": "🏦 ACTIVOS", "tipo": "ACTIVOS"},
            {"nombre": "💳 PASIVOS", "tipo": "PASIVOS"},
            {"nombre": "💰 PATRIMONIO", "tipo": "PATRIMONIO"},
            {"nombre": "📈 INGRESOS", "tipo": "INGRESOS"},
            {"nombre": "📉 GASTOS", "tipo": "GASTOS"}
        ]
        
        tipo_seleccionado = tk.StringVar()
        
        for tipo_info in tipos_cuenta:
            tk.Radiobutton(
                frame_tipos,
                text=tipo_info["nombre"],
                variable=tipo_seleccionado,
                value=tipo_info["tipo"],
                bg=self.parent_app.bg_principal,
                fg=self.parent_app.color_texto,
                selectcolor=self.parent_app.bg_principal,
                font=("Segoe UI", 10),
                cursor="hand2"
            ).pack(anchor="w", pady=5)
        
        # ----- PASO 2 -----
        label_paso2 = tk.Label(
            frame_scroll,
            text="Paso 2: Clasificación",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.bg_principal,
            fg=self.parent_app.color_acento
        )
        label_paso2.pack(anchor="w", pady=(10, 8))
        
        frame_subrubros = tk.Frame(frame_scroll, bg=self.parent_app.bg_principal)
        frame_subrubros.pack(fill="x", pady=(0, 15))
        
        subrubro_seleccionado = tk.StringVar()
        
        def actualizar_subrubros(*args):
            for widget in frame_subrubros.winfo_children():
                widget.destroy()
            
            tipo = tipo_seleccionado.get()
            
            if tipo == "ACTIVOS":
                opciones = [("Activo Corriente","Activo Corriente"), ("Activo No Corriente","Activo No Corriente")]
            elif tipo == "PASIVOS":
                opciones = [("Pasivo Corriente","Pasivo Corriente"), ("Pasivo No Corriente","Pasivo No Corriente")]
            elif tipo == "PATRIMONIO":
                opciones = [("Capital Contable","Capital Contable")]
            elif tipo == "INGRESOS":
                opciones = [("Ingresos Operacionales","Ingresos Operacionales"), ("Ingresos Financieros","Ingresos Financieros")]
            elif tipo == "GASTOS":
                opciones = [("Gastos Operacionales","Gastos Operacionales"), ("Gastos Financieros","Gastos Financieros")]
            else:
                opciones = []
            
            for nombre, valor in opciones:
                tk.Radiobutton(
                    frame_subrubros,
                    text=nombre,
                    variable=subrubro_seleccionado,
                    value=valor,
                    bg=self.parent_app.bg_principal,
                    fg=self.parent_app.color_texto,
                    selectcolor=self.parent_app.bg_principal,
                    font=("Segoe UI", 9),
                    cursor="hand2"
                ).pack(anchor="w", pady=4)
            
            if opciones:
                subrubro_seleccionado.set(opciones[0][1])
        
        tipo_seleccionado.trace("w", actualizar_subrubros)
        
        # ----- PASO 3 -----
        label_paso3 = tk.Label(
            frame_scroll,
            text="Paso 3: Nombre de la Cuenta",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.bg_principal,
            fg=self.parent_app.color_acento
        )
        label_paso3.pack(anchor="w", pady=(10, 5))
        
        entry_nombre = tk.Entry(
            frame_scroll,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            relief="flat"
        )
        entry_nombre.pack(fill="x", ipady=8, pady=(0, 15))
        
        # ----- PASO 4 -----
        label_paso4 = tk.Label(
            frame_scroll,
            text="Paso 4: Valor de la Cuenta",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.bg_principal,
            fg=self.parent_app.color_acento
        )
        label_paso4.pack(anchor="w", pady=(0, 5))
        
        label_ayuda = tk.Label(
            frame_scroll,
            text="💡 Nota: Los gastos deben ser valores negativos. Ejemplo: -1000",
            font=("Segoe UI", 8, "italic"),
            bg=self.parent_app.bg_principal,
            fg="#94a3b8"
        )
        label_ayuda.pack(anchor="w")
        
        entry_valor = tk.Entry(
            frame_scroll,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            relief="flat"
        )
        entry_valor.pack(fill="x", ipady=8, pady=(0, 20))
        
        # ----- BOTONES ABAJO -----
        frame_botones = tk.Frame(ventana_asistente, bg=self.parent_app.bg_principal)
        frame_botones.pack(side="bottom", fill="x", padx=20, pady=15)
        
        botones_inner = tk.Frame(frame_botones, bg=self.parent_app.bg_principal)
        botones_inner.pack(anchor="center")
        
        color_peligro = getattr(self.parent_app, "color_peligro", "#e74c3c")
        color_exito = getattr(self.parent_app, "color_exito", "#2ecc71")
        
        # Cancelar
        tk.Button(
            botones_inner,
            text="✕ Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg=color_peligro,
            fg="white",
            relief="flat",
            pady=10,
            padx=25,
            cursor="hand2",
            command=ventana_asistente.destroy
        ).pack(side="left", padx=(0, 10))
        
        # Agregar
        def agregar_cuenta_nueva():
            tipo = tipo_seleccionado.get()
            subrubro = subrubro_seleccionado.get()
            nombre = entry_nombre.get().strip()
            valor_str = entry_valor.get().strip()
            
            if not (tipo and subrubro and nombre and valor_str):
                messagebox.showwarning("Campos incompletos", "Debes llenar todos los campos.")
                return
            
            try:
                valor = float(valor_str)
            except ValueError:
                messagebox.showerror("Error", "El valor debe ser numérico.")
                return
            
            nombre_normalizado = (
                nombre.replace(" ", "_")
                      .replace("á","a").replace("é","e").replace("í","i")
                      .replace("ó","o").replace("ú","u")
            )
            
            clave = f"{tipo}_{nombre_normalizado}"
            
            datos = {
                "clave": clave,
                "nombre": nombre,
                "tipo": tipo,
                "subrubro": subrubro,
                "valor": valor
            }
            
            if self.callback:
                self.callback(datos)
            
            messagebox.showinfo("Éxito", "Cuenta agregada correctamente.")
            ventana_asistente.destroy()
        
        tk.Button(
            botones_inner,
            text="✔ Agregar",
            font=("Segoe UI", 11, "bold"),
            bg=color_exito,
            fg="white",
            relief="flat",
            pady=10,
            padx=25,
            cursor="hand2",
            command=agregar_cuenta_nueva
        ).pack(side="left")
        
        # Selección inicial
        tipo_seleccionado.set("ACTIVOS")
        actualizar_subrubros()