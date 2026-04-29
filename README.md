# Dinastía de Bajo Costo: NFL Storytelling 🏈

| *Bruno Gael Ramos Huerta - Lic. IIA* 

**Enlace a la aplicación en vivo:** [LINK DE STREAMLIT COMMUNITY CLOUD]

## Descripción del Proyecto
Este proyecto de *Data Storytelling* analiza la reestructuración financiera y táctica de los Kansas City Chiefs tras la salida del receptor estrella Tyreek Hill en 2022. A través de visualizaciones interactivas, se demuestra cómo la ofensiva comandada por Andy Reid y Patrick Mahomes logró ganar campeonatos consecutivos optimizando el tope salarial y distribuyendo el balón mediante un esquema basado en la eficiencia, demostrando que el gasto de élite en receptores no es un requisito para construir una dinastía en la NFL moderna.

---

## Parte 1: Obtención y Preparación de los Datos (Fuentes)

Para la elaboración de este artículo se utilizaron tres fuentes principales de datos. Todos los procesos de extracción, limpieza y transformación (manejo de nulos, normalización y cruces) se encuentran documentados y son reproducibles en el archivo `01_extraccion_limpieza.ipynb`.

### 1. Datos de Juego (Play-by-Play) y Rosters Oficiales
* **URL / Herramienta:** Librería oficial de Python `nfl_data_py` (https://pypi.org/project/nfl-data-py/)
* **Fecha de descarga:** Abril de 2026
* **Formato original:** DataFrame de Pandas / CSV
* **Condiciones de uso:** Datos públicos de uso educativo y analítico, sin fines comerciales.
* **Descripción:** Se procesaron jugadas de pase y estadísticas avanzadas como *Air Yards* y *Expected Points Added (EPA)* de las temporadas 2018 a 2023.

### 2. Datos Financieros (Positional Spending / Cap Hit) - Spotrac
* **URL exacta:** [https://www.spotrac.com/nfl/position/wide-receiver/_/year/2022/table/active/sort/cap_total](https://www.spotrac.com/nfl/position/wide-receiver/_/year/2022/table/active/sort/cap_total)
* **Fecha de consulta/descarga:** Abril de 2026
* **Formato original:** Tablas web (HTML) estructuradas / CSV manual.
* **Condiciones de uso y licencia:** Spotrac opera en asociación con USA TODAY Sports Media Group y declara no estar afiliado directamente a la NFL. Los datos se utilizan bajo la doctrina de *Fair Use* (Uso Justo) con fines estrictamente académicos y periodísticos, sin fines de lucro.

### 3. Histórico de Inversión Salarial - Over The Cap (OTC)
* **URL exacta:** [https://overthecap.com/position/wide-receiver](https://overthecap.com/position/wide-receiver)
* **Fecha de consulta/descarga:** Abril de 2026
* **Formato original:** Tablas web (HTML) y archivos PDF.
* **Condiciones de uso y licencia:** OTC declara ser un sitio web independiente no afiliado a la NFL ni a la NFLPA. Su uso en este repositorio es puramente referencial, educativo y protegido bajo *Fair Use*.

---

## Instrucciones para ejecutar localmente

Para reproducir este proyecto en tu entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
```bash
git clone [ENLACE_AL_REPOSITORIO_DE_GITHUB]
cd [NOMBRE_DE_LA_CARPETA]
```


2. **Crear un entorno virtual e instalar dependencias:**
Se recomienda usar un entorno virtual. Las librerías necesarias están en *requirements.txt*.

```bash
pip install -r requirements.txt
```

***(Asegúrate de que tu requirements.txt incluya: streamlit, pandas, plotly, numpy, nfl_data_py)***

3. **Ejecutar el Notebook de extracción (Opcional):**
Si deseas ver cómo se limpiaron los datos desde cero, ejecuta todas las celdas de *01_extraccion_limpieza.ipynb*. Esto generará los archivos limpios en la carpeta *data/processed/*.

4. **Correr la aplicación de Streamlit:**
```bash
streamlit run app.py
```
