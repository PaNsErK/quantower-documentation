# Fractal Zones

Fractal Zones erkennt zeitnormalisierte Swing-Extrema aus kanonischen Ein-Minuten-Daten und zeichnet daraus segmenttreue horizontale Level. Es sind **keine Pivot Points**: Ein Kandidat entsteht aus einem strikten lokalen Hoch oder Tief und reift über reale offene Sessionminuten links und rechts.

!!! info "Versionen richtig lesen"
    **Fractal Zones** ist der sichtbare Produktname. Produktgeneration, Dokumentationsvertrag, FZCP-Spezifikation und Runtime-Evidenz besitzen getrennte Versionsachsen. Der [aktuelle Stand](current-state.md) weist sie einzeln aus.

## Das Wichtigste in einem Bild

```text
Candidate → Provisional/Dot → Active/Solid → BreakPending
                                      ↓ bestätigt
                               BrokenWatch/Dash
                                      ↓ Retest
                      RoleChange oder RoleReaffirmation
                                      ↓
                                Active/Solid
                                      ↓ terminaler Bruch
                                   Ended
```

- Frühere Segmente werden nicht rückwirkend umgestylt.
- Top-Ursprung bleibt grün, Bottom-Ursprung rot – auch nach Rollenwechsel.
- Linien werden nicht geclustert, gemergt, gesampelt oder unterdrückt.
- Berechnung ist timeframe-unabhängig; der Chart-Timeframe ist nur die Ansicht.
- Vier Calculation-Range-Modi reichen vom festen 90-Tage-Fenster bis zur dynamischen Active-Level-Range; die dynamische Variante ist ein Berechnungsscope, kein optischer Linienfilter.
- Datenlücken, Sidecar-Fehler und Quotenprobleme degradieren fail-closed statt unvollständige Ergebnisse als vollständig zu veröffentlichen.

## Drei Tiefen

=== "Kurz"
    Starte mit [Erste 15 Minuten](learning/first-15-minutes.md) und [Current State](current-state.md).

=== "Praxis"
    Nutze [Alle Einstellungen](configure/index.md), den [dynamischen Historienbereich](understand/dynamic-history.md), die Simulatoren und die [interaktive Testsuite](test/manual-suite.md).

=== "Technik"
    Lies [Break Engine](understand/break-engine.md), [Mehrblock-Historie](understand/multiblock-history.md), [Recovery](understand/recovery.md) und [Runtime-Acceptance](test/runtime-acceptance.md).

!!! warning "Sicherheitsgrenze"
    Fractal Zones ist ein nicht-tradender Indikator. Tests bleiben auf Chart- und Indikatoroberflächen.
