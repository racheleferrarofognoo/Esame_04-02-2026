import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def popola_dd_ruolo(self):
        self._view.dd_ruolo.options.clear()
        ruoli = self._model.get_ruoli()
        for ruolo in ruoli:
            self._view.dd_ruolo.options(ft.dropdown.Option(ruolo))

        self._view.update()


    def handle_crea_grafo(self, e):
        self._view.list_risultato.controls.clear()
        try:
            ruolo = self._view.get_ruolo.value
            self._model.build_graph(ruolo)
            archi, nodi = self._model.num_archi_nodi()
            self._view.list_risultato.controls.append(ft.TextField(f'Nodi: {nodi}| Archi : {archi}'))
        except ValueError:
            self._view.show_alert('Inserire un valore numerico')



        self._view.update()


    def handle_classifica(self, e):
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.TextField(f'Artisti in ordine decrescente'))
        lista = self._model.get_classifica()
        for el in lista:
            elemento = self._model.id_map(el[0])
            self._view.list_risultato.controls.append(ft.TextField(f'{elemento.name}'))

        self._view.update()

