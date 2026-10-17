"""Visual editor for GZDoom ListMenu MENUDEF files."""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox,
    QPushButton, QSpinBox, QSplitter, QVBoxLayout, QWidget,
)

PROJECT_VERSION = 1
LANGUAGES = {"it": "Italiano", "en": "English", "fr": "Français", "de": "Deutsch"}
UI_TRANSLATIONS = {
    "en": {
        "Anubi — GZDoom Menu Editor": "Anubi — GZDoom Menu Editor", "Nuovo menu": "New menu",
        "Elimina menu": "Delete menu", "Menu del progetto": "Project menus", "Nome MENUDEF": "MENUDEF name",
        "Titolo": "Title", "Posizione X": "Position X", "Posizione Y": "Position Y",
        "Spaziatura righe": "Line spacing", "Font": "Font", "Colore testo": "Text color",
        "Cursore": "Selector", "Offset cursore": "Selector offset", "Posizione rapida": "Quick position",
        "Applica posizione": "Apply position", "Aggiungi voce": "Add item", "Modifica voce": "Edit item",
        "Rimuovi voce": "Remove item", "Voci (doppio clic per modificare)": "Items (double-click to edit)",
        "Apri progetto": "Open project", "Salva progetto": "Save project", "Esporta MENUDEF": "Export MENUDEF",
        "Crea PK3": "Build PK3", "Lingua:": "Language:", "Alto sinistra": "Top left",
        "Alto centro": "Top center", "Alto destra": "Top right", "Centro sinistra": "Middle left",
        "Centro": "Center", "Centro destra": "Middle right", "Basso sinistra": "Bottom left",
        "Basso centro": "Bottom center", "Basso destra": "Bottom right", "Teschio Doom": "Doom skull",
        "Freccia trattino": "Dash cursor", "Cursore Strife": "Strife cursor",
        "Cursore Heretic/Hexen": "Heretic/Hexen cursor", "Nessuno": "None", "Freccia": "Arrow",
        "Voce del menu": "Menu item", "TextItem (collegamento)": "TextItem (link)",
        "StaticText (testo)": "StaticText (text)", "Tipo": "Type", "Testo": "Text",
        "Tasto rapido": "Hotkey", "Menu di destinazione": "Destination menu", "Nuovo menu dialogo": "New menu",
        "Annulla": "Cancel",
        "Nome interno": "Internal name", "Nome già usato": "Name already used",
        "Scegli un nome interno univoco.": "Choose a unique internal name.",
        "Nome non valido": "Invalid name", "Il nome deve essere presente e univoco.": "The name must be present and unique.",
        "Progetto": "Project", "Il progetto deve contenere almeno un menu.": "The project must contain at least one menu.",
        "Apri progetto errore": "Open project error", "Voce non valida": "Invalid item",
        "Errore esportazione": "Export error", "Errore creazione PK3": "PK3 creation error",
        "Inserisci il testo della voce.": "Enter the item text.",
        "Un collegamento richiede un tasto rapido e un menu di destinazione.": "A link needs a hotkey and a destination menu.",
        "Progetto menu (*.json)": "Menu project (*.json)", "Tutti i file (*)": "All files (*)",
        "Crea archivio per GZDoom": "Create GZDoom archive", "GZDoom PK3 (*.pk3)": "GZDoom PK3 (*.pk3)",
        "MENUDEF (*.txt);;Tutti i file (*)": "MENUDEF (*.txt);;All files (*)",
    },
    "fr": {
        "Anubi — GZDoom Menu Editor": "Anubi — Éditeur de menus GZDoom", "Nuovo menu": "Nouveau menu",
        "Elimina menu": "Supprimer le menu", "Menu del progetto": "Menus du projet", "Nome MENUDEF": "Nom MENUDEF",
        "Titolo": "Titre", "Posizione X": "Position X", "Posizione Y": "Position Y",
        "Spaziatura righe": "Espacement des lignes", "Font": "Police", "Colore testo": "Couleur du texte",
        "Cursore": "Curseur", "Offset cursore": "Décalage du curseur", "Posizione rapida": "Position rapide",
        "Applica posizione": "Appliquer la position", "Aggiungi voce": "Ajouter une entrée", "Modifica voce": "Modifier l’entrée",
        "Rimuovi voce": "Supprimer l’entrée", "Voci (doppio clic per modificare)": "Entrées (double-clic pour modifier)",
        "Apri progetto": "Ouvrir le projet", "Salva progetto": "Enregistrer le projet", "Esporta MENUDEF": "Exporter MENUDEF",
        "Crea PK3": "Créer PK3", "Lingua:": "Langue :", "Alto sinistra": "En haut à gauche",
        "Alto centro": "En haut au centre", "Alto destra": "En haut à droite", "Centro sinistra": "Au milieu à gauche",
        "Centro": "Au centre", "Centro destra": "Au milieu à droite", "Basso sinistra": "En bas à gauche",
        "Basso centro": "En bas au centre", "Basso destra": "En bas à droite", "Teschio Doom": "Crâne de Doom",
        "Freccia trattino": "Curseur tiret", "Cursore Strife": "Curseur Strife",
        "Cursore Heretic/Hexen": "Curseur Heretic/Hexen", "Nessuno": "Aucun", "Freccia": "Flèche",
        "Voce del menu": "Entrée du menu", "TextItem (collegamento)": "TextItem (lien)",
        "StaticText (testo)": "StaticText (texte)", "Tipo": "Type", "Testo": "Texte",
        "Tasto rapido": "Raccourci", "Menu di destinazione": "Menu de destination", "Nuovo menu dialogo": "Nouveau menu",
        "Annulla": "Annuler",
        "Nome interno": "Nom interne", "Nome già usato": "Nom déjà utilisé",
        "Scegli un nome interno univoco.": "Choisissez un nom interne unique.",
        "Nome non valido": "Nom invalide", "Il nome deve essere presente e univoco.": "Le nom doit être renseigné et unique.",
        "Progetto": "Projet", "Il progetto deve contenere almeno un menu.": "Le projet doit contenir au moins un menu.",
        "Apri progetto errore": "Erreur d’ouverture du projet", "Voce non valida": "Entrée invalide",
        "Errore esportazione": "Erreur d’exportation", "Errore creazione PK3": "Erreur de création du PK3",
        "Inserisci il testo della voce.": "Saisissez le texte de l’entrée.",
        "Un collegamento richiede un tasto rapido e un menu di destinazione.": "Un lien nécessite un raccourci et un menu de destination.",
        "Salva progetto": "Enregistrer le projet", "Progetto menu (*.json)": "Projet de menu (*.json)",
        "Tutti i file (*)": "Tous les fichiers (*)", "Crea archivio per GZDoom": "Créer une archive GZDoom",
        "GZDoom PK3 (*.pk3)": "GZDoom PK3 (*.pk3)",
        "MENUDEF (*.txt);;Tutti i file (*)": "MENUDEF (*.txt);;Tous les fichiers (*)",
    },
    "de": {
        "Anubi — GZDoom Menu Editor": "Anubi — GZDoom-Menüeditor", "Nuovo menu": "Neues Menü",
        "Elimina menu": "Menü löschen", "Menu del progetto": "Projektmenüs", "Nome MENUDEF": "MENUDEF-Name",
        "Titolo": "Titel", "Posizione X": "Position X", "Posizione Y": "Position Y",
        "Spaziatura righe": "Zeilenabstand", "Font": "Schriftart", "Colore testo": "Textfarbe",
        "Cursore": "Auswahlmarker", "Offset cursore": "Marker-Versatz", "Posizione rapida": "Schnellposition",
        "Applica posizione": "Position anwenden", "Aggiungi voce": "Eintrag hinzufügen", "Modifica voce": "Eintrag bearbeiten",
        "Rimuovi voce": "Eintrag entfernen", "Voci (doppio clic per modificare)": "Einträge (Doppelklick zum Bearbeiten)",
        "Apri progetto": "Projekt öffnen", "Salva progetto": "Projekt speichern", "Esporta MENUDEF": "MENUDEF exportieren",
        "Crea PK3": "PK3 erstellen", "Lingua:": "Sprache:", "Alto sinistra": "Oben links",
        "Alto centro": "Oben mittig", "Alto destra": "Oben rechts", "Centro sinistra": "Mitte links",
        "Centro": "Mitte", "Centro destra": "Mitte rechts", "Basso sinistra": "Unten links",
        "Basso centro": "Unten mittig", "Basso destra": "Unten rechts", "Teschio Doom": "Doom-Schädel",
        "Freccia trattino": "Bindestrich-Marker", "Cursore Strife": "Strife-Marker",
        "Cursore Heretic/Hexen": "Heretic/Hexen-Marker", "Nessuno": "Keiner", "Freccia": "Pfeil",
        "Voce del menu": "Menüeintrag", "TextItem (collegamento)": "TextItem (Link)",
        "StaticText (testo)": "StaticText (Text)", "Tipo": "Typ", "Testo": "Text",
        "Tasto rapido": "Tastenkürzel", "Menu di destinazione": "Zielmenü", "Nuovo menu dialogo": "Neues Menü",
        "Annulla": "Abbrechen",
        "Nome interno": "Interner Name", "Nome già usato": "Name bereits vergeben",
        "Scegli un nome interno univoco.": "Wähle einen eindeutigen internen Namen.",
        "Nome non valido": "Ungültiger Name", "Il nome deve essere presente e univoco.": "Der Name muss angegeben und eindeutig sein.",
        "Progetto": "Projekt", "Il progetto deve contenere almeno un menu.": "Das Projekt muss mindestens ein Menü enthalten.",
        "Apri progetto errore": "Fehler beim Öffnen des Projekts", "Voce non valida": "Ungültiger Eintrag",
        "Errore esportazione": "Exportfehler", "Errore creazione PK3": "Fehler beim Erstellen des PK3",
        "Inserisci il testo della voce.": "Gib den Text des Eintrags ein.",
        "Un collegamento richiede un tasto rapido e un menu di destinazione.": "Ein Link benötigt ein Tastenkürzel und ein Zielmenü.",
        "Apri progetto": "Projekt öffnen", "Salva progetto": "Projekt speichern",
        "Progetto menu (*.json)": "Menüprojekt (*.json)", "Tutti i file (*)": "Alle Dateien (*)",
        "Crea archivio per GZDoom": "GZDoom-Archiv erstellen", "GZDoom PK3 (*.pk3)": "GZDoom PK3 (*.pk3)",
        "MENUDEF (*.txt);;Tutti i file (*)": "MENUDEF (*.txt);;Alle Dateien (*)",
    },
}


