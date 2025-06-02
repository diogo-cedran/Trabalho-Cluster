import math
from typing import List, Optional

class Elemento:
    def __init__(self, nome: str, atributos: List[float]):
        self.nome = nome
        self.atributos = atributos
        self.is_centroide = False

    def __repr__(self):
        flag = " (Centroide)" if self.is_centroide else ""
        return f"{self.nome}: {self.atributos}{flag}"

class Cluster:
    def __init__(self, id_cluster: int):
        self.id = id_cluster
        self.elementos: List[Elemento] = []
        self.centroide: Optional[Elemento] = None

    def adicionar_elemento(self, elemento: Elemento):
        self.elementos.append(elemento)
        self.atualizar_centroide()

    def atualizar_centroide(self):
        if not self.elementos:
            self.centroide = None
            return

        for elem in self.elementos:
            elem.is_centroide = False

        num_atributos = len(self.elementos[0].atributos)
        soma = [0.0] * num_atributos
        for elem in self.elementos:
            for i in range(num_atributos):
                soma[i] += elem.atributos[i]

        media = [x / len(self.elementos) for x in soma]

        self.centroide = Elemento(f"Centroide_{self.id}", media)
        self.centroide.is_centroide = True

    def __repr__(self):
        return f"Cluster {self.id} - Centroide: {self.centroide}\nElementos:\n" + "\n".join(str(e) for e in self.elementos)

def distancia_euclidiana(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

class KMeans:
    def __init__(self):
        self.clusters: List[Cluster] = []

    def inicializar_clusters(self, elementos_iniciais: List[Elemento]):
        self.clusters = []
        for idx, elem in enumerate(elementos_iniciais, start=1):
            cluster = Cluster(idx)
            cluster.adicionar_elemento(elem)
            self.clusters.append(cluster)

    def adicionar_elemento(self, novo_elemento: Elemento):
        distancias = []
        for cluster in self.clusters:
            if cluster.centroide is None:
                dist = float('inf')
            else:
                dist = distancia_euclidiana(novo_elemento.atributos, cluster.centroide.atributos)
            distancias.append((dist, cluster))

        dist_min, cluster_mais_proximo = min(distancias, key=lambda x: x[0])

        cluster_mais_proximo.adicionar_elemento(novo_elemento)

        return cluster_mais_proximo.id

if __name__ == "__main__":
    elem1 = Elemento("Elem1", [1.0, 2.0])
    elem2 = Elemento("Elem2", [5.0, 6.0])

    kmeans = KMeans()
    kmeans.inicializar_clusters([elem1, elem2])

    novo = Elemento("NovoElem", [2.0, 3.0])
    id_cluster = kmeans.adicionar_elemento(novo)

    for c in kmeans.clusters:
        print(c)
