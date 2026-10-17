# Anubi GZDoom Menu Editor

A Python GUI for creating GZDoom `ListMenu` definitions and exporting them as a `MENUDEF` lump or a `.pk3` archive. Requires Python 3.10+ and PySide6.

## Run

```powershell
python anubi_gzdoom_menu_editor.py
```

PySide6 is already installed in the Python environment used to prepare this program.

## Features

- Choose the editor interface language from the top toolbar: Italian, English, French, or German. Your choice is remembered for the next launch and does not change the menu text you are creating.
- Create or select menus in the left panel.
- Edit the internal menu name, title, position, and line spacing.
- Choose a font, text color, and selection cursor; adjust the cursor's X/Y offset.
- Add `TextItem` entries (links with a hotkey and destination) or `StaticText` entries.
- Preview the menu, save the project as JSON, export `MENUDEF`, or create a `.pk3` archive.

The `M_SKULL1`, `M_CURS1`, and `M_SLCTR1` graphic cursors correspond to the default menus in Doom, Strife, and Heretic/Hexen. Choose the cursor that matches the loaded base game. See the [GZDoom MENUDEF reference](https://github.com/rheit/zdoom/blob/master/wadsrc/static/menudef.txt) for syntax details.

## Load the PK3 in GZDoom

Launch GZDoom with your IWAD and the generated archive, for example:

```powershell
gzdoom -iwad doom2.wad -file menu-addon.pk3
```