def tr(language: str, text: str) -> str:
    return UI_TRANSLATIONS.get(language, {}).get(text, text)


DEFAULT_PROJECT = {
    "format": "AnubiGZDoomMenuProject", "version": PROJECT_VERSION,
    "menus": [
        {"name": "MainMenu", "title": "ANUBI", "x": 160, "y": 80, "spacing": 18, "placement": "Centro",
         "font": "BigFont", "color": "Gold", "selector": "M_SKULL1", "selector_x": -32, "selector_y": -5,
         "items": [
             {"kind": "TextItem", "label": "Avvia partita", "hotkey": "a", "target": "PlayerclassMenu"},
             {"kind": "TextItem", "label": "Opzioni", "hotkey": "o", "target": "OptionsMenu"},
             {"kind": "TextItem", "label": "Esci", "hotkey": "e", "target": "QuitMenu"},
         ]},
        {"name": "AnubiOptions", "title": "OPZIONI", "x": 160, "y": 80, "spacing": 18, "placement": "Centro",
         "font": "BigFont", "color": "Gold", "selector": "M_SKULL1", "selector_x": -32, "selector_y": -5,
         "items": [
             {"kind": "TextItem", "label": "Comandi", "hotkey": "c", "target": "CustomizeControls"},
             {"kind": "TextItem", "label": "Audio e video", "hotkey": "v", "target": "VideoOptions"},
             {"kind": "TextItem", "label": "Indietro", "hotkey": "i", "target": "MainMenu"},
         ]},
    ],
}


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def generate_menudef(project: dict) -> str:
    lines = ["// Generated by Anubi GZDoom Menu Editor", ""]
    for menu in project["menus"]:
        name = menu["name"].strip()
        if not name:
            raise ValueError("Ogni menu deve avere un nome.")
        lines.extend([f"ListMenu {quote(name)}", "{"])
        font = menu.get("font", "BigFont")
        color = menu.get("color", "Untranslated")
        lines.append(f"    Font {quote(font)}, {quote(color)}")
        lines.append(f"    Position {int(menu['x'])}, {int(menu['y'])}")
        lines.append(f"    Linespacing {int(menu['spacing'])}")
        selector = menu.get("selector", "M_SKULL1")
        if selector:
            lines.append(f"    Selector {quote(selector)}, {int(menu.get('selector_x', -32))}, {int(menu.get('selector_y', -5))}")
        if menu["title"].strip():
            title_x = int(menu.get("title_x", 160))
            title_y = int(menu.get("title_y", 32))
            lines.append(f"    StaticTextCentered {title_x}, {title_y}, {quote(menu['title'].strip())}")
        for item in menu["items"]:
            label = quote(item["label"])
            if item["kind"] == "StaticText":
                lines.append(f"    StaticText {label}")
            else:
                hotkey = quote(item["hotkey"][:1])
                target = quote(item["target"])
                lines.append(f"    TextItem {label}, {hotkey}, {target}")
        lines.extend(["}", ""])
    return "\n".join(lines)


