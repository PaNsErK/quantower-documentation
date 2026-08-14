# Lernpfad 4: Rendering und Historie

**Dauer:** 20–30 Minuten. **Ziel:** Erkennen, welche Einstellung nur zeichnet und welche den Berechnungsumfang verändert.

## Rendering-Modi

| Modus | Beobachtung |
|---|---|
| Adaptive | Standard; erzeugt einen viewportbezogenen Darstellungsplan ohne Linienverlust |
| Full | zeigt alle im relevanten Darstellungsbereich liegenden Segmente vollständig |
| Active focus | aktive Linien bleiben voll sichtbar; Provisional und BrokenWatch verwenden `Inactive state opacity` |

Wechsle nacheinander `Adaptive → Full → Active focus → Adaptive`. Pan und Zoom dürfen keinen semantischen Rebuild auslösen. Es wird nicht geclustert, zusammengelegt, gesampelt oder unterdrückt.

!!! success "FZRUI-01 in der Runtime bestätigt"
    `Inactive state opacity` zeigt den Standard `0,35` mit zwei Dezimalstellen. Ein Schritt auf `0,40` und zurück auf `0,35` verändert nur die vorgesehene Deckkraft; Linienauswahl, Level und Zustände bleiben identisch.

## Historienmodi

| Modus | Beispiel | Bedeutung |
|---|---|---|
| Fixed initial history days | `90` Tage | stabiler Standardumfang ab abgeleitetem oder explizitem Start |
| Chart loaded range plus warm-up | Chartbereich | berechnet den geladenen Bereich plus automatisch nötige Vorgeschichte |

Ein expliziter `Calculation start` wird in Plattformzeit angezeigt und intern UTC verarbeitet. Quantower BusinessLayer 1.146.17.0 zeigt den DateTime-Editor, aber keinen separaten nativen Enable-Toggler. Diese bestätigte Hostdarstellungsgrenze ändert weder den Enabled-Zustand des abhängigen Feldes noch die hosttestbestätigte UTC- und Clear-Semantik.

**Erwartet:** Rendering-Wechsel verändern keine Level. Ein History-Wechsel darf einen kontrollierten Rebuild verursachen, aber keine teilweise Generation veröffentlichen. Derselbe MIN1-Quellbereich soll über Chart-Timeframes hinweg identische Entscheidungen liefern.

**Zurücksetzen:** `Rendering=Adaptive`, `Inactive opacity=0,35`, `Calculation range=Fixed initial history days`, `Initial range=90`, `Calculation start=unset`.

**Vertiefung:** [Darstellung und Marker](../understand/rendering.md) · [Rendering, Marker und Historie einstellen](../configure/rendering-and-history.md)
