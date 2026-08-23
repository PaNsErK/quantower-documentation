# Retest, Rollenwechsel und Ende

Nach einem Break wird das Level als `BrokenWatch` historisch gestrichelt fortgesetzt. Nur tatsächliche geschlossene Bars dürfen einen Retestkontakt beginnen. Die Retest-Bestätigung nutzt offene Sessionminuten und denselben strikten Neutralzonen-Reset.

## Zwei bestätigte Rückkehrpfade

- **RoleChange:** Support wird Resistance oder umgekehrt. `CurrentRole` ändert sich und `CurrentRoleBreakCount` startet neu.
- **RoleReaffirmation:** Die bestehende Rolle bestätigt sich erneut. Der Rollenzähler bleibt erhalten.

Beide beginnen ab Commit ein neues `Active/Solid`-Segment. Die Farbe bleibt vom `OriginType` abhängig: Ein ursprünglich aus einem Swing High entstandenes Level wechselt nicht automatisch die Farbe. Dadurch bleibt seine Herkunft nachvollziehbar.

## Ende

Standardmäßig endet das Level beim dritten committed Break der aktuellen Rolle. Es wird exakt am Confirmation-Close beendet. Es gibt keine nach rechts fortgesetzte Ended-Linie; ein optionaler Endmarker kann den Zeitpunkt zeigen.

--8<-- "docs/includes/diagrams/role-change.md"

Weiter: [Lifecycle und Linien konfigurieren](../configure/lifecycle-and-lines.md).