class ItemDialog(QDialog):
    def __init__(self, parent=None, item=None, language="it"):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(tr(language, "Voce del menu"))
        self.kind = QComboBox()
        self.kind.addItems([tr(language, "TextItem (collegamento)"), tr(language, "StaticText (testo)")])
        self.label = QLineEdit()
        self.hotkey = QLineEdit()
        self.hotkey.setMaxLength(1)
        self.target = QLineEdit()
        form = QFormLayout()
        form.addRow(tr(language, "Tipo"), self.kind)
        form.addRow(tr(language, "Testo"), self.label)
        form.addRow(tr(language, "Tasto rapido"), self.hotkey)
        form.addRow(tr(language, "Menu di destinazione"), self.target)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("OK")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr(language, "Annulla"))
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.kind.currentIndexChanged.connect(self.update_fields)
        if item:
            self.kind.setCurrentIndex(1 if item["kind"] == "StaticText" else 0)
            self.label.setText(item["label"])
            self.hotkey.setText(item.get("hotkey", ""))
            self.target.setText(item.get("target", ""))
        self.update_fields()

    def update_fields(self):
        is_link = self.kind.currentIndex() == 0
        self.hotkey.setEnabled(is_link)
        self.target.setEnabled(is_link)

    def value(self):
        if not self.label.text().strip():
            raise ValueError(tr(self.language, "Inserisci il testo della voce."))
        if self.kind.currentIndex() == 0:
            if not self.hotkey.text().strip() or not self.target.text().strip():
                raise ValueError(tr(self.language, "Un collegamento richiede un tasto rapido e un menu di destinazione."))
            return {"kind": "TextItem", "label": self.label.text().strip(),
                    "hotkey": self.hotkey.text().strip()[:1], "target": self.target.text().strip()}
        return {"kind": "StaticText", "label": self.label.text().strip()}


