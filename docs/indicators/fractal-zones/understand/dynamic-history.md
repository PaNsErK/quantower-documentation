# Dynamische Historie

Der vierte `Calculation range mode` heißt **Dynamic active-level price range**. Er richtet den Berechnungs- und Publikationsscope an offenen, aktiven Solid-Levels relativ zum letzten vollständig geschlossenen kanonischen MIN1-Schluss aus.

--8<-- "docs/includes/diagrams/dynamic-history-range.md"

<div data-fz-simulator="dynamic-history"></div>

## Die drei zugehörigen Einstellungen

| Einstellung | Standard | Sichtbar wann? | Bedeutung |
|---|---:|---|---|
| Active-level price range (+/- %) | 10,00 % | dynamischer Modus | Zielband um den letzten MIN1-Schluss |
| Dynamic history horizon | All available provider history | dynamischer Modus | Anbieterhistorie vollständig oder begrenzt anfordern |
| Dynamic history (days) | 365 | Bounded days | begrenzter Tageshorizont |

Das Zielband hat eine Hysterese: Bei 10 % Zielband wird erst außerhalb des erweiterten Reservenbands eine neue Dynamikentscheidung nötig. Das reduziert unnötige Rangewechsel, ohne den Inhalt einer bereits veröffentlichten Generation umzudeuten.

!!! warning "Keine Zonenbildung"
    Dynamische Historie führt **nicht** zu Clustering, Merging, Sampling, Suppression oder Löschen gezeichneter Linien. Eine spätere Zonenfunktion ist ein getrenntes Produktthema.

Ist der Anbieteranfang für den gewählten Scope nicht belegbar, bleibt der Datenstatus recoverable `Incomplete`; der Indikator publiziert keinen künstlich vollständigen Zustand.
