# Anubi GZDoom Menu Editor

Editor grafico Python per creare menu `ListMenu` ed esportare il lump `MENUDEF`, oppure un archivio `.pk3` caricabile da GZDoom. Richiede Python 3.10+ e PySide6.

## Avvio

```powershell
python anubi_gzdoom_menu_editor.py
```

PySide6 è già installato nell’ambiente Python usato per preparare questo programma.

## Uso

- Scegli la lingua dell’interfaccia dalla barra superiore: italiano, inglese, francese o tedesco. La scelta viene ricordata per l’avvio successivo e non modifica il testo dei menu che stai creando.
- Crea o seleziona i menu nella colonna a sinistra.
- Modifica nome interno, titolo, posizione e spaziatura.
- Scegli font, colore e cursore di selezione; puoi regolare gli offset X/Y del cursore.
- Aggiungi voci `TextItem` (collegamenti con tasto rapido e destinazione) o `StaticText`.
- Usa l’anteprima, salva il progetto JSON, esporta `MENUDEF` o crea un `.pk3`.

I cursori grafici `M_SKULL1`, `M_CURS1` e `M_SLCTR1` corrispondono ai menu predefiniti di Doom, Strife e Heretic/Hexen. Riferimento sintassi: https://github.com/rheit/zdoom/blob/master/wadsrc/static/menudef.txt
