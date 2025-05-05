# Práctica Calificada 2 - Análisis de criptomonedas con redes complejas

Este proyecto explora el mercado de criptomonedas desde el enfoque de **redes complejas**, utilizando datos reales recolectados de CoinMarketCap y CoinGecko. Se representan gráficamente proyectos clasificados como *Gaming*, *RWA* (Real World Assets) y *Meme tokens*.

---

## 🔧 Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.8 o superior
- Las siguientes librerías:

```pip install pandas networkx pyvis```

## ▶️ Ejecución del código
1. Descarga o clona este repositorio:
```
git clone https://github.com/USUARIO/PC2.git
cd PC2
```
2. Asegúrate de que el archivo resultados.csv esté dentro de la carpeta PC2.
3. Ejecuta el script en Python:
```python visualizacionGrafo.py```
4. Esto generará un archivo llamado ```red_criptomonedas.html```

## 🌐 Visualización de la red
Una vez generado el archivo red_criptomonedas.html, puedes abrirlo fácilmente en tu navegador web. Solo haz doble clic sobre el archivo, o ábrelo manualmente desde tu navegador favorito.
El grafo permite explorar interactivamente las relaciones entre proyectos según su categoría.

## 📁 Archivos principales
- resultados.csv → Datos recolectados de CoinMarketCap / CoinGecko
- visualizacionGrafo.py → Script de Python para construir y visualizar la red.
- red_criptomonedas.html → Visualización interactiva de la red.

### 💡 Notas
Asegúrate de tener al menos 1000 proyectos para cumplir con los requisitos de análisis.
Las conexiones entre nodos se realizan dentro de la misma categoría para reflejar similitudes funcionales.
