# Zustandsablauf

```text
Provisional ──Reife──> Active ──bestätigter Bruch──> BrokenWatch
                           ^                           |
                           └──── Retestbestätigung ────┘
                               RoleChange/Reaffirmation

BrokenWatch ──terminaler Break──> Ended
```

## Segmenttreu statt rückwirkend

Jeder Zustandswechsel schließt das bisherige Segment und beginnt ein neues. Die provisorische Vergangenheit bleibt Dot; ab Bestätigung beginnt Solid. Nach einem Bruch beginnt Dash. Diese Zeitlinie zeigt, **wann** der Markt welchen Zustand kannte.

## Zähler

- `LifetimeBreakCount` zählt jeden committed Break und wird nie zurückgesetzt.
- `CurrentRoleBreakCount` zählt nur innerhalb der aktuellen Rolle.
- Ein echter `RoleChange` setzt den Rollenzähler zurück; `RoleReaffirmation` nicht.
- Der terminale Break wird zuerst atomar gezählt und committed, danach wird `Ended` gesetzt.

`Ended` ist unveränderlich und besitzt keinen fortlaufenden Ended-Linienstil. Optional bleibt nur der Endmarker am exakten `EndTimeUtc`.

--8<-- "docs/includes/diagrams/lifecycle.md"

Weiter: [Retest, Rollenwechsel und Ende](role-and-ended.md).
