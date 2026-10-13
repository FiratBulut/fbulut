# 16h Nachtrag 6f – Bettplan 6c EINGEBAUT (C2, gespeichert): Messung, Bilder, drei Probleme

Stand 13.10. 22:05. Euer Plan ist gebaut: Gelände C2 (Abtrag 1 357 m³ / Auftrag 99 m³, Delta −2,90…+1,39 m, Weltkarte
`bilder/swr_p2/bettplan_delta_welt.png` – keine Gruben abseits), 621 Blöcke/Kies (216 mit Kollision), Spline-Z = Plan-Spiegel, Hindernisse
906 + 5 Beckenblöcke, Texturen (Spiegel 2 m, Bachgewicht, Bewuchs) neu, Simulation 5 min, gebacken, gespeichert.
Werkzeugweg: Cloud `p2_bett_welt.py` las `lauf_p2.json` nicht (parallele Listen → `TypeError`); lokale Kopie `scripts/cloud/p2_bett/`. `a15_einbau.py` kann
euer Format NICHT lesen (verlangt `wasser_koerper`) → eigener Adapter `scripts/swr/p2_bett_einbau.py` (Gelände-Datensatz im sehens_einbau-Format,
Instanzen FORMAT §3, Spline-Z, Prüfband). Euer Format ist in Ordnung, nichts ändern.

## 1. Messung nach dem Bake (frischer Dump, `p2bett_pruefband.py`, Kriterium 6b)

| Größe | Wert | Ziel |
|---|---|---|
| Bett nass | 100 % | ≥ 99 % |
| **Band 0,25–2 m hinter der neuen Bettkante nass** | **85 %** | ≤ 5 % |
| Tiefe im Bett Median / p90 | 0,40 / 0,72 m | Kolk 0,8–1,2 |
| Front | 788/788 m | 788 |
| nasse Zellen gesamt | 11 175 (vorher 10 649) | – |

**Ursache des Überlaufs (gefunden):** Die Uferstufe im Gelände stimmt (0,5 m hinter der Kante Median +0,21 m über dem Spiegel, 0,8 % darunter).
Aber die SWR füllt zur **Spline-Höhe**, und die Editor-Spline hat in s 389–580 nur **54 Punkte (~3,5 m)** – zwischen Lippe und Kolk verschmiert sie die
Stufe (an den Punkten bis 0,9 m über dem Plan-Spiegel, z. B. s 398 Soll 98,81 m, Spline 99,72 m). → Wir setzen **Spline-Punkte je 1 m** aus
`spline_z.json` (Werkzeug in Arbeit, Ferat: „mach es“), dann neu füllen, messen, backen. Ferat wollte zuerst „die Spline einen Tick höher“ – das
würde den Überlauf verstärken; wir machen erst die dichten Punkte, dann prüft er die Wassermenge.
Zweiter Fund: Nach einem Bake steht die Darstellung auf WCBS; ein Reset ohne LIVE_SIM simuliert NICHT (Auftrag 230 backte 5 min Leere; jetzt
im Reset-Werkzeug fest).

## 2. Bilder (`bilder/swr_p2/bettplan_p2c_vorher_nachher.jpg`, `bettplan_p2c_oben.jpg`)

- **Gut:** Von oben liest sich die Talkaskade jetzt als Step-Pool-Kette: Kolke unter den Kerben, Blocklippen, bemooste Blöcke, Seitenwechsel.
- **Problem A – Einschnitt-Böschungen schwarz:** Die zurückgelegten Böschungen (Zonen Stufenwand/Böschung) erscheinen als schwarz-braune
  Felswände (t430/t550 links). Die Lagen je Zone hat unser Agent aus B2/Uferplan abgeleitet (`antworten/fluss_sim/p2_lokal/p2_bett_lagen_regeln_lokal.json`,
  Annahme!). Bitte die Lagen je Zone vorgeben (Böschung: Erde/Geröll/Gras-Reste statt Fels? Stufenwand: Fels nur an den Lippen?).
- **Problem B – Beckenwasser braun-trüb**, Oberfläche zäh (S6-Grund + Absorption F; tiefere Kolke 1 m sollten jetzt dunkler/klarer wirken – tun
  sie noch nicht, weil die Kolke erst 0,72 m (p90) Wasser haben, s. Überlauf/Spline).
- **Problem C – Blöcke:** Einzelne Lippenblöcke 1,5–1,8 m wirken an der Kamera riesig (t430: Mountain-Block grau, Paketmaterial); 20 Netztypen
  ohne unsere MI (Mountain/Fab) – Optik ok, aber keine Nasslinie.
- Kies-Fächer und Keystones sind klein und noch nicht beurteilbar (Kamera im Ufergras: der Halm im t500-Bild ist die Kamera, kein Weltfehler).

## 3. Fragen

1. Lagen je Zone (Problem A) – bitte als Tabelle Zone → Lagen-Mischung.
2. Nach dem Verdichten der Spline: Wenn das Band immer noch > 5 % nass ist – `remove_outside` 50 (F1) oder Band schmaler? Reihenfolge?
3. Beckenfarbe bei 1 m Tiefe: Absorption F (222/1000/1250) – reicht das für „dunkel“ im Kolk, oder Kind-Instanz „bergbach klar“ (3.3 aus N6)?
