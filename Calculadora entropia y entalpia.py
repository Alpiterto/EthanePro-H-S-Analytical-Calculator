#!/usr/bin/env python3
"""
GUI optimizada para calcular entalpía/entropía (ideal, residual y total) para etano.
Utiliza integración analítica para las propiedades ideales y añade funcionalidades
mejoradas como copiar con máxima precisión.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import csv

# -----------------------
# Constantes y Parámetros
# -----------------------
R = 8.31446261815324      # J/mol-K
P0_REF = 101300.0         # Pa (Presión de referencia)
T0_REF = 300.0            # K  (Temperatura de referencia)
H0_REF_KJ_PER_KG = 1068.3   # kJ/kg
S0_REF_KJ_PER_KGK = 7.634   # kJ/(kg·K)

M_ETHANE_G_PER_MOL = 30.069
M_ETHANE_KG_PER_MOL = M_ETHANE_G_PER_MOL / 1000.0  # kg/mol

H0_REF_J_PER_MOL = H0_REF_KJ_PER_KG * 1000.0 * M_ETHANE_KG_PER_MOL
S0_REF_J_PER_MOLK = S0_REF_KJ_PER_KGK * 1000.0 * M_ETHANE_KG_PER_MOL

# Propiedades críticas y factor acéntrico para el etano
T_C = 305.3  # K
P_C = 4.9e6  # Pa
OMEGA = 0.100

# Coeficientes para el cálculo de Cp (ya multiplicados por R para eficiencia)
# Cp = A + B*T + C*T^2
CP_A = 1.131 * R
CP_B = 19.225e-3 * R
CP_C = -5.561e-6 * R

# -----------------------
# Funciones Termodinámicas
# -----------------------
def compute_h_ig_molar_analytical(T):
    """Calcula la entalpía ideal molar mediante integración analítica de Cp."""
    integral = (CP_A * (T - T0_REF) +
                (CP_B / 2) * (T**2 - T0_REF**2) +
                (CP_C / 3) * (T**3 - T0_REF**3))
    return H0_REF_J_PER_MOL + integral

def compute_s_ig_molar_analytical(T, P):
    """Calcula la entropía ideal molar mediante integración analítica de Cp/T."""
    if T <= 0: raise ValueError("La temperatura (T) debe ser positiva.")
    if P <= 0: raise ValueError("La presión (P) debe ser positiva.")
    
    integral = (CP_A * math.log(T / T0_REF) +
                CP_B * (T - T0_REF) +
                (CP_C / 2) * (T**2 - T0_REF**2))
    
    log_term = -R * math.log(P / P0_REF)
    return S0_REF_J_PER_MOLK + integral + log_term

def h_r_molar(T, P):
    """Calcula la entalpía residual molar."""
    Tr = T / T_C
    if Tr <= 0: raise ValueError("La temperatura reducida (Tr) debe ser positiva.")
    
    bracket = (0.083 - 1.097 / (Tr**1.6) + OMEGA * (0.139 - 0.894 / (Tr**4.2)))
    return (R * T_C / P_C) * (P - P0_REF) * bracket

def s_r_molar(T, P):
    """Calcula la entropía residual molar."""
    Tr = T / T_C
    if Tr <= 0: raise ValueError("La temperatura reducida (Tr) debe ser positiva.")
    
    bracket = (0.675 / (Tr**2.6) + OMEGA * (0.722 / (Tr**5.2)))
    return - (R / P_C) * (P - P0_REF) * bracket

# -----------------------
# Utilidades
# -----------------------
def parse_pressure_input(s):
    """Parsea la entrada de presión, permitiendo Pa, bar o atm."""
    s = s.strip().lower()
    try:
        if "bar" in s:
            return float(s.replace("bar", "").strip()) * 1e5
        if "atm" in s:
            return float(s.replace("atm", "").strip()) * 101325.0
        return float(s)  # Asume Pa por defecto
    except (ValueError, TypeError):
        raise ValueError("Formato de presión inválido. Use '2e5', '2 bar' o '1.5 atm'.")

def to_kj_per_kg(j_per_mol):
    """Convierte de J/mol a kJ/kg."""
    return (j_per_mol / M_ETHANE_KG_PER_MOL) / 1000.0

# -----------------------
# Clase Principal de la GUI
# -----------------------
class EntropyEnthalpyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de H y S para Etano")
        self.geometry("820x450")
        self.resizable(False, False)

        self.last_results_raw = []
        self.last_T_P = (None, None)

        self._create_widgets()

    def _create_widgets(self):
        """Crea y organiza todos los widgets de la interfaz."""
        # --- Panel de Entradas ---
        frm_inputs = ttk.Frame(self, padding=10)
        frm_inputs.pack(side="top", fill="x")

        ttk.Label(frm_inputs, text="Temperatura T [K]:").grid(row=0, column=0, sticky="e")
        self.entry_T = ttk.Entry(frm_inputs, width=15)
        self.entry_T.grid(row=0, column=1, padx=(5, 20))
        self.entry_T.insert(0, "350")

        ttk.Label(frm_inputs, text="Presión P (Pa, bar, atm):").grid(row=0, column=2, sticky="e")
        self.entry_P = ttk.Entry(frm_inputs, width=20)
        self.entry_P.grid(row=0, column=3, padx=(5, 20))
        self.entry_P.insert(0, "2 bar")

        # --- Botones de Acción ---
        btn_calc = ttk.Button(frm_inputs, text="Calcular", command=self.on_calculate)
        btn_calc.grid(row=0, column=4, padx=5)
        btn_clear = ttk.Button(frm_inputs, text="Limpiar", command=self.on_clear)
        btn_clear.grid(row=0, column=5, padx=5)
        btn_save = ttk.Button(frm_inputs, text="Guardar CSV", command=self.on_save_csv)
        btn_save.grid(row=0, column=6, padx=5)

        # --- Información de Referencia ---
        frm_ref = ttk.Frame(self, padding=(10, 0))
        frm_ref.pack(side="top", fill="x")
        ttk.Label(frm_ref, text=f"Referencia: T₀ = {T0_REF:.1f} K, P₀ = {P0_REF:.1f} Pa").pack(side="left")

        # --- Panel de Condiciones Calculadas ---
        info_frame = ttk.LabelFrame(self, text="Condiciones Calculadas")
        info_frame.pack(side="top", fill="x", padx=10, pady=(10, 5))

        self.T_var = tk.StringVar(value="---")
        self.P_var = tk.StringVar(value="---")

        ttk.Label(info_frame, text="Temperatura (K):").pack(side="left", padx=(10, 2), pady=5)
        ttk.Label(info_frame, textvariable=self.T_var, font=("Arial", 10, "bold")).pack(side="left", padx=(0, 20))
        ttk.Label(info_frame, text="Presión (Pa):").pack(side="left", padx=(10, 2), pady=5)
        ttk.Label(info_frame, textvariable=self.P_var, font=("Arial", 10, "bold")).pack(side="left")

        # --- Tabla de Resultados ---
        columns = ("propiedad", "valor")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("propiedad", text="Propiedad")
        self.tree.heading("valor", text="Valor")
        self.tree.column("propiedad", width=300, anchor="w")
        self.tree.column("valor", width=180, anchor="e")
        self.tree.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))

        # --- Barra de Estado ---
        self.status = ttk.Label(self, text="Listo", relief="sunken", anchor="w", padding=2)
        self.status.pack(side="bottom", fill="x")

        # --- Menú Contextual para Copiar ---
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copiar Valor (Máxima Precisión)", command=self.copy_selected_value)
        self.context_menu.add_command(label="Copiar Fila", command=self.copy_selected_row)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def on_calculate(self):
        """Valida entradas, ejecuta los cálculos y actualiza la GUI."""
        try:
            T = float(self.entry_T.get().strip())
            P = parse_pressure_input(self.entry_P.get().strip())

            if not (298.0 <= T <= 1500.0):
                msg = f"La temperatura T = {T:.1f} K está fuera del rango de validez (298-1500 K).\n¿Desea continuar de todos modos?"
                if not messagebox.askyesno("Advertencia de Rango", msg):
                    return
            
            # --- Lógica de Cálculo ---
            H_ig_molar = compute_h_ig_molar_analytical(T)
            S_ig_molar = compute_s_ig_molar_analytical(T, P)
            H_r_val = h_r_molar(T, P)
            s_r_val = s_r_molar(T, P)
            
            H_total_molar = H_ig_molar + H_r_val
            s_total_molar = S_ig_molar + s_r_val

            # Guardar resultados con máxima precisión
            self.last_results_raw = [
                ("Entalpía Ideal (kJ/kg)", to_kj_per_kg(H_ig_molar)),
                ("Entalpía Residual (kJ/kg)", to_kj_per_kg(H_r_val)),
                ("Entalpía Total (kJ/kg)", to_kj_per_kg(H_total_molar)),
                ("Entropía Ideal (kJ/kg·K)", to_kj_per_kg(S_ig_molar)),
                ("Entropía Residual (kJ/kg·K)", to_kj_per_kg(s_r_val)),
                ("Entropía Total (kJ/kg·K)", to_kj_per_kg(s_total_molar)),
            ]
            self.last_T_P = (T, P)

            # --- Actualización de la GUI ---
            self.update_display()
            self.status.config(text=f"Cálculo completado para T={T:.2f} K, P={P:.2e} Pa.")

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error durante el cálculo:\n{e}")

    def update_display(self):
        """Actualiza la tabla y los labels con los últimos resultados calculados."""
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Formatear y mostrar resultados
        rows_display = [(prop, f"{valor:.5f}") for prop, valor in self.last_results_raw]
        for r in rows_display:
            self.tree.insert("", "end", values=r)
        
        T, P = self.last_T_P
        self.T_var.set(f"{T:.2f}")
        self.P_var.set(f"{P:.2e}")

    def on_clear(self):
        """Limpia la tabla de resultados, los labels y los datos almacenados."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.status.config(text="Tabla limpiada.")
        self.last_results_raw = []
        self.last_T_P = (None, None)
        self.T_var.set("---")
        self.P_var.set("---")

    def on_save_csv(self):
        """Guarda los últimos resultados calculados en un archivo CSV."""
        if not self.last_results_raw:
            messagebox.showinfo("Guardar CSV", "No hay resultados para guardar. Ejecute 'Calcular' primero.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not path: return

        T_val, P_val_pa = self.last_T_P
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Propiedad", "Valor", "Temperatura (K)", "Presión (Pa)"])
            for propiedad, valor in self.last_results_raw:
                writer.writerow([propiedad, f"{valor:.8f}", f"{T_val:.4f}", f"{P_val_pa:.4e}"])
        messagebox.showinfo("Guardar CSV", f"Resultados guardados en:\n{path}")

    def show_context_menu(self, event):
        """Muestra el menú contextual al hacer clic derecho en la tabla."""
        if self.tree.identify_row(event.y):
            self.tree.focus(self.tree.identify_row(event.y)) # Selecciona la fila
            self.context_menu.post(event.x_root, event.y_root)

    def _copy_to_clipboard(self, content):
        """Helper para copiar contenido al portapapeles."""
        self.clipboard_clear()
        self.clipboard_append(str(content))
        self.update()

    def copy_selected_value(self):
        """Copia el valor numérico con máxima precisión de la fila seleccionada."""
        selected_item = self.tree.focus()
        if not selected_item: return
        
        prop_name = self.tree.item(selected_item, 'values')[0]
        for prop, val in self.last_results_raw:
            if prop == prop_name:
                self._copy_to_clipboard(val)
                self.status.config(text=f"Valor '{val}' copiado al portapapeles.")
                break

    def copy_selected_row(self):
        """Copia la propiedad y su valor (máxima precisión) de la fila seleccionada."""
        selected_item = self.tree.focus()
        if not selected_item: return

        prop_name = self.tree.item(selected_item, 'values')[0]
        for prop, val in self.last_results_raw:
            if prop == prop_name:
                row_data = f"{prop}\t{val}"  # Separado por tabulador
                self._copy_to_clipboard(row_data)
                self.status.config(text=f"Fila '{prop}' copiada al portapapeles.")
                break

# -----------------------
# Punto de Entrada Principal
# -----------------------
if __name__ == "__main__":
    try:
        app = EntropyEnthalpyApp()
        app.mainloop()
    except tk.TclError:
        print("No se pudo iniciar la GUI. Asegúrese de ejecutar este script en un entorno con soporte gráfico.")


     