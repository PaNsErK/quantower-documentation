# Aktueller Stand

Die Dokumentation beschreibt den aktuellen gemergten und technisch runtime-validierten Stand von **Fractal Zones v2**.

| Fläche | Aktueller Zustand |
|---|---|
| Produktinventar | 56 Setting-Zeilen, 7 LineOptions, 70 atomare Controls, 2 Aktionen |
| Konformität | FZ-001..FZ-102, GT-01..GT-180, MVA-01..MVA-25; FZCP v1–v4 |
| Lokale Tests | vollständig bestanden |
| Deployment | flaches Neun-Dateien-Paket, 9/9 Hashparität |
| Runtime-Gate | MVA-17..25 abgeschlossen; 10k/30k/ca. 130k; 2.700,009 s Soak; 188/188 responsiv |
| Benutzerabnahme | `manual_acceptance_complete=false` |
| Neue Benutzerfälle | 19 Fälle, `pending_user_evaluation`, Ergebnisse und Notizen leer |

`runtime_acceptance_complete=true` bedeutet nicht, dass der Benutzer die 19 neuen Bewertungsfälle schon bestätigt hat. Beide Ebenen bleiben absichtlich getrennt.

## Was neu im dokumentierten Stand ist

- `Break price source`: Close oder High/Low; doppelseitige High/Low-Candles werden als `AmbiguousBothSides` behandelt.
- Echte Nullschwellen: Distanz und Break-Bestätigung dürfen null sein.
- Break-Boundary mit optionalem vertikalem Connector.
- Statusoverlay mit Loading, Recalculating, Ready, Incomplete und Error.
- Reversibler Preisrelevanzfilter als reine Anzeigeabfrage.
- Offene Linien enden wahlweise an aktueller Bar, nach Minuten oder Chartkerzen.
- Getrennte Markerfarben, X-Modi, X/Y-Offsets und Schriftgrößen.
- Drei History-Modi einschließlich bestätigt gespeichertem Fixed Start und automatischem/manuellem Warm-up.
- Settings-Generation, atomarer Redraw und Semantic Snapshot V2 ohne doppelte Replay-Bar-Kopie.

## Verbleibende Warnung

Die technische Abnahme enthält eine akzeptierte, nicht blockierende Persistenz-/Quotenwarnung. Ein persistenter Root oberhalb der 4-GiB-Grenze pausiert optionale Sidecar-Schreibvorgänge. Kernberechnung, Rendering, Restore-Fallback und sicherer Raw Rebuild bleiben funktionsfähig. Details: [Performance und Sidecar](troubleshoot/performance-and-sidecar.md).
