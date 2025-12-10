import os

# CONFIG

IMAGE_DIR  = "SLFloors/SLFloor1"   # <<< change if your floor-1 folder differs
OUTPUT_JS = "nodes_floor1.js"     # will define window.NODES_F1

YAW_FORWARD   = 20
YAW_BACK      = -120
YAW_LEFT      = -90
YAW_RIGHT     = 90
PITCH_DEFAULT = 0

# these only matter for the automatic fallback path
MAP_TOP_START  = 40
MAP_LEFT_START = 30
MAP_STEP       = 1


DIR_TO_YAW = {
    "forward": YAW_FORWARD,
    "back":    YAW_BACK,
    "left":    YAW_LEFT,
    "right":   YAW_RIGHT,
}

# EDGE VIEW ORIENTATIONS (arrival view per edge)
# When going FROM node A TO node B, force an arrival yaw/pitch:
#   ("SL1_001", "SL1_002"): (yaw, pitch),
EDGE_VIEW_ORIENTATIONS = {
    ("SL1_053", "SL1_052"): (166.2, -4.4),
    ("SL1_052", "SL1_054"): (180.0, 0.0),
    ("SL1_054", "SL1_055"): (180.0, 0.0),
    ("SL1_055", "SL1_056"): (177.3, 0),
    ("SL1_056", "SL1_058"): (180, 0),
    ("SL1_058", "SL1_059"): (173.0, -2.2),
    ("SL1_059", "SL1_060"): (180, -0),
    ("SL1_061", "SL1_060"): (-96.6, 4.3),
    ("SL1_064", "SL1_063"): (-86.9, 4.9),
    ("SL1_063", "SL1_065"): (-178.3, -11.9),
    ("SL1_065", "SL1_066"): (180, 3.2),
    ("SL1_066", "SL1_068"): (87.6, 0.4),

    ("SL1_068", "SL1_067"): (-107.1, -0.2),
    ("SL1_067", "SL1_068"): (-90, -0.2),
    ("SL1_068", "SL1_066"): (-90, 0),
    ("SL1_066", "SL1_069"): (-178.9, -2.3),
    ("SL1_069", "SL1_071"): (174.9, -9.5),
    ("SL1_071", "SL1_072"): (-179.8, -0.1),
    ("SL1_072", "SL1_071"): (-2.5, -0.5),
    ("SL1_072", "SL1_073"): (-179.0, -8.0),
    ("SL1_073", "SL1_074"): (-88.6, -3.8),
    ("SL1_074", "SL1_075"): (-172.3, -1.5),
    ("SL1_074", "SL1_073"): (90, 0),
    ("SL1_073", "SL1_074"): (180, 0),
    ("SL1_074", "SL1_075"): (-90, 0),
    ("SL1_075", "SL1_074"): (-90,0),
    ("SL1_074", "SL1_078"): (177.3, -7.4),
    ("SL1_078", "SL1_079"): (-175.4, 1.4),
    ("SL1_079", "SL1_078"): (-90, -4.0),
    ("SL1_078", "SL1_054"): (90, -4.7),
    ("SL1_081", "SL1_071"): (90, 0.5),
    ("SL1_080", "SL1_081"): (175.5, -0.8),
    ("SL1_056", "SL1_080"): (180, 0),
    ("SL1_080", "SL1_056"): (90, 0),
    ("SL1_073", "SL1_113"): (180, 0),
    ("SL1_113", "SL1_073"): (90,0),
    ("SL1_073", "SL1_115"): (-180, 0),
    ("SL1_059", "SL1_122"): (180, 0),
    ("SL1_122", "SL1_059"): (-5.7, -4.8),
    ("SL1_122", "SL1_059"): (90,0),
    ("SL1_123", "SL1_122"): (180, 0),
    ("SL1_122", "SL1_063"): (180, 0),
    ("SL1_124", "SL1_126"): (-150,4),
    ("SL1_124", "SL1_125"): (-179,0),
    ("SL1_060", "SL1_130"): (180, 0),
    ("SL1_130", "SL1_127"): (180.0, 1.0),
    ("SL1_127", "SL1_130"): (90,0),
    ("SL1_130", "SL1_128"): (180,0),
    ("SL1_128", "SL1_130"): (-90,0),
    ("SL1_130", "n1"): (0,0),
    ("SL1_052", "SL2_050"): (-180,0),
    ("SL1_070", "SL1_131"): (180,0),

}

