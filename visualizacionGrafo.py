import pandas as pd
import networkx as nx
from pyvis.network import Network
import random

df = pd.read_csv("resultados.csv")

categorias_validas = ["real-world-assets-rwa", "meme-token", "gaming"]
df = df[df["categoria"].isin(categorias_validas)]

if len(df) < 1000:
    raise ValueError(f"Se requieren al menos 1000 proyectos, pero solo hay {len(df)}.")

G = nx.Graph()

for _, row in df.iterrows():
    G.add_node(
        row["nombre"],
        categoria=row["categoria"],
        market_cap=row["market_cap"],
        valor_usd=row["valor_usd"]
    )

nodos = list(G.nodes())
for node in nodos:
    categoria_node = G.nodes[node]['categoria']
    vecinos_posibles = [n for n in nodos if n != node and G.nodes[n]['categoria'] == categoria_node]
    if len(vecinos_posibles) >= 5:
        conexiones = random.sample(vecinos_posibles, k=random.randint(3, 6))
        for conn in conexiones:
            G.add_edge(node, conn)

net = Network(height="750px", width="100%", bgcolor="#111111", font_color="white")

color_map = {
    "AI": "#FF6F61",
    "Videojuego": "#6B5B95",
    "RWA": "#88B04B",
    "Memes": "#F7CAC9"
}

for node, data in G.nodes(data=True):
    label = node
    title = f"Categoría: {data['categoria']}<br>Valor USD: {data['valor_usd']}<br>Market Cap: {data['market_cap']}"
    color = color_map.get(data['categoria'], "#CCCCCC")
    net.add_node(node, label=label, title=title, color=color)

for source, target in G.edges():
    net.add_edge(source, target)

output_file = "red_criptomonedas.html"
net.save_graph(output_file)
print(f"Archivo generado correctamente: {output_file}")