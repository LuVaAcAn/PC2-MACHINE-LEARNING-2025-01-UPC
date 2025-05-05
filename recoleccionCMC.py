import requests
import time
import csv

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1"
CMC_API_KEY = "ae09f3af-d239-489c-85e4-0802d71182ab"

HEADERS_CMC = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
}

CATEGORIAS = ['real-world-assets-rwa', 'meme-token', 'gaming']
NODOS_OBJETIVO = 1000
MAX_POR_PAGINA = 100  # CoinGecko permite hasta 250 pero vamos con 100 para estabilidad

def obtener_monedas_por_categoria(category_id, max_nodos_categoria):
    monedas_categoria = []
    pagina = 1

    while len(monedas_categoria) < max_nodos_categoria:
        url = f"{COINGECKO_BASE_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "category": category_id,
            "order": "market_cap_desc",
            "per_page": MAX_POR_PAGINA,
            "page": pagina,
            "sparkline": False
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            datos = response.json()
            if not datos:
                break  # No más datos
            monedas_categoria.extend(datos)
            pagina += 1
            time.sleep(1)
        else:
            print(f"❌ Error al obtener {category_id} página {pagina}: {response.status_code}")
            break

    return monedas_categoria[:max_nodos_categoria]

def obtener_datos_avanzados(symbol):
    url = f"{CMC_BASE_URL}/cryptocurrency/quotes/latest"
    params = {"symbol": symbol}

    response = requests.get(url, headers=HEADERS_CMC, params=params)
    if response.status_code == 200:
        data = response.json()
        if symbol in data["data"]:
            return data["data"][symbol]
    return None

def calcular_metricas(datos_cmc):
    if not datos_cmc:
        return None

    quote = datos_cmc["quote"]["USD"]
    volumen = quote.get("volume_24h", 0)
    market_cap = quote.get("market_cap")

    if volumen is None or market_cap is None or market_cap == 0:
        volumen_marketcap_ratio = None
    else:
        volumen_marketcap_ratio = volumen / market_cap

    return {
        "valor_usd": quote.get("price"),
        "market_cap": market_cap,
        "ranking": datos_cmc.get("cmc_rank"),
        "volumen_24h": volumen,
        "volumen/marketcap": volumen_marketcap_ratio,
        "circulating_supply": datos_cmc.get("circulating_supply"),
        "total_supply": datos_cmc.get("total_supply"),
        "max_supply": datos_cmc.get("max_supply"),
        "multichain": datos_cmc.get("platform") is not None,
        "exchanges": datos_cmc.get("num_market_pairs"),
        "pagina_web": "; ".join(datos_cmc.get("urls", {}).get("website", [])),
        "contrato": datos_cmc.get("platform", {}).get("token_address") if datos_cmc.get("platform") else None,
    }

def exportar_a_csv(nombre_archivo, datos):
    if not datos:
        print("⚠️ No hay datos para exportar.")
        return

    campos = datos[0].keys()
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)
    print(f"✅ Datos exportados exitosamente en '{nombre_archivo}'")

def analizar_proyectos():
    resultados = []
    nodos_por_categoria = NODOS_OBJETIVO // len(CATEGORIAS)

    for categoria in CATEGORIAS:
        print(f"\n🔍 Analizando categoría: {categoria.upper()}")
        monedas = obtener_monedas_por_categoria(categoria, nodos_por_categoria)

        for moneda in monedas:
            nombre = moneda['name']
            symbol = moneda['symbol'].upper()
            print(f"→ {nombre} ({symbol})")

            datos_cmc = obtener_datos_avanzados(symbol)
            time.sleep(2)  # evitar limitaciones de la API

            metricas = calcular_metricas(datos_cmc)
            if metricas:
                resultados.append({
                    "nombre": nombre,
                    "symbol": symbol,
                    "categoria": categoria,
                    **metricas
                })

    return resultados

if __name__ == "__main__":
    datos_finales = analizar_proyectos()
    print(f"\n📊 RESULTADOS ({len(datos_finales)} proyectos):")
    for proyecto in datos_finales:
        print(proyecto)

    exportar_a_csv("resultados.csv", datos_finales)