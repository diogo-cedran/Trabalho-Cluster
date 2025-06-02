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

    def reorganizar(self):
        """
        Método para reorganizar os elementos do cluster baseado no novo centróide,
        opcional, pode incluir ordenação ou outras regras. Aqui vamos ordenar
        por distância crescente ao centróide.
        """
        if self.centroide is None:
            return
        self.elementos.sort(key=lambda e: euclidiana(e.atributos, self.centroide.atributos))

    def __repr__(self):
        return f"Cluster {self.id} - Centroide: {self.centroide}\nElementos:\n" + "\n".join(str(e) for e in self.elementos)

def euclidiana(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


if __name__ == "__main__":
    cluster = Cluster(1)
    cluster.adicionar_elemento(Elemento("Elem1", [1.0, 2.0]))
    cluster.adicionar_elemento(Elemento("Elem2", [2.0, 3.0]))
    cluster.adicionar_elemento(Elemento("Elem3", [3.0, 4.0]))

    print("Antes da reorganização:")
    print(cluster)

    cluster.reorganizar()

    print("\nApós reorganização pelo centroide:")
    print(cluster)
