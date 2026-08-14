# Darstellung und Marker

<section markdown="1" class="fz-topic" data-topic="FZT-18" data-modes="understand configure">

## Ursprungsstabile Farben

<div markdown="1" class="fz-depth" data-depth="short">Top bleibt in der gewählten Top-Farbe, Bottom in der Bottom-Farbe – auch nach Rollenwechsel.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Die Farbe beantwortet „Wo entstand das Level?“. Linienart und Segment beantworten „Welchen Zustand hat es jetzt?“.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Farbe hängt an `OriginType`, nicht an `CurrentRole`. Dadurch bleibt die komplette Segmentgeschichte visuell konsistent und die Rolle wird nicht durch rückwirkende Farbwechsel verfälscht.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-19" data-modes="understand configure">

## Rendering-Modi

<div markdown="1" class="fz-depth" data-depth="short">Adaptive ist Standard, Full zeigt den vollständigen Stil, Active focus reduziert nur die Deckkraft inaktiver Zustände.</div>

<div markdown="1" class="fz-depth" data-depth="practice">

- **Adaptive:** optimierter Render-Plan bei vollständigem Inhalt.
- **Full:** direkte Vollprojektion als Vergleichs- und Diagnosemodus.
- **Active focus:** Active bleibt klar, Provisional und BrokenWatch werden mit einstellbarer Deckkraft gezeichnet.

</div>

<div markdown="1" class="fz-depth" data-depth="technical">Viewport-Segment- und Annotation-Indizes, Cache und source-identical timeframe reuse sind reine Performancepfade. Der semantische Vergleich gegen Full muss identisch bleiben.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-20" data-modes="understand test">

## No-cluster-Vertrag

<div markdown="1" class="fz-depth" data-depth="short">Kein Clustering, Zusammenlegen, Sampling, Löschen oder Unterdrücken.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Auch wenn viele Linien nah beieinanderliegen, bleibt jede einzelne Linie erhalten. Eine spätere Zonenbildung ist ein eigener Produkt-Slice.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Performanceoptimierung darf nur Kandidaten außerhalb des Viewports schneller ausschließen oder einen identischen Render-Plan wiederverwenden. Anzahl und Identität sichtbarer Segmente bleiben unverändert.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-21" data-modes="understand configure">

## Marker und Segmentgeschichte

<div markdown="1" class="fz-depth" data-depth="short">Standard: End- und Rollenwechselmarker an, Bruchmarker aus.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Marker erklären Ereignisse, die eine Linie allein nicht vollständig zeigt. DATA GAP und EPOCH kennzeichnen Datenkontinuität; sie sind keine Trading-Signale.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Marker sind indexierte Annotationen. Reine Sichtbarkeitsschalter dürfen weder Reducer, ReplayGeneration noch Levelsemantik verändern.</div>

</section>

## Linienarten

Fractal Zones bietet bewusst nur `Solid`, `Dash`, `Dot` und `DashDot`. Quantower kennt weitere `LineStyle`-Werte, sie passen aber nicht zum horizontalen Segmentvertrag dieses Indikators.
