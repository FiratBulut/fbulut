#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eldarien – Asset-Taxonomie (Auftrag 11, Teil A).

Ordnet alle Netze aus daten/netze.csv regelbasiert einer Rolle und einer Biom-Eignung (0–2 je Biom) zu
und schreibt antworten/assets-taxonomie.json (+ optional die Markdown-Auswertung).

Aufruf:
    python -I taxonomie_erzeugen.py daten/netze.csv antworten/assets-taxonomie.json [antworten/assets-taxonomie.md]

Nur Standardbibliothek (csv, json, re). Deterministisch, keine Zufallszahlen.

Vorgehen (Reihenfolge der Entscheidung je Netz):
  1. manuelle Korrekturtabelle KORREKTUREN (Name -> Rolle/Biome/Notiz) schlägt alle Regeln
  2. Paket-Sonderfälle (Eldarien-Kacheln, Megaplant-Bauteile, Testnetze)
  3. Namensmuster (Reihenfolge der Liste ROLLEN_REGELN ist Priorität)
  4. Maßregeln (Felsen: größte Kante > 3 m hero, 0,8–3 m block, < 0,8 m stein; flache Felsen z/h < 0,3 und h >= 1 m -> geroell_platte;
     Bäume: Höhe < 8 m jung, 8–17 m mittel, > 17 m alt; Totholz stehend < 8 m, sonst baum_<art>_tot)
  5. Biom-Eignung aus Herkunfts-Hinweisen (HINWEISE: Icelandic/Nordic/Mossy/Sandstone/Lava/Beach/… und Paketname),
     Standardwerte je Rollengruppe, danach Plausibilitäts-Filter (keine Laubpflanzen auf Gletscher/Lava/Wüste ohne Hinweis).
