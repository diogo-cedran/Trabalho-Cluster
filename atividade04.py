import math
from typing import List, Optional, Tuple

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

    def remover_elemento(self, elemento: Elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
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

    def dispersao(self) -> List[Tuple[Elemento, float]]:
        """
        Retorna lista de tuplas (elemento, distância do centróide)
        """
        if not self.centroide:
            return []
        return [(elem, euclidiana(elem.atributos, self.centroide.atributos)) for elem in self.elementos]

    def __repr__(self):
        return f"Cluster {self.id} - Centroide: {self.centroide}\nElementos:\n" + "\n".join(str(e) for e in self.elementos)

def euclidiana(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

class GerenciadorClusters:
    def __init__(self, limiar: float, k: int):
        self.clusters: List[Cluster] = []
        self.limiar = limiar
        self.k = k
        self.proximo_id = 1

    def adicionar_cluster(self, cluster: Cluster):
        self.clusters.append(cluster)
        self.proximo_id = max(self.proximo_id, cluster.id + 1)

    def analisar_e_criar_novos(self):
        """
        Analisa dispersão e cria novos clusters retirando elementos muito distantes
        dos seus centróides originais e que estejam mais próximos de outro cluster.
        """
        elementos_para_novos_clusters = []

        for cluster in self.clusters:
            dispersoes = cluster.dispersao()
            distantes = [item for item in dispersoes if item[1] > self.limiar]
            distantes.sort(key=lambda x: x[1], reverse=True)

            selecionados = distantes[:self.k]

            for elem, dist in selecionados:
                distancias_outros = []
                for outro in self.clusters:
                    if outro.id != cluster.id and outro.centroide:
                        d = euclidiana(elem.atributos, outro.centroide.atributos)
                        distancias_outros.append((d, outro))

                if distancias_outros:
                    dist_min_outro, cluster_mais_proximo = min(distancias_outros, key=lambda x: x[0])
                    if dist_min_outro < dist:
                        cluster.remover_elemento(elem)
                        elementos_para_novos_clusters.append(elem)

            cluster.atualizar_centroide()

        for elem in elementos_para_novos_clusters:
            novo_cluster = Cluster(self.proximo_id)
            novo_cluster.adicionar_elemento(elem)
            self.adicionar_cluster(novo_cluster)

        for cluster in self.clusters:
            cluster.atualizar_centroide()

    def __repr__(self):
        return "\n\n".join(str(c) for c in self.clusters)

if __name__ == "__main__":
    c1 = Cluster(1)
    c1.adicionar_elemento(Elemento("A", [1, 1]))
    c1.adicionar_elemento(Elemento("B", [1, 2]))
    c1.adicionar_elemento(Elemento("C", [10, 10]))  

    c2 = Cluster(2)
    c2.adicionar_elemento(Elemento("D", [5, 5]))
    c2.adicionar_elemento(Elemento("E", [6, 5]))

    gerenciador = GerenciadorClusters(limiar=5.0, k=1)
    gerenciador.adicionar_cluster(c1)
    gerenciador.adicionar_cluster(c2)

    print("Antes da análise:")
    print(gerenciador)

    gerenciador.analisar_e_criar_novos()

    print("\nApós análise e possível criação de novos clusters:")
    print(gerenciador)
