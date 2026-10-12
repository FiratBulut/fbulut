# Auftrag 15g – C2 Version 2 gebaut (Plan ae09234 mit Querprofil): Bildbefund

Stand 12.10.2026, 08:50. Erst zurückgebaut, dann auf 1 m neu geplant (0 FEHLER) und eingebaut. Das Netz hat 26 303 Punkte; an 5 301 Quads mit Deckung < 0,3
fehlt es, dort scheint Fels durch. Schaum lokal `Schaum_Menge` 0,15 / `Zungen_Schaum` 0,25. Bild: [`bilder/gefaelle_c2/c2_v1_gegen_v2.jpg`](../bilder/gefaelle_c2/c2_v1_gegen_v2.jpg),
links Version 1, rechts Version 2.

## Ergebnis

**Großer Schritt.** Das Wasser ist klar, Schaum gibt es nur an den Lippen, die Blöcke sitzen in den Stufen. Die Becken wirken wie Gumpen (`kn0_nah_s119`):
ein Fall über eine Felsnase in ein grünes Becken.

## Was noch stört

1. **Eckige Schaumflecken:** Die Schaumbereiche an den Lippen erscheinen als weiße Rechtecke bzw. Strichreihe (`s1`, `s1_weg`, `fern`). Das kommt von der
   Vertexfarbe auf dem 0,5-m-Gitter mit harten Übergängen (Schaum 1 neben 0,1). Wunsch: weiche Übergänge im `quer`-Schaum (Rampe über 1–2 Querpunkte, Rauschen in den
   Kanten). `quer_punkte` 21 statt 11, damit der Querabstand ≤ 1 m bleibt (lokal getestet: Fehler 1,6 statt 4,1 cm).
2. **Becken zu kräftig grün und deckend.** Ich baue lokal ein `M_EL_Kaskade_SLW2`, das Tiefe und Deckung nutzt (UV1 = Tiefe/150 cm, Deckung; Vertexfarbe A =
   Deckung): Absorption/Streuung × clamp(Tiefe/1,5; 0,35; 1).
3. **Aus `kn0_unten` (von unten hangauf)** wirkt die Folge der Becken noch wie Terrassen. Ursache sind die waagrechten Beckenspiegel mit gleichmäßig breiten
   Rändern. Wunsch: Beckenränder unregelmäßiger (Uferlinie mit Buchten, Blöcke am Rand), damit die Terrassenkante nicht durchgehend ist.

Ferat sieht C2 heute früh. Die übrigen 19 Piloten erst nach seinem OK.
