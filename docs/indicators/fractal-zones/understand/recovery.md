# Kontinuität, Sidecar und Wiederherstellung

Fractal Zones veröffentlicht nur vollständige Generationen. Bei Datenlücke, Revision, Restore oder Deep Verify bleibt die letzte gute Projektion sichtbar, bis ein Offscreen-Replay vollständig validiert und atomar ausgetauscht wurde.

## Recovery-Kette

1. `checkpoint-current`
2. `checkpoint-previous`
3. jüngster gültiger geschützter Restore Point
4. vollständiger Rohneuaufbau

Hashes, StateIdentity, ReplayGeneration und Tagged Unions werden fail-closed geprüft. Unbekannte oder beschädigte Daten werden quarantänisiert und niemals teilweise veröffentlicht.

## Quoten und Degradierung

Das content-addressed Sidecar nutzt Deduplication und geschützte Wurzeln. Standard sind 512 MiB Persistenz pro StateIdentity und 4 GiB pro Sidecar-Root. Wird die Quote erreicht, pausieren nur optionale Restore-Point-Schreibvorgänge. Berechnung, Rendering, aktuelle Generation und bestmögliche Crashrotation laufen weiter; Levels werden nicht reduziert.

## Deep Verify

`Verify full history now…` startet eine asynchrone Single-Flight-Prüfung, `Cancel full-history verify` bricht nur die optionale Prüfung sicher ab. Ein sauberer Lauf erzeugt keine neue Generation. Erkannte Dirty Blocks gehen durch denselben Offscreen-Replay-Pfad.

Weiter: [Performance und Sidecar](../troubleshoot/performance-and-sidecar.md).
