from tkinter.constants import CENTER

import flet as ft
from flet.core.alignment import center

from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)

    #AUTO NUOVA CON MARCA, MODELLO E ANNO
    nuovaAuto_txt = ft.Text(value = "Aggiungi Nuova Automobile", size = 20)
    marca_field = ft.TextField( label = "Marca", text_size= 18)
    modello_field = ft.TextField( label = "Modello", text_size= 18)
    anno_field = ft.TextField( label = "Anno", text_size= 18 )


    #CONTATORE NUMERO POSTI
    count = 0
    counterBtn = ft.TextField( value = str(count), disabled = True ,text_size= 18, width= 50, text_align= ft.TextAlign.CENTER)
    def aggiungi(e):
        currentVal = counterBtn.value
        counterBtn.value = int(currentVal) + 1
        counterBtn.update()

    def togli(e):
        currentVal = counterBtn.value
        counterBtn.value = int(currentVal) - 1
        counterBtn.update()

    btnPiu = ft.IconButton(icon = ft.Icons.ADD, icon_color = "green", icon_size= 15, on_click= aggiungi)
    btnMeno = ft.IconButton(icon = ft.Icons.REMOVE, icon_color = "red", icon_size= 15, on_click= togli)
    counter = ft.Row(controls=[btnMeno, counterBtn, btnPiu])


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    #AGGIUNGI LA NUOVA AUTO
    def aggiungi_auto(e):
        #prendi solo i valori
        marca = marca_field.value.strip()
        modello = modello_field.value.strip()
        anno = anno_field.value.strip()

        #controlli se i valori sono giusti
        if not marca or not modello or not anno:
            alert.show_alert("❌Errore: inserisci valori numerici validi per anno e posti")
            return

        if not anno.isdigit() or counterBtn.value < 0:
            alert.show_alert("❌Errore: inserisci valori numerici validi per anno e posti")
            return

        #aggiungi l'auto alla lista di oggetti
        try:
            auto = autonoleggio.aggiungi_automobile(marca, modello, anno, counterBtn.value) #ritorna l'oggetto auto
        except ValueError:
            alert.show_alert("❌Errore: inserisci valori numerici validi per anno e posti")
            return

        #resetta i singoli valori dei TextFields
        marca_field.value = ""
        modello_field.value = ""
        anno_field.value = ""

        stato = "✅" if auto.disponibile else "⛔"

        #aggiungo l'auto alla ListView
        lista_auto.controls.append(ft.Text(f"{stato} {auto}"))

        page.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto

    # ELEVATED BUTTON AGIGUNGI AUTOMOBILE PER CONFERMARE
    btnNuovaAuto = ft.ElevatedButton(text="Aggiungi Automobile", on_click=aggiungi_auto)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        nuovaAuto_txt,
        ft.Row(spacing=20, alignment=ft.MainAxisAlignment.CENTER,
               controls=[marca_field, modello_field, anno_field, counter]),
        btnNuovaAuto,


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