"""
import csv
import json
import re
import sys
from collections import Counter, OrderedDict, defaultdict

BIOME = ["aue", "bergwald", "gletscher", "tundra", "canyon", "oedland", "heide", "elfenwald",
         "dschungel", "kueste", "wueste", "lava", "frost", "sumpf", "fjord"]

# --------------------------------------------------------------------------------------------------
# Herkunfts-Hinweise -> Biomwerte (2 typisch, 1 möglich). Mehrere Hinweise werden per Maximum verknüpft.
# --------------------------------------------------------------------------------------------------
HINWEISE = {
    "nordisch":   {"fjord": 2, "tundra": 2, "gletscher": 2, "frost": 2, "kueste": 2, "bergwald": 1, "heide": 1},
    "island_lava": {"lava": 2, "fjord": 1, "tundra": 1, "oedland": 1},
    "moosig":     {"bergwald": 2, "elfenwald": 2, "aue": 2, "sumpf": 1, "dschungel": 1, "fjord": 1, "heide": 1},
    "japan_moos": {"elfenwald": 2, "bergwald": 1, "dschungel": 1, "aue": 1},
    "sandstein":  {"wueste": 2, "canyon": 2, "oedland": 2, "heide": 1, "kueste": 1},
    "kalk":       {"canyon": 2, "dschungel": 2, "oedland": 1, "heide": 1, "wueste": 1, "kueste": 1},
    "granit":     {"bergwald": 2, "tundra": 2, "gletscher": 2, "fjord": 2, "frost": 1, "heide": 1, "canyon": 1, "elfenwald": 1},
    "strand":     {"kueste": 2, "fjord": 2, "aue": 1, "heide": 1},
    "lava":       {"lava": 2, "oedland": 1},
    "gebirge":    {"bergwald": 2, "tundra": 2, "fjord": 2, "gletscher": 1, "frost": 1, "heide": 1, "canyon": 1},
    "wiese":      {"aue": 2, "heide": 2, "elfenwald": 1, "bergwald": 1, "kueste": 1},
    "laubwald":   {"bergwald": 2, "aue": 2, "elfenwald": 2, "sumpf": 1, "heide": 1},
    "nadelwald":  {"bergwald": 2, "tundra": 1, "frost": 1, "fjord": 2, "heide": 1},
    "wueste":     {"wueste": 2, "canyon": 1, "oedland": 1},
    "tropisch":   {"dschungel": 2, "kueste": 1},
    "oase":       {"dschungel": 2, "wueste": 1, "kueste": 1},
    "orient":     {"wueste": 2, "canyon": 1},
    "tundra":     {"tundra": 2, "frost": 2, "fjord": 2, "heide": 2, "gletscher": 1, "bergwald": 1},
    "feucht":     {"sumpf": 2, "aue": 2, "elfenwald": 1, "kueste": 1, "fjord": 1, "heide": 1, "dschungel": 1},
    "eis":        {"frost": 2, "gletscher": 2, "tundra": 1},
    "tot_duester": {"sumpf": 2, "oedland": 2, "heide": 2, "aue": 1, "bergwald": 1, "tundra": 1, "lava": 1, "frost": 1, "elfenwald": 1},
    "dorf":       {"aue": 2, "heide": 2, "bergwald": 1, "kueste": 1, "fjord": 1, "sumpf": 1, "tundra": 1},
    "ruine":      {"elfenwald": 2, "dschungel": 1, "aue": 1, "heide": 1, "oedland": 1, "canyon": 1, "sumpf": 1},
    "stein_allg": {"aue": 1, "bergwald": 1, "gletscher": 1, "tundra": 1, "canyon": 1, "oedland": 1, "heide": 1,
                   "elfenwald": 1, "dschungel": 1, "kueste": 1, "wueste": 1, "frost": 1, "sumpf": 1, "fjord": 1},
    "gemaessigt": {"aue": 2, "bergwald": 2, "elfenwald": 2, "heide": 1, "sumpf": 1, "kueste": 1, "fjord": 1},
    "suedafrika": {"wueste": 2, "heide": 1, "oedland": 1},
    "wald_boden": {"bergwald": 2, "elfenwald": 2, "aue": 1, "sumpf": 1, "fjord": 1},
}

# Namens-/Pfadmuster (regex, klein geschrieben) -> Hinweisschlüssel
HINWEIS_MUSTER = [
    (r"icelandiclavaspire", "island_lava"),
    (r"icelandic|nordic|tundra", "nordisch"),
    (r"japanese", "japan_moos"),
    (r"mossy|lichened|forestrock|forestroot|forestterrain|forestground|forest_boulder|forest_rock|forest_terrain|rockyforestpath|grassyembankment", "moosig"),
    (r"sandstone|desert|western|quarry|eroded|dryriverbed|ledge", "sandstein"),
    (r"limestone|kalk|asiantemple/.*cliff", "kalk"),
    (r"granite|sharp_cliff|layered_rock", "granit"),
    (r"beach|coast|dune|driftwood|sea_|seaside", "strand"),
    (r"lava|vulkan", "lava"),
    (r"mountain_environment_set", "gebirge"),
    (r"meadow_environment_set", "wiese"),
    (r"forest_environment_set", "laubwald"),
    (r"environment_set/environment/foliage/models/fir_|dwarf_pine|forest_pine|pine_", "nadelwald"),
    (r"namaqualand|quiver|rooibos|searsia|didelta|othonna|leipoldtia|cheiridopsis|iceplant|gazania|ursinia|stinkkruid|heliophila|empodium", "wueste"),
    (r"palm|bazaar_meshingun/.*foliage", "oase"),
    (r"asiantemple|kikuyu|crownbeard|jungle", "tropisch"),
    (r"bazaar_meshingun/.*(architecture|prop)", "orient"),
    (r"tundra_grass|wk2oaeyqx", "tundra"),
    (r"rohrkolben|reed|toadrush|horsetail|petasites|waterplant|willow|sumpf|moss|eaglefern|hivemind", "feucht"),
    (r"eiszapfen", "eis"),
    (r"graveyard|dead_tree|deadtree|dead_forest|_dead|dead_|haunted", "tot_duester"),
    (r"/village/|medievalfantasyvillage|/town/|medievalcastle|fence|wooden_pales|half_log|sviatovid", "dorf"),
    (r"ancientruins", "ruine"),
    (r"redlachenalia", "suedafrika"),
    (r"megascans/3d_plants|fab/megascans/plants|elderberry|hornbeam|windflower|archangel|lilyofthevalley|periwinkle|shamrock|clover|groundcover|ivy|beechfern|silverladyfern|/fern/|wood_sorrel|uchkajuia", "gemaessigt"),
    (r"deadleaves|drybranches|woodensticks|detail_leaves|detail_branches|poplar_leaves|mushroom|moss_0", "wald_boden"),
    (r"hazel|maple|cherry|anemone", "gemaessigt"),
]

# --------------------------------------------------------------------------------------------------
# Rollenregeln: (regex auf Name klein, Rolle oder Funktionsname, Notiz). Erste Übereinstimmung gewinnt.
# "FELS", "BAUM:<art>", "TOTBAUM:<art>" sind Marker, die anschließend über Maße aufgelöst werden.
# --------------------------------------------------------------------------------------------------
ROLLEN_REGELN = [
    # --- Testnetze / Kacheln -----------------------------------------------------------------
    (r"^sm_icon_|^sm_cube$|^sm_splash$", "sonst", "Test-/Hilfsnetz, nicht platzieren"),
    (r"^sm_k\d+_|^sm_r_[mp]\d_[mp]\d__|^sm_weg_flicken|^sm_vulkan_region|^sm_welt__", "sonst", "Houdini-Kachelnetz (Gelände/Wasser/Wege), nicht streubar"),
    # --- Mensch / Spuren -----------------------------------------------------------------------
    (r"fence|wooden_pales|^sm_rail_|^sm_half_log$", "mensch_zaun", "Zaun/Zaunpfahl"),
    (r"^sm_well_", "mensch_brunnen", "Brunnen (orientalisch)"),
    (r"carriage|^sm_cart|wagon|^sm_wheel", "mensch_karren", "Karren/Wagen"),
    (r"firewood|pile_woodlog", "mensch_holzstapel", "Holzstapel"),
    (r"strawpile|^sm_hay", "mensch_heu", "Heu/Stroh"),
    (r"foodsac|barrel|crate|trough", "mensch_vorrat", "Vorrat/Gefäß"),
    (r"^sm_plank|wood_beam|^sm_beam_", "mensch_bauholz", "Bauholz/Balken"),
    (r"^sm_lamp$", "mensch_laterne", "Laterne"),
    (r"flaggurland", "mensch_schmuck", "Fahnengirlande"),
    (r"^sm_cross$", "mensch_wegkreuz", "Wegkreuz/Grabkreuz"),
    (r"sviatovid", "mensch_schrein", "Steinidol (slawisch)"),
    (r"^sm_column_|^sm_main_arch|ancientruins/meshes/sm_wall", "mensch_ruine", "Ruinenstück"),
    (r"^sm_arch_|^sm_dome_|^sm_floor_|^sm_trim_|^sm_wall_|^sm_window", "mensch_gebaeude", "Bauteil orientalisch (Bazaar)"),
    # --- Pflanzen: Sonderfälle vor den allgemeinen ---------------------------------------------
    (r"rohrkolben", "schilf", "Rohrkolben-Horst"),
    (r"toadrush", "schilf", "Binse (niedrig, Ufer/Nass)"),
    (r"eiszapfen", "sonst", "Eiszapfen (Fels-/Klippendekor)"),
    (r"waterplant", "sonst", "Seerosenblatt-Fläche (Wasseroberfläche)"),
    (r"^sm_mushroom", "bodendecker", "Pilz"),
    (r"deadleaves|detail_leaves|poplar_leaves", "bodendecker", "Laubfläche"),
    (r"^sm_moss_|mossclump|mossplane|custommoss", "bodendecker", "Moos"),
    (r"beach_rose_\d+_(pink|white)_flowers$", "sonst", "Blüten-Overlay zu SM_beach_rose_xx (nur zusammen mit dem Strauch)"),
    (r"beach_rose_\d+_with_", "STRAUCH", "Strandrose mit Blüten"),
    (r"ivy|vines", "bodendecker", "Kletterpflanze (Ranke, an Wand/Stamm)"),
    (r"fern", "farn", "Farn"),
    (r"grass|dead_grass", "grasbueschel", "Grasbüschel"),
    (r"wk2oaeyqx", "grasbueschel", "Tundra-Gras (Megascans)"),
    (r"flower|daisy|windflower|archangel|lilyofthevalley|^sm_lily_|periwinkle|lachenalia|crownbeard|sea_holly|kidney_vetch|bedstraw|groundsel|chamomile|poppy|cornflower|goldenrod|sunroot|chicory|knapweed|bouncing_bet|wort", "blume", "Blume/Blühstaude"),
    (r"clover|shamrock|groundcover|ground_foliage|stonecrop|sea_pea|nettle|horsetail|petasites|shaggy_soldier|heath|heather|lingonberry|billberry|bilberry|^sm_plant|^sm_plants|uchkajuia|iceplant|dry_quiver_leaf", "bodendecker", "Bodendecker/Kraut"),
    (r"leipoldtia|cheiridopsis|wild_rooibos|othonna_cerarioides_[efg]", "bodendecker", "Sukkulente/Zwergstrauch (Wüste)"),
    (r"dwarf_pine|hazel|rose|buckthorn|elderberry|grey_willow|maple_bush|rhododendron|black_cherry|searsia|didelta|othonna|wormwood|^sm_bush_|bush", "STRAUCH", "Strauch"),
    (r"quiver_tree", "jungbaum", "Köcherbaum (Wüste, klein)"),
    (r"pine_beach_short|pine_beach_crooked", "strauch", "Krüppelkiefer"),
    (r"_plant_|_plant$|sapling|seedling|^sm_beech_plant|pine_beach_small|pine_beach_medium", "JUNG", "Jungbaum"),
    # --- Totholz ---------------------------------------------------------------------------------
    (r"stump", "totholz_stumpf", "Baumstumpf"),
    (r"roots|_root_|crooked_root", "totholz_wurzel", "Wurzelteller/Wurzelwerk"),
    (r"fallen|_log|dead_log|driftwood|brokentreeassembly|mossytree|^sm_trunk_", "totholz_liegend", "Liegender Stamm"),
    (r"branch|sticks|twigs|bark_debris|^sm_branch", "totholz_ast", "Ast/Zweig"),
    (r"dead_quiver_trunk", "totholz_stehend", "Toter Köcherbaum-Stamm"),
    (r"deadtree|dead_tree|_dead|dead_", "TOTBAUM", "Toter Baum"),
    # --- Bäume -----------------------------------------------------------------------------------
    (r"hornbeam", "BAUM:hainbuche", "Hainbuche"),
    (r"beech", "BAUM:buche", "Buche"),
    (r"birch", "BAUM:birke", "Birke"),
    (r"willow", "BAUM:weide", "Weide"),
    (r"poplar", "BAUM:pappel", "Pappel"),
    (r"oak", "BAUM:eiche", "Eiche"),
    (r"spruce", "BAUM:fichte", "Fichte"),
    (r"^fir_", "BAUM:tanne", "Tanne"),
    (r"pine", "BAUM:kiefer", "Kiefer"),
    (r"larch", "BAUM:laerche", "Lärche"),
    (r"palm", "BAUM:palme", "Palme"),
    (r"^sm_tree_", "BAUM:laub", "Laubbaum (Art unbekannt, Tempel-Set)"),
    # --- Felsen ----------------------------------------------------------------------------------
    (r"cliff|escarpment|rock_wall|lava_wall|rockface|sandy_slope|scarp", "klippe_schale", "Klippen-/Wandschale"),
    (r"lavaspire", "fels_hero", "Lavaturm"),
    (r"rockyground|rockformation|rockshelf|rockslab|flat_rock|embankment|nordicbeach_|forestterrain|forest_terrain|dryriverbed|forestground|rockyforestpath|sandwithpebbles", "geroell_platte", "Flache Felsplatte/Bodenstück"),
    (r"smallstonespack|nordicbeachrock_01", "ufer_stein", "Gerundeter Kiesel/Strandstein"),
    (r"boulder|rock|stone|pebble|granite|_tier_0|_tier_2|^sm_s_rock|^sm_stone", "FELS", "Fels nach Größe"),
]

# --------------------------------------------------------------------------------------------------
# Manuelle Korrekturen (Name -> dict mit rolle / biome (Teilmenge) / note). Schlagen alle Regeln.
# --------------------------------------------------------------------------------------------------
KORREKTUREN = {
    # Megascans Mossy/Tundra
    "SM_MossyRockFace_02": {"rolle": "fels_block", "note": "Felswandstück 2,4 m, als Block nutzbar"},
    "SM_MassiveTundraRockFormation_01": {"rolle": "fels_hero", "note": "77 m Felsrücken, nur als Akteur (Grat/Kuppe)"},
    "SM_MassiveTundraRockFormation_02": {"rolle": "fels_hero", "note": "29 m Felsrücken, nur als Akteur"},
    "SM_NordicBeachRocks_01": {"rolle": "fels_hero", "note": "Strandfels-Gruppe 5,8 m"},
    "SM_TundraMossyBoulder_01": {"rolle": "fels_hero", "note": "flacher Moosblock 7,4 m (Hero liegend)"},
    "SM_stones_roots_01": {"rolle": "totholz_wurzel", "note": "Wurzelwerk mit Steinen 7,5 m (Hangkante)"},
    "SM_stones_roots_02": {"rolle": "totholz_wurzel", "note": "Wurzelwerk mit Steinen 7,5 m (Hangkante)"},
    "SM_stones_roots_03": {"rolle": "totholz_wurzel", "note": "Wurzelwerk mit Steinen 3 m"},
    "SM_BeachSandWithPebbles_01": {"rolle": "geroell_platte", "biome": {"kueste": 2, "fjord": 1, "aue": 1}, "note": "Sandfläche mit Kieseln (Strand)"},
    "SM_BeachSandWithPebbles_02": {"rolle": "geroell_platte", "biome": {"kueste": 2, "fjord": 1, "aue": 1}, "note": "Sandfläche mit Kieseln (Strand)"},
    "SM_Sviatovid_Stone": {"biome": {"heide": 2, "aue": 1, "bergwald": 1, "sumpf": 1, "elfenwald": 1, "fjord": 1}},
    # Meadow: 'Tree_Stump' sind liegende Stammstücke mit Wurzel
    "SM_Tree_Stump_01": {"rolle": "totholz_liegend", "note": "Stammstück mit Wurzel 4,3 m"},
    "SM_Tree_Stump_02": {"rolle": "totholz_liegend", "note": "Stammstück 2,3 m"},
    "SM_Tree_Stump_03": {"rolle": "totholz_liegend", "note": "Stammstück 3,4 m"},
    # Coast Dunes
    "SM_beach_escarpment_01_A": {"note": "niedrige Abbruchkante 1,1 m (Dünenkante)"},
    "SM_beach_escarpment_01_B": {"note": "niedrige Abbruchkante 1,0 m (Dünenkante)"},
    "SM_beach_escarpment_01_C": {"note": "niedrige Abbruchkante 1,0 m (Dünenkante)"},
    "SM_sea_wormwood_01": {"rolle": "bodendecker", "note": "Strand-Beifuß (Halbstrauch)"},
    "SM_sea_wormwood_02": {"rolle": "bodendecker", "note": "Strand-Beifuß (Halbstrauch)"},
    "SM_sea_pea_01": {"rolle": "bodendecker", "note": "Strandplatterbse, flach"},
    # Forest set
    "SM_sandy_slope_01": {"note": "Böschungsstück 1,4 m (Wegkante/Hangfuß)"},
    "SM_sandy_slope_02": {"note": "Böschungsstück 1,2 m"},
    "SM_sandy_slope_03": {"note": "Böschungsstück 1,4 m"},
    "SM_sandy_slope_04": {"note": "Böschungsstück 7 m"},
    "SM_sandy_slope_05": {"note": "Böschungsstück 7 m"},
    "SM_scarp_01": {"note": "Böschungsstück 1,2 m"},
    "SM_scarp_02": {"note": "Böschungsstück 0,5 m"},
    "SM_grass_01": {"rolle": "sonst", "note": "Höhe 0 m: Platzhalter/defekt"},
    "SM_plants_01": {"rolle": "sonst", "note": "Höhe 0 m: Platzhalter/defekt"},
    # Environment_Set
    "SM_crooked_roots_small": {"rolle": "totholz_wurzel", "note": "kleines Wurzelstück"},
    "SM_forest_heather_01": {"biome": {"heide": 2, "bergwald": 2, "tundra": 1, "fjord": 1, "aue": 1}},
    "SM_forest_heather_simple_01": {"biome": {"heide": 2, "bergwald": 2, "tundra": 1, "fjord": 1, "aue": 1}},
    # Mountain set
    "SM_heath_A_01": {"biome": {"heide": 2, "tundra": 2, "bergwald": 2, "fjord": 2, "frost": 1, "gletscher": 1}},
    "SM_heath_B_01": {"biome": {"heide": 2, "tundra": 2, "bergwald": 2, "fjord": 2, "frost": 1, "gletscher": 1}},
    "SM_heath_cross_01": {"biome": {"heide": 2, "tundra": 2, "bergwald": 2, "fjord": 2, "frost": 1, "gletscher": 1}},
    "SM_ground_rock_03_01": {"rolle": "geroell_platte", "note": "flache Bodenplatte 2,4 m"},
    # Megaplant_Library: Bauteile
    # (werden über das Paket behandelt)
    # AsianTemple
    "SM_Bush_01a": {"rolle": "strauch", "note": "großer Busch 4,7 m (Dschungel), bereits WIT/WELT"},
    "SM_Vines_01a": {"rolle": "bodendecker", "note": "hängende Ranke 5,7 m (Klippe/Baum)"},
    "SM_Fern_01a": {"note": "Farninsel 3 m, Dschungel"},
    # Namaqualand
    "SM_namaqualand_boulders_01_a_NN": {"rolle": "fels_stein", "note": "Steingruppe 0,56 m"},
    "SM_namaqualand_boulders_01_b_NN": {"rolle": "fels_stein", "note": "Steingruppe 0,6 m"},
    # Megascans Pflanzen
    "SM_CloverVarieties_04": {"note": "Kleefläche 5 m, Wiese/Aue"},
    "SM_CloverVarieties_05": {"note": "Kleefläche 5 m, Wiese/Aue"},
    "SM_Crownbeard_01": {"rolle": "bodendecker", "note": "Keimling 8 cm"},
    "SM_Crownbeard_02": {"rolle": "bodendecker", "note": "Keimling 10 cm"},
    "SM_MossyTree_01": {"rolle": "totholz_liegend", "note": "bemooster liegender Stamm 7,8 m"},
    "SM_OldTreeBranch_05": {"rolle": "totholz_ast", "note": "Astgabel 3 m (groß)"},
    # Graveyard / Dead trees
    "SM_Dead_Tree_01": {"rolle": "baum_laub_tot", "note": "Toter Laubbaum 12 m, Friedhof-Set"},
    "SM_Dead_Tree_02": {"rolle": "baum_laub_tot", "note": "Toter Laubbaum 10,5 m, Friedhof-Set"},
    "SM_Dead_Tree_03": {"rolle": "baum_laub_tot", "note": "Toter Laubbaum 11,8 m, Friedhof-Set"},
    "qlEtl_tier_0": {"rolle": "totholz_stehend", "note": "Megascans Dead Tree 6,2 m (Raw)"},
    # Eldarien Brücke
    "SM_K14_AETHELGARD__BRUECKE": {"rolle": "sonst", "note": "Kachel-Brücke (Houdini), nicht streubar"},
    # Bazaar Palme
    "SM_Tree_Palm_01": {"note": "Palme 30 m (Bazaar), bereits WELT"},
    # Village plank/beam as fence-like material
    "SM_Lamp": {"biome": {"aue": 2, "heide": 1, "kueste": 1}},
}

# Pakete mit Pflanzen-Bauteilen (Blätter/Zweige für Baumbau), keine fertigen Streunetze
BAUTEIL_PAKETE = {"Megaplant_Library"}


def hinweise_fuer(name_l, pfad_l):
    text = pfad_l + " " + name_l
    keys = []
    for muster, key in HINWEIS_MUSTER:
        if re.search(muster, text):
            keys.append(key)
    return keys


def biome_aus_hinweisen(keys):
    b = {k: 0 for k in BIOME}
    for key in keys:
        for biom, wert in HINWEISE[key].items():
            if wert > b[biom]:
                b[biom] = wert
    return b


def groesse_klasse(x, y, z):
    m = max(x, y, z)
    if m > 3.0:
        return "fels_hero"
    if m >= 0.8:
        return "fels_block"
    return "fels_stein"


def baum_alter(z):
    if z < 8.0:
        return "jung"
    if z <= 17.0:
        return "mittel"
    return "alt"


def rolle_bestimmen(r, name_l, pfad_l, x, y, z):
    """Liefert (rolle, note)."""
    paket = r["paket"]
    if paket in BAUTEIL_PAKETE:
        return "sonst", "Pflanzen-Bauteil (Megaplant Library: Blatt/Zweig/Ast-Karte), kein Streunetz"
    if paket == "AncientRuins":
        return "mensch_ruine", "Ruinenstück (AncientRuins)"
    for muster, rolle, note in ROLLEN_REGELN:
        if not re.search(muster, name_l):
            continue
        if rolle == "FELS":
            h = max(x, y)
            if h >= 1.0 and z / max(h, 1e-6) < 0.27:
                return "geroell_platte", "flacher Fels (z/h < 0,27)"
            k = groesse_klasse(x, y, z)
            return k, "Fels, größte Kante %.1f m" % max(x, y, z)
        if rolle == "JUNG":
            if z < 0.5:
                return "bodendecker", "Keimling < 0,5 m"
            if z > 5.0:
                art = baum_art(name_l)
                return "baum_%s_jung" % art, "junger Baum %.1f m" % z
            return "jungbaum", "Jungbaum %.1f m" % z
        if rolle == "STRAUCH":
            if z < 0.5:
                return "bodendecker", "Zwergstrauch/Keimling < 0,5 m"
            return "strauch", "%s %.1f m" % (note, z)
        if rolle == "totholz_ast" and max(x, y) > 3.0:
            return "totholz_liegend", "großer Ast %.1f m, wie liegender Stamm" % max(x, y)
        if rolle == "TOTBAUM":
            art = baum_art(name_l)
            if z < 8.0:
                return "totholz_stehend", "toter Stamm/Schnag %.1f m" % z
            return "baum_%s_tot" % art, "toter Baum %.1f m" % z
        if rolle.startswith("BAUM:"):
            art = rolle.split(":", 1)[1]
            if z < 3.0:
                return "jungbaum", "%s klein %.1f m" % (note, z)
            return "baum_%s_%s" % (art, baum_alter(z)), "%s %.1f m" % (note, z)
        return rolle, note
    return "sonst", "keine Regel getroffen"


def baum_art(name_l):
    for muster, art in [("hornbeam", "hainbuche"), ("beech", "buche"), ("birch", "birke"), ("willow", "weide"),
                        ("poplar", "pappel"), ("oak", "eiche"), ("spruce", "fichte"), ("fir", "tanne"),
                        ("pine", "kiefer"), ("larch", "laerche"), ("palm", "palme"), ("quiver", "koecherbaum")]:
        if muster in name_l:
            return art
    return "laub"


def wirkname(pfad, name):
    """Megascans-Fab-Netze heißen nur nach Hash (z. B. 'vdssailfa_tier_2'); der Ordner trägt den Klartext
    ('Massive_Nordic_Coastal_Cliff_vdssailfa'). Für die Regeln wird dann Ordnername + Hash verwendet."""
    m = re.match(r"/game/fab/megascans/(3d|plants)/([^/]+)/", pfad.lower())
    if m:
        return (m.group(2) + "_" + name).lower()
    return name.lower()


def rollengruppe(rolle):
    if rolle.startswith("baum_"):
        return "baum"
    if rolle.startswith("totholz_"):
        return "totholz"
    if rolle.startswith("mensch_"):
        return "mensch"
    if rolle in ("fels_hero", "fels_block", "fels_stein"):
        return "fels"
    return rolle


PFLANZEN_GRUPPEN = {"baum", "jungbaum", "strauch", "farn", "bodendecker", "blume", "grasbueschel", "schilf"}


def biome_bestimmen(r, rolle, keys, name_l, pfad_l):
    b = biome_aus_hinweisen(keys)
    grp = rollengruppe(rolle)
    hat_hinweis = any(v > 0 for v in b.values())

    if rolle == "sonst":
        # Kacheln, Testnetze, Bauteile: 0 überall, Ausnahmen (Eiszapfen, Seerosen) über Hinweise
        if r["paket"] in BAUTEIL_PAKETE or "kachel" in name_l or re.search(r"^sm_k\d+_|^sm_r_|^sm_weg_|^sm_vulkan|^sm_welt|^sm_icon|^sm_cube|^sm_splash", name_l):
            return {k: 0 for k in BIOME}
        return b

    if grp in ("fels", "geroell_platte", "klippe_schale", "ufer_stein"):
        if not hat_hinweis:
            b = biome_aus_hinweisen(["stein_allg"])
        else:
            # Felsen sind weiter einsetzbar als Pflanzen: überall mindestens 1, außer Lava ohne Lava-Hinweis
            for k in BIOME:
                if b[k] == 0 and k != "lava":
                    b[k] = 1 if grp != "klippe_schale" else 0
        if "lava" in keys or "island_lava" in keys:
            # Lavafels passt nur in Lava/Ödland/Fjord(Basalt)
            b = {k: 0 for k in BIOME}
            b["lava"] = 2
            b["oedland"] = 1
            if "island_lava" in keys:
                b["fjord"] = 1
                b["tundra"] = 1
        if rolle == "ufer_stein":
            for k in ("aue", "kueste", "fjord", "sumpf"):
                b[k] = 2
        if "strand" in keys:
            b["kueste"] = 2
        return b

    if grp in PFLANZEN_GRUPPEN:
        if not hat_hinweis:
            b = biome_aus_hinweisen(["gemaessigt"])
        # Plausibilität: Pflanzen ohne passenden Hinweis nicht auf Gletscher/Lava/Wüste
        if "lava" not in keys:
            b["lava"] = 0
        if not ({"wueste", "suedafrika", "sandstein", "orient"} & set(keys)):
            b["wueste"] = 0
            b["canyon"] = min(b["canyon"], 1)
        if not ({"nordisch", "tundra", "eis", "gebirge", "nadelwald", "granit"} & set(keys)):
            b["gletscher"] = 0
            b["frost"] = min(b["frost"], 1)
        if grp == "baum":
            if "wueste" in keys or "oase" in keys:
                pass
            elif not ({"tropisch", "oase"} & set(keys)):
                b["dschungel"] = min(b["dschungel"], 1)
            b["gletscher"] = 0
            if rolle.endswith("_tot"):
                b = {k: max(v, w) for k, v, w in zip(BIOME, b.values(), biome_aus_hinweisen(["tot_duester"]).values())}
        if grp == "schilf":
            b["sumpf"] = 2
            b["aue"] = 2
        if "tundra" in keys:
            for k in ("aue", "elfenwald", "bergwald", "sumpf"):
                b[k] = min(b[k], 1)
        if "tropisch" in keys or "suedafrika" in keys:
            for k in ("aue", "elfenwald", "bergwald", "sumpf", "fjord", "kueste", "heide"):
                b[k] = min(b[k], 1)
        if "wueste" in keys and "oase" not in keys:
            b = {k: 0 for k in BIOME}
            b.update(HINWEISE["wueste"])
        return b

    if grp == "totholz":
        if not hat_hinweis:
            b = biome_aus_hinweisen(["gemaessigt"])
        for k in ("sumpf", "heide", "fjord", "tundra"):
            b[k] = max(b[k], 1)
        b["lava"] = 0 if "lava" not in keys else b["lava"]
        if "wueste" not in keys:
            b["wueste"] = 0
        else:
            b = {k: 0 for k in BIOME}
            b.update(HINWEISE["wueste"])
        return b

    if grp == "mensch":
        if not hat_hinweis:
            b = biome_aus_hinweisen(["dorf"])
        return b
    return b


def stufe_aus_pfad(pfad):
    if "/Raw/" in pfad:
        return "raw"
    if "/High/" in pfad:
        return "high"
    if "/Medium/" in pfad:
        return "medium"
    if "/Low/" in pfad:
        return "low"
    return "unbekannt"


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def einordnen(rows):
    out = OrderedDict()
    for r in rows:
        name = r["name"]
        pfad_l = r["pfad"].lower()
        name_l = wirkname(r["pfad"], name)
        x, y, z = fnum(r["groesse_x_m"]), fnum(r["groesse_y_m"]), fnum(r["groesse_z_m"])
        rolle, note = rolle_bestimmen(r, name_l, pfad_l, x, y, z)
        if name_l.endswith("_cross"):
            note += " (Billboard-Kreuz, nur Fernbereich)"
        keys = hinweise_fuer(name_l, pfad_l)
        korr = KORREKTUREN.get(name, {})
        if "rolle" in korr:
            rolle = korr["rolle"]
            note = korr.get("note", note + " (manuell korrigiert)")
        elif "note" in korr:
            note = korr["note"]
        biome = biome_bestimmen(r, rolle, keys, name_l, pfad_l)
        if "biome" in korr:
            biome = {k: 0 for k in BIOME}
            biome.update(korr["biome"])
        dreiecke = int(fnum(r["dreiecke"]))
        flaeche = x * y
        genutzt = r["foliage_typen"].split() + r["grasarten"].split()
        out[r["pfad"]] = OrderedDict([
            ("rolle", rolle),
            ("biome", OrderedDict((k, biome[k]) for k in BIOME)),
            ("hoehe_m", z),
            ("groesse_m", [x, y, z]),
            ("dreiecke", dreiecke),
            ("dreiecke_je_m2", round(dreiecke / flaeche, 1) if flaeche > 0 else None),
            ("nanite", r["nanite"].strip() == "1"),
            ("stufe", stufe_aus_pfad(r["pfad"])),
            ("materialien", int(fnum(r["materialien"]))),
            ("kollision", fnum(r["kollision_primitive"]) > 0),
            ("genutzt_in", genutzt),
            ("paket", r["paket"]),
            ("name", name),
            ("note", note + ("; Hinweise: " + ",".join(keys) if keys else "")),
        ])
    return out


# --------------------------------------------------------------------------------------------------
# Markdown-Auswertung
# --------------------------------------------------------------------------------------------------
GRUPPEN_REIHE = ["fels_hero", "fels_block", "fels_stein", "geroell_platte", "klippe_schale", "ufer_stein",
                 "baum", "baum_tot", "jungbaum", "strauch", "farn", "bodendecker", "blume", "grasbueschel", "schilf",
                 "totholz_stehend", "totholz_liegend", "totholz_stumpf", "totholz_ast", "totholz_wurzel",
                 "mensch", "sonst"]


def gruppe_fein(rolle):
    if rolle.startswith("baum_"):
        return "baum_tot" if rolle.endswith("_tot") else "baum"
    if rolle.startswith("mensch_"):
        return "mensch"
    return rolle


BIOM_TEXT = {
    "aue": "Flussauen/Weißgarten-Typ: Laubbäume, Weiden, Schilf und Wiesenblumen sind reichlich da. Es fehlen liegende Stämme mit Uferbezug in Hero-Größe (> 5 m: 5 Netze), Obstbäume/Solitäre und Hecken als Feldgrenze (keine).",
    "bergwald": "Beste Abdeckung im Inventar (Mountain + Forest + Megascans Mossy). Lücken: Fichte/Lärche fehlen als Art ganz (nur Kiefer, Tanne, Buche, Hainbuche); junge Nadelbäume 2–5 m nur Kiefer (3 Forest_pine_plant, 8 pine_beach), keine junge Tanne/Fichte.",
    "gletscher": "Nur Felsen (nordisch/granit) und Eiszapfen. Keine Pflanzen außer Tundra-Gras (Eignung 1), kein Moränenschutt als Platte, keine Eisblöcke/Firnreste, kein Totholz (zulässig: 0–1 Netze).",
    "tundra": "Felsen gut (Icelandic/Nordic/Mountain), Tundra-Gras und Heidekraut vorhanden. Fehlt: Zwergbirke/Weidengebüsch 0,3–1 m (nur Krüppelkiefer), Flechtenpolster, liegende Totholz-Stämme ohne Moos.",
    "canyon": "Sandstein-Klippen und -Blöcke gut (Megascans Sandstone, Desert Western). Fehlt: Mittelschicht komplett (Sträucher nur Namaqualand mit Eignung 1), kein Schilf/Ufer für Canyon-Bach, keine Felssäulen (Hoodoo) < 10 m.",
    "oedland": "Nur Zweitverwertung: tote Bäume (Graveyard/Megascans) und Sandstein-Felsen. Fehlt: Trockengras-Büschel, verdorrte Sträucher, Knochen/Spuren, Risse/Bodenplatten für Trockenboden.",
    "heide": "Heidekraut (Mountain), Meadow-Blumen und Dorf-Spuren vorhanden. Fehlt: Ginster/Wacholder-Sträucher 1–2 m, Findlinge als Hero > 3 m ohne Moos (nur Nordic/Icelandic), Steinmauern (keine).",
    "elfenwald": "Mossy-Megascans und Hainbuche tragen das Biom. Fehlt: Riesenbaum/Hero-Solitär > 25 m (nur AsianTemple-Bäume 31–49 m, stilistisch fremd), Lichtpflanzen/Blüten in Höhe 0,5–1,5 m, Ruinenstücke (nur 5 AncientRuins).",
    "dschungel": "Palmen (12 + 1), AsianTemple-Karst und Farninseln vorhanden. Fehlt: Lianen/Luftwurzeln (nur SM_Vines_01a), großblättrige Stauden 1–3 m, Bodenlaub tropisch, Kalk-Blöcke 0,8–3 m (nur 2 LimestoneRocks).",
    "kueste": "Coast_Dunes trägt die Mittelschicht (Strandrose, Sanddorn, Strandhafer). Nordic-Klippen 7–38 m vorhanden. Fehlt: Strandkiesel-Felder als Platte (2), Treibholz-Varianten (1), Fischerstege/Boote (keine), Tang/Algen.",
    "wueste": "Namaqualand vollständig (eigener Planer). Fehlt: Dünen-Platten, Sandstein-Hero > 10 m frei stehend (nur Klippen), Totholz-Stämme vertrocknet (nur Köcherbaum-Teile).",
    "lava": "Lava_Volcano-Set (29 Netze, 2 880–129 216 Dreiecke) und 3 IcelandicLavaSpire. Fehlt: Lava-Kiesel < 0,3 m, erstarrte Lava-Platten/Pahoehoe, Asche-Totholz, Lava-Schale > 5 m.",
    "frost": "Wie Gletscher: Felsen und Eiszapfen. Fehlt: Schnee-Überzug-Varianten aller Felsen, vereiste Totholz-Stämme, Krüppelkiefer mit Schnee, Eisblöcke.",
    "sumpf": "Schilf (Rohrkolben, Binse), Weidenbüsche, tote Bäume, Moos vorhanden. Fehlt: Torf-/Schlammplatten, umgestürzte Stämme im Wasser (Treibholz 1), Wurzelteller groß (> 3 m: 4, alle Gebirgs-/Nadelholz-Optik), Stege (keine).",
    "fjord": "Nordic-Klippen und Icelandic-Boulder tragen die Felsen. Fehlt: Fjord-Nadelwald (nur Forest_pine als Kiefer, keine Fichte), Küstengras-Büschel nordisch (Tundra-Gras passt), Bootssteg/Fischerhütte-Spuren (keine).",
}

PLANER_HINWEISE = """\
- Felsgruppen (Teil C): Hauptfels aus `fels_hero` je Biom, Nebenblöcke aus `fels_block` derselben Herkunft (gleicher Hinweis-Schlüssel in `note`), Geröll aus `fels_stein`/`ufer_stein`. Die Lava- und Namaqualand-Felsen nur im eigenen Biom.
- Mittelschicht (Teil D): `strauch` + `jungbaum` + `farn` je Biom; in gletscher/frost/lava/oedland/canyon gibt es keine passende Mittelschicht – dort Felsen 0,3–3 m und Totholz als Ersatz.
- Nicht-Nanite-Bäume (Forest/Meadow/Environment_Set/Palms) nur mit `sichtweite` [0,0] und LOD prüfen; Nanite-Bäume (Hornbeam, Beech_Dead) bevorzugen.
- `genutzt_in` zeigt, welche Ebene ein Netz schon streut (WIT/BST/UF/FS/WELT); neue Planer sollen dieselben Netze mit `entfernen`-Filter ersetzen oder bewusst ergänzen.
- Megaplant_Library (122 Netze) sind Baukasten-Karten (Leaf_/Twig_/Branch_) – nicht als Foliage streuen.
- Eldarien-Kachelnetze (SM_K*, SM_R_*, 123 Netze) sind Houdini-Gelände/Wasser/Wege und tauchen nur der Vollständigkeit halber auf.
"""


def md_schreiben(tax, pfad_md):
    n = len(tax)
    rollen = Counter(v["rolle"] for v in tax.values())
    lines = []
    L = lines.append
    L("# Asset-Taxonomie Eldarien (Teil A, Auftrag 11)")
    L("")
    L("Stand: erzeugt aus `vorlagen/daten/netze.csv` (%d Netze) mit `antworten/skripte/taxonomie_erzeugen.py`. Ergebnis je Pfad in `antworten/assets-taxonomie.json`." % n)
    L("")
    L("## Methode")
    L("")
    L("1. **Regeln** (im Skript `ROLLEN_REGELN`, erste Übereinstimmung gewinnt): Namensmuster auf dem Netznamen (Cliff/Boulder/Rock/Stump/Log/Branch/Root/Fern/Grass/Flower/Bush/Pine/Beech/…), dann Maße aus der CSV: Felsen nach größter Kante (> 3 m `fels_hero`, 0,8–3 m `fels_block`, < 0,8 m `fels_stein`), flache Felsen mit z/Grundkante < 0,27 und Grundkante ≥ 1 m → `geroell_platte`; Bäume nach Höhe (< 8 m jung, 8–17 m mittel, > 17 m alt; < 3 m `jungbaum`, strauchartige Namen < 0,5 m `bodendecker`); tote Bäume < 8 m → `totholz_stehend`, sonst `baum_<art>_tot`.")
    L("2. **Biom-Eignung** aus Herkunfts-Hinweisen in Pfad/Paket/Name (`HINWEIS_MUSTER` → `HINWEISE`): Icelandic/Nordic/Tundra → fjord/tundra/gletscher/frost/kueste 2; Mossy/Forest → bergwald/elfenwald/aue 2; Sandstone/Desert → wueste/canyon/oedland 2; Lava → lava 2; Beach/Coast → kueste/fjord 2; Paketnamen (Mountain, Meadow, Forest, Namaqualand, Coast_Dunes, Lava_Volcano, AsianTemple, Bazaar, Village…) ebenso. Mehrere Hinweise → Maximum. Danach Plausibilitäts-Filter: Pflanzen ohne Wüsten-/Nord-Hinweis bekommen wueste/gletscher 0 und lava 0; Felsen ohne Hinweis 1 überall außer lava; Lavafels nur lava 2 / oedland 1.")
    L("3. **Manuelle Korrekturen** (`KORREKTUREN`, %d Einträge): z. B. Meadow `SM_Tree_Stump_*` sind liegende Stammstücke, `SM_MossyTree_01` ist ein liegender Stamm, `SM_MassiveTundraRockFormation` ist Hero statt Platte, Heide-/Heidekraut-Biome, AsianTemple-Busch/Ranke, Namaqualand-Steingruppen." % len(KORREKTUREN))
    L("4. **Qualitätsmarken** je Netz: Dreiecke je m² Grundfläche (x·y), Nanite, Megascans-Stufe aus dem Pfad (`/Raw/` = Raw 8K, `/Medium/`; `/High/` und `/Low/` kommen im Inventar nicht vor), Material-Anzahl, Kollision (Primitive > 0), `genutzt_in` (Foliage-Typen + Grasarten).")
    L("")
    L("**Unsicherheiten:** (a) Größenklasse nach größter Kante – ein 3,3 m langer, 2 m hoher Block zählt als Hero. (b) Baumalter rein aus der Höhe, nicht aus Stammform. (c) Biom-Eignung ist Stil-Zuordnung, nicht Botanik: `KikuyuGrass`/`Crownbeard` (Megascans, warm) stehen mit 1 auch in aue/heide, weil die Witcher-Ebene sie dort schon nutzt. (d) Megaplant_Library (122) und Eldarien-Kacheln (123) sind `sonst` mit Biom 0 – sie sind keine Streunetze. (e) AsianTemple-Bäume (31–49 m) sind als `baum_laub_*` eingeordnet, stilistisch nur dschungel. (f) `_cross`-Varianten der Meadow-Blumen sind Billboard-Kreuze (Fern-LOD), nicht für Nahbereich.")
    L("")
    # Rolle × Anzahl
    L("## Rolle × Anzahl")
    L("")
    L("| Rolle | Netze | Nanite | mit Kollision | bereits genutzt |")
    L("|---|---:|---:|---:|---:|")
    for rolle, cnt in sorted(rollen.items(), key=lambda kv: (-kv[1], kv[0])):
        vs = [v for v in tax.values() if v["rolle"] == rolle]
        L("| `%s` | %d | %d | %d | %d |" % (rolle, cnt, sum(v["nanite"] for v in vs), sum(v["kollision"] for v in vs), sum(1 for v in vs if v["genutzt_in"])))
    L("")
    # Biom × Rollengruppe
    L("## Biom × verfügbare Rollen (Netze mit Eignung 2 / Eignung ≥ 1)")
    L("")
    gruppen = [g for g in GRUPPEN_REIHE if g not in ("sonst",)]
    L("| Biom | " + " | ".join(gruppen) + " |")
    L("|---|" + "---:|" * len(gruppen))
    for biom in BIOME:
        zeile = []
        for g in gruppen:
            n2 = sum(1 for v in tax.values() if gruppe_fein(v["rolle"]) == g and v["biome"][biom] == 2)
            n1 = sum(1 for v in tax.values() if gruppe_fein(v["rolle"]) == g and v["biome"][biom] >= 1)
            zeile.append("%d/%d" % (n2, n1))
        L("| %s | " % biom + " | ".join(zeile) + " |")
    L("")
    L("Lesart: `Eignung-2 / Eignung-≥1`. Spalte `baum` = lebende Bäume aller Arten, `baum_tot` = tote Bäume ≥ 8 m, `mensch` = alle `mensch_*`.")
    L("")
    # Baumarten je Biom
    L("### Baumarten je Biom (Netze mit Eignung ≥ 1, lebend)")
    L("")
    arten = sorted({v["rolle"].split("_")[1] for v in tax.values() if v["rolle"].startswith("baum_") and not v["rolle"].endswith("_tot")})
    L("| Biom | " + " | ".join(arten) + " |")
    L("|---|" + "---:|" * len(arten))
    for biom in BIOME:
        zeile = []
        for art in arten:
            c = sum(1 for v in tax.values() if v["rolle"].startswith("baum_%s_" % art) and not v["rolle"].endswith("_tot") and v["biome"][biom] >= 1)
            zeile.append(str(c))
        L("| %s | " % biom + " | ".join(zeile) + " |")
    L("")
    # Lücken je Biom
    L("## Lücken je Biom: was fehlt?")
    L("")
    L("Als Lücke gilt eine Rollengruppe mit 0–2 Netzen der Eignung ≥ 1 (Mittelschicht = strauch/jungbaum/farn, Felsen = hero/block/stein/platte/schale, Totholz = 5 Rollen, Spuren = mensch).")
    L("")
    for biom in BIOME:
        luecken = []
        for g in gruppen:
            n1 = sum(1 for v in tax.values() if gruppe_fein(v["rolle"]) == g and v["biome"][biom] >= 1)
            if n1 <= 2:
                luecken.append("%s (%d)" % (g, n1))
        L("- **%s** – Lücken (≤ 2 Netze): %s. %s" % (biom, ", ".join(luecken) if luecken else "keine nach Zählung", BIOM_TEXT.get(biom, "")))
    L("")
    # Qualität
    L("## Qualitätshinweise")
    L("")
    hohe = sorted([v for v in tax.values() if v["dreiecke_je_m2"] is not None and v["dreiecke_je_m2"] > 10000
                   and v["groesse_m"][0] * v["groesse_m"][1] >= 0.25 and v["rolle"] != "sonst"], key=lambda v: -v["dreiecke_je_m2"])
    L("**Extreme Dreiecksdichte (> 10 000 Dreiecke/m² Grundfläche bei Grundfläche ≥ 0,25 m², ohne Kachel-/Testnetze; %d Netze, Top 15):**" % len(hohe))
    L("")
    L("| Netz | Rolle | Dreiecke | Dreiecke/m² | Nanite |")
    L("|---|---|---:|---:|---|")
    for v in hohe[:15]:
        L("| `%s` | %s | %d | %.0f | %s |" % (v["name"], v["rolle"], v["dreiecke"], v["dreiecke_je_m2"], "ja" if v["nanite"] else "nein"))
    L("")
    raw = [v for v in tax.values() if v["stufe"] == "raw"]
    L("**Raw-8K-Stufe (%d Netze, alle unter `/Game/Fab/Megascans/`):** %s. Raw heißt 8K-Texturen und Tier-0-Geometrie – Speicher je Netz hoch; für Foliage-Streuung die Medium-Stufe nachladen (vorhanden nur für 4 Netze: %s)." % (
        len(raw), ", ".join("`%s`" % v["name"] for v in raw[:12]) + (" …" if len(raw) > 12 else ""),
        ", ".join("`%s`" % v["name"] for v in tax.values() if v["stufe"] == "medium")))
    L("")
    ohne_koll = [v for v in tax.values() if v["rolle"] in ("fels_hero", "fels_block", "klippe_schale") and not v["kollision"]]
    L("**Fehlende Kollision bei `fels_block`/`fels_hero`/`klippe_schale` (%d von %d):** %s. Setzer muss für diese Netze Komplex-als-Einfach oder Konvex-Hülle erzeugen, sonst läuft der Spieler durch." % (
        len(ohne_koll), sum(1 for v in tax.values() if v["rolle"] in ("fels_hero", "fels_block", "klippe_schale")),
        ", ".join("`%s`" % v["name"] for v in ohne_koll[:40]) + (" … (+%d)" % (len(ohne_koll) - 40) if len(ohne_koll) > 40 else "")))
    L("")
    nn = sorted([v for v in tax.values() if not v["nanite"] and v["dreiecke"] >= 8000 and v["rolle"] != "sonst"], key=lambda v: -v["dreiecke"])
    L("**Nicht-Nanite mit ≥ 8 000 Dreiecken (%d Netze):** %s. Das sind die LOD-Bäume (Poplar, Beech, Forest_pine, Palms, Big_Tree_*, Dead_Tree); für Nanite-Umstellung Masken-Material prüfen (WPO/Wind)." % (
        len(nn), ", ".join("`%s` (%d)" % (v["name"], v["dreiecke"]) for v in nn[:25]) + (" …" if len(nn) > 25 else "")))
    L("")
    L("**Weitere Auffälligkeiten:** `SM_lava_m_rock_06` 129 216 Dreiecke für 3 m Block (Nanite, akzeptabel, aber 29 Lava-Netze = 1,4 M Dreiecke); AncientRuins `SM_Main_Arch_01` 529 640 und `SM_Wall_01` 372 163 Dreiecke (Nanite, nur als Einzelakteur); `SM_K13_FROSTSEE__RUINEN` 2,36 M Dreiecke, 76 Materialien, kein Nanite (Kachel). Meadow-Bäume existieren doppelt (`_Optimised`), nur die `_Optimised`-Variante ist in Foliage genutzt. `SM_grass_01`/`SM_plants_01` (Meadow) haben Höhe 0 m.")
    L("")
    # Paletten
    L("## Hinweise für die Planer: empfohlene Paletten")
    L("")
    L(PLANER_HINWEISE)
    L("Paletten je Rolle und Biom (3–8 Pfade; Reihenfolge: Eignung 2 vor 1, Nanite vor Nicht-Nanite, höchstens 2 Netze je Namensfamilie; bereits genutzte Netze mit `*`; Pfade ohne `/Game/`):")
    L("")
    palett_rollen = ["fels_hero", "fels_block", "fels_stein", "geroell_platte", "klippe_schale", "baum", "jungbaum", "strauch", "farn", "bodendecker", "grasbueschel", "totholz_liegend", "totholz_stumpf", "mensch"]
    for biom in BIOME:
        L("### %s" % biom)
        L("")
        for g in palett_rollen:
            if g == "baum":
                kand = [(p, v) for p, v in tax.items() if v["rolle"].startswith("baum_") and not v["rolle"].endswith("_tot") and v["biome"][biom] >= 1]
            else:
                kand = [(p, v) for p, v in tax.items() if gruppe_fein(v["rolle"]) == g and v["biome"][biom] >= 1]
            if not kand:
                L("- %s: **keine**" % g)
                continue
            kand.sort(key=lambda pv: (-pv[1]["biome"][biom], not pv[1]["nanite"], pv[0]))
            je_familie = Counter()
            gefiltert = []
            for p, v in kand:
                fam = re.sub(r"[_\-]?(\d+|[a-i]|var[a-z]|nn|_nn|_g|_a\d)+$", "", v["name"].lower())
                fam = re.sub(r"[_\-]?(\d+|[a-i])$", "", fam)
                if g == "baum":
                    fam = v["rolle"]
                if je_familie[fam] < 2:
                    je_familie[fam] += 1
                    gefiltert.append((p, v))
            kurz = []
            for p, v in gefiltert[:8]:
                kurz.append("`%s`%s%s" % (p.replace("/Game/", ""), "*" if v["genutzt_in"] else "", "" if v["nanite"] else " (kein Nanite)"))
            L("- %s (%d verfügbar): %s" % (g, len(kand), ", ".join(kurz)))
        L("")
    with open(pfad_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    csv_pfad, json_pfad = argv[1], argv[2]
    md_pfad = argv[3] if len(argv) > 3 else None
    with open(csv_pfad, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    tax = einordnen(rows)
    with open(json_pfad, "w", encoding="utf-8") as f:
        json.dump(tax, f, ensure_ascii=False, indent=1)
    rollen = Counter(v["rolle"] for v in tax.values())
    print("Netze: %d, Rollen: %d" % (len(tax), len(rollen)))
    for rolle, cnt in sorted(rollen.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %-24s %4d" % (rolle, cnt))
    if md_pfad:
        md_schreiben(tax, md_pfad)
        print("Markdown: %s" % md_pfad)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
