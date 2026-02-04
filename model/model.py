import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.dao = DAO()
        self.artists = []
        self.id_map = {}
        self.nodi = []

    def get_ruoli(self):
        return self.dao.get_ruoli()

    def build_graph(self, role: str):
        self.G.clear()
        self.nodi = self.dao.get_artista(role)
        for nodo in self.nodi:
            self.G.add_node(nodo)
            self.id_map[nodo.artist_id] = nodo

        connessioni = self.dao.get_connessioni()
        for connessione in connessioni:
            if connessione['artista1'] in self.id_map and connessione['artista2'] in self.id_map:
                e1 = self.id_map[connessione['artista1']]
                e2 = self.id_map[connessione['artista2']]
                indice_a1 = connessione['indice_a1']
                indice_a2 = connessione['indice_a2']
                peso = connessione['peso']
                if indice_a1 < indice_a2:
                    self.G.add_edge(e1, e2, weight=peso)
                elif indice_a1 > indice_a2:
                    self.G.add_edge(e2, e1, weight=peso)


    def num_archi_nodi(self):
        return self.G.number_of_edges(), self.G.number_of_nodes()


    def classifica(self):
        lista =[]
        for n in self.G.nodes():
            somma_usc = 0
            somma_entr = 0
            for e_out in self.G.out_edges(n, data = True):
                somma_usc += e_out[2]['weight']
            for e_in in self.G.in_edges(n, data = True):
                somma_entr += e_in[2]['weight']
            diff = somma_usc - somma_entr
            lista.append((n, diff))
        lista.sort(key=lambda x: x[1], reverse = True)
        return lista


