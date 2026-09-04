# Performance und Sidecar

## Rendering-Latenz

Adaptive nutzt Viewport-Indizes und Render-Plan-Cache; Full ist der Referenzweg. Pan/Zoom darf keinen fachlichen Rebuild auslösen. Bei Vergleich immer gleichen Instrument-, Session-, Daten- und Chartzustand verwenden.

## Persistenzwachstum

Das Sidecar speichert content-addressed Chunks und dedupliziert identische Inhalte. Aktuelle Standardhüllen sind 256 MiB Live-State pro Identity, 1 GiB pro Prozess, 512 MiB Persistenz pro Identity und 4 GiB pro Root. StateIdentity bleibt über reine Darstellungsänderungen stabil.

## QuotaExceeded

QuotaExceeded bedeutet nicht, dass Linien fehlen. Es pausiert optionale Restore-Point-Schreibvorgänge. Geschützte Recovery-Wurzeln, Berechnung, Rendering und veröffentlichte Generation bleiben erhalten. Nach Pruning unter die Hysteresegrenze werden optionale Writes automatisch wieder zugelassen.

## Deep Verify ist keine Performance-Taste

Nutze Deep Verify bei Revisionsverdacht oder gezielter Diagnose. Mehrfachklicks werden Single-Flight koalesziert. Ein sauberer Lauf erstellt keine neue Generation.