# ICON YAW / PITCH PER EDGE
# Controls hotspot (icon) location for a neighbor edge.
NEIGHBOR_YAWS = {
    ("SL1_052", "SL1_053"): (79.2, -0.6),
    ("SL1_052", "SL1_054"): (179.2, -13.6),
    ("SL1_053", "SL1_052"): (-66.8, 1.7),
    ("SL1_054", "SL1_052"): (-5.7, -9.2),
    ("SL1_054", "SL1_055"): (178.6, -3.9),
    ("SL1_055", "SL1_054"): (0.8, -3.4),
    ("SL1_055", "SL1_056"): (-177.2, -2.2),
    ("SL1_056", "SL1_055"): (-4.0, 2.2),
    ("SL1_056", "SL1_058"): (177.3, -2.5),
    ("SL1_058", "SL1_056"): (-7.7, 1.5),
    ("SL1_058", "SL1_059"): (173.0, -2.2),
    ("SL1_059", "SL1_058"): (-3.0, 1.8),
    ("SL1_059", "SL1_060"): (175.9, -16.2),
    ("SL1_060", "SL1_059"): (-4.8, -0.2),
    ("SL1_060", "SL1_061"): (100.3, -1.1),
    ("SL1_061", "SL1_060"): (-87.8, 0.9),

    ("SL1_122", "SL1_063"): (178.6, -4.4),

    ("SL1_063", "SL1_064"): (118.5, -2.5),
    ("SL1_063", "SL1_065"): (178.7, -12.7),

    ("SL1_064", "SL1_063"): (88.5, -1.0),

    ("SL1_065", "SL1_063"): (0.5, -9.2),
    ("SL1_065", "SL1_066"): (-99.1, -2.1),

    ("SL1_066", "SL1_065"): (-3.1, -1.2),
    ("SL1_066", "SL1_068"): (83.3, -5.4),
    ("SL1_068", "SL1_067"): (74.3, -8.7),
    ("SL1_067", "SL1_068"): (76.0, -10.6),
    ("SL1_068", "SL1_066"): (-111.3, -12.1),
    ("SL1_066", "SL1_069"): (178.7, -8.0),
    ("SL1_069", "SL1_066"): (-3.8, -4.1),
    ("SL1_069", "SL1_070"): (83.2, -4.9),
    ("SL1_069", "SL1_071"): (174.9, -9.5),
    ("SL1_071", "SL1_069"): (-2.8, -5.5),
    ("SL1_072", "SL1_071"): (-2.5, -0.5),
    ("SL1_071", "SL1_072"): (176.0, -5.5),
    ("SL1_072", "SL1_073"): (-179.0, -8.0),
    ("SL1_073", "SL1_072"): (-3.2, -2.5),
    ("SL1_073", "SL1_074"): (-88.6, -3.8),
    ("SL1_075", "SL1_074"): (-68.3, 1.2),
    ("SL1_074", "SL1_075"): (101.3, -0.9),
    ("SL1_074", "SL1_073"): (-1.7, -14.6),
    ("SL1_074", "SL1_076"): (176.6, -5.2),
    ("SL1_075", "SL1_076"): (136.2, -0.6),
    ("SL1_076", "SL1_075"): (152.4, -6.9),
    ("SL1_074", "SL1_078"): (177.3, -7.4),
    ("SL1_078", "SL1_074"): (-3.3, -3.8),
    ("SL1_078", "SL1_079"): (83.2, -10.0),
    ("SL1_079", "SL1_078"): (-3.6, -4.0),
    ("SL1_078", "SL1_054"): (179.5, -5.4),
    ("SL1_054", "SL1_078"): (-93.9, -3.5),
    ("SL1_071", "SL1_081"): (-95.9, -5.0),
    ("SL1_081", "SL1_071"): (-176.1, -6.8),
    ("SL1_081", "SL1_080"): (3.5, -4.0),
    ("SL1_080", "SL1_056"): (-1.1, -1.8),
    ("SL1_080", "SL1_081"): (-178.1, -4.7),
    ("SL1_056", "SL1_080"): (-94.1, -5.3),
    ("SL1_073", "SL1_113"): (-134.9, -18.5),
    ("SL1_113", "SL1_073"): (92.1, -22.3),
    ("SL1_113", "n20"): (172.3, -26.4),
    ("SL1_073", "SL1_115"): (-177.4, -2.7),
    ("SL1_115", "SL1_073"): (6.0, -0.1),
    ("SL1_059", "SL1_122"): (-93.6, -8.1),
    ("SL1_122", "SL1_059"): (-6.4, -3.8),
    ("SL1_122", "SL1_123"): (94.4, -5.6),
    ("SL1_123", "SL1_122"): (-88.5, -1.5),
    ("SL1_063", "SL1_122"): (-2.9, -1.2),
    ("SL1_122", "SL1_063"): (173.0, -4.9),
    ("SL1_115", "SL1_124"): (-169.2, -1.9),
    ("SL1_124", "SL1_115"): (177.9, -2.8),

    ("SL1_124", "SL1_125"): (86.9, -4.5),
    ("SL1_124", "SL1_126"): (-93.4, -5.2),
    ("SL1_125", "SL1_124"): (173.0, -4.9),
    ("SL1_125", "SL1_126"): (173.0, -4.9),
    ("SL1_126", "SL1_124"): (-7.4, -0.6),
    ("SL1_126", "SL1_125"): (173.0, -4.9),
    ("SL1_125", "SL1_124"): (-15.5, -1.4),
    ("SL1_130", "SL1_060"): (-15.5, -1.4),
    ("SL1_060", "SL1_130"): (-15.5, -1.4),
    ("SL1_130", "SL1_060"): (0.4, 1.9),
    ("SL1_060", "SL1_130"): (175.4, -2.0),
    ("SL1_130", "SL1_127"): (-90.9, -1.4),
    ("SL1_127", "SL1_130"): (55.9, 2.9),
    ("SL1_130", "SL1_128"): (81.4, -1.2),
    ("SL1_128", "SL1_130"): (-41.2, 3.1),
    ("SL1_129", "SL1_052"): (-174.9, -0.5),
    ("SL1_052", "SL1_129"): (-0.5, 1.1),
    ("SL1_130", "n1"): (-179.5, -13.1),
    ("SL1_052", "n25"): (5.8, -5.5),
    ("SL1_130", "SL2_048"): (169.6, 9.8),
    ("SL1_052", "SL2_050"): (-6.0, 10.4),
    ("SL1_131", "SL1_070"): (86.5, -0.6),
    ("SL1_070", "SL1_131"): (69.7, -1.5),
    ("SL1_131", "SL1_132"): (166.1, 12.7),
    ("SL1_132", "SL1_131"): (6.0, -21.9),
    ("SL1_132", "SL2_051"): (-11.9, 20.2),
    ("SL1_131", "n27"): (-176.4, -19.4),

    
}

