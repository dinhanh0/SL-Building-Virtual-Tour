import os

# CONFIG (FLOOR 2) 

IMAGE_DIR = "SLFloors/SLFloor2"   # folder with your floor-2 images
OUTPUT_JS = "nodes_floor2.js"     # JS file to generate

YAW_FORWARD = 20
YAW_BACK    = -120
YAW_LEFT    = -90
YAW_RIGHT   = 90
PITCH_DEFAULT = 0

MAP_TOP_START  = 40
MAP_LEFT_START = 30
MAP_STEP       = 1

# EXTRA NEIGHBOR LINKS (shortcuts / cross-floor)
# Format: (from_id, to_id, direction[, view_yaw, view_pitch])
# Node IDs here are *filename bases*, e.g. "SL2_001", "SL2_002", "SL1_113"
EXTRA_LINKS = [
    # examples:
    # ("SL2_001", "SL2_010", "forward"),
    # ("SL2_050", "SL1_113", "forward", 174.9, -6.3),  # cross-floor
    ("SL2_030", "SL2_032", "forward"),
    ("SL2_032", "SL2_030", "forward"),
    ("SL2_032", "SL2_035", "forward"),
    ("SL2_035", "SL2_032", "forward"),
    ("SL2_046", "SL2_028", "forward"),
    ("SL2_028", "SL2_046", "forward"),
    ("SL2_034", "SL2_038", "forward"),
    ("SL2_038", "SL2_034", "forward"),
    ("SL2_027", "SL2_047", "forward"),
    ("SL2_047", "SL2_027", "forward"),
    ("SL2_047", "SL2_026", "forward"),
    ("SL2_026", "SL2_047", "forward"),
    ("SL2_036", "SL2_049", "forward"),
    ("SL2_049", "SL2_036", "forward"),
    ("SL2_048","SL1_130", "forward"),
    ("SL2_050","SL1_052", "forward"),
    ("SL2_049","SL3_108", "forward"),
    ("SL2_047","SL3_110", "forward"),
    ("SL2_039","SL2_051", "forward"),
    ("SL2_051","SL2_039", "forward"),
    ("SL2_052","SL3_111", "forward"),
    ("SL2_051","SL1_132", "forward"),

]

DIR_TO_YAW = {
    "forward": YAW_FORWARD,
    "back":    YAW_BACK,
    "left":    YAW_LEFT,
    "right":   YAW_RIGHT,
}

#  DEFAULT ORIENTATIONS 
# "SL2_001": (yaw, pitch),
DEFAULT_ORIENTATIONS = {
    # fill using dev panel "Save DEFAULT_ORIENTATION"
}

# EDGE VIEW ORIENTATIONS (arrival camera)
# ("SL2_001", "SL2_002"): (yaw, pitch),
EDGE_VIEW_ORIENTATIONS = {
    # fill using "Save EDGE_VIEW"
    ("SL2_027", "SL2_028"): (180, 0),
    ("SL2_028", "SL2_029"): (179.1, 0.5),
    ("SL2_029", "SL2_030"): (180,0),
    ("SL2_031", "SL2_030"): (180,0),
    ("SL2_030", "SL2_032"): (180,0),
    ("SL2_032", "SL2_035"): (-180,0),
    ("SL2_035", "SL2_036"): (-180,0),
    ("SL2_036", "SL2_037"): (-180, 0),
    ("SL2_037", "SL2_036"): (90, 0),
    ("SL2_039", "SL2_044"): (-90,0),
    ("SL2_044", "SL2_039"): (180,0),
    ("SL2_044", "SL2_045"): (180,0),
    ("SL2_045", "SL2_046"): (180,0),
    ("SL2_046", "SL2_028"): (-90,0),
    ("SL2_032", "SL2_033"): (180,0),
    ("SL2_033", "SL2_032"): (-90,0),    
    ("SL2_033", "SL2_034"): (180,0),  
    ("SL2_039", "SL2_038"): (180,0),
    ("SL2_034", "SL2_038"): (90,0),    
    ("SL2_047", "SL2_027"): (-180,0),
    ("SL2_048", "SL2_047"): (180,0),
    ("SL2_047", "SL2_026"): (-180,0),
    ("SL2_036", "SL2_049"): (180,0),
    ("SL2_049", "SL2_050"): (180,0),
    ("SL2_049", "SL3_108"): (-180,0),
    ("SL2_047", "SL3_110"): (-180,0),
    ("SL2_039", "SL2_051"): (-180,0),
    ("SL2_051", "SL2_039"): (96.8, -1.2),
    ("SL2_051", "SL1_132"): (-180,0),
    


}

