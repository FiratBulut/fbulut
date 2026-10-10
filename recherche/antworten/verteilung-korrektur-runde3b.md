# Antwort zu Korrektur Runde 3b (Auftrag 11)

Stand: 10.10.2026. Beide Punkte sind umgesetzt und synthetisch getestet, nicht mit Echtdaten. Tabellen je Feld: `verteilung-STATUS.md`
Abschnitt „Runde 3b“, ausführlich `verteilung-entfernen.md`.

## 1. Keine Pflanzen auf Schnee (hochgebirge)

- Alpenrose, Grasbüschel und Beere kommen über die Mittelschicht. Latsche, Krüppelkiefer, Polster und Totholz setzt `hochgebirge_plan.py`.
  Beide Planer setzen Pflanzen nur noch, wo `lage_Schnee` < 60 und `lage_Eis` < 30 ist.
- `mittelschicht_plan.py` sperrt das global für alle pflanzlichen Klassen in allen Biomen (`lagen_max_pflanzen`), weil es Schnee auch in
  tundra, bergwald und fjord gibt. Neuer Schlüssel `lagen_max` steht in KONVENTIONEN §6. Ohne Schnee und Eis bleiben die Ergebnisse
  byteidentisch.
- Steine und Kiesel auf Schnee sind je nach Schneemenge zu 40–60 % eingegraben. Eiszapfen standen schon nur an Wänden ab 55°.

| Synthetisch E1-artig | vorher | nachher |
|---|---|---|
| Pflanzen auf Schnee/Eis, hochgebirge | 679 | 0 |
| Pflanzen auf Schnee/Eis, mittelschicht | 161 | 0 |
| Bergwiese, mittelschicht | – | −0,4 % |
| Polster auf der Wiese | – | +11 % |

Die Polster nehmen zu, weil ihr Klassenbudget nicht mehr teils auf Schnee verbraucht wird. Die Dichte je Fläche ist gleich.

## 2. `entfernen`-Filter von nordkueste und dschungel

- **Ohne Freigabe wird nichts entfernt.** Neuer Schalter `--ersetzen` bzw. Regel `entfernen_aktiv`, Standard aus. Dann bleibt `entfernen`
  leer, und `plan.json["entfernen_vorschlag"]` nennt die Kandidaten mit Zahl, getrennt nach eigenen Zellen, Saum und fremden Zellen, je Netz.
- **nordkueste:** Der alte Filter war zu breit. `sm_forest_pine_0` traf auch liegende Stämme, `fir_0` auch Jungpflanzen und Totbäume. Die
  85-%-Prüfung zählte Meerzellen mit. Jetzt greift er nur bei ≥ 85 % eigenem Biom im Feldland und ≤ 5 % Kandidaten in Saum- oder
  Fremdzellen, und nur auf die Baumarten, die der Planer neu setzt.
- **dschungel:** entfernt keine Bäume, nur Witcher-Lianen `sm_vines_01a`, mit Freigabe und nur in G6, H6, I6.
- **Erwartung:** Mit `--ersetzen` entfernt nordkueste nur in A3, B3, I3, A4, B4, A5, B5 Bäume, zusammen etwa 2 100–11 000.
  Alle anderen Nordküsten-Felder ergänzen nur. Die Zahlen sind Schätzungen aus Dichte × Fläche, weil es keine Baumzählung je Feld gibt.
- **Andere Planer:** aue, heide_tundra, wueste_ergaenzung, sumpf, hochgebirge, mittelschicht und spuren entfernen nichts. lava (kleine
  Witcher-Steine), felsgruppen (`FT_EL_FS_*`-Blöcke) und elfenwald (Witcher-Kleinzeug, ab 50 % Elfenwald) entfernen keine Bäume.

## Bitte lokal beachten

1. Der Setzer sollte beim Entfernen nur auf `entfernen_nur_ft` (`FT_EL_WIT_`, `FT_EL_BST_`) wirken. Vergleicht er Netznamen, trifft er auch
   Houdini-/WELT-Kiefern und die eigenen neuen Bäume.
2. Zellgenaues Entfernen in Mischfeldern kann der heutige Setzer nicht. Deshalb ist der Filter auf Felder mit ≥ 85 % eigenem Biom begrenzt.
3. Exakte Zahl: nordkueste und dschungel ohne `--ersetzen` laufen lassen und `entfernen_vorschlag` lesen.