# EXTRA NEIGHBOR LINKS (third directions, shortcuts)
# Format: (from_node, to_node, direction[, view_yaw, view_pitch])
EXTRA_LINKS = [
    ("SL1_052", "SL1_054", "forward"),
    ("SL1_054", "SL1_052", "forward"),
    ("SL1_059", "SL1_122", "forward"),
    ("SL1_058", "SL1_056", "forward"),
    ("SL1_056", "SL1_058", "forward"),
    ("SL1_122", "SL1_059", "forward"),
    ("SL1_063", "SL1_065", "forward"),
    ("SL1_065", "SL1_063", "forward"),
    ("SL1_066", "SL1_068", "forward"),
    ("SL1_068", "SL1_066", "forward"),
    ("SL1_066", "SL1_069", "forward"),
    ("SL1_069", "SL1_066", "forward"),
    ("SL1_069", "SL1_071", "forward"),
    ("SL1_071", "SL1_069", "forward"),
    ("SL1_078", "SL1_074", "forward"),
    ("SL1_074", "SL1_078", "forward"),
    ("SL1_078", "SL1_054", "forward"),
    ("SL1_054", "SL1_078", "forward"),
    ("SL1_056", "SL1_080", "forward"),
    ("SL1_080", "SL1_056", "forward"),
    ("SL1_071", "SL1_081", "forward"),
    ("SL1_081", "SL1_071", "forward"),
    ("SL1_073", "SL1_113", "forward"),
    ("SL1_113", "SL1_073", "forward"),
    ("SL1_113", "n20", "forward"),
    ("SL1_073", "SL1_115", "forward"),
    ("SL1_115", "SL1_073", "forward"),
    ("SL1_122", "SL1_063", "forward"),
    ("SL1_063", "SL1_122", "forward"),
    ("SL1_124", "SL1_115", "forward"),
    ("SL1_115", "SL1_124", "forward"),
    ("SL1_124", "SL1_126", "forward"),
    ("SL1_126", "SL1_124", "forward"),
    ("SL1_060", "SL1_130", "forward"),
    ("SL1_130", "SL1_060", "forward"),
    ("SL1_127", "SL1_130", "forward"),
    ("SL1_130", "SL1_127", "forward"),
    ("SL1_130", "SL1_128", "forward"),
    ("SL1_128", "SL1_130", "forward"),
    ("SL1_129", "SL1_052", "forward"),
    ("SL1_052", "SL1_129", "forward"),
    ("SL1_130", "n1", "forward"),
    ("SL1_052","n25", "forward"),
    ("SL1_130","SL2_048", "forward"),
    ("SL1_052", "SL2_050", "forward"),
    ("SL1_070", "SL1_131", "forward"),
    ("SL1_131", "SL1_070", "forward"),
    ("SL1_132","SL2_051", "forward"),
    ("SL1_131","n27", "forward"),


]

