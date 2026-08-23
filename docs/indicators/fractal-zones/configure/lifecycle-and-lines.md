# Lifecycle, Linien und Break-Boundary konfigurieren

## Retest und Ende

- `Retest confirmation (minutes)` – Standard 5: Nur reale geschlossene Bars können einen Kontakt starten. Die Bestätigung zählt offene Sessionminuten; Neutralzone setzt strikt zurück.
- `End on current-role break number` – Standard 3: Der terminale Break wird zuerst atomar committed und gezählt; danach endet das Level exakt am Confirmation-Close.

`RoleChange` ändert die aktuelle Rolle und setzt `CurrentRoleBreakCount` zurück. `RoleReaffirmation` bestätigt dieselbe Rolle. Beide beginnen ab Commit ein neues Active/Solid-Segment. `LifetimeBreakCount` wird nie zurückgesetzt.

## Segmenttreue Linien

| Zustand | Standard | Bedeutung |
|---|---|---|
| Provisional | Dot, 1, Top grün / Bottom rot | noch nicht reifer Kandidat |
| Active | Solid, 1, Top grün / Bottom rot | bestätigtes aktuelles Segment |
| BrokenWatch | Dash, 1, Top grün / Bottom rot | historisch fortgesetzt und für Retest beobachtet |
| Ended | kein eigener Stil | Linie endet vollständig am EndTimeUtc |

Jede LineOptions-Zeile bietet `Solid`, `Dash`, `Dot`, `DashDot`, Breite 1–10 und Color Picker. `Show provisional lines` beziehungsweise `Show historical lines` sind reine Sichtbarkeitsschalter. Frühere Segmente werden weder umgefärbt noch rückwirkend solid gemacht.

## Ursprungsfarbe statt Rollenfarbe

Top-Origin bleibt in der Voreinstellung grün, Bottom-Origin rot. Ein Support→Resistance- oder Resistance→Support-Wechsel tauscht die Farbe nicht. Dadurch bleibt sichtbar, aus welcher Fraktalart das Level ursprünglich entstand.

## Current break boundary

Die optionale Boundary zeigt **genau die aktuelle handlungsrelevante Grenze** eines aktiven Segments. Standard: aus, Dot, Breite 1, Gelb. Der optionale Connector verbindet am Start des aktuellen Segments Hauptlinie und Boundary vertikal. Er verlängert keine historischen oder beendeten Segmente und verändert keine Semantik.

<div data-fz-simulator="break-boundary"></div>
