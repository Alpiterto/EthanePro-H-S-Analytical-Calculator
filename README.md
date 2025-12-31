# ⚗️ EthanePro: Analytical Enthalpy & Entropy Calculator

![Python](https://img.shields.io/badge/Python-3.x-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Physics](https://img.shields.io/badge/Thermodynamics-Analytical%20Integration-red)

**[English]**
A lightweight, high-precision desktop tool to calculate the thermodynamic properties (**Enthalpy $H$** and **Entropy $S$**) of **Ethane ($C_2H_6$)**. Unlike approximation methods, this tool uses **analytical integration** of the Heat Capacity ($C_p$) polynomial for Ideal Gas properties and Pitzer correlations for Residual properties.

**[Español]**
Una herramienta de escritorio ligera y de alta precisión para calcular propiedades termodinámicas (**Entalpía $H$** y **Entropía $S$**) del **Etano ($C_2H_6$)**. A diferencia de los métodos de aproximación, esta herramienta utiliza **integración analítica** del polinomio de Capacidad Calorífica ($C_p$) para las propiedades de Gas Ideal y correlaciones de Pitzer para las propiedades Residuales.

---

## ⚡ Key Features / Características Principales

### 🇬🇧 English
* **Analytical Precision:** Exact calculation of $\Delta H^{ig}$ and $\Delta S^{ig}$ using polynomial integration (no numerical errors).
* **Residual Properties:** Calculates deviations from ideal behavior ($H^R, S^R$) using critical properties ($T_c, P_c, \omega$).
* **Flexible Inputs:** Accepts pressure in **Pa, bar, or atm**.
* **Data Export:**
    * Export results to **CSV**.
    * Context menu (Right-Click) to **copy values** with maximum floating-point precision to clipboard.
* **Zero Dependencies:** Runs on standard Python (uses built-in `tkinter`).

### 🇪🇸 Español
* **Precisión Analítica:** Cálculo exacto de $\Delta H^{ig}$ y $\Delta S^{ig}$ usando integración de polinomios (sin errores numéricos).
* **Propiedades Residuales:** Calcula desviaciones del comportamiento ideal ($H^R, S^R$) usando propiedades críticas ($T_c, P_c, \omega$).
* **Entradas Flexibles:** Acepta presión en **Pa, bar, o atm**.
* **Exportación de Datos:**
    * Exportar resultados a **CSV**.
    * Menú contextual (Click Derecho) para **copiar valores** con máxima precisión de punto flotante al portapapeles.
* **Cero Dependencias:** Funciona con Python estándar (usa el `tkinter` nativo).

---

## 📉 Thermodynamics / Termodinámica

The software calculates total properties using the relation:
El software calcula las propiedades totales usando la relación:

$$H_{total} = H^{ig}(T) + H^R(T, P)$$
$$S_{total} = S^{ig}(T, P) + S^R(T, P)$$



Where ideal gas properties are derived from:
Donde las propiedades de gas ideal se derivan de:
$$C_p^{ig} = A + BT + CT^2$$

---

## 📦 Installation / Instalación

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/TU_USUARIO/EthanePro-Calc.git](https://github.com/TU_USUARIO/EthanePro-Calc.git)
    cd EthanePro-Calc
    ```

2.  **Run the application:**
    *(No external libraries required / No requiere librerías externas)*
    ```bash
    python main.py
    ```

*Note for Linux users: You might need to install `python3-tk` if it's not included in your distro.*

---

## 🖼️ Screenshots

*(Add a screenshot of the app here)*

---

**Author:** [Tu Nombre]
**Reference State:** $T_0 = 300 K$, $P_0 = 101.3 kPa$
