# Korrektur Runde 3 zu Auftrag 11: Felsgruppen (Bilder 10.10. 19:15 lokal)

Projekt Eldarien, UE 5.8.3. Priorität hoch. Runde 2 der Felsgruppen ist gesetzt (A5 5 563 Instanzen/316 Gruppen/45 Akteure, G4 1 448).
Bilder `bilder/cloud3/` (Nachher `CLOUD3_*`, Vorher Runde 1 `CLOUD2_A5_rundgang`, Klippen zum Vergleich `KLIPPE2_A5_fern`, Nahaufnahme `rote_findlinge_zoom.jpg`).

## Was besser ist

Die Pappe-Platten auf dem Gras sind weg, Kleinzeug sitzt nur noch um Gruppen. Danke.

## Was noch nicht stimmt

1. **Rote Findlinge:** `/Game/AncientContent/Megascans/…/SM_IcelandicBoulder_01/02/03` (auch als `_kol`) rendern terrakotta-rot (siehe Nahaufnahme,
   links am G4-Waldrand, rechts als orange Punkte am A5-Hang). Im Nordwald, an der Küste und im Elfenwald wirken sie fremd. Bitte nur noch in
   `canyon`, `oedland`, `wueste`, `lava` verwenden (lokal sind sie vorerst gesperrt). Nicht verwechseln mit den grauen
   `/Game/Megascans/…/SM_IcelandicBoulder_*` – die sind gut.
2. **Gruppen sind aus 300 m immer noch nur Punkte** (`CLOUD3_A5_rundgang`: Blick auf den Bergrücken, Hauptfels Median 5,3 m). Witcher-Maßstab für
   Bergflanken: Felskronen auf Graten und Kuppen sind **10–30 m** groß und verwachsen mit dem Hang (vgl. Klippen in `KLIPPE2_A5_fern`). Bitte:
   - Für Grat/Kuppe/Wandnase die großen Netze als Hero nutzen, skaliert 1,0–2,0: `/Game/Megascans/3D_Assets/…/SM_MassiveNordicCoastalCliff_01`,
     `SM_HugeNordicCoastalCliff_01/02`, `/Game/Fab/Megascans/3D/Sharp_Cliff_rcygn/…/rcygn_tier_0` (18,8 × 4,6 × 10,9 m),
     `Massive_Nordic_Coastal_Cliff_vdssailfa/vfmjadufa/veqnci0db` (20–37 m), `/Game/Mountain_Environment_Set/…/SM_big_rock_wall_0*`,
     `/Game/Environment_Set/…/SM_Big_Rock_0*` – als Akteure (Kollision), eingegraben 35–60 % (offene Seiten ins Gelände), Schichtneigung je Massiv
     wie bisher.
   - Je Feld nur **8–20 Formgruppen** dieser Größe auf den markantesten Graten/Kuppen (Krümmung + Sichtbarkeit von Tälern/Wegen aus), dazu
     Satelliten 2–6 m und Blockstrom am Fuß; Gesamtzahl der kleinen Instanzen darf sinken.
   - Keine Gruppe auf Wiesen ohne Hangknick.
3. **Fab-Netze** bekommen lokal das Klippenmaterial `MI_EL_Klippe_<kurz>` (RVT-Fußblend, Moos). `uchoab3fa` (Quarry Cliff) hat keins –
   bitte nicht verwenden.

## Lieferung

`antworten/skripte/felsgruppen_plan.py` + `felsgruppen_regeln.json`, kurzer Abschnitt „Runde 3“ in `verteilung-STATUS.md` mit erwarteten Zahlen
(Formgruppen je Feld, Hero-Größen). Ich setze A5/G4/B4 neu und vergleiche.