#  ICON YAW / PITCH PER EDGE 
# ("SL2_001", "SL2_002"): (yaw, pitch),
NEIGHBOR_YAWS = {
    # fill using Q + right-click "ICON_YAW" workflow or button
    ("SL2_027", "SL2_028"): (-178.5, -12.8),
    ("SL2_028", "SL2_027"): (-2.2, -9.4),
    ("SL2_028", "SL2_029"): (180.0, -4.3),
    ("SL2_029", "SL2_030"): (175.6, -3.0),
    ("SL2_029", "SL2_028"): (-5.1, 0.4),
    ("SL2_030", "SL2_029"): (-0.8, 0.4),
    ("SL2_030", "SL2_031"): (89.2, -4.3),
    ("SL2_031", "SL2_030"): (-47.0, 3.4),
    ("SL2_030", "SL2_032"): (179.2, -7.4),
    ("SL2_032", "SL2_030"): (-4.9, -3.0),
    ("SL2_032", "SL2_035"): (-4.9, -3.0),
    ("SL2_035", "SL2_032"): (-4.9, -3.0),
    ("SL2_032", "SL2_035"): (175.4, -1.8),
    ("SL2_035", "SL2_036"): (173.3, -2.6),
    ("SL2_036", "SL2_035"): (-5.4, 0.6),
    ("SL2_037", "SL2_036"): (-100.8, 0.6),
    ("SL2_036", "SL2_037"): (-98.6, -4.0),
    ("SL2_038", "SL2_039"): (-1.6, 2.5),
    ("SL2_039", "SL2_044"): (-3.8, -0.3),
    ("SL2_044", "SL2_045"): (174.8, -2.8),
    ("SL2_044", "SL2_039"): (81.2, -1.0),
    ("SL2_045", "SL2_044"): (-1.4, -2.9),
    ("SL2_045", "SL2_046"): (178.9, -4.2),
    ("SL2_046", "SL2_028"): (178.9, -4.2),
    ("SL2_028", "SL2_046"): (88.3, -1.3),
    ("SL2_046", "SL2_045"): (-1.8, 1.2),
    ("SL2_032", "SL2_033"): (84.5, -0.3), 
    ("SL2_033", "SL2_032"): (-8.2, 1.1), 
    ("SL2_033", "SL2_034"): (172.3, -9.7), 
    ("SL2_034", "SL2_033"): (-4.6, 0.2), 
    ("SL2_039", "SL2_038"): (175.0, -8.1),
    ("SL2_038", "SL2_034"): (-93.3, -0.3),
    ("SL2_034", "SL2_038"): (177.3, -7.5), 
    ("SL2_027", "SL2_047"): (-1.1, 2.7),   
    ("SL2_047", "SL2_027"): (-176.8, -2.3),
    ("SL2_047", "SL2_048"): (5.4, -19.4),
    ("SL2_048", "SL2_047"): (165.8, 12.9),
    ("SL2_047", "SL2_026"): (-63.0, -7.8),
    ("SL2_026", "SL2_047"): (1.3, 2.0),
    ("SL2_036", "SL2_049"): (177.4, -1.1),
    ("SL2_049", "SL2_036"): (-5.5, 3.5),
    ("SL2_049", "SL2_050"): (173.1, -19.9),
    ("SL2_050", "SL2_049"): (-4.9, 18.2),
    ("SL2_048", "SL1_130"): (-173.9, -28.5),
    ("SL2_050", "SL1_052"): (-24.3, -25.7),
    ("SL2_049", "SL3_108"): (-174.7, 10.9),
    ("SL2_047", "SL3_110"): (-5.4, 16.7),
    ("SL2_039", "SL2_051"): (82.4, -0.2),
    ("SL2_051", "SL2_039"): (96.8, -1.2),
    ("SL2_051", "SL2_052"): (175.9, 13.5),
    ("SL2_052", "SL3_111"): (166.6, 15.0),
    ("SL2_051", "SL1_132"): (-168.5, -24.2),
}

#  BLOCKED EDGES 
# ("SL2_003", "SL2_004"), ...
BLOCKED_EDGES = {
    # if you want to break the automatic linear path, add pairs here
    ("SL2_031", "SL2_032"),
    ("SL2_032", "SL2_031"),
    ("SL2_037", "SL2_038"),
    ("SL2_038", "SL2_037"),
    ("SL2_034", "SL2_035"),
    ("SL2_035", "SL2_034"),
    ("SL2_036", "SL2_038"),
    ("SL2_038", "SL2_036"),
    ("SL2_046", "SL2_047"),
    ("SL2_047", "SL2_046"),
    ("SL2_026", "SL2_027"),
    ("SL2_027", "SL2_026"),
    ("SL2_048", "SL2_049"),
    ("SL2_049", "SL2_048"),
    ("SL2_050", "SL2_051"),
    ("SL2_051", "SL2_050"),

}

