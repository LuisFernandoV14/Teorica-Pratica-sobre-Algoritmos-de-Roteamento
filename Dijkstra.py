#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Questão 5 - Algoritmo de Dijkstra (Estado de Enlace) aplicado a roteadores.

Cada roteador conhece a topologia COMPLETA (via LSAs/inundação) e calcula
localmente o caminho de custo mínimo até todos os outros.

Passos:
  1. D(origem)=0, D(v)=custo direto se vizinho, senão infinito. N' = {origem}
  2. Escolhe w fora de N' com menor D(w) e o adiciona a N'
  3. Para cada vizinho v de w fora de N': D(v) = min(D(v), D(w) + c(w,v))
  4. Repete até N' conter todos os nós
"""

import heapq

INF = float("inf")

# Mesma topologia da questão 4 (5 roteadores, cada um com >= 2 enlaces)
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
graph = {n: {} for n in NODES}
for a, b, c in LINKS:
    graph[a][b] = c
    graph[b][a] = c


def dijkstra(origem, verbose=False):
    D = {n: INF for n in NODES}
    p = {n: "-" for n in NODES}
    D[origem] = 0
    for v, c in graph[origem].items():
        D[v] = c
        p[v] = origem
    Np = {origem}
    fila = []  # só para escolher o mínimo; usamos varredura simples abaixo

    if verbose:
        print(f"\nDijkstra a partir de {origem}")
        cab = "Passo | N'".ljust(22) + "".join(f"D({n}),p({n})".ljust(12) for n in NODES if n != origem)
        print(cab)

    def linha(passo):
        s = f"{passo:<5} | {''.join(sorted(Np))}".ljust(22)
        for n in NODES:
            if n == origem:
                continue
            if n in Np:
                s += "-".ljust(12)
            else:
                val = "inf" if D[n] == INF else f"{D[n]},{p[n]}"
                s += val.ljust(12)
        print(s)

    passo = 0
    if verbose:
        linha(passo)

    while len(Np) < len(NODES):
        # escolhe w não visitado com menor D(w)
        w = min((n for n in NODES if n not in Np), key=lambda n: (D[n], n))
        Np.add(w)
        # relaxa as arestas de w
        for v, c in graph[w].items():
            if v not in Np and D[w] + c < D[v]:
                D[v] = D[w] + c
                p[v] = w
        passo += 1
        if verbose:
            linha(passo)
    return D, p


def caminho(p, origem, destino):
    c = [destino]
    while c[-1] != origem:
        c.append(p[c[-1]])
    return " -> ".join(reversed(c))


if __name__ == "__main__":
    print("=== TOPOLOGIA E CUSTOS INICIAIS ===")
    for a, b, c in LINKS:
        print(f"  {a} <-> {b} : custo {c}")

    # Passo a passo apenas para o roteador A
    dijkstra("A", verbose=True)

    print("\n=== RESULTADO FINAL: tabela de roteamento de cada roteador ===")
    for o in NODES:
        D, p = dijkstra(o)
        print(f"\nRoteador {o}:")
        for d in NODES:
            if d != o:
                print(f"  -> {d}: custo {D[d]:>2} | caminho: {caminho(p, o, d)}")