class MenuDialog(QDialog):
    def __init__(self, parent=None, language="it"):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(tr(language, "Nuovo menu"))
        self.name = QLineEdit("NewMenu")
        form = QFormLayout()
        form.addRow(tr(language, "Nome interno"), self.name)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("OK")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr(language, "Annulla"))
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)


class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(330, 300)
        self.menu = None

    def set_menu(self, menu):
        self.menu = menu
        self.update()

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#171a20"))
        painter.setPen(QColor("#313844"))
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
        if not self.menu:
            return
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setPen(QColor("#f0c674"))
        painter.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        scale_x, scale_y = self.width() / 320, self.height() / 200
        title_x = self.menu.get("title_x", 160) * scale_x
        title_y = max(14, self.menu.get("title_y", 32)) * scale_y
        color_map = {"Red": "#ff5555", "Gold": "#f0c674", "Green": "#8bd49c",
                     "Blue": "#82aaff", "White": "#f0f0f0", "Untranslated": "#f0f0f0"}
        painter.setPen(QColor(color_map.get(self.menu.get("color", "Gold"), "#f0c674")))
        font_map = {"BigFont": 12, "SmallFont": 10, "ConsoleFont": 10}
        painter.setFont(QFont("Consolas", font_map.get(self.menu.get("font", "BigFont"), 12), QFont.Weight.Bold))
        painter.drawText(int(title_x - 60 * scale_x), int(title_y), self.menu["title"] or self.menu["name"])
        painter.setPen(QColor(color_map.get(self.menu.get("color", "Gold"), "#f0c674")))
        painter.setFont(QFont("Consolas", font_map.get(self.menu.get("font", "BigFont"), 12), QFont.Weight.Bold))
        x = self.menu["x"] * scale_x
        y = self.menu["y"] * scale_y
        for index, item in enumerate(self.menu["items"]):
            prefix = f"[{item.get('hotkey','')}] " if item["kind"] == "TextItem" else "    "
            if index == 0 and self.menu.get("selector"):
                painter.setPen(QColor("#f0c674"))
                cursor_x = x + self.menu.get("selector_x", -32) * scale_x
                cursor_y = y + (index * self.menu["spacing"] + self.menu.get("selector_y", -5)) * scale_y
                painter.drawText(int(cursor_x), int(cursor_y), "➤")
                painter.setPen(QColor(color_map.get(self.menu.get("color", "Gold"), "#f0c674")))
            painter.drawText(int(x), int(y + index * self.menu["spacing"] * scale_y), prefix + item["label"])


class MenuEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = QSettings("Anubi", "GZDoomMenuEditor").value("language", "it")
        self.setWindowTitle("Anubi — GZDoom Menu Editor")
        self.resize(900, 620)
        self.project = json.loads(json.dumps(DEFAULT_PROJECT))
        self.current_index = 0

        self.menu_list = QListWidget()
        self.menu_list.currentRowChanged.connect(self.select_menu)
        self.new_menu_btn = QPushButton("Nuovo menu")
        self.delete_menu_btn = QPushButton("Elimina menu")
        self.new_menu_btn.clicked.connect(self.new_menu)
        self.delete_menu_btn.clicked.connect(self.delete_menu)
        left = QVBoxLayout()
        self.project_menus_label = QLabel("Menu del progetto")
        left.addWidget(self.project_menus_label)
        left.addWidget(self.menu_list, 1)
        left.addWidget(self.new_menu_btn)
        left.addWidget(self.delete_menu_btn)
        left_widget = QWidget()
        left_widget.setLayout(left)

        self.name = QLineEdit()
        self.title = QLineEdit()
        self.x = QSpinBox(); self.x.setRange(0, 320)
        self.y = QSpinBox(); self.y.setRange(0, 200)
        self.spacing = QSpinBox(); self.spacing.setRange(8, 64)
        self.font = QComboBox(); self.font.addItems(["BigFont", "SmallFont", "ConsoleFont"])
        self.color = QComboBox(); self.color.addItems(["Gold", "Red", "Green", "Blue", "White", "Untranslated"])
        self.selector = QComboBox()
        self.selector_options = [("Teschio Doom", "M_SKULL1"), ("Freccia trattino", "-"),
                                 ("Cursore Strife", "M_CURS1"), ("Cursore Heretic/Hexen", "M_SLCTR1"),
                                 ("Nessuno", "")]
        for label, patch in self.selector_options:
            self.selector.addItem(label, patch)
        self.selector_x = QSpinBox(); self.selector_x.setRange(-100, 100)
        self.selector_y = QSpinBox(); self.selector_y.setRange(-100, 100)
        self.placement = QComboBox()
        self.placement_options = ["Alto sinistra", "Alto centro", "Alto destra", "Centro sinistra",
                                  "Centro", "Centro destra", "Basso sinistra", "Basso centro", "Basso destra"]
        for position in self.placement_options:
            self.placement.addItem(position, position)
        self.apply_placement_btn = QPushButton("Applica posizione")
        self.apply_placement_btn.clicked.connect(self.apply_placement)
        form = QFormLayout()
        form.addRow("Nome MENUDEF", self.name)
        form.addRow("Titolo", self.title)
        form.addRow("Posizione X", self.x)
        form.addRow("Posizione Y", self.y)
        form.addRow("Spaziatura righe", self.spacing)
        form.addRow("Font", self.font)
        form.addRow("Colore testo", self.color)
        form.addRow("Cursore", self.selector)
        selector_offset = QHBoxLayout()
        selector_offset.addWidget(QLabel("X")); selector_offset.addWidget(self.selector_x)
        selector_offset.addWidget(QLabel("Y")); selector_offset.addWidget(self.selector_y)
        form.addRow("Offset cursore", selector_offset)
        placement_row = QHBoxLayout()
        placement_row.addWidget(self.placement)
        placement_row.addWidget(self.apply_placement_btn)
        form.addRow("Posizione rapida", placement_row)
        self.form_labels = {
            "Nome MENUDEF": form.labelForField(self.name), "Titolo": form.labelForField(self.title),
            "Posizione X": form.labelForField(self.x), "Posizione Y": form.labelForField(self.y),
            "Spaziatura righe": form.labelForField(self.spacing), "Font": form.labelForField(self.font),
            "Colore testo": form.labelForField(self.color), "Cursore": form.labelForField(self.selector),
            "Offset cursore": form.labelForField(selector_offset), "Posizione rapida": form.labelForField(placement_row),
        }
        self.name.editingFinished.connect(self.update_menu_fields)
        self.title.textChanged.connect(self.update_menu_fields)
        self.x.valueChanged.connect(self.update_menu_fields)
        self.y.valueChanged.connect(self.update_menu_fields)
        self.spacing.valueChanged.connect(self.update_menu_fields)
        self.font.currentTextChanged.connect(self.update_menu_fields)
        self.color.currentTextChanged.connect(self.update_menu_fields)
        self.selector.currentIndexChanged.connect(self.update_menu_fields)
        self.selector_x.valueChanged.connect(self.update_menu_fields)
        self.selector_y.valueChanged.connect(self.update_menu_fields)

        self.item_list = QListWidget()
        self.item_list.currentRowChanged.connect(self.update_preview)
        self.add_item_btn = QPushButton("Aggiungi voce")
        self.edit_item_btn = QPushButton("Modifica voce")
        self.remove_item_btn = QPushButton("Rimuovi voce")
        self.add_item_btn.clicked.connect(self.add_item)
        self.edit_item_btn.clicked.connect(self.edit_item)
        self.remove_item_btn.clicked.connect(self.remove_item)
        item_buttons = QHBoxLayout()
        item_buttons.addWidget(self.add_item_btn)
        item_buttons.addWidget(self.edit_item_btn)
        item_buttons.addWidget(self.remove_item_btn)
        items_panel = QVBoxLayout()
        self.items_label = QLabel("Voci (doppio clic per modificare)")
        items_panel.addWidget(self.items_label)
        items_panel.addWidget(self.item_list)
        items_panel.addLayout(item_buttons)
        items_widget = QWidget(); items_widget.setLayout(items_panel)
        self.item_list.itemDoubleClicked.connect(lambda _: self.edit_item())

        self.preview = Preview()
        right = QVBoxLayout()
        right.addLayout(form)
        right.addWidget(items_widget, 1)
        right_widget = QWidget(); right_widget.setLayout(right)
        splitter = QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.addWidget(self.preview)
        splitter.setSizes([180, 370, 350])
        self.setCentralWidget(splitter)

        toolbar = self.addToolBar("File")
        self.toolbar_actions = []
        for label, callback in (("Apri progetto", self.open_project), ("Salva progetto", self.save_project),
                                ("Esporta MENUDEF", self.export_menudef), ("Crea PK3", self.export_pk3)):
            action = toolbar.addAction(label)
            action.triggered.connect(callback)
            self.toolbar_actions.append((label, action))
        self.language_label = QLabel("Lingua:")
        toolbar.addWidget(self.language_label)
        self.language_combo = QComboBox()
        for code, display_name in LANGUAGES.items():
            self.language_combo.addItem(display_name, code)
        self.language_combo.currentIndexChanged.connect(lambda: self.set_language(self.language_combo.currentData()))
        toolbar.addWidget(self.language_combo)
        self.refresh_menu_list()
        self.menu_list.setCurrentRow(0)
        language_index = self.language_combo.findData(self.language)
        self.language_combo.setCurrentIndex(max(0, language_index))
        self.set_language(self.language)

    def refresh_menu_list(self):
        self.menu_list.blockSignals(True)
        self.menu_list.clear()
        self.menu_list.addItems([m["name"] for m in self.project["menus"]])
        self.menu_list.setCurrentRow(self.current_index)
        self.menu_list.blockSignals(False)
        self.load_menu_fields()

    def set_language(self, language):
        if language not in LANGUAGES:
            language = "it"
        self.language = language
        self.setWindowTitle(tr(language, "Anubi — GZDoom Menu Editor"))
        self.project_menus_label.setText(tr(language, "Menu del progetto"))
        self.new_menu_btn.setText(tr(language, "Nuovo menu"))
        self.delete_menu_btn.setText(tr(language, "Elimina menu"))
        self.items_label.setText(tr(language, "Voci (doppio clic per modificare)"))
        self.add_item_btn.setText(tr(language, "Aggiungi voce"))
        self.edit_item_btn.setText(tr(language, "Modifica voce"))
        self.remove_item_btn.setText(tr(language, "Rimuovi voce"))
        self.language_label.setText(tr(language, "Lingua:"))
        for key, label in self.form_labels.items():
            if label:
                label.setText(tr(language, key))
        for key, action in self.toolbar_actions:
            action.setText(tr(language, key))
        placement_data = self.placement.currentData()
        self.placement.blockSignals(True)
        self.placement.clear()
        for position in self.placement_options:
            self.placement.addItem(tr(language, position), position)
        self.placement.setCurrentIndex(max(0, self.placement.findData(placement_data)))
        self.placement.blockSignals(False)
        selector_data = self.selector.currentData()
        self.selector.blockSignals(True)
        self.selector.clear()
        for label, patch in self.selector_options:
            self.selector.addItem(tr(language, label), patch)
        self.selector.setCurrentIndex(max(0, self.selector.findData(selector_data)))
        self.selector.blockSignals(False)
        self.apply_placement_btn.setText(tr(language, "Applica posizione"))
        QSettings("Anubi", "GZDoomMenuEditor").setValue("language", language)

    def select_menu(self, index):
        if index < 0 or index >= len(self.project["menus"]):
            return
        self.current_index = index
        self.load_menu_fields()

    def menu(self):
        return self.project["menus"][self.current_index]

    def load_menu_fields(self):
        if not self.project["menus"]:
            return
        menu = self.menu()
        for widget in (self.name, self.title, self.x, self.y, self.spacing, self.placement,
                       self.font, self.color, self.selector, self.selector_x, self.selector_y):
            widget.blockSignals(True)
        self.name.setText(menu["name"])
        self.title.setText(menu["title"])
        self.x.setValue(menu["x"]); self.y.setValue(menu["y"]); self.spacing.setValue(menu["spacing"])
        self.placement.setCurrentIndex(max(0, self.placement.findData(menu.get("placement", "Centro"))))
        self.font.setCurrentText(menu.get("font", "BigFont"))
        self.color.setCurrentText(menu.get("color", "Untranslated"))
        selector_index = self.selector.findData(menu.get("selector", "M_SKULL1"))
        self.selector.setCurrentIndex(max(0, selector_index))
        self.selector_x.setValue(menu.get("selector_x", -32))
        self.selector_y.setValue(menu.get("selector_y", -5))
        for widget in (self.name, self.title, self.x, self.y, self.spacing, self.placement,
                       self.font, self.color, self.selector, self.selector_x, self.selector_y):
            widget.blockSignals(False)
        self.refresh_items()

    def update_menu_fields(self, *args):
        if not self.project["menus"]:
            return
        menu = self.menu()
        old_name = menu["name"]
        new_name = self.name.text().strip() or old_name
        if any(i != self.current_index and m["name"] == new_name for i, m in enumerate(self.project["menus"])):
            QMessageBox.warning(self, tr(self.language, "Nome già usato"), tr(self.language, "Scegli un nome interno univoco."))
            self.name.setText(old_name)
            new_name = old_name
        menu.update(name=new_name, title=self.title.text(), x=self.x.value(), y=self.y.value(), spacing=self.spacing.value(),
                    font=self.font.currentText(), color=self.color.currentText(), selector=self.selector.currentData(),
                    selector_x=self.selector_x.value(), selector_y=self.selector_y.value())
        if new_name != old_name:
            for other in self.project["menus"]:
                for item in other["items"]:
                    if item.get("target") == old_name:
                        item["target"] = new_name
            self.refresh_menu_list()
            self.menu_list.setCurrentRow(self.current_index)
        self.preview.set_menu(menu)

    def apply_placement(self):
        """Fit the selected menu block into a familiar screen position."""
        menu = self.menu()
        placement = self.placement.currentData()
        menu["placement"] = placement
        labels = [item["label"] for item in menu["items"]]
        max_chars = max([len(s) for s in labels] + [len(menu["title"])])
        width = min(280, max(48, max_chars * 8 + 28))
        block_height = max(1, len(menu["items"])) * menu["spacing"]
        if menu["title"]:
            block_height += 26
        if placement.endswith("sinistra"):
            x = 20
        elif placement.endswith("destra"):
            x = max(20, 300 - width)
        else:
            x = (320 - width) // 2
        if placement.startswith("Alto"):
            y = 44
        elif placement.startswith("Basso"):
            y = max(28, 192 - block_height)
        else:
            y = max(28, (200 - block_height) // 2 + 16)
        menu.update(x=x, y=y, title_x=x + width // 2, title_y=max(18, y - 12))
        self.load_menu_fields()

    def refresh_items(self):
        self.item_list.clear()
        if not self.project["menus"]:
            self.preview.set_menu(None)
            return
        for item in self.menu()["items"]:
            if item["kind"] == "TextItem":
                display = f"{item['label']}   [{item['hotkey']}]  →  {item['target']}"
            else:
                display = f"[Testo] {item['label']}"
            self.item_list.addItem(display)
        self.preview.set_menu(self.menu())

    def update_preview(self, *args):
        """Refresh the mock game screen when the selected menu item changes."""
        if self.project["menus"]:
            self.preview.set_menu(self.menu())

    def add_item(self):
        dialog = ItemDialog(self, language=self.language)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.menu()["items"].append(dialog.value())
                self.refresh_items()
            except ValueError as exc:
                QMessageBox.warning(self, tr(self.language, "Voce non valida"), str(exc))

    def edit_item(self):
        row = self.item_list.currentRow()
        if row < 0:
            return
        dialog = ItemDialog(self, self.menu()["items"][row], self.language)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.menu()["items"][row] = dialog.value()
                self.refresh_items()
                self.item_list.setCurrentRow(row)
            except ValueError as exc:
                QMessageBox.warning(self, tr(self.language, "Voce non valida"), str(exc))

    def remove_item(self):
        row = self.item_list.currentRow()
        if row >= 0:
            self.menu()["items"].pop(row)
            self.refresh_items()

    def new_menu(self):
        dialog = MenuDialog(self, self.language)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        name = dialog.name.text().strip()
        if not name or any(m["name"] == name for m in self.project["menus"]):
            QMessageBox.warning(self, tr(self.language, "Nome non valido"), tr(self.language, "Il nome deve essere presente e univoco."))
            return
        self.project["menus"].append({"name": name, "title": name.upper(), "x": 160, "y": 80,
                                       "spacing": 18, "placement": "Centro", "font": "BigFont",
                                       "color": "Gold", "selector": "M_SKULL1", "selector_x": -32,
                                       "selector_y": -5, "items": []})
        self.current_index = len(self.project["menus"]) - 1
        self.refresh_menu_list()
        self.menu_list.setCurrentRow(self.current_index)

    def delete_menu(self):
        if len(self.project["menus"]) <= 1:
            QMessageBox.information(self, tr(self.language, "Progetto"), tr(self.language, "Il progetto deve contenere almeno un menu."))
            return
        self.project["menus"].pop(self.current_index)
        self.current_index = max(0, self.current_index - 1)
        self.refresh_menu_list()
        self.menu_list.setCurrentRow(self.current_index)

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, tr(self.language, "Salva progetto"), "menu-project.json", tr(self.language, "Progetto menu (*.json)"))
        if path:
            Path(path).write_text(json.dumps(self.project, ensure_ascii=False, indent=2), encoding="utf-8")

    def open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, tr(self.language, "Apri progetto"), "", tr(self.language, "Progetto menu (*.json)"))
        if not path:
            return
        try:
            project = json.loads(Path(path).read_text(encoding="utf-8"))
            if project.get("format") != "AnubiGZDoomMenuProject" or not project.get("menus"):
                raise ValueError("Il file non è un progetto Anubi GZDoom Menu Editor valido.")
            for menu in project["menus"]:
                for item in menu.get("items", []):
                    if item.get("kind") not in ("StaticText", "TextItem"):
                        raise ValueError("Il progetto contiene un tipo di voce non supportato.")
            self.project = project
            self.current_index = 0
            self.refresh_menu_list()
            self.menu_list.setCurrentRow(0)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            QMessageBox.critical(self, tr(self.language, "Apri progetto errore"), str(exc))

    def export_menudef(self):
        path, _ = QFileDialog.getSaveFileName(self, tr(self.language, "Esporta MENUDEF"), "MENUDEF", tr(self.language, "MENUDEF (*.txt);;Tutti i file (*)"))
        if not path:
            return
        try:
            Path(path).write_text(generate_menudef(self.project), encoding="utf-8", newline="\n")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, tr(self.language, "Errore esportazione"), str(exc))

    def export_pk3(self):
        path, _ = QFileDialog.getSaveFileName(self, tr(self.language, "Crea archivio per GZDoom"), "menu-addon.pk3", tr(self.language, "GZDoom PK3 (*.pk3)"))
        if not path:
            return
        if Path(path).suffix.lower() != ".pk3":
            path = str(Path(path).with_suffix(".pk3"))
        try:
            menudef = generate_menudef(self.project)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("MENUDEF", menudef.encode("utf-8"))
                archive.writestr("README.txt", b"Generated with Anubi GZDoom Menu Editor. Load this PK3 with GZDoom.\n")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, tr(self.language, "Errore creazione PK3"), str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuEditor()
    window.show()
    raise SystemExit(app.exec())
