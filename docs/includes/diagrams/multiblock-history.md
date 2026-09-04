```text
Provider-Historie
  Block 1 ──► Cache ──► kanonische Minuten
  Block 2 ──► Cache ──► kanonische Minuten
  …
  Block N ──► genau ein DirectReload-Fallback, falls erforderlich
                       │
                       ▼
              Ready oder recoverable Incomplete
```

Es werden keine synthetischen Minuten erzeugt. Eine belegte Anbietergrenze oder Lücke bleibt als begrenzter Datenstatus sichtbar und darf nicht als vollständige Projektion ausgegeben werden.
