# Quantower Documentation – lokaler Kandidat

Lokaler, noch nicht veröffentlichter Dokumentationskandidat für den Quantower-Indikator **Fractal Zones**.

Status: `runtime_inventory_pending`. Die 29 vom Produkt selbst erzeugten `SettingItem`-Zeilen sind dokumentiert. Von Quantower geerbte `base.Settings` sowie der sichtbare native Zugriff auf `HelpLink` werden erst in einem getrennten Runtime-Gate inventarisiert. Deshalb behauptet dieser Stand ausdrücklich keine vollständige Quantower-UI-Inventur.

## Lokaler Build

```powershell
uv venv --python 3.12.13
uv pip sync --python .venv requirements.lock.txt
.venv/Scripts/python.exe tools/validate_public_docs.py all
.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v
.venv/Scripts/python.exe -m mkdocs build --strict
.venv/Scripts/python.exe -m mkdocs build --strict -f mkdocs.offline.yml
```

Online-Vorschau:

```powershell
.venv/Scripts/python.exe -m mkdocs serve --dev-addr 127.0.0.1:8765
```

Der Offline-Build liegt in `site-offline/` und kann ohne Server über `index.html` geöffnet werden. Die Volltextsuche ist dort bewusst deaktiviert, damit keine Browser-Worker oder externen Netzwerkressourcen benötigt werden; Navigation, Inhalte und der lokale Teststand bleiben verfügbar.

## Datenschutz und Lizenz

Die Testfunktion speichert Status und optionale Notizen ausschließlich im lokalen Browserprofil. Es gibt keine Anwendungs-Telemetrie, keine Analyse-Skripte und keine externen Laufzeit-Assets. GitHub Pages selbst kann als Plattform technische Sicherheits- und Zugriffsdaten verarbeiten.

Für die Dokumentationsinhalte wurde noch keine Open-Source-Lizenz gewählt. Ohne ausdrückliche Lizenz werden keine zusätzlichen Nutzungsrechte eingeräumt.
