# Lernpfad 4: Rendering und Historie

**Dauer:** 20–30 Minuten. **Ziel:** Erkennen, welche Einstellung nur zeichnet und welche den Berechnungsumfang verändert.

## Rendering-Modi

| Modus | Beobachtung |
|---|---|
| Adaptive | Standard; erzeugt einen viewportbezogenen Darstellungsplan ohne Linienverlust |
| Full | zeigt alle im relevanten Darstellungsbereich liegenden Segmente vollständig |
| Active focus | aktive Linien bleiben voll sichtbar; Provisional und BrokenWatch verwenden `Inactive state opacity` |

Wechsle nacheinander `Adaptive → Full → Active focus → Adaptive`. Pan und Zoom dürfen keinen semantischen Rebuild auslösen. Es wird nicht geclustert, zusammengelegt, gesampelt oder unterdrückt.

!!! warning "Bekanntes Residual FZRUI-01"
    Der Quellstandard für `Inactive state opacity` ist `0,35`. Eine frühere Runtime-Beobachtung zeigte `0`; die Ursache ist statisch als fehlende Dezimaldarstellungs-Konfiguration eingegrenzt. Bis zur separaten Produktkorrektur den UI-Wert nicht als neuen Standard interpretieren.

## Historienmodi

| Modus | Beispiel | Bedeutung |
|---|---|---|
| Fixed initial history days | `90` Tage | stabiler Standardumfang ab abgeleitetem oder explizitem Start |
| Chart loaded range plus warm-up | Chartbereich | berechnet den geladenen Bereich plus automatisch nötige Vorgeschichte |

Ein expliziter `Calculation start` wird in Plattformzeit angezeigt und intern UTC verarbeitet. Der Quell- und Hosttest-Vertrag enthält einen Enable-Toggler; seine konkrete Hostdarstellung bleibt FZRUI-02.

**Erwartet:** Rendering-Wechsel verändern keine Level. Ein History-Wechsel darf einen kontrollierten Rebuild verursachen, aber keine teilweise Generation veröffentlichen. Derselbe MIN1-Quellbereich soll über Chart-Timeframes hinweg identische Entscheidungen liefern.

**Zurücksetzen:** `Rendering=Adaptive`, `Inactive opacity=0,35`, `Calculation range=Fixed initial history days`, `Initial range=90`, `Calculation start=unset`.

**Vertiefung:** [Darstellung und Marker](../understand/rendering.md) · [Rendering, Marker und Historie einstellen](../configure/rendering-and-history.md)
