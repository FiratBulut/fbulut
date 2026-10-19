# Auftrag 16h-6t – Wasserplatte an der Mündung: Ursache ist der alte Epic-Fluss C3_Fluss_F_ERLENBACH_2, nicht die SWR; Zonen C3/D3 auf 4096 gespeichert

Stand 19.10.2026 18:00. Bezug: Antwort 16h-6s (0bcecb5) §2. Bild: `bilder/swr_p2/muendung_t9_t10_zsp.jpg` (4 Zeilen, Mündungskamera, je 2 Ausschnitte).

## 1. Einzeltests nach 6s §2 (je harter Neustart, nur Speicher, Bake-Dump vorher/nachher bitgleich)

| Test | Wirkung |
|---|---|
| T1 `swr_set_render_state(BAKED_SIM)` erneut | keine (aus T6R) |
| T2 `bottom_contour_capture_offset` gleich setzen | keine |
| T3 `use_capture` aus | keine |
| T4 Nanite der 4 Landschaftsteile um die Mündung | keine (Teile waren schon aktuell, „nicht aktuell 0“) |
| T6 Felder C2/C3/D2 geladen + 90 s, dann T1 | keine (in allen Tests enthalten) |
| **T9** `C3_Fluss_F_ERLENBACH_2` im Editor ausgeblendet | **alles Wasser an der Mündungskamera weg** (Zeile 2) |
| T10 Zonen C3/D3 `render_target_resolution` 1024 → 4096 + `rebuild_native_body` beider Flussstücke | Treppen weg, Rand glatt (Zeile 3) |

**Ergebnis:** Die Wasserplatte mit Treppenrand ist der **alte Epic-Fluss F_ERLENBACH_2** (C3/D3, Houdini-Zeit; Kopf am 13.10. für die p2-Mündung umgestellt:
Punkte 0–2 auf dist 24/31/38 m, Breiten 7/11/14/17/22 m), nicht die p2-SWR. Sie wird über die Wasser-Info der Zone C3 gezeichnet (1024 = 1,18 m/Pixel →
Treppen von ca. 1 m). Ferats Vermutung „Houdini-Reste“ stimmt.

## 2. Umgesetzt

- **Zonen C3 und D3 auf 4096 gespeichert** (wie C2 seit 13.10.), Speicherbeleg für beide Pakete, nach Neustart 4096 bestätigt.
- **Frisch nach Neustart (Zeile 4):** Die Stufen sind jetzt etwa 0,3 m statt 1,2 m. Der alte Fluss zeichnet aber weiter eine flache Platte mit
  senkrechtem Rand über trockenem Kies, links sogar etwas breiter. Nach einer Landschaftsänderung bzw. mit `rebuild_native_body` (T10) ist der Rand
  glatt.
- **Ferat 17:00:** Das Erlenbach-Skript (SWR) wird auf die anderen Bäche übertragen. Ein Rollout-Plan ist in Arbeit. Der alte F_ERLENBACH_2 wird dabei
  durch die SWR-Fortsetzung ersetzt: ein Fluss von der Quelle bis zur Mündung.
- **Nebenbei:**
  - 41 doppelte `ELWaterAdapter`-Akteure (zeichnen nichts) aus der Karte genommen, verschoben in die Sicherung.
  - Viele Feld-Wasserzonen melden 40-km-Grenzen ihres WaterMesh (A3, B3, B5, B6, D5–D7, E3, F1, F2, F4–F6, H3, H7). C2/C3/D2/D3 dagegen 604 m.

## Fragen

1. **Platte nach Neustart:** Warum zeichnet ein Epic-WaterBodyRiver direkt nach dem Editorstart Wasser über trockenem Boden, als fehle die Bodentiefe in
   der Wasser-Info? Und warum heilt `rebuild_native_body` bzw. eine Landschaftsänderung das, ein Zonen-Neuaufbau oder ForceUpdateWaterInfo aber nicht?
   Tritt das im Spiel genauso auf? Gibt es eine Einstellung am Fluss oder an der Zone, z. B. Wasser-Info mit Landschaft erst nach dem Streaming?
2. **Übergang bis zum Rollout:** Sollen wir den alten Fluss nach jedem Start per Subsystem einmal neu aufbauen lassen (eigener C++-Code in
   `EldarienMap`)? Oder lieber gleich die Fortsetzung als SWR (Rollout-Pilot 1)?
3. **40-km-Grenzen der WaterMesh-Komponenten:** Ist das normal (Fernfläche?), oder sollten wir die Felder-Zonen prüfen? Kosten im Spiel?
4. **4096 für alle Zonen mit schmalen Bächen** (Rollout): Was kostet es an Grafikspeicher, wenn 20–30 Zonen auf 4096 stehen? Und gilt die Regel
   „Breite < 6 m → 4096“?
