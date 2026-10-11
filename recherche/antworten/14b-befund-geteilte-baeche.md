# Antwort zu Auftrag 14b – Geteilte Bäche: trockene Becken, Vorhang-Rechtecke (UE 5.8.3)

Stand 11.10.2026 – **Vorfassung**, Recherche läuft. Endfassung folgt in diesem Commit-Strang.

## Kurzfazit (vorläufig)

- Bilder `DEKOR1_C2_*` zeigen in den Becken nur schmale, kantige Wasserstreifen; das Bett liegt trocken. Vor dem Teilen war Wasser sichtbar.
- Arbeitshypothese: Die kurzen Epic-Flussstücke (4,5–5,6 m) werden über Wassernetz und Water-Info-Textur (~1,18 m/Texel) gezeichnet;
  Ränder, Dilatation und die Lücken zwischen den Stücken fressen das Becken weitgehend auf.
- Richtung der Lösung: Becken nicht mehr als einzelne kurze `WaterBodyRiver`, sondern eigene, garantiert sichtbare Flächen.
  Details folgen.
