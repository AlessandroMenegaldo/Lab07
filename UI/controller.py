import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()

        mese = self._view.dd_mese.value
        media_genova, media_torino, media_milano = self._model.calcola_umidita_media(mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese di {mese} è:"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {media_genova}"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {media_torino}"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {media_milano}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.clean()
        mese = self._view.dd_mese.value
        soluzione, costo = self._model.calcola_sequenza_citta_analisi(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo}:"))
        for giorno in soluzione:
            self._view.lst_result.controls.append(ft.Text(giorno))

        self._view.update_page()



    def read_mese(self, e):
        self._mese = int(e.control.value)