# BLOCKED EDGES
# Disable automatic prev/next linking between certain pairs.
BLOCKED_EDGES = {
    ("SL1_052", "SL0_123"),
    ("SL1_052", "SL1_054"),
    ("SL1_054", "SL1_052"),
    ("SL1_053", "SL1_054"),
    ("SL1_054", "SL1_053"),
    ("SL1_058", "SL1_057"),
    ("SL1_057", "SL1_058"),
    ("SL1_061", "SL1_062"),
    ("SL1_062", "SL1_061"),
    ("SL1_056", "SL1_057"),
    ("SL1_057", "SL1_056"),
    ("SL1_064", "SL1_065"),
    ("SL1_065", "SL1_064"),
    ("SL1_068", "SL1_069"),
    ("SL1_069", "SL1_068"),
    ("SL1_067", "SL1_066"),
    ("SL1_066", "SL1_067"),
    ("SL1_070", "SL1_071"),
    ("SL1_071", "SL1_070"),
    ("SL1_076", "SL1_077"),
    ("SL1_077", "SL1_076"),
    ("SL1_078", "SL1_077"),
    ("SL1_077", "SL1_078"),
    ("SL1_079", "SL1_080"),
    ("SL1_080", "SL1_079"),
    ("SL1_081", "SL1_113"),
    ("SL1_113", "SL1_081"),
    ("SL1_113", "SL1_115"),
    ("SL1_115", "SL1_113"),
    ("SL1_122", "SL1_115"),
    ("SL1_115", "SL1_122"),
    ("SL1_123", "SL1_124"),
    ("SL1_124", "SL1_123"),
    ("SL1_126", "SL1_125"),
    ("SL1_125", "SL1_126"),
    ("SL1_126", "SL1_127"),
    ("SL1_127", "SL1_126"),
    ("SL1_127", "SL1_128"),
    ("SL1_128", "SL1_127"),
    ("SL1_130", "SL1_129"),
    ("SL1_129", "SL1_130"),
    ("SL1_128", "SL1_129"),
    ("SL1_129", "SL1_128"),
    ("SL1_130", "SL1_131"),
    ("SL1_131", "SL1_130"),
}

