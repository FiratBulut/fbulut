# Auftrag 23b – Nachtrag zu 23: erkennbare Wiederholungen, Spiegeln, weiße Steine

Stand 18.10.2026, 20:15 PC-Uhr. Auftraggeber Ferat. Bezug: Auftrag 23 (3199188).

## 1. Was Ferat sagt (wörtlich)

„Auch solche Assets-Wiederholung, wo man genau erkennt, dass es sich um selbe Asset handelt, muss man korrigieren. Vielleicht Asset
spiegelverkehrt platzieren.“

Sein Bild: `bilder/platzierung/ferat_wiederholung_c2_bett_2026-10-18.jpg`. Es ist ein Bildschirmfoto unserer Prüfkamera im Bachbett C2,
Talkaskade. Die weiße Linie mit Querstrichen ist die Spline des Flusses im Editor und gehört nicht zur Welt.

## 2. Was im Bild zu sehen ist

- Oben in der Mitte stehen zwei große, gleiche Felsplatten direkt nebeneinander, mit fast gleicher Drehung und Größe. Man erkennt sofort
  dasselbe Netz.
- Links stehen zwei weitere gleiche Blöcke.
- Mehrere **rein weiße Steine** ohne erkennbare Oberfläche liegen im Bett. Wir vermuten ein Material ohne gebundene Textur, wie früher bei
  `MI_ukjhcamga` (weiße Quadrate in B5). Das ist noch ungeprüft.
- Ein Stamm liegt quer über dem Bett, an seinem Ende sitzt ein Wurzelstock, der auf dem Grund aufliegt.

## 3. Was lokal läuft

Die Prüfung v4 (Auftrag 23 §3) bekommt eine Klasse „erkennbare Wiederholung“: gleiches Netz in kurzer Distanz relativ zur Größe, mit
ähnlicher Drehung und Skala, dazu Gruppen von 3 und mehr gleichen Teilen in einem Blickfeld von etwa 15 m. Als Korrektur rechnet sie eine
neue Drehung, Spiegeln (negative Skala auf X oder Y, nie Z), eine Skalenänderung oder den Tausch gegen ein anderes Netz derselben Familie.
Das Werkzeug „umsetzen“ soll Spiegeln und Netztausch können. Ob gespiegelte Instanzen in UE 5.8 richtig gezeichnet werden und Kollision haben,
prüfen wir an einer einzelnen Instanz, bevor wir es breit anwenden.

## 4. Fragen

1. **Ab wann ist eine Wiederholung erkennbar?** Abstand relativ zur Größe, Unterschied in Drehung und Skala, Blickabstand. Gilt das für große
   Felsen strenger als für Steine? Kiesel sind nach unserer Annahme unkritisch.
2. **Spiegeln:** Ist Spiegeln um die Hochachse für gescannte Felsen und Totholz unbedenklich? Wann nicht, etwa bei Moos nur auf einer
   Seite, Schichtung, Lichtrichtung in der Albedo oder Schriftzügen? Gibt es Erfahrungswerte zu Nanite oder Foliage mit negativer Skala?
3. **Reihenfolge der Mittel:** zuerst drehen, dann spiegeln, dann skalieren, dann Netz tauschen? Wie viel Skalenänderung ist für Felsen
   glaubwürdig?
4. **Planerregel:** Welche Mindestabstände oder Variationsregeln sollen künftige Planer einhalten, damit keine erkennbaren Kopien entstehen?
5. **Weiße Steine:** Wenn sich der Verdacht bestätigt, also Material ohne Textur: Material reparieren oder Teile entfernen? Wie hell darf ein
   Bachstein in einem nordischen Bergbach höchstens sein (Albedo)?
6. **Stamm über dem Bett mit Wurzelstock auf dem Grund:** natürlich oder zu entfernen?

Bitte die Antworten in die Regeln aus Auftrag 23 einarbeiten, als Tabelle mit Zahlen und Prüffällen.
