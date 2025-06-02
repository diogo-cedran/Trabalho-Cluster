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

    def remover_elemento(self, elemento: Elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
            self.atualizar_centroide()

    def alterar_elemento(self, elemento_antigo: Elemento, elemento_novo: Elemento):
        try:
            idx = self.elementos.index(elemento_antigo)
            self.elementos[idx] = elemento_novo
            self.atualizar_centroide()
        except ValueError:
            print("Elemento não encontrado para alteração.")

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


if __name__ == "__main__":
    cluster1 = Cluster(1)
    cluster1.adicionar_elemento(Elemento("Elem1", [1.0, 2.0]))

    cluster2 = Cluster(2)
    cluster2.adicionar_elemento(Elemento("Elem2", [5.0, 6.0]))

    print(cluster1)
    print(cluster2)
