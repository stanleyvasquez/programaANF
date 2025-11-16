import tkinter as tk
from tkinter import messagebox, ttk

class AgregarCuenta:
    def __init__(self, parent_app, callback=None):
        self.parent_app = parent_app
        self.callback = callback  # añadido callback para devolver datos
        
    def abrir_ventana(self):
        """Abre el asistente interactivo para agregar cuentas"""
        ventana_asistente = tk.Toplevel(self.parent_app.root)
        ventana_asistente.title("Agregar Cuenta Personalizada")
        ventana_asistente.geometry("600x700")
        ventana_asistente.config(bg=self.parent_app.bg_principal)
        ventana_asistente.resizable(False, False)
        
        # Centrar ventana
        ventana_asistente.update_idletasks()
        x = (ventana_asistente.winfo_screenwidth() // 2) - (300)
        y = (ventana_asistente.winfo_screenheight() // 2) - (350)
        ventana_asistente.geometry(f'600x700+{x}+{y}')
        
        # Header
        frame_header = tk.Frame(ventana_asistente, bg=self.parent_app.bg_secundario, height=60)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)
        
        titulo = tk.Label(
            frame_header,
            text="➕ Agregar Cuenta Personalizada",
            font=("Segoe UI", 16, "bold"),
            bg=self.parent_app.bg_secundario,
            fg=self.parent_app.color_texto
        )
        titulo.pack(pady=10)
        
        # Frame con scroll
        canvas = tk.Canvas(ventana_asistente, bg=self.parent_app.bg_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_asistente, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.parent_app.bg_principal)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        scrollbar.pack(side="right", fill="y")
        
        # Paso 1: Seleccionar tipo de cuenta
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
            {"nombre": "🏦 ACTIVOS", "tipo": "ACTIVOS", "color": "#3498db"},
            {"nombre": "💳 PASIVOS", "tipo": "PASIVOS", "color": "#e74c3c"},
            {"nombre": "💰 PATRIMONIO", "tipo": "PATRIMONIO", "color": "#2ecc71"}
        ]
        
        tipo_seleccionado = tk.StringVar()
        
        for tipo_info in tipos_cuenta:
            radio_btn = tk.Radiobutton(
                frame_tipos,
                text=tipo_info["nombre"],
                variable=tipo_seleccionado,
                value=tipo_info["tipo"],
                bg=self.parent_app.bg_principal,
                fg=self.parent_app.color_texto,
                selectcolor=self.parent_app.bg_principal,
                activebackground=self.parent_app.bg_principal,
                activeforeground=self.parent_app.color_texto,
                font=("Segoe UI", 10),
                cursor="hand2",
                highlightthickness=0
            )
            radio_btn.pack(anchor="w", pady=5)
        
        # Paso 2: Seleccionar subrubro
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
        
        def actualizar_subrubros():
            # Limpiar los radiobuttons previos
            for widget in frame_subrubros.winfo_children():
                widget.destroy()
            
            tipo = tipo_seleccionado.get()
            
            if tipo == "ACTIVOS":
                opciones = [
                    ("Activo Corriente", "Activo Corriente"),
                    ("Activo No Corriente", "Activo No Corriente")
                ]
            elif tipo == "PASIVOS":
                opciones = [
                    ("Pasivo Corriente", "Pasivo Corriente"),
                    ("Pasivo No Corriente", "Pasivo No Corriente")
                ]
            elif tipo == "PATRIMONIO":
                opciones = [("Capital Contable", "Capital Contable")]
            else:
                opciones = []
            
            for opcion_nombre, opcion_valor in opciones:
                radio_btn = tk.Radiobutton(
                    frame_subrubros,
                    text=opcion_nombre,
                    variable=subrubro_seleccionado,
                    value=opcion_valor,
                    bg=self.parent_app.bg_principal,
                    fg=self.parent_app.color_texto,
                    selectcolor=self.parent_app.bg_principal,
                    activebackground=self.parent_app.bg_principal,
                    activeforeground=self.parent_app.color_texto,
                    font=("Segoe UI", 9),
                    cursor="hand2",
                    highlightthickness=0
                )
                radio_btn.pack(anchor="w", pady=4)
            
            if opciones:
                subrubro_seleccionado.set(opciones[0][1])
        
        tipo_seleccionado.trace("w", lambda *args: actualizar_subrubros())
        
        # Paso 3: Nombre de la cuenta
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
            insertbackground="white",
            relief="flat"
        )
        entry_nombre.pack(fill="x", ipady=8, pady=(0, 15))
        entry_nombre.focus()
        
        # Paso 4: Valor de la cuenta
        label_paso4 = tk.Label(
            frame_scroll,
            text="Paso 4: Valor de la Cuenta",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.bg_principal,
            fg=self.parent_app.color_acento
        )
        label_paso4.pack(anchor="w", pady=(0, 5))
        
        entry_valor = tk.Entry(
            frame_scroll,
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        entry_valor.pack(fill="x", ipady=8, pady=(0, 20))
        
        # Frame de botones
        frame_botones = tk.Frame(ventana_asistente, bg=self.parent_app.bg_principal)
        frame_botones.pack(fill="x", padx=20, pady=15)
        
        def agregar_cuenta_nueva():
            tipo = tipo_seleccionado.get()
            subrubro = subrubro_seleccionado.get()
            nombre = entry_nombre.get().strip()
            valor_str = entry_valor.get().strip()
            
            # Validaciones
            if not tipo:
                messagebox.showwarning("Campo Requerido", "Por favor selecciona un tipo de cuenta")
                return
            
            if not subrubro:
                messagebox.showwarning("Campo Requerido", "Por favor selecciona una clasificación")
                return
            
            if not nombre:
                messagebox.showwarning("Campo Requerido", "Por favor ingresa el nombre de la cuenta")
                return
            
            if not valor_str:
                messagebox.showwarning("Campo Requerido", "Por favor ingresa el valor de la cuenta")
                return
            
            try:
                valor = float(valor_str)
            except ValueError:
                messagebox.showerror("Valor Inválido", "El valor debe ser un número válido")
                return
            
            nombre_normalizado = nombre.replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            clave = f"{tipo}_{nombre_normalizado}"
            
            datos_cuenta = {
                "clave": clave,
                "nombre": nombre,
                "tipo": tipo,
                "subrubro": subrubro,
                "valor": valor
            }
            
            if self.callback:
                self.callback(datos_cuenta)
            
            messagebox.showinfo(
                "Cuenta Agregada",
                f"Cuenta agregada exitosamente:\n\n"
                f"Tipo: {tipo}\n"
                f"Clasificación: {subrubro}\n"
                f"Nombre: {nombre}\n"
                f"Valor: ${valor:,.2f}\n\n"
                f"Se guardará cuando guardes los datos financieros"
            )
            ventana_asistente.destroy()
        
        btn_agregar = tk.Button(
            frame_botones,
            text="✓ Agregar Cuenta",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.color_exito,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10,
            activebackground="#2d8f5a",
            command=agregar_cuenta_nueva
        )
        btn_agregar.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_cancelar = tk.Button(
            frame_botones,
            text="✕ Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg=self.parent_app.color_peligro,
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=30,
            pady=10,
            activebackground="#c23850",
            command=ventana_asistente.destroy
        )
        btn_cancelar.pack(side="right", padx=10, expand=True, fill="x")
        
        tipo_seleccionado.set("ACTIVOS")
        actualizar_subrubros()
