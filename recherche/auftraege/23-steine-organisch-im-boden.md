# Auftrag 23 – Steine, Platten und Totholz sollen organisch im Boden sitzen

Stand 18.10.2026, 19:55 PC-Uhr. Auftraggeber Ferat, weitergegeben von Opus-PM. Bezug: Platzierungsauftrag PLZ-2026-10, Antworten 16h-N3, 20, 22/22b.

## 1. Was Ferat sagt (wörtlich)

- „Bei komisch platzierten Assets habe ich genau solche gemeint.“ (dazu ein Bild mit acht Kreisen, siehe §2)
- „Nicht nur meine eingekreisten, sondern alle, die so aussehen. Assets-Positionierungen sind schlecht.“
- „Ja, die müssen organisch in den Boden passen.“

Die bisherige Platzierungsreparatur (v3, 16 967 Instanzen in 58 Feldern) hat nur Pflanzen und Bäume im Wasser, Bäume und Büsche auf Wegen und
ineinander gewachsene Bäume entfernt. Schwebende, schräge oder hochkant stehende Steine waren dort **ausdrücklich ausgeklammert**. Am 15.10. hatte
Opus-PM schwebende Felsen in C2/B5 als „gewollte Stapel“ eingestuft. Das war nach Ferats Bild falsch.

## 2. Das Bild

Ferats Bild liegt nur im Chat vor. Es zeigt die Talkaskade des Erlenbachs in C2 bei etwa 430 m Bachlänge, bachaufwärts gesehen, etwas näher als
unser Prüfbild `bilder/platzierung/c2_talkaskade_t430_2026-10-18.jpg`. Dieselbe Strecke zeigen auch `c2_talkaskade_m_2026-10-18.jpg` und
`c2_talkaskade_t500_2026-10-18.jpg`. Seine acht Kreise:

| Nr. | Ort im Bild | Was dort falsch aussieht |
|---|---|---|
| 1 | linkes Ufer oben | flache Steinplatten ragen steil schräg aus dem Hang, kleine weiße Kiesel liegen obenauf |
| 2 | Mitte oben | ein Stamm liegt quer über dem Wasser, an seinem Ende ein brauner Klumpen (Wurzel oder Moosballen) im Wasser |
| 3 | rechts oben | flache Platten liegen über dem Gras oder schweben, Gras wächst hindurch |
| 4 | rechts | eine Platte steht wie ein Brett schräg aus dem Boden |
| 5 | rechts Mitte | große flache Platten liegen schräg am Hang übereinander geschoben, eine dünne Kiesplatte schwebt |
| 6 | unten links | dunkle, dünne Platten mit Kiestextur stehen hochkant im Wasser, dazu orange und weiße kleine Steine im Wasser |
| 7 | unten Mitte | ein oranger Stein im Wasser, dünne Äste oder Platten unter Wasser neben einem Rohrkolben |
| 8 | unten rechts | eine dünne Kiesplatte ragt schräg aus dem Gras |

Gemeinsam ist allen: Die Teile sitzen nicht im Boden. Sie schweben ganz oder teilweise, stehen hochkant oder schräg gegen den Hang, ragen mit
einer Kante heraus, durchdringen sich oder treiben im Wasser. Dazu kommen fremdfarbige, orange oder weiße Steine im Bach.

## 3. Was lokal läuft

- **Rolle 1** baut eine Prüfung „sitzt organisch im Boden“ (v4) für alle 70 Felder. Grundlage sind der Zensus (Lage, Drehung, Skala je Instanz),
  die Netzgrenzen und das 1-m-Gelände; später kommt die echte Netzform als Punktwolke aus dem Editor dazu. Sie misst unter anderem Lücken unter der
  Unterseite, Eingrabtiefe, den Winkel zwischen Platte und Geländenormale, freie Kantenhöhe, Durchdringung, Treiben im Wasser und frei hängendes Totholz.
  Die Schwellen sind vorläufig, bis diese Antwort vorliegt.
