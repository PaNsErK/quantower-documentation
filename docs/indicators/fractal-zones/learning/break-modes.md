# Lernpfade 2 und 3: Bruchmodi und Lifecycle

Die folgenden Beispielwerte dienen nur dem Verständnis. Beobachte dokumentiertes Verhalten auf einer nicht-tradenden Oberfläche und stelle danach die Ausgangswerte wieder her.

## Lernpfad 2: Bruchdistanz vergleichen

**Dauer:** 20–30 Minuten. **Ziel:** Verstehen, welcher Teil der äußeren Bruchgrenze absolut und welcher markt-/preisrelativ ist.

| Durchlauf | Beispielkonfiguration | Was du lernst |
|---|---|---|
| A | `One-minute ATR`, Periode `60`, Multiplikator `0,50`, Minimum `2` Ticks | Volatilitätsrelative Distanz auf einer timeframe-unabhängigen MIN1-Basis |
| B | `Percent of level`, `0,05 %`, Minimum `2` Ticks | Preisrelative Distanz mit Tick-Untergrenze |
| C | `Fixed ticks`, `2` Ticks | Absolute, instrumentabhängige Distanz |

Die Grenze wird am gültigen Tickraster nach außen quantisiert. Ein Minimum von zwei Ticks verhindert, dass eine relative Formel eine zu kleine Bestätigungsdistanz erzeugt.

**Erwartet:** Nur die sichtbaren Zweig-Settings wechseln. Die Linie gilt nicht schon beim ersten Überschreiten als gebrochen; `Break confirmation=5` verlangt eine fortlaufende Zeit außerhalb der neutralen Zone. Jede Rückkehr setzt den Timer strikt zurück.

**Typische Falle:** Ein kurzer Spike ist kein bestätigter Bruch. Ebenso darf Hin-und-her innerhalb weniger Minuten nicht mehrfach gezählt werden; dafür wirken strikter Reset und `Minimum between breaks=5` zusammen.

**Zurücksetzen:** `One-minute ATR / 60 / 0,50 / Minimum 2 / Confirmation 5 / Minimum between 5`.

**Vertiefung:** [Bruchlogik](../understand/break-engine.md) · [Maturity und Break Engine einstellen](../configure/maturity-and-break.md)

## Lernpfad 3: Lifecycle beobachten

**Dauer:** 25–40 Minuten. **Ziel:** Einen vollständigen, segmenttreuen Ablauf lesen.

1. Eine aktive Solid-Linie überschreitet die eingefrorene äußere Grenze.
2. `BreakPending` prüft intern die Bestätigungszeit; die Linie erhält dafür keinen neuen sichtbaren Stil.
3. Nach Bestätigung wird das neue Segment `BrokenWatch` und nutzt Dash.
4. Ein Retest beginnt nur durch reale geschlossene Bars. Rückkehr in die neutrale Zone setzt den Retesttimer strikt zurück; im selben Slot startet er nicht neu.
5. `RoleChange` ändert die Rolle und setzt `CurrentRoleBreakCount` zurück. `RoleReaffirmation` stellt ebenfalls Active/Solid her, ändert die Rolle aber nicht.
6. `LifetimeBreakCount` bleibt über Rollen hinweg erhalten. Beim standardmäßig dritten Bruch der aktuellen Rolle endet die Linie exakt am Commit-Zeitpunkt.

**Beispielwerte:** `Retest confirmation=5`, `End on current-role break number=3`, `Show role-change marker=true`, `Show end marker=true`, `Show break markers=false`.

**Erwartet:** Ein Rollenwechsel tauscht die Farbe nicht. Grün bleibt Top-Origin, Rot bleibt Bottom-Origin. Es gibt keinen Ended-Linienstil; nach `EndTimeUtc` wird nichts fortgezeichnet.

**Zurücksetzen:** Die Beispielwerte entsprechen den Standards. Falls du Marker geändert hast, stelle `End=true`, `Break=false`, `RoleChange=true` wieder her.

**Vertiefung:** [Retest, Rollenwechsel und Ende](../understand/role-and-ended.md) · [Lifecycle und Linien einstellen](../configure/lifecycle-and-lines.md)
