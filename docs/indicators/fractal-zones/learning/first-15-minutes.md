# Lernpfad 1: Erste 15 Minuten

**Voraussetzung:** Fractal Zones ist auf einem neutralen Chart geladen. **Ziel:** Du erkennst Ursprung, Reife und sichtbaren Linienzustand, ohne die Break- oder Recovery-Logik zu verändern.

## Minute 0–3: Orientierung

- Öffne die Einstellungen und finde die neun Produktgruppen.
- Prüfe `Before (minutes)=30`, `After (minutes)=30` und `Rendering mode=Adaptive`.
- Merke dir: Die Entscheidung basiert auf MIN1-Zeit, nicht auf der Anzahl sichtbarer Chartkerzen.

## Minute 3–8: Top und Bottom lesen

- **Top-Origin:** standardmäßig grüne Linie.
- **Bottom-Origin:** standardmäßig rote Linie.
- **Dot:** provisorisch; die rechte Reifezeit ist noch nicht vollständig bestätigt.
- **Solid:** ab dem Bestätigungszeitpunkt aktiv. Der frühere provisorische Abschnitt bleibt segmenttreu gepunktet.
- **Dash:** nach einem bestätigten Bruch historisch weiter beobachtet.

Beispiel: Ein Hoch entsteht um 10:00 Uhr. Mit `After=30` kann es frühestens nach 30 gültigen Sessionminuten bestätigt werden. Die Linie von 10:00 Uhr bis zur Bestätigung bleibt Dot; erst der folgende Abschnitt ist Solid.

## Minute 8–12: Drei Ebenen trennen

| Ebene | Frage |
|---|---|
| Semantik | Welcher Zustand gilt zu welchem Zeitpunkt? |
| Darstellung | Welche Segmente und Marker liegen im Viewport? |
| Betrieb | Sind Historie, Datenkontinuität und Restore vollständig? |

Ein Wechsel zwischen `Adaptive`, `Full` und `Active focus` darf die berechneten Level nicht verändern.

## Minute 12–15: Sicherer Abschluss

- Ändere nichts an den Action-Settings `Verify full history now…` und `Cancel full-history verify`.
- Prüfe die [vollständige Einstellungstabelle](../configure/index.md).
- Stelle versehentlich geänderte Werte auf `30 / 30 / Adaptive` zurück.

**Erwartetes Ergebnis:** Du kannst Dot, Solid und Dash erklären und weißt, warum Farbe und aktuelle Rolle nicht dasselbe sind.

**Vertiefung:** [Kurz/Praxis/Technik zur Fraktallogik](../understand/time-and-fractals.md) · [Zustandsablauf](../understand/lifecycle.md)
