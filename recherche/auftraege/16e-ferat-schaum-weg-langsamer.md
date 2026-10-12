# Auftrag 16e – Ferat zu den Bächen: Schaum weg, langsamer, Tempo nach Steigung

Stand 12.10.2026, 18:50. Ferat nach den C2-Bildern (SWR, gebacken, WCBS, `MI_EL_SWR_Klar`):

> „Bei den Bächen fällt mir auf: zu viel Schaum, das zeigt es unnatürlich. Vielleicht auch Fließgeschwindigkeit je nach Steigung anpassen. Ich habe
> das Gefühl, das Wasser fließt einen Tick zu schnell. Ich würde Schaum komplett wegmachen, damit man Wasser sieht. Dann nur bei Wasserfällen
> vielleicht ein wenig Schaum.“

## Bitte festlegen (für `fluss_sim` und die Material-Werte)

1. **Schaum:** in Bächen und Flüssen grundsätzlich aus (Simulation + Material), nur an Fällen (Aufprall/Vorhang) wenig. Welche Werte in
   `M_Eldarien_Wasser_Schaum8`-Instanzen bzw. im Niagara-System (`Grid2D_SW_River`) schalten den Simulationsschaum wirklich ab, ohne die
   Wasseroberfläche (Normalen, Spiegelungen) zu verlieren? Lokal teste ich vorab `Foam Opacity` 0 / `Foam Boost` 0 / `Sim Foam Scale` hoch.
2. **Tempo nach Steigung:** Regel für `WaterVelocityScalar` je Splinepunkt (heute aus `tempo` des Plans) abhängig vom Gefälle (flache Becken
   langsam, Schnellen schneller), insgesamt etwas langsamer als heute. Dazu: welche Material-Parameter steuern, wie schnell die Oberfläche
   sichtbar „fließt“ (`Simulation Flowmap Speed` 0,75, `SIm Flowmap Speed` 1,5, `River Flowmap Speed`, `MaxFlowVelocity` 1024 …), und welche
   SWR-Werte (`sim_speed` 10, `num_steps` 10) die Strömung der gebackenen Simulation beeinflussen?
3. Bitte Werte + kurze Begründung; lokal setze ich sie um und schicke Bilder.