# MAP POSITIONS (override minimap placement) 
# "SL2_001": (top_pct, left_pct),
MAP_POSITIONS = {
    # paste from dev panel "MAP_POSITION" output
    "SL2_036": (30.1, 16.1),
    "SL2_037": (24.5, 19.6),
    "SL2_035": (30.9, 29.1),
    "SL2_032": (29.9, 52.2),
    "SL2_030": (30.4, 59.8),
    "SL2_029": (30.1, 73.3),
    "SL2_028": (29.1, 82.8),
    "SL2_031": (38.3, 57.2),
    "SL2_033": (43.0, 51.5),
    "SL2_034": (62.5, 52.4),
    "SL2_027": (29.1, 88.5),
    "SL2_046": (40.2, 82.5),
    "SL2_045": (56.9, 82.9),
    "SL2_044": (72.2, 81.5),
    "SL2_039": (72.7, 67.5),
    "SL2_038": (72.2, 52.4),
    "SL2_047": (28.4, 95.6),
    "SL2_048": (28.7, 97.2),
    "SL2_049": (30.9, 8.7),
    "SL2_050": (31.9, 5.2),
    "SL3_111": (91.0, 60.9),
    "SL2_051": (96.3, 66.1),
    "SL2_052": (97.0, 69.6),
}

# NODES HIDDEN FROM MINIMAP 
HIDDEN_NODES = {
    # e.g. "SL2_stairs_mid"
}



def main():
    # 1. Collect images
    files = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png"}
    ])

    if not files:
        raise SystemExit(f"No images found in: {IMAGE_DIR}")

    print(f"[Floor2] Found {len(files)} images.")

    # 2. Build base node list (linear prev/next)
    nodes = {}

    for idx, filename in enumerate(files):
        base = os.path.splitext(filename)[0]   # e.g. "SL2_001"
        node_id = base

        neighbors = []

        # ---- back neighbor (previous file) ----
        if idx > 0:
            prev_base = os.path.splitext(files[idx - 1])[0]
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
                    "pitch": pitch_back,
                })

        # ---- forward neighbor (next file) ----
        if idx < len(files) - 1:
            next_base = os.path.splitext(files[idx + 1])[0]
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
                    "pitch": pitch_fwd,
                })

        # Default automatic path-based minimap position
        auto_top  = min(100, MAP_TOP_START  + idx * MAP_STEP)
        auto_left = min(100, MAP_LEFT_START + idx * MAP_STEP)

        # Override with MAP_POSITIONS if present
        if node_id in MAP_POSITIONS:
            map_top, map_left = MAP_POSITIONS[node_id]
        else:
            map_top, map_left = auto_top, auto_left

        # Default camera orientation
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

    # 3. Apply EXTRA_LINKS (including optional view overrides)
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
            print(f"NOTE: EXTRA_LINK to_id {to_id} not in this floor's nodes (probably cross-floor)")

        if direction not in DIR_TO_YAW:
            print(f"WARNING: invalid direction '{direction}' in EXTRA_LINK: {entry}")
            continue

        base_yaw = DIR_TO_YAW[direction]

        # allow NEIGHBOR_YAWS to override icon yaw/pitch
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
        print(f"Added extra link (F2): {from_id} -> {to_id} ({direction}, yaw={base_yaw})")

    # 4. Apply EDGE_VIEW_ORIENTATIONS
    for (from_id, to_id), (view_yaw, view_pitch) in EDGE_VIEW_ORIENTATIONS.items():
        if from_id not in nodes:
            print(f"WARNING: EDGE_VIEW from_id {from_id} not in nodes")
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
            print(f"WARNING: EDGE_VIEW pair {from_id}->{to_id} not found among neighbors")

    # 5. Write nodes_floor2.js
    print("\nWriting nodes_floor2.js...")

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_nodes_floor2.py\n")
        f.write("window.NODES_F2 = {\n\n")

        first = True
        for node_id in nodes:
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

            if not first:
                f.write(",\n\n")
            first = False
            f.write(block)

        f.write("\n\n};\n")

    print("nodes_floor2.js generated successfully.")


if __name__ == "__main__":
    main()
