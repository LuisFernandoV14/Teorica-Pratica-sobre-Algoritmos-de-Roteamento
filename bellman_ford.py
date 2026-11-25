#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Questão 4 - Algoritmo de Bellman-Ford (Vetor de Distâncias) aplicado a roteadores.

Cada roteador conhece apenas o custo até os vizinhos diretos. A cada rodada,
todos os roteadores enviam seu vetor de distâncias aos vizinhos, e cada um
recalcula:  D_x(y) = min sobre vizinhos v de { c(x,v) + D_v(y) }
O processo termina quando nenhum vetor muda (convergência).
"""

INF = float("inf")

# ---------------- Topologia (5 roteadores, cada um com >= 2 enlaces) ----------------
#
#            4            5
#       A ------- B ------------ D
#        \       /               / \
#       2 \     / 1             /   \ 2
#          \   /               / 8   \
#            C ---------------       E
#             \_____________________/
#                       10
#
LINKS = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2),
]

NODES = sorted({n for l in LINKS for n in l[:2]})

# custo direto entre vizinhos
cost = {n: {} for n in NODES}
for a, b, c in LINKS:
    cost[a][b] = c
    cost[b][a] = c


def mostrar_tabela(titulo, dist, nxt):
    print(f"\n--- {titulo} ---")
    print("Roteador | " + " | ".join(f"{d:>7}" for d in NODES))
    for n in NODES:
        linha = []
        for d in NODES:
            v = dist[n][d]
            if v == INF:
                linha.append(f"{'inf':>7}")
            elif n == d:
                linha.append(f"{'0':>7}")
            else:
                linha.append(f"{str(v) + '/' + nxt[n][d]:>7}")
        print(f"   {n}     | " + " | ".join(linha))
    print("(formato: custo/próximo salto)")


def bellman_ford_distance_vector():
    # --- Inicialização: cada nó só conhece a si mesmo (0) e seus vizinhos diretos
    dist = {n: {d: INF for d in NODES} for n in NODES}
    nxt = {n: {d: "-" for d in NODES} for n in NODES}
    for n in NODES:
        dist[n][n] = 0
        for v, c in cost[n].items():
            dist[n][v] = c
            nxt[n][v] = v

    mostrar_tabela("Tabelas INICIAIS (rodada 0)", dist, nxt)

    rodada = 0
    while True:
        rodada += 1
        mudou = False
        # Cópia: todos os nós usam os vetores recebidos na rodada anterior
        # (troca síncrona de vetores de distância).
        antigo = {n: dict(dist[n]) for n in NODES}
        for x in NODES:
            for y in NODES:
                if x == y:
                    continue
                # Equação de Bellman-Ford: minimiza sobre todos os vizinhos v
                for v, c_xv in cost[x].items():
                    novo = c_xv + antigo[v][y]
                    if novo < dist[x][y]:
                        dist[x][y] = novo
                        nxt[x][y] = v  # próximo salto passa a ser o vizinho v
                        mudou = True
        mostrar_tabela(f"Após rodada {rodada}", dist, nxt)
        if not mudou:
            print(f"\nConvergiu: nenhuma alteração na rodada {rodada}.")
            break
    return dist, nxt


def caminho(nxt, origem, destino):
    """Reconstrói o caminho seguindo os próximos saltos."""
    p = [origem]
    atual = origem
    while atual != destino:
        atual = nxt[atual][destino]
        p.append(atual)
    return " -> ".join(p)


if __name__ == "__main__":
    print("=== TOPOLOGIA E CUSTOS INICIAIS (enlaces) ===")
    for a, b, c in LINKS:
        print(f"  {a} <-> {b} : custo {c}")
    print("\nEnlaces por roteador:")
    for n in NODES:
        print(f"  {n}: " + ", ".join(f"{v}({c})" for v, c in sorted(cost[n].items())))

    dist, nxt = bellman_ford_distance_vector()

    print("\n=== RESULTADO FINAL: melhores caminhos de cada roteador ===")
    for o in NODES:
        for d in NODES:
            if o != d:
                print(f"  {o} -> {d}: custo {dist[o][d]:>2} | caminho: {caminho(nxt, o, d)}")