# MAP POSITIONS (overrides for mapTop/mapLeft)
MAP_POSITIONS = {
    "SL1_115": (65.2, 10.9),
    "SL1_073": (64.7, 21.3),
    "SL1_113": (61.2, 18.5),
    "SL1_072": (64.9, 30.0),
    "SL1_071": (63.4, 50.0),
    "SL1_069": (64.9, 58.7),
    "SL1_066": (64.7, 66.9),
    "SL1_068": (71.6, 66.9),
    "SL1_067": (81.5, 68.1),
    "SL1_065": (64.7, 79.1),
    "SL1_063": (53.8, 79.8),
    "SL1_064": (56.8, 84.4),
    "SL1_122": (34.6, 79.8),
    "SL1_123": (33.6, 85.0),
    "SL1_059": (22.7, 79.6),
    "SL1_060": (22.2, 84.3),
    "SL1_061": (16.8, 84.6),
    "SL1_058": (22.0, 74.4),
    "SL1_056": (22.5, 50.4),
    "SL1_055": (23.0, 38.0),
    "SL1_054": (22.2, 21.3),
    "SL1_052": (21.5, 16.7),
    "SL1_053": (14.3, 16.3),
    "SL1_078": (41.5, 21.5),
    "SL1_074": (50.6, 20.7),
    "SL1_080": (36.6, 50.6),
    "SL1_081": (55.3, 50.2),
    "SL1_070": (80.5, 60.0),
    "SL1_075": (54.8, 14.3),
    "SL1_076": (57.8, 10.9),
    "SL1_079": (44.9, 14.4),
    "SL1_129": (14.3, 4.2),
    "SL1_130": (23.1, 93.7),
    "SL1_131": (91.3, 63.1),
    "SL1_132": (91.3, 68.5),
}

# NODES HIDDEN FROM MINIMAP
HIDDEN_NODES = {
    "SL1_077",
    "SL1_124",
    "SL1_125",
    "SL1_126",
    "SL1_127",
    "SL1_128",
    "SL1_127",
}

# DEFAULT ORIENTATIONS
# Per-node default camera view when you FIRST arrive at that pano.
DEFAULT_ORIENTATIONS = {
    # to be filled later using dev tools
}

