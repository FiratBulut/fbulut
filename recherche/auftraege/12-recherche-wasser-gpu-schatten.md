# Auftrag 12 – Recherche (Web, UE 5.8): Stufen-Wasserfälle, GPU-Hänger, Schatten-Kacheln

Stand 11.10.2026 11:15 lokal. Reine Recherche mit Quellen (Epic-Doku, Foren, Breakdowns, GDC/Unreal-Fest-Vorträge). Antwort als
`recherche/antworten/12-recherche-wasser-gpu-schatten.md`, je Teil: Befund, konkrete Einstellungen/CVars mit Werten, Quellen-Links, Risiken.
Keine Projektdateien nötig; Kontext steht hier.

## Teil A – Kleine Wasserfälle an Stufen eines Bergbachs (Epic Water, UE 5.8)
Lage: Bergbäche als Epic `WaterBodyRiver` (Spline, Breite/Tiefe/Tempo je Punkt) mit eigenem Material (Kind von MI_Eldarien_Wasser_Basis, Schaum aus
Abstandsfeld). Ein Bach (203 m, 59 m Fall) läuft als Becken-Schnellen-Folge: Becken ~12 % Gefälle, kurze Schnellen bis 57 % über 2–4 m. Im Bild wirken
die Stufen wie regelmäßige Terrassen ohne Fallkante. Ziel (Witcher 3): an jeder Stufe ein kleiner Wasserfall mit weißem Schaum am Fuß.
Geplant: je Stufe ein Static-Mesh-Vorhang (durchscheinendes Material mit Flow-UVs, Vertex-Farben Tempo/Fallanteil/Rand/Schaum) + Schaumfläche am Fuß.
Fragen: 1) Wie lösen andere das in UE5 (Epic Water + Mesh-Wasserfälle + Niagara)? Welche Übergangs-Tricks zwischen Fluss-Spline-Oberfläche und
Wasserfall-Netz (Höhenversatz, Sortierung durchscheinender Flächen, Depth Fade)? 2) Schaum: Decal, Mesh mit Flipbook, Niagara (GPU-Sprites/Ribbons)?
Kosten. 3) Zeichnet Epic Water steile Flussstücke (> 30 %) korrekt (Water-Info-Textur ~1,2 m Auflösung, Wassernetz-Kacheln 24 m)? Bekannte Grenzen/Tipps.
4) Bekannte Fertig-Assets (Fab, kostenlos oder günstig) für kleine Wasserfälle/Schaum, die in UE 5.8 laufen.

## Teil B – GPU-Hänger im Editor (D3D12, Nanite)
Zweimal in 2 Tagen: `DXGI_ERROR_DEVICE_HUNG` bzw. „GPU timeout: payload on the Compute queue has not completed after 5 s“, aktive Breadcrumbs:
ShadowDepths → RenderVirtualShadowMaps(Nanite) → Nanite::DrawGeometry → PostPass → PatchSplit; daneben LumenReflections. Einmal ~100 s nach dem
Editorstart im Leerlauf, einmal beim Kameraflug zu einem Bild (gleiche Kamera lief beim zweiten Versuch ohne Hänger). Welt: Landschaft mit Nanite,
viele Nanite-Felsen (Fab Megascans, teils Nanite-Tessellation/Displacement), Lumen, VSM. TDR-Delay ist auf 60 s gesetzt. GPU/Treiber bitte als
unbekannt behandeln, Hinweise je Hersteller geben. Fragen: bekannte Ursachen für Hänger in PatchSplit (Nanite-Tessellation), CVars zum Entschärfen
(z. B. Tessellation begrenzen/aus, r.Nanite.*, r.Shadow.Virtual.*), Diagnose (r.GPUCrashDebugging, Aftermath, Breadcrumbs), Treiber-Empfehlungen.

## Teil C – Veraltete Kacheln der virtuellen Schattenkarte (VSM) nach Editor-Laden
Befund: Nach dem Laden von World-Partition-Bereichen im Editor (LocationVolume laden, dann Kamera hin, 2 min warten, HighResShot) liegen dunkle,
scharfkantige Rechteck-/Treppenflecken am Boden. Mit `r.Shadow.Virtual.Enable 0` und nach Wieder-Einschalten sind sie weg (also Cache).
Fragen: Ist das ein bekanntes Problem (Foliage/HISM/Landschaft beim Streaming, Cache-Invalidierung)? Gibt es einen CVar/Befehl, der nur den VSM-Cache
leert (statt aus/an), z. B. r.Shadow.Virtual.Cache.* ? Tritt es auch im Spiel (PIE/Paket) auf, und wie verhindert man es dort?
