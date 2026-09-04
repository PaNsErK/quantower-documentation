# Datenschutz

## Was die Website speichert

- Dokumentationstiefe und zuletzt gewählter Modus im lokalen Browserprofil.
- Status und optionale Notizen der manuellen Tests im lokalen Browserprofil, getrennt nach FZMT, FZV2-RM und FZCURRENT.

## Was die Website nicht tut

- keine Anwendungs-Telemetrie oder Analytics;
- keine externen Skripte, Fonts, CDNs oder Laufzeit-Assets;
- keine Uploads und keine Netzwerk-API für Testdaten;
- keine Konto-, Order-, Positions-, Portfolio-, Verbindungs- oder Strategiedaten;
- keine lokalen Pfade, Prozesskennungen, Fensterkennungen, Screenshots oder vollständigen Logs.

Notizen werden nur exportiert, wenn die Checkbox ausdrücklich aktiviert wurde. Importdateien werden lokal auf Größe, das geschlossene V2-/V3-Schema, exakt passende Suite-ID, bekannte Test-IDs, Statuswerte und sensible Datenmuster geprüft. Ein alter FZMT-v1/v2-Stand darf ausschließlich in den FZMT-Namespace migriert werden; historische und aktuelle Benutzerabnahmen werden nie vorausgefüllt.

## Plattformhinweis

Die öffentliche Beta wird über GitHub Pages bereitgestellt und enthält keine eigene Anwendungstelemetrie. GitHub kann als Hostingplattform jedoch technische Zugriffsdaten wie IP-Adressen für Betrieb und Sicherheit verarbeiten. Daher verspricht diese Dokumentation **keine Übertragung eigener Testdaten**, nicht „null Plattformdaten“.