- **Rolle 4** baut ein Editorwerkzeug „umsetzen“: alte Instanz entfernen und im selben Foliage-Typ mit korrigierter Lage neu hinzufügen, mit
  Sicherung, Speicherbeleg je Paket und Rückweg. Bisher gab es nur „entfernen“.
- Die alte Prüfung v2 hatte: schwebend = Unterkante über dem **höchsten** von 5 Bodenpunkten (Stein 5 cm, Fels 20 cm, Totholz 10 cm), umgekippt
  > 60° gegen Welt-Z, Stein auf Stein als Auflage. Damit gilt eine schräg herausragende Platte als „ok“, solange eine Ecke den Boden berührt.

## 4. Fragen

1. **Sollzustand je Klasse.** Klassen: großer Fels, Stein, Kiesel, Platte (dünn), Kleinschutt-Fläche (sehr dünnes Netz mit Kies- oder
   Schutttextur, zum flachen Auflegen), Totholz (Stamm, Ast, Stumpf, Wurzel). Je Klasse bitte festlegen:
   - Eingrabtiefe (Anteil der Höhe im Boden), mit Spanne;
   - größte sichtbare Lücke unter der Unterseite;
   - erlaubte Abweichung von der Geländenormale;
   - die Bedingung, unter der ein Teil als „frei liegend“ noch natürlich wirkt (z. B. Geröll in der Halde).
2. **Platten.** Wann dürfen Platten schräg oder gestellt stehen, etwa als Schichtausbiss im Steilhang mit einheitlicher Fallrichtung in der
   Gruppe? Wann müssen sie flach liegen? Wie viel darf eine Kante überstehen?
3. **Stapel und Auflage.** Wann gilt ein Stein als getragen (Auflagefläche, Kontaktpunkte, Schwerpunkt über der Auflage)? Wie viel
   Durchdringung zwischen Steinen ist bei einer Felsgruppe erlaubt, und ab wann wirkt sie falsch?
4. **Im Wasser.** Steine im Bach: Wie viel muss im Grund sitzen? Welche dürfen über die Wasserfläche ragen (Tiefe, Größe)? Wie sehen
   Kleinschutt und Äste unter Wasser richtig aus?
5. **Totholz.** Wie muss ein Stamm aufliegen (Auflagepunkte, Durchhang)? Sind Stämme quer über einem Bach erlaubt, und wie müssen ihre Enden im
   Ufer sitzen? Wurzelklumpen im Wasser: wann ja, wann nein?
6. **Farbe.** Welche Steinfarben gehören in einen nordischen Bergbach? Wie mit orangen oder weißen Steinen verfahren: Material tauschen,
   entfernen oder ersetzen? Gemessene Helligkeit Y einiger Netze: SmallStonesPack 0,125, mountain_rock_small 0,229, Bett unter Wasser 0,067.
7. **Reparatur.** Wann neu setzen, wann entfernen, wann ersetzen? Beim Neusetzen: Darf sich die Lage in XY ändern oder nur Höhe und Drehung?
   Darf die Skala geändert werden? Welche Reihenfolge, wenn mehrere Fehler zusammenkommen, etwa Platten übereinander?
8. **Planer.** Welche Regeln müssen die Planer künftig beim Setzen einhalten, damit der Fehler nicht wiederkommt? Betroffen sind unter anderem
   detailgrad (Antwort 20), p2bett, kantenufer, Bachdekor, Felsschalen und die B5-Themen.
9. **Prüfkriterien.** Bitte Kriterien für einen Piloten an der Talkaskade C2 (s 389–580) angeben, mit Messweg und Abbruchregeln, und danach für
   die Ausweitung auf die Welt.

## 5. Lieferform

Regeln als Tabelle je Klasse mit Zahlen und Begründung, dazu Prüffälle (gut/schlecht), wie bei den Ufer-Regeln aus 16h
(`antworten/bachbett_ufer_regeln.json`). Wenn möglich zusätzlich eine maschinenlesbare JSON-Datei.
