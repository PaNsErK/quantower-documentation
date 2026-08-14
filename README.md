# Inoffizielle Quantower-Dokumentation – öffentliche Beta

Öffentliche, inoffizielle Dokumentation für den Quantower-Indikator **Fractal Zones**. Dieses Projekt steht in keiner Verbindung zu Quantower und wird nicht von Quantower unterstützt oder herausgegeben.

Publikationsstatus: `public_beta_manual_acceptance_pending`. Die Inhalte, Einstellungen und Runtime-Inventur sind technisch validiert und bereits zum Lernen nutzbar. Der vollständige manuelle Quantower-Abnahmetest ist noch nicht abgeschlossen; deshalb ist `manual_acceptance_complete=false` fest im öffentlichen Manifest verankert.

Inventarstatus: `runtime_inventory_confirmed_with_residuals`. Dokumentiert sind 29 produktseitige `SettingItem`-Zeilen mit bis zu 41 atomaren Controls sowie die bestätigte geerbte `base.Settings`-Union mit 11 Zeilen und bis zu 25 weiteren Controls. Die geladene Bundle-Version ist erfasst; Quantower zeigt sie in der Fractal-Zones-UI nicht separat an. `HelpLink` ist aktuell leer und daher nicht nutzbar. Zwei klar begrenzte Runtime-Abweichungen bleiben sichtbar dokumentiert, weshalb dieser Stand keine uneingeschränkte Vollständigkeitsbehauptung abgibt.

Die [geführten Lernpfade](docs/indicators/fractal-zones/learning/index.md) bieten einen schnellen Einstieg, gezielte Übungen zu Bruchlogik, Lifecycle, Rendering und Recovery sowie sichere Beispielkonfigurationen. Änderungen können mit dem lokalen, fail-closed Dokumentationslauf gegen einen berechtigten Quell-Checkout geprüft werden; dabei werden weder private Pfade noch Quelltext oder Repository-Metadaten in dieses öffentliche Repository übernommen.

## Lokaler Build

```powershell
uv venv --python 3.12.13
uv pip sync --python .venv requirements.lock.txt
.venv/Scripts/python.exe tools/validate_public_docs.py all
.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v
.venv/Scripts/python.exe -m mkdocs build --strict
.venv/Scripts/python.exe -m mkdocs build --strict -f mkdocs.offline.yml
```

Der vollständige Wartungslauf ist unter [Dokumentation pflegen](docs/maintenance/documentation-workflow.md) beschrieben. Er klassifiziert das Ergebnis geschlossen als `no_drift`, `documentation_drift`, `runtime_confirmation_required` oder `unsafe_or_ambiguous_source`.

Online-Vorschau:

```powershell
.venv/Scripts/python.exe -m mkdocs serve --dev-addr 127.0.0.1:8765
```

Der Offline-Build liegt in `site-offline/` und kann ohne Server über `index.html` geöffnet werden. Die Volltextsuche ist dort bewusst deaktiviert, damit keine Browser-Worker oder externen Netzwerkressourcen benötigt werden; Navigation, Inhalte und der lokale Teststand bleiben verfügbar.

## Datenschutz und Lizenz

Die Testfunktion speichert Status und optionale Notizen ausschließlich im lokalen Browserprofil. Es gibt keine Anwendungs-Telemetrie, keine Analyse-Skripte und keine externen Laufzeit-Assets. GitHub Pages selbst kann als Plattform technische Sicherheits- und Zugriffsdaten verarbeiten.

Für die Dokumentationsinhalte wurde noch keine Open-Source-Lizenz gewählt. Ohne ausdrückliche Lizenz werden keine zusätzlichen Nutzungsrechte eingeräumt.