def main():
    # 1. Collect images
    files = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png"}
    ])

    if not files:
        raise SystemExit(f"No images found in: {IMAGE_DIR}")

    print(f"[Floor1] Found {len(files)} images in {IMAGE_DIR}")

    # 2. Build base node list (linear prev/next)
    nodes = {}

    for i, filename in enumerate(files, start=1):
        base, _ = os.path.splitext(filename)
        node_id = base

        neighbors = []

        # back neighbor (previous file)
        if i > 1:
            prev_base, _ = os.path.splitext(files[i - 2])
            back_id = prev_base
            if (node_id, back_id) not in BLOCKED_EDGES:
                yaw_back   = YAW_BACK
                pitch_back = PITCH_DEFAULT
                pair_back  = (node_id, back_id)
                if pair_back in NEIGHBOR_YAWS:
                    yaw_back, pitch_back = NEIGHBOR_YAWS[pair_back]
                neighbors.append({
                    "id": back_id,
                    "yaw": yaw_back,
                    "pitch": pitch_back
                })

        # forward neighbor (next file)
        if i < len(files):
            next_base, _ = os.path.splitext(files[i])
            fwd_id = next_base
            if (node_id, fwd_id) not in BLOCKED_EDGES:
                yaw_fwd   = YAW_FORWARD
                pitch_fwd = PITCH_DEFAULT
                pair_fwd  = (node_id, fwd_id)
                if pair_fwd in NEIGHBOR_YAWS:
                    yaw_fwd, pitch_fwd = NEIGHBOR_YAWS[pair_fwd]
                neighbors.append({
                    "id": fwd_id,
                    "yaw": yaw_fwd,
                    "pitch": pitch_fwd
                })

        # automatic fallback map position
        auto_top  = min(100, MAP_TOP_START  + (i - 1) * MAP_STEP)
        auto_left = min(100, MAP_LEFT_START + (i - 1) * MAP_STEP)

        if node_id in MAP_POSITIONS:
            map_top, map_left = MAP_POSITIONS[node_id]
        else:
            map_top, map_left = auto_top, auto_left

        default_yaw, default_pitch = DEFAULT_ORIENTATIONS.get(node_id, (0, 0))

        nodes[node_id] = {
            "image": filename,
            "label": node_id,
            "description": "",
            "defaultYaw": default_yaw,
            "defaultPitch": default_pitch,
            "neighbors": neighbors,
            "mapTop": map_top,
            "mapLeft": map_left,
            "hideOnMap": (node_id in HIDDEN_NODES),
        }

    # 3. Apply extra links
    for entry in EXTRA_LINKS:
        if len(entry) not in (3, 5):
            print(f"WARNING: EXTRA_LINK invalid format: {entry}")
            continue

        if len(entry) == 3:
            from_id, to_id, direction = entry
            view_yaw = None
            view_pitch = None
        else:
            from_id, to_id, direction, view_yaw, view_pitch = entry

        if from_id not in nodes:
            print(f"WARNING: EXTRA_LINK from_id {from_id} not in nodes (skipping)")
            continue
        if to_id not in nodes:
            print(f"NOTE: EXTRA_LINK to_id {to_id} not in this floor's nodes")
        if direction not in DIR_TO_YAW:
            print(f"WARNING: invalid direction '{direction}' in EXTRA_LINK: {entry}")
            continue

        base_yaw = DIR_TO_YAW[direction]

        icon_yaw, icon_pitch = base_yaw, PITCH_DEFAULT
        pair = (from_id, to_id)
        if pair in NEIGHBOR_YAWS:
            icon_yaw, icon_pitch = NEIGHBOR_YAWS[pair]

        neighbor_dict = {
            "id": to_id,
            "yaw": icon_yaw,
            "pitch": icon_pitch,
        }
        if view_yaw is not None:
            neighbor_dict["viewYaw"] = view_yaw
        if view_pitch is not None:
            neighbor_dict["viewPitch"] = view_pitch

        nodes[from_id]["neighbors"].append(neighbor_dict)
        print(f"Added extra link: {from_id} -> {to_id} ({direction}, baseYaw={base_yaw})")

    # 4. Apply EDGE_VIEW_ORIENTATIONS
    for (from_id, to_id), (view_yaw, view_pitch) in EDGE_VIEW_ORIENTATIONS.items():
        if from_id not in nodes:
            print(f"WARNING: EDGE_VIEW_ORIENTATIONS from_id {from_id} not in nodes")
            continue

        neighbor_list = nodes[from_id]["neighbors"]
        found = False
        for n in neighbor_list:
            if n["id"] == to_id:
                n["viewYaw"] = view_yaw
                n["viewPitch"] = view_pitch
                found = True
                break
        if not found:
            print(f"WARNING: EDGE_VIEW_ORIENTATIONS pair {from_id}->{to_id} not found")

    # 5. Write nodes_floor1.js
    print("\nWriting nodes_floor1.js...")

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_nodes_floor1.py\n")
        f.write("window.NODES_F1 = {\n\n")

        for base, _ext in sorted((os.path.splitext(fn)[0], fn) for fn in files):
            node_id = base
            node = nodes[node_id]

            neighbor_lines = []
            for n in node["neighbors"]:
                parts = [
                    f'id: "{n["id"]}"',
                    f"yaw: {n['yaw']}",
                    f"pitch: {n['pitch']}",
                ]
                if "viewYaw" in n:
                    parts.append(f"viewYaw: {n['viewYaw']}")
                if "viewPitch" in n:
                    parts.append(f"viewPitch: {n['viewPitch']}")
                neighbor_lines.append("      { " + ", ".join(parts) + " }")

            neighbors_block = ",\n".join(neighbor_lines)

            block = f"""  "{node_id}": {{
    image: "{node["image"]}",
    label: "{node["label"]}",
    description: "",
    defaultYaw: {node["defaultYaw"]},
    defaultPitch: {node["defaultPitch"]},
    neighbors: [
{neighbors_block}
    ],
    mapTop: {node["mapTop"]},
    mapLeft: {node["mapLeft"]},
    hideOnMap: {str(node["hideOnMap"]).lower()}
  }}"""

            f.write(block + ",\n\n")

        f.write("};\n")

    print("nodes_floor1.js generated successfully.")


if __name__ == "__main__":
    main()
